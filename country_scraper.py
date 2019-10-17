from typing import Dict, List, Any
import time
import requests
from bs4 import BeautifulSoup
import pandas as pd

# Jacob
def get_country_list(country_list_page: BeautifulSoup) -> List[str]:
    """Get the list of country URLs from list of a tags"""
    pass

# Aileen
def get_general_information(country_page: BeautifulSoup) -> Dict[str, Any]:
    """Get country info from general information block as a dict"""
    pass

# Jacob
def get_economic_indicators(country_page: BeautifulSoup) -> Dict[str, Any]:
    """Get country info from economic indicators block as a dict"""
    pass

def get_social_indicators(country_page: BeautifulSoup) -> Dict[str, Any]:
    """Get country info from social indicators block as a dict"""
    pass

def get_environmental_indicators(country_page: BeautifulSoup) -> Dict[str, Any]:
    """Get country info from environmental and infrastructure indicators block as a dict"""
    pass

# Jacob
def scrape_country_data(country_page: BeautifulSoup) -> Dict[str, Any]:
    """Scrapes data for an individual country from a url and returns a dict"""
    pass

# Jacob
def scrape_countries_data(countries_list_url: str) -> Dict[str, Any]:
    """Scrapes all country data from a list of countries url and yields each row as a dict"""
    pass

# Jacob
def export_to_csv(country_data: List[Dict[str, Any]], data_out_path: str) -> None:
    """Exports country_data as a csv to data_out_path"""
    pass

# Entry point of script
if __name__ == '__main__':
    country_list_url: str = 'http://data.un.org/en/index.html'
    test_country_url: str = 'http://data.un.org/en/iso/af.html'
    # The following line makes an HTTP request to the sample country's URL and parses it as a soup object
    test_soup = BeautifulSoup(requests.get(test_country_url).content, 'html.parser')
    # This test_soup can be passed to the get methods we are implementing to test them

