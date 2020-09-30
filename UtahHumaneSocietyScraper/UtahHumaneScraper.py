import requests
from bs4 import BeautifulSoup
from datetime import datetime, date
import re

#Beautiful Soup/Python web scrapper documentation found here: https://realpython.com/beautiful-soup-web-scraper-python/
availableAnimals = []

def get_age (age_elementString):
    if re.match('^getWords\(\d{1}\);$', age_elementString):
        return age_elementString[9]
    elif re.match('^getWords\(\d{2}\);$', age_elementString):
        return age_elementString[9:11]
    if re.match('^getWords\(\d{3}\);$', age_elementString):
        return age_elementString[9:12]
    else:
        return 'this shouldnt happen.'
    
def get_price (price_elementString):
    if re.match('^price\(\d{1}\);$', price_elementString):
        return price_elementString[6]
    elif re.match('^price\(\d{2}\);$', price_elementString):
        return price_elementString[6:8]
    if re.match('^price\(\d{3}\);$', price_elementString):
        return price_elementString[6:9]
    else:
        return 'this shouldnt happen.'

URL = 'https://www.utahhumane.org/adopt?f%5B0%5D=field_species%3A3'
page = requests.get(URL)
soup = BeautifulSoup(page.content, 'html.parser')
results = soup.find(class_='adoption-search')
job_elements = results.find_all('div', class_='item')

listings = []

for job_element in job_elements:
    listing_number = job_element.find('span')
    listings.append(listing_number.text)
    
# At this point, we have all of the listings on the Humane Society of Utah.

outputFileName = 'UtahHumanParsed'+ str(date.today()) +'.txt'
output = open(outputFileName, 'w', encoding='cp1252')
output.write('UP TO DATE AS OF: ' + str(datetime.now())+ '\n')

for listing in listings:
    URL = 'https://www.utahhumane.org/listing/' + str(listing)
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, 'html.parser')
    results = soup.find(class_='ds-2col-stacked-fluid node node-pet view-mode-full clearfix')
    job_element = results.find('div', class_='group-right')
    
    name_element = job_element.find('h2')
    sex_element = job_element.find('div', class_='field field-name-field-sex field-type-list-text')
    primary_breed_element = job_element.find('div', class_='field field-name-field-primary-breed field-type-taxonomy-term-reference')
    weight_element = job_element.find('div', class_='field field-name-weight field-type-ds')
    age_element = job_element.find('div', class_='field field-name-age-converter field-type-ds')
    availabilty_element = job_element.find('div', class_='field field-name-field-kennelstatus field-type-taxonomy-term-reference')
    price_element = job_element.find('div', class_='field field-name-price-converter field-type-ds')
    
    age_element = age_element.text.split()[-1]
    price_element = price_element.text.split()[-1]
    
    name = name_element.text
    sex = sex_element.text.split()[1]
    breed = ''.join(primary_breed_element.text.split()[2:])
    weight = weight_element.text.split()[1]
    age = get_age(age_element)
    availability = availabilty_element.text.split()[1]
    price = get_price(price_element)
    availableAnimals.append((name, sex, breed, weight, age, availability, price))
    output.write('Name: ' + name + '\tSex: ' + sex + '\tBreed: ' + breed + '\tWeight: ' + weight + '\tAge(Months): ' + age + '\tAvailability: ' + availability + '\tPrice: ' + price + '\n')

output.close()