"""
Manages access to google drive ressources
"""

from io import BytesIO
import json
from google.oauth2 import service_account
from googleapiclient.discovery import build
from constants import JSON_KEY_FILE, SCOPES, STATS_SALARIES_FILE_ID
from googleapiclient.http import MediaIoBaseUpload


# TODO: Banner
# --- SETUP
def authenticate(json_key_file) -> dict[str:build]:
    """Authenticate with Google Drive API using service account credentials."""
    credentials = service_account.Credentials.from_service_account_file(
        json_key_file, scopes=SCOPES
    )
    DRIVE_SERVICE = build("drive", "v3", credentials=credentials)
    return DRIVE_SERVICE


DRIVE_SERVICE = authenticate(JSON_KEY_FILE)


# TODO: Banner for usefull functions to write/read files stored in google drive

# TODO: organize functions and clean the documentation

# TODO: Remove all comments. Keep only the documentation.

# TODO: add clean logging INSTEAD of debug prints (very important)
# Always have a clean format for errors => already setup with json logger format in settings


def list_files(folder_id="root"):
    """List all files in Google Drive."""
    files_tree = {}
    results = (
        DRIVE_SERVICE.files()
        .list(
            pageSize=10,
            fields="nextPageToken, files(id, name, mimeType)",
            q=f"'{folder_id}' in parents",
        )
        .execute()
    )

    items = results.get("files", [])
    for item in items:
        if item["mimeType"] == "application/vnd.google-apps.folder":
            folder_info = {"id": item["id"]}
            folder_info.update(list_files(item["id"]))
            files_tree[item["name"]] = folder_info
        else:
            files_tree[item["name"]] = item["id"]
    return files_tree


def delete_file(file_id):
    """Delete a file given its ID."""
    try:
        DRIVE_SERVICE.files().delete(fileId=file_id).execute()
        print(f"File with ID {file_id} has been deleted successfully.")
    except Exception as e:
        print(f"An error occurred while deleting the file: {e}")


def delete_folder(folder_id):
    """Delete a folder and all files inside it given its ID."""
    try:
        # List all files in the folder
        files = (
            DRIVE_SERVICE.files()
            .list(q=f"'{folder_id}' in parents", fields="files(id)")
            .execute()
        )
        file_ids = [file["id"] for file in files.get("files", [])]

        # Delete each file inside the folder
        for file_id in file_ids:
            DRIVE_SERVICE.files().delete(fileId=file_id).execute()
            print(f"{file_id} has been deleted succesfully")

        # Delete the folder itself
        DRIVE_SERVICE.files().delete(fileId=folder_id).execute()

        print(
            f"Folder with ID {folder_id} and all its files have been deleted successfully."
        )
    except Exception as e:
        print(f"An error occurred while deleting the folder: {e}")


def read_json_file(file_id):
    """Read the content of a JSON file."""
    request = DRIVE_SERVICE.files().get_media(fileId=file_id)
    json_content = request.execute()
    decoded_string = json_content.decode("utf-8")
    json_data = json.loads(decoded_string)
    return json_data


def create_folder(folder_name, parent_id="root"):
    """Create a folder with the given name and parent folder ID."""
    try:
        folder_metadata = {
            "name": folder_name,
            "mimeType": "application/vnd.google-apps.folder",
            "parents": [parent_id],
        }
        folder = (
            DRIVE_SERVICE.files().create(body=folder_metadata, fields="id").execute()
        )
        print(f"Folder '{folder_name}' created with ID: {folder.get('id')}")
        return folder.get("id")
    except Exception as e:
        print(f"An error occurred while creating the folder: {e}")
        return None


def create_json_file(file_name, json_content, parent_id="root"):
    """Create a JSON file with the given name, content, and parent folder ID."""
    try:
        media_body = MediaIoBaseUpload(
            BytesIO(json.dumps(json_content).encode("utf-8")),
            mimetype="application/json",
        )
        file_metadata = {"name": file_name, "parents": [parent_id]}
        file = (
            DRIVE_SERVICE.files()
            .create(body=file_metadata, media_body=media_body, fields="id")
            .execute()
        )
        print(f"JSON file '{file_name}' created with ID: {file.get('id')}")
        return file.get("id")
    except Exception as e:
        print(f"An error occurred while creating the JSON file: {e}")
        return None


json_data = read_json_file(STATS_SALARIES_FILE_ID)
print(json.dumps(json_data, indent=4))
