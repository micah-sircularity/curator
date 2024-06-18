from minio import Minio
from minio.error import S3Error

def upload_file_to_bucket(source_file_path, bucket_name, destination_file_name):
    # Create a client with the MinIO server playground, its access key and secret key.
    client = Minio("bucket-production-36c0.up.railway.app",
                   access_key="9HuQB4dYiwzLQlkwtLd3",
                   secret_key="ahoqbEbEW7pyW1M3dHEQBSg5Ofxjn2FNGnaIEFLX",
                   )

    # Use the provided destination file name
    destination_file = destination_file_name

    # Make the bucket if it doesn't exist.
    found = client.bucket_exists(bucket_name)
    if not found:
        client.make_bucket(bucket_name)
        print("Created bucket", bucket_name)
    else:
        print("Bucket", bucket_name, "already exists")

    # Upload the file, renaming it in the process
    client.fput_object(bucket_name, destination_file, source_file_path)
    print(source_file_path, "successfully uploaded as object", destination_file, "to bucket", bucket_name)

    # Generate the URL of the uploaded file
    file_url = client.presigned_get_object(bucket_name, destination_file)
    print("File URL:", file_url)
    return file_url

#file = upload_file_to_bucket("/Users/annajohnson/Downloads/curatorai/requirements.txt", "images")

#print(file)