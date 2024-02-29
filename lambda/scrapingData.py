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
            inscriptions_data = inscriptions.getJoellebitarDetails(url)
            return inscriptions_data
        case "groupelavoie.com":
            grouplavoie_data = grouplavoie.getGroupelavoieDetails(url)
            return grouplavoie_data
        case _:
            return {
                'statusCode': 500,
                'body': 'Please check your url'
            }
