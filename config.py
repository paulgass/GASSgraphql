import graphene
import os
import subprocess
from collections import namedtuple
from enums import (SexEnum, AssignmentCodeEnum, RankEnum,
                    EducationEnum, AssessmentCodeEnum, SportsEnum)

import os
''' Database configuration '''


# def db_connection_string():
#     if os.path.exists("/usr/src/app/app.py"):
#         # DatabaseInfo = namedtuple('DatabaseInfo', ['engine', 'user', 'password',
#         #                                             'port', 'database', 'host'])
#         # db_info = DatabaseInfo(engine='postgresql', user=os.getenv('POSTGRES_USER'),
#         #                     password=os.getenv('POSTGRES_PASSWORD'), port=os.getenv('DB_PORT', 5432),
#         #                     database=os.getenv('POSTGRES_DB'), host=os.getenv('DB_HOST'))
#         port = os.environ.get('POSTGRESQL_SERVICE_PORT', 5432)
#         host = os.environ.get('POSTGRESQL_SERVICE_HOST','db')
#         user = os.environ.get('POSTGRESQL_USER', 'brandiadmin')
#         database = os.environ.get('POSTGRES_DB', 'brandidb')
#         password = os.environ.get('POSTGRES_PASSWORD')
#         if password:
#             return f'postgresql://{user}:{password}@{host}:{port}/{database}'
#     return "postgresql://brandiadmin:qnHQJT2FZpKG4KqV@lionscale.live:5999/brandidb"



DB_NAME = 'database.sqlite3'
basedir = os.path.abspath(os.path.dirname(__file__))
engine = 'sqlite'

def db_connection_string():
    return f'{engine}:////{os.path.join(basedir, DB_NAME)}'
