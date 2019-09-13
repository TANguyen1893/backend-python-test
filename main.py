"""AlayaNotes

Usage:
  main.py [run]
  main.py initdb
  main.py apply_schema
  main.py revert_schema
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

def apply_schema_update():
    _run_sql('resources/update_todos_schema.sql')

def revert_schema_update():
    _run_sql('resources/revert_todos_schema_update.sql')

if __name__ == '__main__':
    args = docopt(__doc__)
    if args['initdb']:
        initialize_database()
        apply_schema_update()
        print("AlayaTodo: Database initialized.")
    elif args['apply_schema']:
        apply_schema_update()
        print("AlayaTodo: Todos schema updated.")
    elif args['revert_schema']:
        revert_schema_update()
        print("AlayaTodo: Todos schema reverted to original definition.")
    else:
        app.run(use_reloader=True)
