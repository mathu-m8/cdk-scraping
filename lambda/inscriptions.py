# joellebitar.com
import json
import requests

field_mapping = {
    "mls_no": "uls_number",
    "price_buy": "asking_price",
    "price_rent": "asking_price_condo",
    "municipality_code": "city_id",
    "street_name": "street_name",
    "postal_code": "postal_code",
    "year_constructed": "year_built",
    "liveable_area": "living_space_area",
    "facade_batiment": "facade_terrain",
    "profondeur_batiment": "profondeur_terrain",
    "superficie_terrain": "superficie_terrain",
    "annee_evaluation": "tax_year",
    "evaluation_municipale_terrain": "assessment_municipal_land",
    "evaluation_municipale_batiment": "assessment_municipal_building",
    "bedrooms": "bedrooms",
    "bathrooms": "bathrooms",
    "powder_rooms": "bathrooms_half",
    "waterfront": "waterfront",
    "date_added": "date_added",
    "status": "status",
    "latitude": "latitude",
    "longitude": "longitude",
    "remarks": "description_en",
    "parking_interior": "parking",
    "parking_exterior": "parking_spaces",
    'total_number_of_rooms': 'rooms',
    "property_type": "unit_type",
    "region_code": "region_id",
    "virtual_visit_url": "video_url_en",
    "full_address": "address_newdev_salesoffices",
    "annee_evaluation": "assessment_municipal_year",
    "year_constructed": "year_built_condo",
}


def getJoellebitarDetails(url):
    session = requests.Session()
    headers = {
        'authority': 'joellebitar.com',
        'accept': '*/*',
        'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
        'cookie': '_gcl_au=1.1.363217433.1708420908; _fbp=fb.1.1708420910008.39121455; PHPSESSID=dce2c939d03805ac53a8badff6b3ce6e; _ga=GA1.2.1403743402.1708420910; _gid=GA1.2.192695077.1708936487; _ga_JPHCNP4QPX=GS1.1.1708936486.2.0.1708936547.60.0.0',
        'referer': url,
        'sec-ch-ua': '"Chromium";v="122", "Not(A:Brand";v="24", "Google Chrome";v="122"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
        'x-requested-with': 'XMLHttpRequest'
    }
    custom_url = url.split('/')
    if custom_url[len(custom_url) - 1] == '':
        ref_number = custom_url[len(custom_url) - 2]
    else:
        ref_number = custom_url.pop()
    get_url = f"https://joellebitar.com/wp-json/mw-properties/v2/properties?mls={ref_number}&type=single"
    data = session.get(get_url, headers=headers)
    if data.status_code == 200:
        details = json.loads(data.text)
        property_details = details.get('results', [])[0].get('property', {})
        if property_details["full_address"]:
            property_details["street_number"] = property_details["full_address"].split(' ')[0]
        mapped_data = {field_mapping.get(key, key): value for key, value in property_details.items()}
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Content-Type': 'application/json'
            },
            'body': json.dumps(mapped_data),
        }
