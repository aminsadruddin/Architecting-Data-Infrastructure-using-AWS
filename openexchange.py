import requests
import boto3
from datetime import datetime
import os

def lambda_handler(event, context):
    api_key = os.environ["OER_API_KEY"]
    url = f"https://openexchangerates.org/api/latest.json?app_id={api_key}"
    response = requests.get(url)
    data = response.json()
    
    # Upload to S3
    now = datetime.utcnow()
    file_path = f"raw/OpenExchangeRates/{now:%Y/%m/%d}/{now:%H%M}.json"
    s3 = boto3.client("s3")
    s3.put_object(
        Bucket="data-hackathon-smit-amin",
        Key=file_path,
        Body=json.dumps(data),
        Metadata={"source": "OpenExchangeRates", "timestamp": now.isoformat()}
    )