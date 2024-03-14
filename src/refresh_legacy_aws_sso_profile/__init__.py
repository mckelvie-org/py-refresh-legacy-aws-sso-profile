"""
Simmple tool that reads temporary AWS credentials from a profile (which
may be a newer SSO-based profile) and writes them to a different AWSprofile that can be used by tools that
do not yet support the new SSO model.

Since the derived credentials are temporary, they will eventually expire (typically 12 hours SSO refresh).
After refreshing SSO credentials, you can run this utility again to update the legacy profile.

By default, this utility directly manipulates the ~/.aws/credentials file. An attempt is made to preserve
the file's round-trip integrity.
"""
from .version import __version__
from .refresh import refresh_legacy_sso
