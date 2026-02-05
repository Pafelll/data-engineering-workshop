import pandas as pd
from concurrent.futures import ThreadPoolExecutor
from google.cloud import storage
from google.api_core.exceptions import NotFound, Forbidden
import time
from io import BytesIO


BUCKET_NAME = "zoomcamp-485019-bucket"
MONTHS = [f"{i:02d}" for i in range(1, 7)]

CREDENTIALS_FILE = "kestra-secret-key.json"
client = storage.Client.from_service_account_json(CREDENTIALS_FILE)


CHUNK_SIZE = 8 * 1024 * 1024

bucket = client.bucket(BUCKET_NAME)


def create_bucket(bucket_name):
    try:
        client.get_bucket(bucket_name)
        project_bucket_ids = [bckt.id for bckt in client.list_buckets()]
        if bucket_name in project_bucket_ids:
            print(
                f"Bucket '{bucket_name}' exists and belongs to your project. Proceeding..."
            )
        else:
            print(
                f"A bucket with the name '{bucket_name}' already exists, but it does not belong to your project."
            )

    except NotFound:
        client.create_bucket(bucket_name)
        print(f"Created bucket '{bucket_name}'")
    except Forbidden:
        print(
            f"A bucket with the name '{bucket_name}' exists, but it is not accessible. Bucket name is taken. Please try a different bucket name."
        )


def verify_gcs_upload(blob_name):
    return storage.Blob(bucket=bucket, name=blob_name).exists(client)


def upload_to_gcs(file_path, blob_name, max_retries=3):
    blob = bucket.blob(blob_name)
    blob.chunk_size = CHUNK_SIZE

    create_bucket(BUCKET_NAME)

    for attempt in range(max_retries):
        try:
            print(f"Uploading {file_path} to {BUCKET_NAME} (Attempt {attempt + 1})...")
            blob.upload_from_file(file_path)
            print(f"Uploaded: gs://{BUCKET_NAME}/{blob_name}")

            if verify_gcs_upload(blob_name):
                print(f"Verification successful for {blob_name}")
                return
            else:
                print(f"Verification failed for {blob_name}, retrying...")
        except Exception as e:
            print(f"Failed to upload {file_path} to GCS: {e}")

        time.sleep(5)

    print(f"Giving up on {file_path} after {max_retries} attempts.")


def fetch_files_and_upload(month):
    url = f"https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2024-{month}.parquet"
    df = pd.read_parquet(url)
    buffer = BytesIO()
    df.to_parquet(buffer, index=False)
    buffer.seek(0)
    blob_name = url.split("/")[-1]
    upload_to_gcs(buffer, blob_name)


if __name__ == "__main__":
    create_bucket(BUCKET_NAME)

    with ThreadPoolExecutor(max_workers=4) as executor:
        executor.map(fetch_files_and_upload, MONTHS)

    print("All files processed and verified.")