import json
from urllib.parse import urlparse
import inscriptions
import grouplavoie

def lambda_handler(event, response):
    body = json.loads(event["body"])
    url = body["url"]

    parsed_url = urlparse(url)
    domain_name = parsed_url.netloc
    match domain_name:
        case "joellebitar.com":
            inscriptions.getJoellebitarDetails(url)
        case "groupelavoie.com":
            grouplavoie.getGroupelavoieDetails(url)
        case _:
            return {
                'statusCode': 500,
                'body': 'Please check your url'
            }


