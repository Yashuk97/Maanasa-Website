"""
One-time script: adds "Maanasa Swathi Mansion" to Current Projects.

RUN THIS ON YOUR OWN COMPUTER — the sandbox Claude runs in can't write to
your database directly.

RUN WITH:
    python add_swathi_mansion.py
"""

from app import app, db, Project

with app.app_context():
    p = Project(
        name='Maanasa Swathi Mansion',
        location='Flat No. 348, Rd No 4, Gautam Nagar, Malkajgiri',
        description=(
            "A 10-flat residential development at Flat No. 348, Rd No 4, "
            "Gautam Nagar, Malkajgiri, ready to move in. Each floor offers "
            "an east-facing 1425 sq.ft flat and a west-facing 1050 sq.ft "
            "flat. Built with an RCC framed structure, teakwood main door "
            "and internal door frames, granite kitchen platform, vitrified "
            "tile flooring, UPVC windows with safety grills, a 6-passenger "
            "lift, 24-hour water supply, and CCTV security in the parking "
            "area and corridors."
        ),
        status='Ongoing',
        flats_count=10,
        floors_count=5,
        duration='Ready to Move',
        project_type='Residential',
        facing='East & West',
        main_photo_url='swathi_mansion_elevation.png',
        gallery_photo_url='swathi_mansion_floorplan.png',
    )
    db.session.add(p)
    db.session.commit()
    print(f"Added project id: {p.id}")
