import pandas as pd

def merge_singe_year_datasets(original_data, census_data, whi_data):
    merged_data = original_data.copy()

    # Copy over census updates
    merged_data.assign(Midyear_pop=census_data['Midyear_pop'])
    merged_data['Growth_rate'] = census_data['Growth_rate']
    merged_data['Total_fertility'] = census_data['Total_fertility']
    merged_data['Crude_birth_rate'] = census_data['Crude_birth_rate']
    merged_data['Births'] = census_data['Births']
    merged_data['Life_expectancy'] = census_data['Life_expectancy']
    merged_data['Infant_mortality'] = census_data['Infant_mortality']
    merged_data['Under_5_mortality'] = census_data['Under_5_mortality']
    merged_data['Crude_death_rate'] = census_data['Crude_death_rate']
    merged_data['Deaths'] = census_data['Deaths']
    merged_data['Net_migration_rate'] = census_data['Net_migration_rate']
    merged_data['Net_num_migrants'] = census_data['Net_num_migrants']

    # Copy over WHI updates
    merged_data['Life Ladder'] = whi_data['Life Ladder']
    merged_data['Log GDP per capita'] = whi_data['Log GDP per capita']
    merged_data['Social support'] = whi_data['Social support']
    merged_data['Healthy life expectancy at birth'] = whi_data['Healthy life expectancy at birth']
    merged_data['Freedom to make life choices'] = whi_data['Freedom to make life choices']
    merged_data['Generosity'] = whi_data['Generosity']
    merged_data['Perceptions of corruption'] = whi_data['Perceptions of corruption']
    merged_data['Positive affect'] = whi_data['Positive affect']
    merged_data['Negative affect'] = whi_data['Negative affect']
    merged_data['Confidence in national government'] = whi_data['Confidence in national government']
    merged_data['Democratic Quality'] = whi_data['Democratic Quality']
    merged_data['Delivery Quality'] = whi_data['Delivery Quality']
    merged_data['Standard deviation of ladder by country-year'] = whi_data['Standard deviation of ladder by country-year']
    merged_data['Standard deviation/Mean of ladder by country-year'] = whi_data['Standard deviation/Mean of ladder by country-year']

    return merged_data


def merge_datasets():
    datasets_by_year = [[],[],[]]
    # Read original data
    datasets_by_year[0].append(pd.read_csv('to-merge/original-data/alldata_year2016.csv'))
    datasets_by_year[0].append(pd.read_csv('to-merge/original-data/alldata_year2017.csv'))
    datasets_by_year[0].append(pd.read_csv('to-merge/original-data/alldata_year2018.csv'))

    # Read updated census data
    datasets_by_year[1].append(pd.read_csv('to-merge/census-fixed-data/mergedyear2016.csv'))
    datasets_by_year[1].append(pd.read_csv('to-merge/census-fixed-data/mergedyear2017.csv'))
    datasets_by_year[1].append(pd.read_csv('to-merge/census-fixed-data/mergedyear2018.csv'))
    
    # Read updated WHI data
    datasets_by_year[2].append(pd.read_csv('to-merge/whi-fixed-data/mergedyear2016 - aileen.csv'))
    datasets_by_year[2].append(pd.read_csv('to-merge/whi-fixed-data/mergedyear2017 - aileen.csv'))
    datasets_by_year[2].append(pd.read_csv('to-merge/whi-fixed-data/mergedyear2018 - aileen.csv'))

    for i in range(0,3):
        merged_data = merge_singe_year_datasets(datasets_by_year[0][i], datasets_by_year[1][i], datasets_by_year[2][i])
        merged_data.to_csv(f'to-merge/output/crowded-data-{2016+i}.csv')


if __name__ == "__main__":
    merge_datasets()
    print('done')
