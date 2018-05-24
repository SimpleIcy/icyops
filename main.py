# -*- coding:utf-8 -*-

import datetime
import os
import re

import yaml

PROJECT_ROOT = os.path.realpath(os.path.dirname(__file__))

#import system env
os.environ["DJANGO_SETTINGS_MODULE"] = 'admin.settings_scan'
import django
import time
django.setup()
from scanhosts.models import Hostscaninfo
