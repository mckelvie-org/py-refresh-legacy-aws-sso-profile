#!/usr/bin/env python3

import sys
from typing import Optional, Sequence

# Note that this file is run as a script, so we need to use the full import path
from refresh_legacy_aws_sso_profile.cli.refresh_legacy_sso import main

def run(argv: Optional[Sequence[str]]=None) -> int:
  rc = main(argv)
  return rc

if __name__ == '__main__':
  sys.exit(run())
