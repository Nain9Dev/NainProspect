"""One-off helper: obtain the Google Drive refresh token.

Run this once on a machine with a browser. It prints the refresh token so it
can be stored as a GitHub secret. Nothing is written to disk on purpose: a
token file next to the source is one careless commit away from a leak.

Prerequisites:
  1. Google Cloud project with the Drive API enabled.
  2. OAuth consent screen of type External, PUBLISHED to production.
     While it stays in Testing, the refresh token expires after 7 days.
  3. OAuth client of type "Desktop app"; download the JSON next to this file.
"""

import os
import sys

SCOPES = ["https://www.googleapis.com/auth/drive.file"]
DEFAULT_SECRETS_FILE = "credentials.json"


def main():
    secrets_file = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_SECRETS_FILE

    if not os.path.exists(secrets_file):
        print("Client secrets file not found: " + secrets_file)
        print("Download it from the Google Cloud console and place it here.")
        return 2

    from google_auth_oauthlib.flow import InstalledAppFlow

    flow = InstalledAppFlow.from_client_secrets_file(secrets_file, SCOPES)
    credentials = flow.run_local_server(port=0, prompt="consent")

    if not credentials.refresh_token:
        print("Google returned no refresh token. Revoke the previous grant at")
        print("https://myaccount.google.com/permissions and run this again.")
        return 1

    print("")
    print("GDRIVE_CLIENT_ID     = " + flow.client_config["client_id"])
    print("GDRIVE_CLIENT_SECRET = " + flow.client_config["client_secret"])
    print("GDRIVE_REFRESH_TOKEN = " + credentials.refresh_token)
    print("")
    print("Store these as GitHub secrets. Do not commit them.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
