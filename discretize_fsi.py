from glob import glob
import pandas as pd
import numpy as np

def get_category(score):
    if score >= 90.0:
        return 'Alert'
    elif score >= 60.0:
        return 'Warning'
    elif score >= 30.0:
        return 'Stable'
    elif score >= 0:
        return 'Sustainable'
    else:
        return np.NaN


def discretize_fsi():
    dataset_paths = glob('output/*.csv')
    for index, dataset_path in enumerate(dataset_paths):
        year = str(index + 2016)
        dataset = pd.read_csv(dataset_path)
        discretized_fsi = []
        for score in dataset['Total']:
            discretized_fsi.append(get_category(score))
        dataset['Category'] = discretized_fsi
        dataset.to_csv(f'output/alldata_year{year}.csv')


if __name__ == "__main__":
    discretize_fsi()
