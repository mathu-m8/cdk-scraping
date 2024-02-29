from aws_cdk import (
    Stack,
)
from constructs import Construct

from aws_cdk.aws_lambda import Runtime

from aws_cdk import aws_lambda_python_alpha as lambda_python
from aws_cdk import (aws_apigateway as apigateway,
                     aws_s3 as s3)


class CdkScrapingStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        bucket = s3.Bucket(self, "ScrapingDataStore")

        scraping_function = lambda_python.PythonFunction(
            self, "scrapingData",
            runtime=Runtime.PYTHON_3_12,
            entry="lambda",
            handler="lambda_handler",
            index="scrapingData.py",
            environment=dict(
                BUCKET=bucket.bucket_name)
        )

        bucket.grant_read_write(scraping_function)

        api = apigateway.RestApi(self, "scraping-api",
                                 rest_api_name="Scraping Data",
                                 description="Scraping details")

        get_widgets_integration = apigateway.LambdaIntegration(scraping_function,
                                                               request_templates={
                                                                   "application/json": '{ "statusCode": "200" }'})

        api.root.add_method("POST", get_widgets_integration)
