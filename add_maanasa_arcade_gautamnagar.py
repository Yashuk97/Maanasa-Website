"""
One-time script: adds a "Maanasa Arcade" project at Gautam Nagar, Malkajgiri
(a separate project from the existing "Maanasa Arcade" entries at Dayanand
Nagar and Rk Nagar — kept as-is, this is added separately). Listed under
Current Projects (Ongoing), even though it's fully built and ready to hand
over, per your request.

RUN THIS ON YOUR OWN COMPUTER — the sandbox Claude runs in can't write to
your database directly.

Safe to run more than once: if you already ran an earlier version of this
script (which set it to Past), running this again will just fix its status
to Ongoing instead of creating a duplicate.

RUN WITH:
    python add_maanasa_arcade_gautamnagar.py
"""

from app import app, db, Project

with app.app_context():
    existing = Project.query.filter_by(
        name='Maanasa Arcade', location='Gautam Nagar, Malkajgiri').first()

    if existing:
        existing.status = 'Ongoing'
        db.session.commit()
        print(f"Updated existing project id {existing.id}: status set to Ongoing")
    else:
        p = Project(
            name='Maanasa Arcade',
            location='Gautam Nagar, Malkajgiri',
            description=(
                "A residential apartment project in Gautam Nagar, Malkajgiri, "
                "now complete and ready to hand over. Built with an RCC framed "
                "structure, teakwood main door and internal door frames, granite "
                "kitchen platform, vitrified tile flooring, UPVC windows with "
                "safety grills, a 6-passenger lift, 24-hour water supply, and "
                "CCTV security in the parking area and corridors."
            ),
            status='Ongoing',
            flats_count=4,
            floors_count=4,
            duration='Ready to Handover',
            completion_percentage=100,
            project_type='Residential',
            facing='West',
            area_sqft=1800,
            main_photo_url='maanasa_arcade_gautamnagar_elevation.png',
            gallery_photo_url='maanasa_arcade_gautamnagar_floorplan.png',
        )
        db.session.add(p)
        db.session.commit()
        print(f"Added project id: {p.id}")
