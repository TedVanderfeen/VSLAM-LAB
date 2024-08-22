import os

import matplotlib.pyplot as plt
import pandas as pd
import yaml

from Compare import plot_functions
from Compare.plot_functions import create_and_show_canvas
from Datasets.dataset_utilities import get_dataset
from utilities import VSLAM_LAB_EVALUATION_FOLDER
from utilities import check_yaml_file_integrity
from utilities import find_common_sequences

SCRIPT_LABEL = "[compare_functions.py] "
VSLAM_LAB_ACCURACY_CSV = 'accuracy.csv'


def full_comparison(experiments, VSLAMLAB_BENCHMARK, COMPARISONS_YAML_DEFAULT, comparison_path):
    figures_path = os.path.join(comparison_path, "figures")

    check_yaml_file_integrity(COMPARISONS_YAML_DEFAULT)
    with open(COMPARISONS_YAML_DEFAULT, 'r') as file:
        comparisons = yaml.safe_load(file)

    dataset_sequences, dataset_nicknames, dataset_rgbHz, exp_names = get_experiments(experiments)
    accuracies = get_accuracies(experiments, dataset_sequences)

    # Comparisons switch
    def switch_comparison(comparison_):
        switcher = {
            'accuracy_boxplot': lambda: plot_functions.boxplot_exp_seq(accuracies, dataset_sequences, exp_names,
                                                                       dataset_nicknames, 'accuracy', figures_path),
            'cumulated_error': lambda: plot_functions.plot_cum_error(accuracies, dataset_sequences, exp_names,
                                                                     dataset_nicknames, 'accuracy', figures_path),
            'accuracy_radar': lambda: plot_functions.radar_seq(accuracies, dataset_sequences, exp_names,
                                                               dataset_nicknames, 'accuracy', figures_path),
            'trajectories': lambda: plot_functions.plot_trajectories(dataset_sequences, exp_names, dataset_nicknames,
                                                                     experiments, accuracies, figures_path),
            'image_canvas': lambda: create_and_show_canvas(dataset_sequences, VSLAMLAB_BENCHMARK, figures_path)
        }

        func = switcher.get(comparison_, lambda: "Invalid case")
        return func()

    # Get comparisons
    for comparison in comparisons:
        if comparisons[comparison]:
            switch_comparison(comparison)

    plt.show()


def get_experiments(experiments):
    """
    ------------ Description:
    This function processes a dictionary of experiments to extract and compile common sequences across all experiments,
    as well as relevant metadata such as dataset nicknames, RGB frame rates, experiment names, and folders. It ensures
    that sequences common to all experiments are identified and organizes the data in a structured format for further
    analysis.

    ------------ Parameters:
    experiments : dict
        experiments[exp_name] = experiment

    ------------ Returns:
    dataset_sequences : dict
        dataset_sequences[dataset_name] = list{sequence_names}
    dataset_nicknames : dict
        dataset_nicknames[dataset_name] = list{sequence_nicknames}
    dataset_rgbHz : dict
        dataset_rgbHz[dataset_name] = sequence_rgbHz
    exp_names : list
        exp_names = list{exp_names}
    exp_folders : list
        exp_folders = list{exp_folders}
"""

    # Find sequences common to all experiments
    dataset_sequences = find_common_sequences(experiments)

    # Lists with the experiment names and folders
    exp_names = []
    exp_folders = []
    for exp_name, exp in experiments.items():
        exp_names.append(exp_name)
        exp_folders.append(exp.folder)

    dataset_nicknames = {}
    dataset_rgbHz = {}
    for dataset_name, sequence_names in dataset_sequences.items():
        dataset = get_dataset(dataset_name, "-")
        dataset_nicknames[dataset_name] = []
        dataset_rgbHz[dataset_name] = dataset.rgb_hz
        for sequence_name in sequence_names:
            sequences_nickname = dataset.get_sequence_nickname(sequence_name)
            dataset_nicknames[dataset_name].append(sequences_nickname)

    return dataset_sequences, dataset_nicknames, dataset_rgbHz, exp_names


def get_accuracies(experiments, dataset_sequences):
    """
    ------------ Description:
    Reads accuracy CSV files from a specified folder structure and stores them in a nested dictionary.
    The CSV files are read with space as a delimiter and no header.

    ------------ Parameters:
    experiments : dict
        experiments[exp_name] = experiment
    dataset_sequences : dict
        dataset_sequences[dataset_name] = list{sequence_names}

    ------------ Returns:
    accuracies : dict
        accuracies[dataset_name][sequence_name][exp_name] = pandas.DataFrame()
    """

    accuracies = {}
    for dataset_name, sequence_names in dataset_sequences.items():
        accuracies[dataset_name] = {}
        for sequence_name in sequence_names:
            accuracies[dataset_name][sequence_name] = {}
            for exp_name, exp in experiments.items():
                accuracy_csv_file = os.path.join(exp.folder, dataset_name.upper(), sequence_name,
                                                 os.path.join(VSLAM_LAB_EVALUATION_FOLDER, VSLAM_LAB_ACCURACY_CSV))
                accuracy = pd.read_csv(accuracy_csv_file)
                accuracies[dataset_name][sequence_name][exp_name] = accuracy

    return accuracies