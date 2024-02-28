import requests
from bs4 import BeautifulSoup
import json

# field_mapping = {
#     "bathroom_count": "bathrooms",
#     "bedroom_count": "bedrooms",
#     "heating_system": "heating",
#     "rental_appliances": "appliances_newdev",
#     "proximity": "proximity",
#     "sewage_system": "sewage_system",
#     "roofing": "roof",
#     "view": "view",
#     "zoning": "zonage",
#     "real_estate_broker(s)": "uls_number",
#     "mls": "uls_number_condo",
#     "building_year:": "year_built_condo",
#     "type": "unit_type",
#     "municipal_taxes": "tax_municipal",
#     "school_taxes": "tax_school",
#     "condo_fees": "cost_common_monthly",
#     "additional_information": "website_url_en"
# }

field_mapping = {
    "bathroom_count": "bathrooms",
    "bedroom_count": "bedrooms",
    "lot_size": "lot_area",
    "land_area:": "lot_area_units",
    "driveway": "driveway",
    "cupboard": "kitchen_cabinets",
    "heating_system": "heating",
    "water_supply": "water_supply",
    "windows": "windows",
    "foundation": "foundation",
    "garage": "garage",
    "siding": "siding",
    "pool": "pool",
    "proximity": "proximity",
    "sewage_system": "sewage_system",
    "roofing": "roof",
    "zoning": "zonage",
    "building_year:": "year_built",
    "municipal_evaluation": "assessment_municipal_building",
    "municipal_taxes": "tax_municipal",
    "school_taxes": "tax_school"
}


def lambda_handler(event, response):
    body = json.loads(event["body"])
    # url = event["url"]
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
    # print(len(data))
    # json_students_data = json.dumps(data, indent=2)
    # with open('duplicate.json', 'w') as json_file:
    #     json_file.write(json_students_data)
    # mapped_data_jon = json.dumps(mapped_data, indent=2)
    # with open('map.json', 'w') as json_file:
    #     json_file.write(mapped_data_jon)
    #
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'text/plain'
        },
        'body': json.dumps(mapped_data)
    }


if __name__ == '__main__':
    lambda_handler(
        {"url": "https://groupelavoie.com/en/houses-for-sale/bungalow-21-ch-d-auteuil-j5r2c8-candiac-10564720/"}, None)
