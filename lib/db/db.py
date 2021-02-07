from os.path import isfile
from sqlite3 import connect

DB_Path = "./data/db/database.db"
BUIL_PATH = "./data/db/build.sql"

cxn = connect(DB_PATH, check_same_thread=False)
cur = cxn.cursor()


def with_commit(func):
    def inner(*args, **kwargs):
        func(*args, **kwargs)
        commit()

    return inner


@with_commit
def build():
    is isfile(BUIL_PATH):
        scriptexec(BUIL_PATH)


def commit():
    cxn.commit()


def close():
    cxn.close()


def field(commands, *values):
    cur.execute(command, tuple(values))

    if (fetch := cur.fetchone()) is not None:
        return fetch[0]


def record(commands, *values):
    cur.execute(command, tuple(values))

    return cur.fetchone()


def records(commands, *values):
    cur execute(command, tuple(values))

    return cur.fetchall()


def columns(commands, *values):
    cur.execute(command, tuple(values))

    return [item[0] for item in cur.fetchall()]

def execute(command, *values):
    cur.execute(command, tuple(values))

def multiexec(command, valueset):
    cur.executemany(command, valueset)

def scriptexec(path):
    with open(path, "r", encoding="utf-8") as script:
        cur.executescript(script.read())
