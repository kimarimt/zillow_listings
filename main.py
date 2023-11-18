import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By

from listing import Listing


def get_listings():
    page = requests.get('https://appbrewery.github.io/Zillow-Clone/')
    soup = BeautifulSoup(page.content, 'html.parser')
    listings_data = soup.find_all(
        'li', class_='ListItem-c11n-8-84-3-StyledListCardWrapper')
    listings = []

    for listing_data in listings_data:
        address_data = listing_data.find(
            'address').text.strip().split(' | ')[-1].split(', ')
        price_data = listing_data.find(
            'span',
            class_='PropertyCardWrapper__StyledPriceLine').text.replace(
            ',',
            '')

        address = ', '.join(address_data) if len(
            address_data) == 3 else ', '.join(address_data[1:])
        price = price_data[:5]
        link = listing_data.find(
            'a', class_='StyledPropertyCardDataArea-anchor')['href']
        listings.append(Listing(address, price, link))

    return listings


def populate_form(listings):
    form_link = 'https://forms.gle/Hv7TmZMc3amTAfG37'
    driver = webdriver.Firefox()
    
    for listing in listings:
        driver.get(form_link)

        address_field = driver.find_element(By.CSS_SELECTOR, 'input[aria-labelledby="i1"]')
        price_field = driver.find_element(By.CSS_SELECTOR, 'input[aria-labelledby="i5"]')
        link_field = driver.find_element(By.CSS_SELECTOR, 'input[aria-labelledby="i9"]')
        submit_button = driver.find_element(By.CLASS_NAME, 'l4V7wb')

        address_field.click()
        address_field.send_keys(listing.address)
        price_field.click()
        price_field.send_keys(listing.price)
        link_field.click()
        link_field.send_keys(listing.link)
        submit_button.click()

    driver.close()


def main():
    listings = get_listings()
    populate_form(listings)


if __name__ == '__main__':
    main()
