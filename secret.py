# Import the Secret Manager client library.
from google.cloud import secretmanager

import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="private/bookcal-7b8357d4f2f3.json"

# GCP project in which to store secrets in Secret Manager.
project_id = "bookcal-300821"

# ID of the secret to create.
secret_id = "my-secret_value3"

# # Create the Secret Manager client.
# client = secretmanager.SecretManagerServiceClient()

# # Build the parent name from the project.
# parent = f"projects/{project_id}"

# # Create the parent secret.
# secret = client.create_secret(
#     request={
#         "parent": parent,
#         "secret_id": secret_id,
#         "secret": {"replication": {"automatic": {}}},
#     }
# )

# # Add the secret version.
# version = client.add_secret_version(
#     request={"parent": secret.name, "payload": {"data": b"hello world!"}}
# )

# # Access the secret version.
# response = client.access_secret_version(request={"name": version.name})

# # Print the secret payload.
# #
# # WARNING: Do not print the secret in a production environment - this
# # snippet is showing how to access the secret material.
# payload = response.payload.data.decode("UTF-8")
# print("Plaintext: {}".format(payload))

def access_secret_version(project_id, secret_id, version_id="latest"):
    # Create the Secret Manager client.
    client = secretmanager.SecretManagerServiceClient()

    # Build the resource name of the secret version.
    name = f"projects/{project_id}/secrets/{secret_id}/versions/{version_id}"

    # Access the secret version.
    response = client.access_secret_version(name=name)

    # Return the decoded payload.
    return response.payload.data.decode('UTF-8')

print(access_secret_version(project_id, secret_id))


def access_secret(project_id, secret_id, version):
    """
    Access a secret- API token, etc- stored in Secret Manager

    Code from https://cloud.google.com/secret-manager/docs/creating-and-accessing-secrets#secretmanager-access-secret-version-python
    """
    client = secretmanager.SecretManagerServiceClient()

    # Build the resource name of the secret version
    name = client.secret_version_path(project_id, secret_id, version)

    # Access the secret version
    response = client.access_secret_version(name=name)

    # Return the secret payload
    payload = response.payload.data.decode('UTF-8')

    return payload

print( access_secret(project_id, secret_id, 'latest'))