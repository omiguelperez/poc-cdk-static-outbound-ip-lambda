import logging
import boto3
from datetime import datetime
import os
import requests

from json import dumps

MY_TABLE = os.getenv("MY_TABLE")
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

dynamodb_client = boto3.resource("dynamodb")


def handler(event, context):
    logger.info("Start function!")

    date = datetime.now()
    time = date.time()

    item = {
        "id": str(time),
    }

    table = dynamodb_client.Table(MY_TABLE)

    table.put_item(Item=item)
    logger.info(f"{dumps(item)=}")

    response = {
        "statusCode": 200,
        "body": dumps(item),
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
        },
    }
    return response
