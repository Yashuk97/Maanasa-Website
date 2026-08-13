"""
One-time script: adds the "Maanasa Sadan" project at Gayatri Nagar, Moulali
(a separate project from the Ramanthapur "Maanasa Sadan" — same name is
reused across sites, same as "Maanasa Arcade" already is in the database).

RUN THIS ON YOUR OWN COMPUTER — the sandbox Claude runs in can't write to
your database directly.

RUN WITH:
    python add_maanasa_sadan_gayatri.py
"""

from app import app, db, Project

with app.app_context():
    p = Project(
        name='Maanasa Sadan',
        location='Gayatri Nagar, Street No 1, Moulali, Hyderabad',
        description=(
            "A residential apartment project at Gayatri Nagar, Street No 1, "
            "Moulali, Hyderabad. Built with an RCC framed structure, teakwood "
            "main door and internal door frames, granite kitchen platform, "
            "vitrified tile flooring, UPVC windows with safety grills, a "
            "6-passenger lift, 24-hour water supply, and CCTV security in "
            "the parking area and corridors."
        ),
        status='Ongoing',
        flats_count=4,
        floors_count=4,
        completion_percentage=80,
        project_type='Residential',
        facing='North',
        area_sqft=1800,
        main_photo_url='maanasa_sadan_gayatri_elevation.png',
        gallery_photo_url='maanasa_sadan_gayatri_floorplan.png',
    )
    db.session.add(p)
    db.session.commit()
    print(f"Added project id: {p.id}")
