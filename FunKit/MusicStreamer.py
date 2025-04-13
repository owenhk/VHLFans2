import random
import aioboto3
import os

async def fetch_song() -> str:
    base_url = "https://vhlfans.sfo2.digitaloceanspaces.com"
    session = aioboto3.session.Session()

    async with session.client(
        's3',
        region_name='sfo2',
        endpoint_url='https://sfo2.digitaloceanspaces.com',
        aws_access_key_id=os.getenv("SPACES_ACCESS_KEY_NAME"),
        aws_secret_access_key=os.getenv("SPACES_SECRET_KEY")
    ) as client:
        paginator = client.get_paginator('list_objects_v2')
        urls = []

        async for page in paginator.paginate(Bucket="vhlfans"):
            for obj in page.get("Contents", []):
                key = obj["Key"]
                urls.append(f"{base_url}/{key}")

    return random.choice(urls)