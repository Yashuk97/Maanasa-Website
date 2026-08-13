"""
One-time script: adds the new "highlight" fields (facing, project type, area)
to the projects table.

RUN THIS ON YOUR OWN COMPUTER (not from Claude) — the sandbox Claude runs in
can't write to your database directly.

BEFORE RUNNING:
- If instance/site.db-journal exists, delete it first (same fix as before).

RUN WITH:
    python add_project_highlight_fields.py

Safe to run more than once. After running, open the admin panel at /login,
edit each project, and fill in Facing / Type of Project / Area (sqft) —
these are plain text/number fields, no image upload needed.
"""

import sqlalchemy as sa
from app import app, db

with app.app_context():
    inspector = sa.inspect(db.engine)
    existing_cols = [c['name'] for c in inspector.get_columns('project')]
    alters = {
        'facing': 'VARCHAR(50)',
        'project_type': 'VARCHAR(50)',
        'area_sqft': 'INTEGER',
    }
    with db.engine.connect() as conn:
        for col, coltype in alters.items():
            if col not in existing_cols:
                conn.execute(sa.text(f'ALTER TABLE project ADD COLUMN {col} {coltype}'))
                print(f"Added column: {col}")
        conn.commit()

    print("Done. Fill in Facing / Type of Project / Area (sqft) for each project from the admin panel.")
