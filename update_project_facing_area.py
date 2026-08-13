"""
One-time script: updates facing + area for the "To Be Announced" and
"Not Announced Yet" projects.

RUN THIS ON YOUR OWN COMPUTER — the sandbox Claude runs in can't write to
your database directly.

RUN WITH:
    python update_project_facing_area.py
"""

from app import app, db, Project

updates = {
    'To Be Announced': {'facing': 'East and West', 'area_sqft': 1150},
    'Not Announced Yet': {'facing': 'East', 'area_sqft': 1800},
}

with app.app_context():
    for name, fields in updates.items():
        p = Project.query.filter_by(name=name).first()
        if not p:
            print(f"Couldn't find a project named '{name}' — skipped.")
            continue
        p.facing = fields['facing']
        p.area_sqft = fields['area_sqft']
        db.session.commit()
        print(f"Updated '{name}': facing={p.facing}, area={p.area_sqft} sqft")
