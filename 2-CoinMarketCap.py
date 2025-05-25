import requests
from bs4 import BeautifulSoup
import boto3
from datetime import datetime

def lambda_handler(event, context):
    url = "https://coinmarketcap.com"
    response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
    soup = BeautifulSoup(response.text, "html.parser")
    
    # Extract top 10 cryptos
    rows = soup.find("table", {"class": "cmc-table"}).find_all("tr")[1:11]
    data = []
    for row in rows:
        cols = row.find_all("td")
        name = cols[2].text.strip()
        symbol = cols[3].text.strip()
        data.append(f"{name},{symbol}")
    
    # Upload to S3
    now = datetime.utcnow()
    file_path = f"raw/CoinMarketCap/{now:%Y/%m/%d}/{now:%H%M}.csv"
    s3 = boto3.client("s3")
    s3.put_object(
        Bucket="data-hackathon-smit-amin",
        Key=file_path,
        Body="\n".join(data),
        Metadata={"source": "CoinMarketCap", "timestamp": now.isoformat()}
    )