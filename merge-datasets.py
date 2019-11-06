from typing import Dict, List, Any
import pandas as pd
import json
from glob import glob
import numpy as np
import time

class Logger(object):
    our_log: List[str] = []

    @classmethod
    def log(cls, msg):
        cls.our_log.append(msg + '\n')
    
    @classmethod
    def out(cls):
        curr_time = int(round(time.time() * 1000))
        with open(fr'output/logs/log_{curr_time}.txt', 'w') as output_file:
            output_file.writelines(cls.our_log)


def merge_census_datasets():
    datasets = []
    fsi_excel_files = glob('fsi-data/*.xlsx')
    raw_census_data = {}
    Logger.log('Loading census_output.json\n')
    with open('output/census_output.json', 'r') as census_json:
        raw_census_data = json.load(census_json)

    Logger.log('Processing census data\n')
    for index, fsi_excel_file in enumerate(fsi_excel_files):
        year = str(index + 2016)
        fsi_df: pd.DataFrame = pd.read_excel(fsi_excel_file)
        processed_census_data: Dict[str, List[Any]] = {}
        Logger.log(f'\n\nYear: {year}')
        # Get the census data columns
        for index, country in enumerate(fsi_df['Country']):
            try:
                country_census_data = [data for data in raw_census_data if data['Country Name'] == country][0][year]
            except:
                Logger.log(f'{country} has no census data!')
                for k, v in processed_census_data.items():
                    processed_census_data[k].append(np.NaN)
                continue
            for k, v in country_census_data.items():
                if k not in processed_census_data:
                    processed_census_data[k] = []
                processed_census_data[k].append(v)
        for k, v in processed_census_data.items():
            fsi_df[k] = v
        # fsi_df.to_csv(fr'output/mergedyear{year}-census.csv')
        # Logger.log('Saved to output!')
        datasets.append(fsi_df)
    return datasets


def merge_whr_datasets(datasets):
    # prev_files = glob('output/*-census.csv')
    Logger.log('\n\nProcessing WHR data')

    whr_data = pd.read_csv('whr-data/whr-data.csv')

    for index, dataset in enumerate(datasets):
        year = index + 2016
        # destination_data = pd.read_csv(prev_file)
        whr_data_yeared = whr_data[whr_data['Year'] == year]
        processed_whr_data: Dict[str, List[Any]] = {}
        Logger.log(f'\n\nYear {year}\n')
        for index, country in enumerate(dataset['Country']):
            try:
                whr_country_data = whr_data_yeared[whr_data_yeared['Country name'] == country].iloc[0]
            except:
                Logger.log(f'{country} has no WHR data!')
                for k, _ in processed_whr_data.items():
                    processed_whr_data[k].append(np.NaN)
                continue
            for key, value in whr_country_data.items():
                if key != 'Year' and key != 'Country name':
                    if key not in processed_whr_data:
                        processed_whr_data[key] = []
                    processed_whr_data[key].append(value)
        for k, v in processed_whr_data.items():
            missing = len(dataset) - len(v)
            while missing > 0:
                v.insert(0, np.NaN)
                missing -= 1
            dataset[k] = v
        dataset.to_csv(fr'output/mergedyear{year}.csv')


def merge_datasets():
    datasets = merge_census_datasets()
    merge_whr_datasets(datasets)
    Logger.out()


if __name__ == "__main__":
    merge_datasets()

