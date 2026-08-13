"""
One-time script: replays everything you added/changed between the April
backup and now (Aug 10-11 scripts: highlight fields, To Be Announced,
Anandbagh, the Maanasa Sadan swap, Maanasa Sadan Gayatri, Maanasa Arcade
Gautam Nagar, Swathi Mansion, and the placeholder/G+3 removals) in the
correct order, safely and idempotently (matches by name+location, so it's
safe to run more than once).

RUN THIS ON YOUR OWN COMPUTER — the sandbox Claude runs in can't reliably
write to your database directly (confirmed: it throws disk I/O errors on
this file over the mounted connection).

BEFORE RUNNING:
1. Make sure instance/site.db is the April-restored copy with 10 projects
   (id 3-12) and the full 16-column schema. If unsure, first run:
       cp instance/site.db.pre_scripts.bak instance/site.db
   to get back to a known-clean starting point.
2. Delete any instance/site.db-journal, -wal, or -shm files if present.
3. Activate your venv: source .venv/bin/activate

RUN WITH:
    python restore_recent_projects.py
"""

import sqlalchemy as sa
from app import app, db, Project

with app.app_context():
    # 1. Make sure all columns exist (safe no-op if already there)
    inspector = sa.inspect(db.engine)
    existing_cols = [c['name'] for c in inspector.get_columns('project')]
    alters = {
        'gallery_photo_url': 'VARCHAR(255)',
        'gallery_photo_url_2': 'VARCHAR(255)',
        'flats_count': 'INTEGER',
        'floors_count': 'INTEGER',
        'duration': 'VARCHAR(50)',
        'completion_percentage': 'INTEGER',
        'facing': 'VARCHAR(50)',
        'project_type': 'VARCHAR(50)',
        'area_sqft': 'INTEGER',
    }
    with db.engine.connect() as conn:
        for col, coltype in alters.items():
            if col not in existing_cols:
                conn.execute(sa.text(f'ALTER TABLE project ADD COLUMN {col} {coltype}'))
                print(f"Added column: {col}")
        conn.commit()

    def find(name, location_contains=None):
        q = Project.query.filter(Project.name.like(f'%{name}%'))
        if location_contains:
            q = q.filter(Project.location.like(f'%{location_contains}%'))
        return q.first()

    # 2. "To Be Announced" — Rd No 4, Gautam Nagar
    p = find('To Be Announced', 'Rd No 4')
    if not p:
        p = Project(
            name='To Be Announced',
            location='Rd No 4, Gautam Nagar, Malkajgiri',
            description=(
                "A 10-flat residential development currently under construction "
                "in Gautam Nagar, Malkajgiri."
            ),
            status='Ongoing',
            flats_count=10, floors_count=5, duration='1 Year',
            completion_percentage=10,
            main_photo_url='gautam_nagar_elevation.jpeg',
            gallery_photo_url='gautam_nagar_floorplan.jpeg',
            gallery_photo_url_2='gautam_nagar_specifications.jpeg',
        )
        db.session.add(p)
        db.session.commit()
        print(f"Added 'To Be Announced' (Rd No 4, Gautam Nagar), id {p.id}")
    p.project_type = 'Residential'
    p.facing = 'East and West'
    p.area_sqft = 1150
    db.session.commit()
    print(f"Set facing/area for 'To Be Announced' (Rd No 4): {p.facing}, {p.area_sqft} sqft")

    # 3. "Not Announced Yet" -> renamed to "To Be Announced" — East Anandbagh
    p = find('To Be Announced', 'Anandbagh') or find('Not Announced Yet', 'Anandbagh')
    if not p:
        p = Project(
            name='Not Announced Yet',
            location='East Anandbagh, Malkajgiri',
            description=(
                "A 3-flat residential development currently under construction "
                "in East Anandbagh, Malkajgiri."
            ),
            status='Ongoing',
            flats_count=3, floors_count=3, duration='1 Year',
            completion_percentage=10,
            main_photo_url='anandbagh_elevation.png',
            gallery_photo_url='anandbagh_floorplan.png',
        )
        db.session.add(p)
        db.session.commit()
        print(f"Added 'Not Announced Yet' (East Anandbagh), id {p.id}")
    p.project_type = 'Residential'
    p.facing = 'East'
    p.area_sqft = 1800
    p.name = 'To Be Announced'
    db.session.commit()
    print(f"Set/renamed East Anandbagh project to 'To Be Announced': {p.facing}, {p.area_sqft} sqft")

    # 4. Replace old Maanasa Sadan (Alwal) with the real one (Ramanthapur Khalsa, Uppal)
    old = find('Maanasa Sadan', 'Alwal')
    if old:
        db.session.delete(old)
        db.session.commit()
        print("Deleted old Maanasa Sadan (Alwal)")
    if not find('Maanasa Sadan', 'Ramanthapur'):
        p = Project(
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
            status='Ongoing', flats_count=6, floors_count=3,
            duration='3 Months to Handover', completion_percentage=90,
            project_type='Residential', facing='East', area_sqft=1000,
            main_photo_url='maanasa_sadan_elevation.png',
            gallery_photo_url='maanasa_sadan_floorplan.png',
        )
        db.session.add(p)
        db.session.commit()
        print(f"Added Maanasa Sadan (Ramanthapur Khalsa, Uppal), id {p.id}")

    # 5. Maanasa Sadan — Gayatri Nagar, Moulali (separate project, same name)
    if not find('Maanasa Sadan', 'Gayatri'):
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
            status='Ongoing', flats_count=4, floors_count=4,
            completion_percentage=80, project_type='Residential',
            facing='North', area_sqft=1800,
            main_photo_url='maanasa_sadan_gayatri_elevation.png',
            gallery_photo_url='maanasa_sadan_gayatri_floorplan.png',
        )
        db.session.add(p)
        db.session.commit()
        print(f"Added Maanasa Sadan (Gayatri Nagar, Moulali), id {p.id}")

    # 6. Maanasa Arcade — Gautam Nagar (separate project, same name)
    p = find('Maanasa Arcade', 'Gautam Nagar')
    if p:
        p.status = 'Ongoing'
        db.session.commit()
        print(f"Updated Maanasa Arcade (Gautam Nagar) id {p.id}: status Ongoing")
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
            status='Ongoing', flats_count=4, floors_count=4,
            duration='Ready to Handover', completion_percentage=100,
            project_type='Residential', facing='West', area_sqft=1800,
            main_photo_url='maanasa_arcade_gautamnagar_elevation.png',
            gallery_photo_url='maanasa_arcade_gautamnagar_floorplan.png',
        )
        db.session.add(p)
        db.session.commit()
        print(f"Added Maanasa Arcade (Gautam Nagar), id {p.id}")

    # 7. Maanasa Swathi Mansion
    if not find('Swathi Mansion'):
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
            status='Ongoing', flats_count=10, floors_count=5,
            duration='Ready to Move', project_type='Residential',
            facing='East & West',
            main_photo_url='swathi_mansion_elevation.png',
            gallery_photo_url='swathi_mansion_floorplan.png',
        )
        db.session.add(p)
        db.session.commit()
        print(f"Added Maanasa Swathi Mansion, id {p.id}")

    # 8. Remove the two original incomplete placeholders
    for name, loc in [('Maanasa Arcade', 'Dayanand Nagar'), ('Sai Maanasa Nilayam', 'Gautam Nagar')]:
        p = find(name, loc)
        if p:
            print(f"Deleting placeholder: {p.name.strip()} — {p.location}")
            db.session.delete(p)
            db.session.commit()

    # 9. Remove G+3 Elevation
    p = find('G+3 Elevation')
    if p:
        print(f"Deleting: {p.name.strip()} — {p.location}")
        db.session.delete(p)
        db.session.commit()

    print("\nDone. Final project list:")
    for row in Project.query.all():
        print(f"  id={row.id} | {row.name.strip()} | {row.location} | {row.status}")
