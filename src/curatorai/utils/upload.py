from minio import Minio
from minio.error import S3Error
import os

def upload_file_to_bucket(file_path: str, bucket_name: str, object_name: str) -> str:
    try:
        # Create a client with the MinIO server playground, its access key and secret key.
        client = Minio("play.min.io",
                    access_key=os.getenv("S3_ACCESS_KEY"),
                    secret_key=os.getenv("S3_SECRET_KEY"),
                    secure=True)

        # Use the provided destination file name
        destination_file = object_name

        # Make the bucket if it doesn't exist.
        found = client.bucket_exists(bucket_name)
        if not found:
            client.make_bucket(bucket_name)
            print("Created bucket", bucket_name)
        else:
            print("Bucket", bucket_name, "already exists")

        # Upload the file, renaming it in the process
        client.fput_object(bucket_name, destination_file, file_path)
        print(file_path, "successfully uploaded as object", destination_file, "to bucket", bucket_name)

        # Generate the URL of the uploaded file
        file_url = client.presigned_get_object(bucket_name, destination_file)
        print("File URL:", file_url)
        return file_url
    except S3Error as e:
        print("Error occurred while uploading file: ", e)

#file = upload_file_to_bucket("/Users/annajohnson/Downloads/curatorai/requirements.txt", "images")

#print(file)