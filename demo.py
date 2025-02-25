"""
Module: VSLAM-LAB - demo.py
- Author: Alejandro Fontan Villacampa
- Version: 1.0
- Created: 2024-09-13
- Updated: 2024-09-13
- License: GPLv3 License
- List of Known Dependencies;
    * ...
"""

import os
import sys

from Datasets.get_dataset import get_dataset
from Baselines.baseline_utilities import get_baseline

from path_constants import VSLAMLAB_BENCHMARK
from utilities import Experiment
from path_constants import VSLAMLAB_EVALUATION
from path_constants import VSLAMLAB_BASELINES
from Run.run_functions import run_sequence

SCRIPT_LABEL = f"\033[95m[{os.path.basename(__file__)}]\033[0m "


def main():
    baseline_name = sys.argv[1]
    dataset_name = sys.argv[2]
    sequence_name = sys.argv[3]

    exp = Experiment()
    exp.config_yaml = ""
    exp.folder = os.path.join(VSLAMLAB_EVALUATION, 'demo')
    exp.module = baseline_name

    os.makedirs(exp.folder, exist_ok=True)
    baseline = get_baseline(baseline_name)
    exp.parameters = baseline.get_default_parameters()

    dataset = get_dataset(dataset_name, VSLAMLAB_BENCHMARK)

    print(f"\n{SCRIPT_LABEL}Running {baseline.label} in {dataset.dataset_label} / {dataset.dataset_color}{sequence_name} ...")
    dataset.download_sequence(sequence_name)
    run_sequence(0, exp, baseline, dataset, sequence_name)

if __name__ == "__main__":
    main()
