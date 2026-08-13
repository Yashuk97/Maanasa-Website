"""
One-time script: removes the "G+3 Elevation" project from Past Projects.

RUN THIS ON YOUR OWN COMPUTER — the sandbox Claude runs in can't write to
your database directly.

RUN WITH:
    python remove_g3_elevation.py
"""

from app import app, db, Project

with app.app_context():
    p = Project.query.filter(Project.name.like('%G+3 Elevation%')).first()
    if not p:
        print("Couldn't find a project named 'G+3 Elevation'.")
    else:
        print(f"Deleting: {p.name.strip()} — {p.location}")
        db.session.delete(p)
        db.session.commit()
        print("Done.")
