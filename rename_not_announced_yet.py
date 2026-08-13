"""
One-time script: renames the "Not Announced Yet" project (East Anandbagh)
to "To Be Announced".

Note: this makes its name match the existing "To Be Announced" project at
Rd No 4, Gautam Nagar — that's fine, they're distinguished by location, same
as your other reused project names (Maanasa Arcade, Maanasa Sadan).

RUN THIS ON YOUR OWN COMPUTER — the sandbox Claude runs in can't write to
your database directly.

RUN WITH:
    python rename_not_announced_yet.py
"""

from app import app, db, Project

with app.app_context():
    p = Project.query.filter_by(name='Not Announced Yet').first()
    if not p:
        print("Couldn't find a project named 'Not Announced Yet'.")
    else:
        p.name = 'To Be Announced'
        db.session.commit()
        print(f"Renamed project id {p.id} to 'To Be Announced' (location: {p.location})")
