from uuid import uuid4
from tempfile import TemporaryDirectory
from os import getenv

from google.oauth2 import service_account
from google.cloud.storage import Client
from google.cloud.storage.blob import Blob
from google.cloud.exceptions import NotFound
from datetime import datetime, timedelta, UTC

from config import BUCKET_NAME, SA_KEY_PATH


def get_gcs_client() -> Client:
    if sa_credentials := getenv("SA_CREDENTIALS"):
        from json import loads
        credentials = service_account.Credentials.from_service_account_info(loads(sa_credentials))
        client = Client(credentials=credentials)
    else:
        credentials = service_account.Credentials.from_service_account_file(SA_KEY_PATH)
        client = Client(credentials=credentials)

    return client


client = get_gcs_client()


def upload_bytes_image(
    image_bytes: bytes, image_extension: str = ".webp", content_type: str = "image/webp"
) -> str:
    file_name = f"{uuid4()}{image_extension}"

    with TemporaryDirectory() as temp_dir:
        temp_file_path = f"{temp_dir}/{file_name}"
        with open(temp_file_path, "wb") as temp_file:
            temp_file.write(image_bytes)

        bucket = client.get_bucket(BUCKET_NAME)

        blob = bucket.blob(file_name)
        blob.upload_from_filename(temp_file_path, content_type=content_type)

    return file_name


def generate_signed_url(file_name, expiration_hours=1):
    try:
        print(client._credentials)
        bucket = client.bucket(BUCKET_NAME)
        blob = Blob(file_name, bucket)

        expiration_time = datetime.now(UTC) + timedelta(hours=expiration_hours)
        signed_url = blob.generate_signed_url(
            version="v4", expiration=expiration_time, method="GET"
        )

        return signed_url
    except Exception as e:
        print(f"Error generating signed URL: {e}")
        return ""


def delete_blob_by_file_name(file_name: str) -> None:
    try:
        bucket = client.bucket(BUCKET_NAME)
        blob = bucket.blob(file_name)
        blob.delete()
        print(f"Deleted {file_name} from storage")
    except NotFound:
        print(f"{file_name} not found in storage")
