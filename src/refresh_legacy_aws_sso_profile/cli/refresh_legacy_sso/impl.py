"""
A simple command-line utility that reads temporary AWS credentials from a profile (which
may be a newer SSO-based profile) and writes them to a different AWSprofile that can be used by tools that
do not yet support the new SSO model.

Since the derived credentials are temporary, they will eventually expire (typically 12 hours SSO refresh).
After refreshing SSO credentials, you can run this utility again to update the legacy profile.

By default, this utility directly manipulates the ~/.aws/credentials file. An attempt is made to preserve
the file's round-trip integrity.
"""

from roundtripini import INI
import argparse
import boto3
import os
import logging
import sys
import datetime
import textwrap

from ...refresh import refresh_legacy_sso

from typing import Optional, Sequence

logger = logging.getLogger(__name__.split('.')[-2])

def main(argv: Optional[Sequence[str]]=None) -> int:
    if argv is None:
        argv = sys.argv[1:]

    parser = argparse.ArgumentParser(
         description=textwrap.dedent("""\
            Update legacy AWS SSO profile with temporary creds from new AWS SSO profile.
                                     
            A simple command-line utility that reads temporary AWS credentials from a profile (which
            may be a newer SSO-based profile) and writes them to a different AWSprofile that can be used by tools that
            do not yet support the new SSO model.

            Since the derived credentials are temporary, they will eventually expire (typically 12 hours SSO refresh).
            After refreshing SSO credentials, you can run this utility again to update the legacy profile.

            By default, this utility directly manipulates the ~/.aws/credentials file. An attempt is made to preserve
            the file's round-trip integrity.
            """)
      )

    parser.add_argument("-p", "--profile", default=None,
        help="""The input SSO-based AWS profile to use. Defaults to $AWS_PROFILE, or 'default'.""")
    parser.add_argument("-o", "--output-profile", default=None,
        help="""The output AWS profile to update with temporary credentials. Defaults to '<input-profile-name>-legacy-sso'.""")
    parser.add_argument("-c", "--config", default = None,
        help="""The AWS Configuration file in which to placer the credentials. Defaults to ~/.aws/credentials.""")
    parser.add_argument("-l", "--log-level", dest="logLevel", default="WARNING",
        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'],
        help="""Set the logging level. Default is 'WARNING'.""")

    args = parser.parse_args(argv)

    logging.basicConfig(level=getattr(logging, args.logLevel))

    expiry_time = refresh_legacy_sso(
        input_profile=args.profile,
        output_profile=args.output_profile,
        credentials_file=args.config
    )


    print(f"Successfully updated Legacy AWS SSO profile", file=sys.stderr)
    if expiry_time:
        print(f"Temporary credentials expire at {expiry_time.astimezone()} local time", file=sys.stderr)

    return 0