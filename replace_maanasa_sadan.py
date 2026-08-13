"""
One-time script: deletes the old "Maanasa Sadan" project (Alwal, no specs)
and adds the correct one (Ramanthapur Khalsa, Uppal) from the brochure.

RUN THIS ON YOUR OWN COMPUTER — the sandbox Claude runs in can't write to
your database directly.

RUN WITH:
    python replace_maanasa_sadan.py
"""

from app import app, db, Project

with app.app_context():
    old = Project.query.filter_by(name='Maanasa Sadan ', location='Alwal').first()
    if not old:
        old = Project.query.filter(Project.name.like('%Maanasa Sadan%')).first()
    if old:
        db.session.delete(old)
        db.session.commit()
        print(f"Deleted old project id {old.id} (Maanasa Sadan, Alwal)")
    else:
        print("Couldn't find the old Alwal 'Maanasa Sadan' entry — skipping delete.")

    new = Project(
        name='Maanasa Sadan',
        location='Ramanthapur Khalsa, Uppal, Hyderabad',
        description=(
            "A luxury apartment project at Plot No. A-11, Doorshan Colony, "
            "Ramanthapur Khalsa, Uppal, Hyderabad. Built with an RCC framed "
            "structure, teakwood main door and internal door frames, granite "
            "kitchen platform, vitrified tile flooring, UPVC windows with "
            "safety grills, a 6-passenger lift, 24-hour water supply, and "
            "CCTV security in the parking area and corridors."
        ),
        status='Ongoing',
        flats_count=6,
        floors_count=3,
        duration='3 Months to Handover',
        completion_percentage=90,
        project_type='Residential',
        facing='East',
        area_sqft=1000,
        main_photo_url='maanasa_sadan_elevation.png',
        gallery_photo_url='maanasa_sadan_floorplan.png',
    )
    db.session.add(new)
    db.session.commit()
    print(f"Added new project id: {new.id}")
