"""
Function that reads temporary AWS credentials from a profile (which
may be a newer SSO-based profile) and writes them to a different AWSprofile that can be used by tools that
do not yet support the new SSO model.

Since the derived credentials are temporary, they will eventually expire (typically 12 hours SSO refresh).
After refreshing SSO credentials, you can run this utility again to update the legacy profile.

By default, this utility directly manipulates the ~/.aws/credentials file. An attempt is made to preserve
the file's round-trip integrity.
"""

from roundtripini import INI
import boto3
import os
import logging
import sys
import datetime

from typing import Optional

logger = logging.getLogger(__name__)

def refresh_legacy_sso(
        input_profile: Optional[str] = None,
        output_profile: Optional[str] = None,
        credentials_file: Optional[str] = None,
  ) -> Optional[datetime.datetime]:
    """Refresh a legacy AWS SSO profile with temporary creds from a new AWS SSO profile.

    Args:
        input_profile (Optional[str], optional):
            The name of an existing AWS profile with valid credentials. May be a newer SSO profile. Defaults to
            The default AWS profile ($AWS_PROFILE or "default").
        output_profile (Optional[str], optional):
            The name of a profile to write refreshed temporary credentials (derived from imput_profile) to.
            Defaults to The input profile name with "-legacy-sso" appended.
        credentials_file (Optional[str], optional):
            The path of the AWS credentials file to be updated. Defaults to "~/.aws/credentials".

    Returns:
        datetime.datetime:
            The expiration time of the refreshed temporary credentials, or None if credentials do not expire.
    """
    
    if credentials_file is None:
        credentials_file = "~/.aws/credentials"
    credentials_file = os.path.abspath(os.path.expanduser(credentials_file))

    session = boto3.Session(profile_name=input_profile)
    input_profile = session.profile_name
    creds = session.get_credentials()
    if creds is None:
         raise ValueError(f"No valid credentials found for profile {input_profile!r}")
    access_key_id = creds.access_key
    secret_access_key = creds.secret_key
    session_token = creds.token

    output_profile = output_profile or f"{input_profile}-legacy-sso"

    logger.debug(f"Credentialsfile: {credentials_file}")
    logger.debug(f"Input Profile: {input_profile}")
    logger.debug(f"Output Profile: {output_profile}")
    logger.debug(f"Access Key: {access_key_id}")
    # logger.debug(f"Secret Access Key: {secret_access_key}")
    # logger.debug(f"Session Token: {session_token}")

    if not os.path.exists(credentials_file):
        with os.fdopen(os.open(credentials_file, os.O_WRONLY | os.O_CREAT, 0o600), 'w') as f:
                pass

    with open(credentials_file, "r") as f:
        config = INI(f)

    config[output_profile, "aws_access_key_id"] = access_key_id
    config[output_profile, "aws_secret_access_key"] = secret_access_key
    if session_token:
        config[output_profile, "aws_session_token"] = session_token

    with open(credentials_file, "w") as f:
        f.write(config.dump())

    logger.debug(f"Successfully updated AWS profile {output_profile!r} in {credentials_file!r}")
    expiry_time: Optional[datetime.datetime] = getattr(creds, "_expiry_time", None)
    if expiry_time:
        logger.debug(f"Temporary credentials expire at {expiry_time.astimezone()} local time")

    return expiry_time
