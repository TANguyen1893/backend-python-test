"""AlayaNotes

Usage:
  main.py [run]
  main.py initdb
"""
from docopt import docopt
import subprocess
import os

from alayatodo import app


def _run_sql(filename):
    try:
        subprocess.check_output(
            "sqlite3 %s < %s" % (app.config['DATABASE'], filename),
            stderr=subprocess.STDOUT,
            shell=True
        )
    except subprocess.CalledProcessError as ex:
        print(ex.output)
        os._exit(1)

def initialize_database():
    _run_sql('resources/database.sql')
    _run_sql('resources/fixtures.sql')

if __name__ == '__main__':
    args = docopt(__doc__)
    if args['initdb']:
        initialize_database()
        print("AlayaTodo: Database initialized.")
    else:
        app.run(use_reloader=True)
