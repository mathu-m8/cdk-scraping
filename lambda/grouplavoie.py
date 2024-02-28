import requests
from bs4 import BeautifulSoup
import json

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
    "school_taxes": "tax_school",
    "condo_fees": "asking_price_condo",
    "equipment_available": "equipment_services",
    "topography": "lot_topography",
    "mls": "uls_number",
    "type": "building_type"
}


def lambda_handler(event, response):
    # body = json.loads(event["body"])
    try:
        url = event["url"]
        # url = body["url"]
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        table = soup.select('table')
        data = {}
        bathroom_element = soup.find('i', class_='c-property-details-bar__bathrooms')
        bedroom_element = soup.find('i', class_='c-property-details-bar__bedrooms')
        data["description_en"] = soup.select_one(".l-article__content--with-border").find('p').text
        address = soup.select_one('.c-property-details-bar__name').text.strip()
        data["address_newdev_salesoffices"] = ' '.join(address.split())
        data["asking_price"] = soup.select_one('.c-property-details-bar__price').text.strip()
        property_details = soup.select_one('.c-property-details-bar__name').text.strip()
        data["city_id"] = property_details.split('\n')[-1].split(',')[0].strip()

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
        print(len(data))
        json_students_data = json.dumps(data, indent=2)
        with open('duplicate.json', 'w') as json_file:
            json_file.write(json_students_data)
        mapped_data_jon = json.dumps(mapped_data, indent=2)
        with open('map.json', 'w') as json_file:
            json_file.write(mapped_data_jon)

        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'text/plain'
            },
            'body': json.dumps(mapped_data)
        }

    except requests.RequestException as e:
        return {
            'statusCode': 500,
            'body': f'Request failed: {str(e)}'
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': f'An error occurred: {str(e)}'
        }


if __name__ == '__main__':
    lambda_handler(
        {
            "url": "https://groupelavoie.com/en/houses-for-sale/commercial-building-office-503-boul-de-melocheville-j6n0e2-beauharnois-21084302/"},
        None)
