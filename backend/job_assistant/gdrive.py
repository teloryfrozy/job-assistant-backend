"""
Manages access to google drive ressources
"""

from io import BytesIO
import json
import logging
from google.oauth2 import service_account
from googleapiclient.discovery import build
from .constants import GDRIVE_SERVICE_CREDS, SCOPES
from googleapiclient.http import MediaIoBaseUpload


# TODO: Banner for usefull functions to write/read files stored in google drive

# TODO: organize functions and clean the documentation + add all required datatypes and what the functions are returning

# TODO: Remove all comments. Keep only the documentation.

# TODO: add clean logging INSTEAD of debug prints (very important)


######################## LOGGING CONFIGURATION ########################
LOGGER = logging.getLogger(__name__)


class GoogleDriveManager:
    """
    Manages access to Google Drive resources.
    """

    def __init__(self):
        """Authenticate with Google Drive API using service account credentials."""
        credentials = service_account.Credentials.from_service_account_info(
            GDRIVE_SERVICE_CREDS, scopes=SCOPES
        )
        self.drive_service = build(
            "drive", "v3", credentials=credentials, cache_discovery=False
        )

    def list_files(self, folder_id="root"):
        """List all files in a Google Drive folder."""
        files_tree = {}
        results = (
            self.drive_service.files()
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
                folder_info.update(self.list_files(item["id"]))
                files_tree[item["name"]] = folder_info
            else:
                files_tree[item["name"]] = item["id"]
        return files_tree

    def get_file_name(self, file_id: str) -> str | None:
        """
        Retrieves the name of a file from Google Drive given its file ID.

        Args:
            file_id (str): The ID of the file on Google Drive.

        Returns:
            str: The name of the file if found, otherwise None.
        """
        try:
            file = (
                self.drive_service.files().get(fileId=file_id, fields="name").execute()
            )
            return file.get("name")
        except Exception as e:
            LOGGER.error(f"An error occurred: {str(e)}")
            return None

    def delete_file(self, file_id):
        """Delete a file given its ID."""
        try:
            self.drive_service.files().delete(fileId=file_id).execute()
            LOGGER.info(f"File with ID {file_id} has been deleted successfully.")
        except Exception as e:
            LOGGER.error(f"An error occurred while deleting the file: {str(e)}")

    def delete_folder(self, folder_id):
        """Delete a folder and all files inside it given its ID."""
        try:
            files = (
                self.drive_service.files()
                .list(q=f"'{folder_id}' in parents", fields="files(id)")
                .execute()
            )
            file_ids = [file["id"] for file in files.get("files", [])]

            for file_id in file_ids:
                self.drive_service.files().delete(fileId=file_id).execute()
                LOGGER.info(f"File with ID {file_id} has been deleted successfully.")

            self.drive_service.files().delete(fileId=folder_id).execute()
            LOGGER.info(
                f"Folder with ID {folder_id} and all its files have been deleted successfully."
            )
        except Exception as e:
            LOGGER.error(f"An error occurred while deleting the folder: {str(e)}")

    def read_json_file(self, file_id):
        """Read the content of a JSON file."""
        try:
            request = self.drive_service.files().get_media(fileId=file_id)
            json_content = request.execute()
            decoded_string = json_content.decode("utf-8")
            json_data = json.loads(decoded_string)
            return json_data
        except Exception as e:
            LOGGER.error(f"An error occurred while reading the JSON file: {str(e)}")
            return None

    def create_folder(self, folder_name, parent_id="root"):
        """Create a folder with the given name and parent folder ID."""
        try:
            query = (
                f"name='{folder_name}' and '{parent_id}' in parents and trashed=false"
            )
            existing_folders = (
                self.drive_service.files().list(q=query, fields="files(id)").execute()
            )
            if existing_folders.get("files"):
                LOGGER.warning(
                    f"A folder with the name '{folder_name}' already exists in the folder."
                )
                return None

            folder_metadata = {
                "name": folder_name,
                "mimeType": "application/vnd.google-apps.folder",
                "parents": [parent_id],
            }
            folder = (
                self.drive_service.files()
                .create(body=folder_metadata, fields="id")
                .execute()
            )
            LOGGER.info(f"Folder '{folder_name}' created with ID: {folder.get('id')}")
            return folder.get("id")
        except Exception as e:
            LOGGER.error(f"An error occurred while creating the folder: {str(e)}")
            return None

    def create_json_file(self, file_name, json_content, parent_id="root"):
        """Create a JSON file with the given name, content, and parent folder ID."""
        try:
            query = f"name='{file_name}' and '{parent_id}' in parents and trashed=false"
            existing_files = (
                self.drive_service.files().list(q=query, fields="files(id)").execute()
            )
            if existing_files.get("files"):
                LOGGER.warning(
                    f"A file with the name '{file_name}' already exists in the folder."
                )
                return None

            media_body = MediaIoBaseUpload(
                BytesIO(json.dumps(json_content).encode("utf-8")),
                mimetype="application/json",
            )
            file_metadata = {"name": file_name, "parents": [parent_id]}
            file = (
                self.drive_service.files()
                .create(body=file_metadata, media_body=media_body, fields="id")
                .execute()
            )
            LOGGER.info(f"JSON file '{file_name}' created with ID: {file.get('id')}")
            return file.get("id")
        except Exception as e:
            LOGGER.error(f"An error occurred while creating the JSON file: {str(e)}")
            return None

    def overwrite_json_file(self, new_json_data, file_id):
        """Overwrite the content of a JSON file with new data."""
        try:
            new_json_content = json.dumps(new_json_data)

            media_body = MediaIoBaseUpload(
                BytesIO(new_json_content.encode("utf-8")),
                mimetype="application/json",
            )

            updated_file = (
                self.drive_service.files()
                .update(fileId=file_id, media_body=media_body)
                .execute()
            )

            LOGGER.info(f"JSON file with ID '{file_id}' updated successfully.")
            return updated_file
        except Exception as e:
            LOGGER.error(f"An error occurred while updating the JSON file: {str(e)}")
            return None
