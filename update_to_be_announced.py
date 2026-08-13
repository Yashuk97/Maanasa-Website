"""
One-time script: fills in Type / Facing / Area for the "To Be Announced"
project (Rd No 4, Gautam Nagar).

RUN THIS ON YOUR OWN COMPUTER — the sandbox Claude runs in can't write to
your database directly.

RUN WITH:
    python update_to_be_announced.py
"""

from app import app, db, Project

with app.app_context():
    p = Project.query.filter_by(name='To Be Announced').first()
    if not p:
        print("Couldn't find a project named 'To Be Announced'.")
    else:
        p.project_type = 'Residential'
        p.facing = 'North'
        p.area_sqft = 1000
        db.session.commit()
        print(f"Updated project id {p.id}: type={p.project_type}, facing={p.facing}, area={p.area_sqft} sqft")
