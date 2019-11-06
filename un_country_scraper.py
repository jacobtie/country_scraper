from typing import Dict, List, Any, Tuple
import time
from string import ascii_lowercase
import json
import requests
from bs4 import BeautifulSoup
import pandas as pd

def get_country_list(country_list_page: BeautifulSoup) -> Dict[str, str]:
    """Returns a list of the country name to the url"""
    # Gets all the list items
    li_elements = country_list_page.find_all('li')
    # Gets the relative link from the a tag of each li tag
    urls = [link.find_next('a')['href'] for link in li_elements]
    # Gets the table cell
    cell_elements = [li.find_all('td')[3] for li in li_elements]
    # Iterates over the cells and gets just the text
    names = []
    for cell in cell_elements:
        names.append([child for child in cell.children if isinstance(child, str)][0])
    # Returns the names and the urls zipped together
    return dict(zip(names, urls))

def get_country_detail(country_page: BeautifulSoup, detail: str) -> Dict[str, Any]:
    """Get country info from economic indicators block as a dict"""
    all_details: List[BeautifulSoup] = country_page.find_all('details')
    economic_details = [details for details in all_details if details.find_all('summary')[0].text == detail][0]
    table_rows = economic_details.find_next('tbody').find_all('tr')
    row_headers = [tr.find_next('td').text for tr in table_rows]
    cleaned_row_headers = []
    for rh in row_headers:
        if '\xa0' in rh:
            cleaned_row_headers.append(rh[:rh.index('\xa0')])
        else:
            cleaned_row_headers.append(rh)
    data_cells = [tr.find_all('td')[-1].text for tr in table_rows]
    cleaned_data_cells = []
    for data_cell in data_cells:
        shortened_data_cell = data_cell.replace(' ', '')
        if shortened_data_cell == '...':
            cleaned_data_cells.append('')
            continue
        bad_index = -1
        for index, char in enumerate(shortened_data_cell):
            if char in ascii_lowercase:
                bad_index = index
                break
        try:
            if bad_index is -1:
                cleaned_data_cells.append(eval(shortened_data_cell))
            else:
                cleaned_data_cells.append(eval(shortened_data_cell[:bad_index]))
        except:
            cleaned_data_cells.append(data_cell)
    section_dict = dict(zip(cleaned_row_headers, cleaned_data_cells))
    return section_dict

def scrape_country_data(country_page: BeautifulSoup) -> Dict[str, Any]:
    """Scrapes data for an individual country from a url and returns a dict"""
    country_data_dict = {}
    # Gets all the section names
    sections = [summary.text for summary in country_page.find_all('summary')]
    # For each section, adds the data
    for section in sections:
        country_data_dict.update(get_country_detail(country_page, section))
    return country_data_dict

def export_to_csv(country_data: List[Dict[str, Any]], data_out_path: str) -> None:
    """Exports country_data as a csv to data_out_path"""
    pass

def run_country_scraper():
    """Runs the scraper and saves the results in un_output.json"""
    # Base url of the site
    base_url = 'http://data.un.org/en/'
    # URL for the list of countries
    country_list_url: str = 'http://data.un.org/en/index.html'
    # Creates a BeautifulSoup object from the country list page
    country_list_page = BeautifulSoup(requests.get(country_list_url).content, 'html5lib')
    # Calls a function to get the country list
    country_list = get_country_list(country_list_page)
    # Iterate over the list of countries to get data for each country
    country_data = []
    for country_name, country_url in country_list.items():
        # Wait .1 seconds so we don't overload the server
        time.sleep(.1)
        print(f'Scraping {country_name}')
        # Create a BeautifulSoup from the individual country page
        country_soup = BeautifulSoup(requests.get(f'{base_url}{country_url}').content, 'html5lib')
        # Calls scrape_country_data, combines that data with the country name, and adds it to the list
        country_data.append({'country_name': country_name, **scrape_country_data(country_soup)})
    with open('un_output.json', 'w') as output_file:
        json.dump(country_data, output_file)
    print('Data output to un_output.json')

# Entry point of script
if __name__ == '__main__':
    run_country_scraper()

