from . import raceinfo
from .models import *
from datetime import datetime
import random
@raceinfo.route('/test_data/', methods=['GET', 'POST'])
def insert_test_data():
    strings=['name', 'surname']
    for i in range(1,30):
        year = random.randint(1950, 2000)
        month = random.randint(1, 12)
        day = random.randint(1, 28)
        birth_date = datetime(year, month, day)
        competitor = Competitor(
            fiscode = i,
            ru_firstname = strings[0]+str(i),
            en_firstname = strings[0]+str(i),
            ru_lastname = strings[1]+str(i),
            en_lastname = strings[1]+str(i),
            gender_id = random.randint(5,6),

            birth = birth_date,
            nation_code_id = 1,

            national_code =1,
            NSA = i,
            category_id = 1,

            points = 1,
            fis_points =1
        )
        db.session.add(competitor)
    return '',200