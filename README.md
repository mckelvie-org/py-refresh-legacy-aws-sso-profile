refresh-legacy-aws-sso-profile: Backwards-compatible AWS SSO login using new-stile SSO profiles 
=================================================

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Latest release](https://img.shields.io/github/v/release/mckelvie-org/py-refresh-legacy-aws-sso-profile.svg?style=flat-square&color=b44e88)](https://github.com/mckelvie-org/py-refresh-legacy-sso-profile/releases)

A simple tool to refresh backwards-compatible AWS profiles using temporary credentials derived from newer SSO profiles.

Table of contents
-----------------

* [Introduction](#introduction)
* [Installation](#installation)
* [Usage](#usage)
  * [API](api)
* [Known issues and limitations](#known-issues-and-limitations)
* [Getting help](#getting-help)
* [Contributing](#contributing)
* [License](#license)
* [Authors and history](#authors-and-history)

Introduction
------------

Some time back, AWS added direct support for IAM Identitity Center token provider credentials into its CLI and
various AWS API language providers (e.g., boto3 for Python). This is really nice because it allows users to log into AWS
via single-sign-on (SSO) with the ```aws sso login` command and the assistance of a browser, and appropriate session
credentials are automatically cached and subsequently used by other CLI commands or API clients with automatic
token refresh. See [AWS documentation](https://docs.aws.amazon.com/cli/latest/userguide/sso-configure-profile-token.html)
for details of how to configure SSO to make this work.

Setting up a profile for SSO involves a new type of profile configuration in `~/.aws/config`. For example:

```ini
[profile my-dev-profile]
sso_session = my-sso
sso_account_id = 123456789011
sso_role_name = readOnly
region = us-west-2
output = json

[sso-session my-sso]
sso_region = us-east-1
sso_start_url = https://my-sso-portal.awsapps.com/start
sso_registration_scopes = sso:account:access
```

All this works great if you have a recent AWS CLI or AWS API language provider; however, if you are using an application that
is bound to an older language provider (e.g., older versions of boto3) that does not support the new SSO profiles, the newer profile (`my-dev-profile` in the example) will be unusable by the application. The workaround for this situation is to run:

```bash
eval `aws configure export-credentials --profile my-dev-profile --format env`
```

This will set environment variables `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY` and `AWS_SESSION_TOKEN` to
temporary credentials that will allow older clients to usethe session until the temporary credentials expire.

While this method works, it has several problems:

* It only allows a single profile to be active at a time. Applications that deal with multiple profiles are problemation
* The credentials are only valid for the current process and child processes that inherit environment variables. It is not possible to
  refresh SSO credentials in a different shell session and have the refresh apply to all shell sessions.
* Child processes that inherit the environment variables do not get refreshed credentials when the parent process refreshes credentials.
* It is awkward to pass refreshed credentials into a container environment (environment variables within the container must be
  updated in all processes, potentially after the container has launched). It's much easier to just bind mount `~/.aws` into
  a container.
* Passing sensitive credentials around in environment variables increases the risk of unintentionally leaking credentials.

This package provides a simple function and associated command-line tool that eliminates all of these concerns by eschewing the
use of environment variables and instead updating an old-style credential profile in `~/.aws/credentials` with temporary
session credentials derived from a newer SSO profile. Older applications simply need to be directed to use the derived
profile instead of the newer SSO profile.  When temporary credentials expire, simply run this tool again and all
clients using the derived profile will start seeing the refreshed credentials.

Installation
------------

### Prerequisites

**Python**: Python 3.10+ is required. See your OS documentation for instructions.

### From PyPi

The current released version of `refresh-legacy-aws-sso-profile` can be installed with:

```bash
pip3 install refresh-legacy-aws-profile
```

### From GitHub

[PDM](https://pdm-project.org/latest/) is required; it can be installed with:

```bash
curl -sSL https://pdm-project.org/install-pdm.py | python3 -
```

Clone the repository and install refresh-legacy-aws-sso-profile into a private virtualenv with:

```bash
cd <parent-folder>
git clone https://github.com/mckelvie-org/py-refresh-legacy-aws-sso-profile.git
cd py-refresh-legacy-aws-sso-profile
pdm install
```

You can then launch a bash shell with the virtualenv activated using:

```bash
pdm run bash
```

Usage
-----

```text
usage: refresh-legacy-aws-sso-profile [-h] [-p PROFILE] [-o OUTPUT_PROFILE] [-c CONFIG] [-l {DEBUG,INFO,WARNING,ERROR,CRITICAL}]

Update legacy AWS SSO profile with temporary creds from new AWS SSO profile. A simple command-line utility that reads temporary AWS credentials from a profile (which may be a newer SSO-based profile) and writes them to a different AWSprofile that can be used by tools that do not yet support the new SSO model. Since the derived credentials are temporary, they will eventually expire (typically 12 hours SSO refresh). After refreshing SSO credentials, you can run this utility again to update the legacy profile. By default, this utility directly manipulates the ~/.aws/credentials file. An attempt is made to preserve the file's round-trip
integrity.

options:
  -h, --help            show this help message and exit
  -p PROFILE, --profile PROFILE
                        The input SSO-based AWS profile to use. Defaults to $AWS_PROFILE, or 'default'.
  -o OUTPUT_PROFILE, --output-profile OUTPUT_PROFILE
                        The output AWS profile to update with temporary credentials. Defaults to '<input-profile-name>-legacy-sso'.
  -c CONFIG, --config CONFIG
                        The AWS Configuration file in which to placer the credentials. Defaults to ~/.aws/credentials.
  -l {DEBUG,INFO,WARNING,ERROR,CRITICAL}, --log-level {DEBUG,INFO,WARNING,ERROR,CRITICAL}
                        Set the logging level. Default is 'WARNING'.```
```

Known issues and limitations
----------------------------

TBD.

Getting help
------------

Please report any problems/issues [here](https://github.com/mckelvie-org/py-refresh-legacy-aws-sso-profile/issues).

Contributing
------------

Pull requests welcome.

License
-------

refresh-legacy-aws-sso-profile is distributed under the terms of the [MIT License](https://opensource.org/licenses/MIT).  The license applies to this file and other files in the [GitHub repository](http://github.com/mckelvie-org/py-refresh-legacy-aws-sso-profile) hosting this file.

Authors and history
---------------------------

The author of refresh-legacy-aws-sso-profile is [Sam McKelvie](https://github.com/sammck).
