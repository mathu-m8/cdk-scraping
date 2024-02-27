#!/usr/bin/env python3

import aws_cdk as cdk

from cdk_scraping.cdk_scraping_stack import CdkScrapingStack


app = cdk.App()
CdkScrapingStack(app, "CdkScrapingStack")

app.synth()
