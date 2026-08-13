"""
One-time script: removes the two original incomplete placeholder projects
("Maanasa Arcade" at Dayanand Nagar, and "Sai Maanasa Nilayam" at Gautam
Nagar) that had no specs filled in.

RUN THIS ON YOUR OWN COMPUTER — the sandbox Claude runs in can't write to
your database directly.

RUN WITH:
    python remove_old_placeholder_projects.py
"""

from app import app, db, Project

targets = [
    ('Maanasa Arcade', 'Dayanand Nagar, Malkajgiri'),
    ('Sai Maanasa Nilayam', 'Gautam Nagar, Malkajgiri'),
]

with app.app_context():
    for name, location in targets:
        p = Project.query.filter(
            Project.name.like(f'%{name}%'),
            Project.location.like(f'%{location.split(",")[0]}%')
        ).first()
        if p:
            print(f"Deleting: {p.name.strip()} — {p.location}")
            db.session.delete(p)
            db.session.commit()
        else:
            print(f"Couldn't find a match for '{name}' at '{location}' — skipped.")

    print("Done.")
