"""
One-time script: adds the new project fields (flats/floors/duration/etc.) to
the database, and inserts the new Rd No 4, Gautam Nagar project.

BEFORE RUNNING:
1. Delete instance/site.db-journal first (see chat instructions) — a leftover
   file from an interrupted write is currently blocking all database writes.
2. Fill in PROJECT_NAME below with the actual project name.
3. Activate your virtual environment.

RUN WITH:
    python add_gautam_nagar_project.py

Safe to run more than once — it only adds columns that don't already exist,
and you can delete this file once it's run successfully.
"""

from app import app, db, Project
import sqlalchemy as sa
PROJECT_NAME = "To be Announced"


with app.app_context():
    # Add any columns that don't exist yet (safe to re-run)
    inspector = sa.inspect(db.engine)
    existing_cols = [c['name'] for c in inspector.get_columns('project')]
    alters = {
        'gallery_photo_url': 'VARCHAR(255)',
        'gallery_photo_url_2': 'VARCHAR(255)',
        'flats_count': 'INTEGER',
        'floors_count': 'INTEGER',
        'duration': 'VARCHAR(50)',
        'completion_percentage': 'INTEGER',
    }
    with db.engine.connect() as conn:
        for col, coltype in alters.items():
            if col not in existing_cols:
                conn.execute(
                    sa.text(f'ALTER TABLE project ADD COLUMN {col} {coltype}'))
                print(f"Added column: {col}")
        conn.commit()

    if PROJECT_NAME.startswith("CHANGE ME"):
        print("\nStop: open this file and set PROJECT_NAME to the real project name, then run again.")
    else:
        new_project = Project(
            name=PROJECT_NAME,
            location="Rd No 4, Gautam Nagar, Malkajgiri",
            description=(
                "A 10-flat residential development currently under construction "
                "in Gautam Nagar, Malkajgiri."
            ),
            status="Ongoing",
            flats_count=10,
            floors_count=5,
            duration="1 Year",
            completion_percentage=10,
            main_photo_url="gautam_nagar_elevation.jpeg",
            gallery_photo_url="gautam_nagar_floorplan.jpeg",
            gallery_photo_url_2="gautam_nagar_specifications.jpeg",
        )
        db.session.add(new_project)
        db.session.commit()
        print(f"\nProject added successfully with id: {new_project.id}")
        print("You can now edit its description any time from the admin panel at /login.")
