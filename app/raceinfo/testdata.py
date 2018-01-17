from . import raceinfo
from .models import *
from datetime import datetime, timedelta
import random
from ..models import Role
@raceinfo.route('/test_data/', methods=['GET', 'POST'])
def insert_test_data():
    # db.create_all()
    # Discipline.insert_discipline()
    # Gender.insert_genders()
    # Status.insert()
    # Jury_function.insert_functions()
    # CourseDeviceType.insert_types()
    # nation =Nation( name='Rus',ru_description='Rus',en_description='Rus' )
    # db.session.add(nation)
    # category =Category(
    #     name='te',
    #     description = 'test',
    #     level =2
    # )
    # db.session.add(category)
    # db.session.commit()
    # strings=['name', 'surname']
    # for i in range(1,30):
    #     year = random.randint(1950, 2000)
    #     month = random.randint(1, 12)
    #     day = random.randint(1, 28)
    #     birth_date = datetime(year, month, day)
    #     competitor = Competitor(
    #         fiscode = i,
    #         ru_firstname = strings[0]+str(i),
    #         en_firstname = strings[0]+str(i),
    #         ru_lastname = strings[1]+str(i),
    #         en_lastname = strings[1]+str(i),
    #         gender_id = random.randint(1,2),
    #
    #         birth = birth_date,
    #         nation_code_id = 1,
    #
    #         national_code =1,
    #         NSA = i,
    #         category_id = 1,
    #
    #         points = 1,
    #         fis_points =1
    #     )
    #     db.session.add(competitor)
    # strings=['name', 'surname']
    # for i in range(1,5):
    #     coursetter = Coursetter(
    #         ru_firstname = strings[0]+str(i),
    #         en_firstname = strings[0]+str(i),
    #         ru_lastname = strings[1]+str(i),
    #         en_lastname = strings[1]+str(i),
    #         nation_id = 1,
    #     )
    #     db.session.add(coursetter)
    #     forerunner = Forerunner(
    #         ru_firstname=strings[0] + str(i),
    #         en_firstname=strings[0] + str(i),
    #         ru_lastname=strings[1] + str(i),
    #         en_lastname=strings[1] + str(i),
    #         nation_id=1,
    #     )
    #
    #     db.session.add(forerunner)
    return '',200
