# This code is part of Qiskit.
#
# (C) Copyright IBM 2021.
#
# This code is licensed under the Apache License, Version 2.0. You may
# obtain a copy of this license in the LICENSE.txt file in the root directory
# of this source tree or at http://www.apache.org/licenses/LICENSE-2.0.
#
# Any modifications or derivative works of this code must retain this
# copyright notice, and modified files need to carry a notice indicating
# that they have been altered from the originals.

"""Spectroscopy tests for resonator spectroscopy experiment."""

from test.base import QiskitExperimentsTestCase
import numpy as np
from ddt import ddt, data

from qiskit.qobj.utils import MeasLevel
from qiskit_experiments.framework import ParallelExperiment

from qiskit_experiments.library import ResonatorSpectroscopy
from qiskit_experiments.test.mock_iq_backend import MockIQBackend, MockIQParallelBackend
from qiskit_experiments.test.mock_iq_helpers import (
    MockIQSpectroscopyHelper as ResonatorSpectroscopyHelper,
    MockIQParallelExperimentHelper as ParallelExperimentHelper,
)


@ddt
class TestResonatorSpectroscopy(QiskitExperimentsTestCase):
    """Tests for the resonator spectroscopy experiment."""

    @data(-5e6, -2e6, 0, 1e6, 3e6)
    def test_end_to_end(self, freq_shift):
        """Test the experiment from end to end."""

        qubit = 1
        backend = MockIQBackend(
            experiment_helper=ResonatorSpectroscopyHelper(
                gate_name="measure",
                freq_offset=freq_shift,
                iq_cluster_centers=[((0.0, 0.0), (-1.0, 0.0))],
                iq_cluster_width=[0.2],
            ),
        )
        backend._configuration.timing_constraints = {"granularity": 16}

        res_freq = backend.defaults().meas_freq_est[qubit]

        frequencies = np.linspace(res_freq - 20e6, res_freq + 20e6, 51)
        spec = ResonatorSpectroscopy(qubit, backend=backend, frequencies=frequencies)

        expdata = spec.run(backend)
        self.assertExperimentDone(expdata)
        result = expdata.analysis_results(1)
        self.assertRoundTripSerializable(result.value, check_func=self.ufloat_equiv)

        self.assertAlmostEqual(result.value.n, res_freq + freq_shift, delta=0.1e6)
        self.assertEqual(str(result.device_components[0]), f"R{qubit}")

    def test_experiment_config(self):
        """Test converting to and from config works"""
        exp = ResonatorSpectroscopy(1, frequencies=np.linspace(100, 150, 20) * 1e6)
        loaded_exp = ResonatorSpectroscopy.from_config(exp.config())
        self.assertNotEqual(exp, loaded_exp)
        self.assertTrue(self.json_equiv(exp, loaded_exp))

    def test_roundtrip_serializable(self):
        """Test round trip JSON serialization"""
        exp = ResonatorSpectroscopy(1, frequencies=np.linspace(int(100e6), int(150e6), int(20e6)))
        self.assertRoundTripSerializable(exp, self.json_equiv)

    @data(-5e6, 0, 3e6)
    def test_kerneled_expdata_serialization(self, freq_shift):
        """Test experiment data and analysis data JSON serialization"""
        qubit = 1
        backend = MockIQBackend(
            experiment_helper=ResonatorSpectroscopyHelper(
                gate_name="measure",
                freq_offset=freq_shift,
                iq_cluster_centers=[((0.0, 0.0), (-1.0, 0.0))],
                iq_cluster_width=[0.2],
            ),
        )
        backend._configuration.timing_constraints = {"granularity": 16}

        res_freq = backend.defaults().meas_freq_est[qubit]

        frequencies = np.linspace(res_freq - 20e6, res_freq + 20e6, 51)
        exp = ResonatorSpectroscopy(qubit, backend=backend, frequencies=frequencies)

        expdata = exp.run(backend).block_for_results()
        self.assertExperimentDone(expdata)

        # since under _experiment in kwargs there is an argument of the backend which isn't serializable.
        expdata._experiment = None
        # Checking serialization of the experiment data
        self.assertRoundTripSerializable(expdata, self.experiment_data_equiv)

        # Checking serialization of the analysis
        self.assertRoundTripSerializable(expdata.analysis_results(1), self.analysis_result_equiv)

    def test_parallel_experiment(self):
        """Test for parallel experiment"""
        # backend initialization
        iq_cluster_centers = [
            ((-1.0, 0.0), (1.0, 0.0)),
            ((0.0, -1.0), (0.0, 1.0)),
            ((3.0, 0.0), (5.0, 0.0)),
        ]

        freq_shift = [-5e6, 3e6]
        exp_helper_list = [
            ResonatorSpectroscopyHelper(
                gate_name="measure",
                freq_offset=freq_shift[0],
                iq_cluster_centers=iq_cluster_centers,
            ),
            ResonatorSpectroscopyHelper(
                gate_name="measure",
                freq_offset=freq_shift[1],
                iq_cluster_centers=iq_cluster_centers,
            ),
        ]

        parallel_backend = MockIQParallelBackend(
            experiment_helper=None,
            rng_seed=0,
        )
        parallel_backend._configuration.timing_constraints = {"granularity": 16}

        qubit1 = 0
        qubit2 = 1

        res_freq1 = parallel_backend.defaults().meas_freq_est[qubit1]
        res_freq2 = parallel_backend.defaults().meas_freq_est[qubit2]

        frequencies1 = np.linspace(res_freq1 - 20e6, res_freq1 + 20e6, 51)
        frequencies2 = np.linspace(res_freq2 - 20e6, res_freq2 + 20e6, 53)

        res_spect1 = ResonatorSpectroscopy(
            qubit1, backend=parallel_backend, frequencies=frequencies1
        )
        res_spect2 = ResonatorSpectroscopy(
            qubit2, backend=parallel_backend, frequencies=frequencies2
        )

        exp_list = [res_spect1, res_spect2]

        # Initializing parallel helper
        parallel_helper = ParallelExperimentHelper(exp_list, exp_helper_list)

        # setting the helper into the backend
        parallel_backend.experiment_helper = parallel_helper

        par_experiment = ParallelExperiment(exp_list, backend=parallel_backend)
        par_experiment.set_run_options(meas_level=MeasLevel.KERNELED, meas_return="single")

        par_data = par_experiment.run().block_for_results()
        self.assertExperimentDone(par_data)

        # since under _experiment in kwargs there is an argument of the backend which isn't serializable.
        par_data._experiment = None
        # Checking serialization of the experiment data
        self.assertRoundTripSerializable(par_data, self.experiment_data_equiv)

        for child_data in par_data.child_data():
            self.assertRoundTripSerializable(child_data, self.experiment_data_equiv)
            for analysis_result in child_data.analysis_results():
                self.assertRoundTripSerializable(analysis_result, self.analysis_result_equiv)
