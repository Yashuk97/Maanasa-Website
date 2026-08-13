"""
Runs once before the app starts on Render. If a secret file with your
base64-encoded database has been uploaded (via Render's Secret Files
feature), and the local database doesn't already have real tables in it,
this decodes the secret file into instance/site.db.

Safe to leave in permanently — once instance/site.db has real tables, this
becomes a no-op on every future restart, so it won't overwrite your live
data by mistake.
"""

import os
import base64
import sqlite3

SECRET_PATH = "/etc/secrets/site_db.b64"
DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "instance", "site.db")


def db_already_has_data(path):
    if not os.path.exists(path) or os.path.getsize(path) == 0:
        return False
    try:
        conn = sqlite3.connect(path)
        cur = conn.cursor()
        cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='project'")
        if not cur.fetchone():
            conn.close()
            return False
        cur.execute("SELECT COUNT(*) FROM project")
        count = cur.fetchone()[0]
        conn.close()
        return count > 0
    except Exception:
        return False


if not os.path.exists(SECRET_PATH):
    print("restore_db_from_secret: no secret file found, skipping.")
elif db_already_has_data(DB_PATH):
    print("restore_db_from_secret: database already has project data, skipping restore.")
else:
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    with open(SECRET_PATH, "r") as f:
        b64_content = f.read()
    with open(DB_PATH, "wb") as f:
        f.write(base64.b64decode(b64_content))
    print("restore_db_from_secret: database restored from secret file.")
