import json
import requests

field_mapping = {
    "mls_no": "uls_number",
    "price_buy": "asking_price",
    "price_rent": "asking_price_condo",
    "postal_code": "area_code",
    "occupation_date": "occupation",
    "total_number_of_rooms": "rooms",
    "property_type": "unit_type",
    "year_constructed": "year_built"
}


def lambda_handler(event, response):
    session = requests.Session()
    body = json.loads(event["body"])
    url = body["url"]

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
        mapped_data = {field_mapping.get(key, key): value for key, value in property_details.items()}

        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'text/plain'
            },
            'body': format(mapped_data)
        }
