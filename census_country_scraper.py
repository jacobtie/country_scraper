from typing import Dict, Tuple, List, Any
import json
import requests
from bs4 import BeautifulSoup

def scrape_country_data(country_data: BeautifulSoup) -> Dict[str, Any]:
    """Scrapes all data from a table as a soup and returns the dict"""
    tbody = country_data.find_next('tbody')
    rows = tbody.find_all('tr')
    data_dict = {2016: {}, 2017: {}, 2018: {}}
    year_index = 4
    for key in data_dict.keys():
        # Population
        data_dict[key]['midyear_pop'] = float([td for td in rows[1].find_all('td')[year_index]][0].replace(',', ''))
        data_dict[key]['growth_rate'] = float([td for td in rows[2].find_all('td')[year_index]][0].replace(',', ''))
        # Fertility
        data_dict[key]['total_fertility_rate'] = float([td for td in rows[4].find_all('td')[year_index]][0].replace(',', ''))
        data_dict[key]['crude_birth_rate'] = float([td for td in rows[5].find_all('td')[year_index]][0].replace(',', ''))
        data_dict[key]['births'] = float([td for td in rows[6].find_all('td')[year_index]][0].replace(',', ''))
        # Mortality
        data_dict[key]['life_expectancy'] = float([td for td in rows[8].find_all('td')[year_index]][0].replace(',', ''))
        data_dict[key]['infant_mortality_rate'] = float([td for td in rows[9].find_all('td')[year_index]][0].replace(',', ''))
        data_dict[key]['under_5_mortality_rate'] = float([td for td in rows[10].find_all('td')[year_index]][0].replace(',', ''))
        data_dict[key]['crude_death_rate'] = float([td for td in rows[11].find_all('td')[year_index]][0].replace(',', ''))
        data_dict[key]['deaths'] = float([td for td in rows[12].find_all('td')[year_index]][0].replace(',', ''))
        # Migration
        data_dict[key]['net_migration_rate'] = float([td for td in rows[14].find_all('td')[year_index]][0].replace(',', ''))
        data_dict[key]['net_num_migrants'] = float([td for td in rows[15].find_all('td')[year_index]][0].replace(',', ''))

        year_index += 1
    return data_dict

def get_country_soups(all_countries_soup: BeautifulSoup) -> List[Dict[str, BeautifulSoup]]:
    """Gets country names and corresponding table soups as a list of dicts"""
    tables = all_countries_soup.find_all('table', class_='query_table')[2:-1]
    captions = [table.find_next('caption').text for table in tables]
    country_names = [caption[caption.rfind('- ')+2:] for caption in captions]
    return dict(zip(country_names, tables))

def run_country_scraper():
    """Runs the scraper and outputs to census_output.json"""
    # all_countries_url = 'https://www.census.gov/data-tools/demo/idb/region.php?T=13&RT=0&A=both&Y=2016,2017,2018&C=&R=1'
    # all_countries_content = requests.get(all_countries_url).content
    all_countries_content = ''
    with open('static_pages/census_page.html', 'r') as census_page:
        all_countries_content = census_page.read()
    all_countries_soup = BeautifulSoup(all_countries_content, 'html5lib')
    country_soups = get_country_soups(all_countries_soup)
    country_data_dicts = [{'Country Name':country_name, **scrape_country_data(country_table)} for country_name, country_table in country_soups.items()]
    with open('output/census_output.json', 'w') as output_file:
        json.dump(country_data_dicts, output_file)
    print('Finished scraping')

if __name__ == '__main__':
    run_country_scraper()

