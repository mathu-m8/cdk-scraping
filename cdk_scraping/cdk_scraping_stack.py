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
        bucket = s3.Bucket(self, "ScrapingStore")

        group_function = lambda_python.PythonFunction(
            self, "groupLavoie",
            runtime=Runtime.PYTHON_3_12,
            entry="lambda",
            handler="lambda_handler",
            index="grouplavoie.py",
            environment=dict(
                BUCKET=bucket.bucket_name)
        )

        inscriptions_function = lambda_python.PythonFunction(
            self, "jollebite",
            runtime=Runtime.PYTHON_3_12,
            entry="lambda",
            handler="lambda_handler",
            index="inscriptions.py",
            environment=dict(
                BUCKET=bucket.bucket_name)
        )

        bucket.grant_read_write(group_function)

        api = apigateway.RestApi(self, "scraping-groupLavoie-api",
                                 rest_api_name="Scraping GroupLavoie",
                                 description="Scraping GroupLavoie details")

        get_widgets_integration = apigateway.LambdaIntegration(group_function,
                                                               request_templates={
                                                                   "application/json": '{ "statusCode": "200" }'})

        api.root.add_method("POST", get_widgets_integration)

        api = apigateway.RestApi(self, "scraping-inscriptions-api",
                                 rest_api_name="Scraping inscriptions",
                                 description="Scraping inscriptions details")

        get_widgets_integration_for_inscriptions = apigateway.LambdaIntegration(inscriptions_function,
                                                                                request_templates={
                                                                                    "application/json": '{ "statusCode": "200" }'})

        api.root.add_method("POST", get_widgets_integration_for_inscriptions)