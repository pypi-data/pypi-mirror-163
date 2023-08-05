# Helper cli to encode urls.
import click
from google_auth_oauthlib.flow import InstalledAppFlow

from tentaclio_gdrive.clients import google_drive_client as gd


SCOPES = ["https://www.googleapis.com/auth/drive"]


@click.group()
def main():
    """Run tentaclio helper commands."""
    ...


@main.group()
def google_token():
    """Manage google tokens."""
    ...


@google_token.command()
@click.option(
    "--credentials-file",
    required=True,
    help=(
        "Settings file to generate the token from, can be obtained from "
        "https://developers.google.com/drive/api/v3/quickstart/python "
        "by clicking enable drive api."
    ),
)
@click.option(
    "--output-file",
    default=gd.DEFAULT_TOKEN_FILE,
    help=(
        "Output token for google api requests. if set to other value than the default,"
        " TENTACLIO_GOOGLE_DRIVE_TOKEN_FILE variable needs to be set accordingly."
    ),
)
def generate(credentials_file, output_file):
    """Generate token file from the settings.json file."""
    flow = InstalledAppFlow.from_client_secrets_file(credentials_file, SCOPES)
    creds = flow.run_local_server(port=0)
    with open(output_file, "w") as f:
        f.write(creds.to_json())
    print(f"Token file saved to {output_file}")


if __name__ == "__main__":
    main(prog_name="python -m tentaclio_gdrive")
