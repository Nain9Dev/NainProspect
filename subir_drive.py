"""Archive pipeline outputs into a Google Drive folder.

Uses OAuth 2.0 user credentials, not a service account: service accounts have
no storage quota and cannot own files, and shared drives do not exist on a
consumer Google One account.

Every run creates a dated subfolder so historical results are never
overwritten. Missing configuration is not an error: the pipeline must keep
working when Drive is not set up.
"""

import datetime
import os
import sys

REQUIRED_ENV = (
    "GDRIVE_CLIENT_ID",
    "GDRIVE_CLIENT_SECRET",
    "GDRIVE_REFRESH_TOKEN",
    "GDRIVE_FOLDER_ID",
)

FOLDER_MIME = "application/vnd.google-apps.folder"
TOKEN_URI = "https://oauth2.googleapis.com/token"


def is_configured():
    """Return True when every Drive setting is present."""
    return all(os.environ.get(name, "").strip() for name in REQUIRED_ENV)


def build_service():
    """Build a Drive client from the refresh token."""
    from google.oauth2.credentials import Credentials
    from googleapiclient.discovery import build

    credentials = Credentials(
        None,
        refresh_token=os.environ["GDRIVE_REFRESH_TOKEN"].strip(),
        client_id=os.environ["GDRIVE_CLIENT_ID"].strip(),
        client_secret=os.environ["GDRIVE_CLIENT_SECRET"].strip(),
        token_uri=TOKEN_URI,
    )
    return build("drive", "v3", credentials=credentials, cache_discovery=False)


def create_run_folder(service, parent_id, name):
    """Create the dated subfolder for this run and return its id."""
    metadata = {"name": name, "parents": [parent_id], "mimeType": FOLDER_MIME}
    folder = service.files().create(body=metadata, fields="id").execute()
    return folder["id"]


def upload_file(service, path, parent_id):
    """Upload a single file into the given folder and return its id."""
    from googleapiclient.http import MediaFileUpload

    metadata = {"name": os.path.basename(path), "parents": [parent_id]}
    media = MediaFileUpload(path, resumable=False)
    uploaded = service.files().create(
        body=metadata, media_body=media, fields="id"
    ).execute()
    return uploaded["id"]


def archive(paths):
    """Upload the given paths. Returns the number of files stored."""
    if not is_configured():
        print("Google Drive is not configured. Skipping archive step.")
        return 0

    service = build_service()
    stamp = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d_%H%M")
    folder_id = create_run_folder(service, os.environ["GDRIVE_FOLDER_ID"].strip(), stamp)
    print("Created Drive folder {0} for this run.".format(stamp))

    stored = 0
    for path in paths:
        if not os.path.exists(path):
            print("Skipped missing file: " + path)
            continue
        file_id = upload_file(service, path, folder_id)
        print("Uploaded {0} (id {1}).".format(path, file_id))
        stored += 1
    return stored


def main():
    paths = sys.argv[1:]
    if not paths:
        print("Usage: python subir_drive.py <file> [file ...]")
        return 2

    try:
        stored = archive(paths)
    except Exception as error:
        # Never leak credentials or full API payloads into the workflow log.
        print("Drive archive failed: " + type(error).__name__)
        return 1

    print("Files archived: {0}".format(stored))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
