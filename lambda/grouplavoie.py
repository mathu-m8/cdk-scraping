import requests
from bs4 import BeautifulSoup
import json

field_mapping = {
    "bathroom_count": "bathrooms",
    "bedroom_count": "bedrooms",
    "heating_system": "heating",
    "rental_appliances": "appliances_newdev",
    "proximity": "proximity",
    "sewage_system": "sewage_system",
    "roofing": "roof",
    "view": "view",
    "zoning": "zonage",
    "real_estate_broker(s)": "uls_number",
    "mls": "uls_number_condo",
    "building_year:": "year_built_condo",
    "type": "unit_type",
    "municipal_taxes": "tax_municipal",
    "school_taxes": "tax_school",
    "condo_fees": "cost_common_monthly",
    "additional_information": "website_url_en"
}

def lambda_handler(event, response):
    body = json.loads(event["body"])
    url = body["url"]
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    table = soup.select('table')
    data = {}
    bathroom_element = soup.find('i', class_='c-property-details-bar__bathrooms')
    bedroom_element = soup.find('i', class_='c-property-details-bar__bedrooms')

    if bathroom_element:
        bathroom_count = bathroom_element.find_next('span', class_='c-property-details-bar__number').text.strip()
        data['bathroom_count'] = bathroom_count
    if bedroom_element:
        bedroom_count = bedroom_element.find_next('span', class_='c-property-details-bar__number').text.strip()
        data['bedroom_count'] = bedroom_count

    for row in table:
        for tr in row.find_all('tr'):
            if tr.find('td'):
                key = tr.find('td').text.strip().lower().replace(' ', '_')
                value = tr.find_all('td')[1].text.strip()
                if key not in data:
                    data[key] = value

    characteristics = soup.select('.c-caracteristiques__row')
    for row_div in characteristics:
        if row_div:
            key = row_div.find('div', recursive=False).text.strip().lower().replace('/', '').replace(' ', '_')
            value = row_div.find_all('div', recursive=False)[1].text.strip()
            data[key] = value
    subtitle_elements = soup.find_all('h2', class_='c-sidebar-property__subtitle')
    for subtitle_element in subtitle_elements:
        key = subtitle_element.text.strip().replace(" ", "_").lower()
        value_element = subtitle_element.find_next(class_='c-sidebar-property__info')
        if value_element:
            value = value_element.text.strip()
            data[key] = value

    mapped_data = {field_mapping.get(key, key): value for key, value in data.items()}

    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'text/plain'
        },
        'body': format(mapped_data)
    }