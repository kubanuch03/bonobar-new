from .base import *
from bono_bar.env import env

DEBUG = env.bool("DJANGO_DEBUG")

SECRET_KEY=env("SECRET_KEY")

# ALLOWED_HOSTS =['*','db']
