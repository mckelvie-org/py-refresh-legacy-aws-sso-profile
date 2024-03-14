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

Update legacy AWS SSO profile with temporary creds from new AWS SSO profile. A simple command-line utility that reads temporary AWS credentials from a profile (which may be a newer SSO-based profile) and writes them to a different AWSprofile that can be used by tools that do not yet support the new SSO model. Since the
derived credentials are temporary, they will eventually expire (typically 12 hours SSO refresh). After refreshing SSO credentials, you can run this utility again to update the legacy profile. By default, this utility directly manipulates the ~/.aws/credentials file. An attempt is made to preserve the file's round-trip
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
