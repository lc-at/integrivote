import random
import time

from app import Vote, config, db

for i in range(800):
    v = Vote()
    v.id = str(time.time() + i)
    v.ts = time.time()
    v.dob = '26 Juli 2003'
    v.pob = 'Selong'
    v.name = 'Nekomamushi'
    v.mother_name = 'Aktif di Sekolah'
    v.gender = 'Laki-laki'
    v.class_ = 0
    v.choice = random.choice([0, 1, 2])
    assert v.validate()
    db.session.add(v)
    db.session.commit()
