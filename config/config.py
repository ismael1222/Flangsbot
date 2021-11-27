import json
import glob

"""
    Here References
"""

def get_owner_ids():
    pass

OWNER_IDS = []
PREFIX = "/"
COGS = [
    path.splith("\\")[-1][:-3] for path in glob("./lib/cogs/*.py")
]