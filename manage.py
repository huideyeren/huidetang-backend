#!/usr/bin/env python
import os
import sys
from dotenv import load_dotenv
from pathlib import Path
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "huidetang.settings.dev")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
