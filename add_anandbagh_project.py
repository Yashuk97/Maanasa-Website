"""
One-time script: adds the new East Anandbagh project to the database.

RUN THIS ON YOUR OWN COMPUTER — the sandbox Claude runs in can't write to
your database directly.

RUN WITH:
    python add_anandbagh_project.py
"""

from app import app, db, Project

with app.app_context():
    p = Project(
        name='Not Announced Yet',
        location='East Anandbagh, Malkajgiri',
        description=(
            "A 3-flat residential development currently under construction "
            "in East Anandbagh, Malkajgiri."
        ),
        status='Ongoing',
        flats_count=3,
        floors_count=3,
        duration='1 Year',
        completion_percentage=10,
        project_type='Residential',
        area_sqft=1660,  # taken from the floor plan you shared (1660.00 Sft) — let me know if this should change
        main_photo_url='anandbagh_elevation.png',
        gallery_photo_url='anandbagh_floorplan.png',
    )
    db.session.add(p)
    db.session.commit()
    print(f"Project added with id: {p.id}")
