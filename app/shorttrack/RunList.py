from . import db
from .models import Competitor, RunOrder, RunInfo, RunGroup, Race, VirtualDevice, ResultDetail
import math
import xlwt
from .Race import timeConverter
import io

CIRCLE_LENGHT = 111.12

class RunList:
    def __init__(self, race_id):
        self.race_id = race_id
        generateVirtualDevices(race_id)

    def builder_1st_run(self):
        competitors_list = Competitor.query.filter(Competitor.race_id == self.race_id).all()
        competitors_list = sorted([item for item in competitors_list if item.points is not None],
                                   key=lambda item: item.points) + \
                           sorted([item for item in competitors_list if item.points is None],
                                   key=lambda item: item.best_season_time)

        run = RunInfo.query.filter(RunInfo.race_id == self.race_id,
                                    RunInfo.number == 1).first()

        if run is None:
            run = RunInfo(
                number=1,
                race_id=self.race_id
            )
            db.session.add(run)
            db.session.commit()


        reversed = False
        
        count = math.ceil(len(competitors_list)/4)
        for index in range(int(count)):
            run_group = RunGroup(
                run_id=run.id,
                number=index+1
            )
            db.session.add(run_group)
        db.session.commit()
        runGroupList = RunGroup.query.filter(RunGroup.run_id == run.id).\
            order_by(RunGroup.number.asc()).all()

        order = 1
        group_order = 1

        for index in range(len(competitors_list)):
            item = competitors_list.pop(0)
            competitor_order = RunOrder(
                competitor_id=item.id,
                run_id=run.id,
                order=order,
                group_id=runGroupList[group_order-1].id
            )
            db.session.add(competitor_order)
            if (index+1) % count == 0:
                group_order += 1
                reversed = not reversed
            elif reversed:
                order -= 1
            else:
                order += 1

def generateVirtualDevices(race_id):
    race = Race.query.get(race_id)
    db.session.query(VirtualDevice).filter(VirtualDevice.race_id == race.id).delete()
    print(round(race.distance/CIRCLE_LENGHT))
    for index in range(round(race.distance/CIRCLE_LENGHT)+1):
        print(index)
        virtualDevice = VirtualDevice(
            race_id=race.id,
            order=index
        )
        db.session.add(virtualDevice)
    db.session.commit()


class ExcelGenerator:
    row = None
    column = None
    wb = None
    ws = None
    def __init__(self, sheet_name):
        self.wb = xlwt.Workbook()
        self.ws = self.wb.add_sheet(sheet_name)

    def set_header(self):
        self.ws.write(0, 0, 'uid')
        self.ws.write(0, 1, 'firstname')
        self.ws.write(0, 2, 'lastname')
        self.ws.write(0, 3, 'time')
        self.ws.write(0, 4, 'diff')
        self.ws.write(0, 5, 'rank')
        self.ws.write(0, 6, 'next run group')
        self.ws.write(0, 7, 'order in group')
        self.row = 1

    def set_data(self, race_id, run_id):
        lastDevice = VirtualDevice.query.filter(VirtualDevice.race_id == race_id).\
            order_by(VirtualDevice.order.desc()).\
            limit(1).first()
        data = db.session.query(ResultDetail, Competitor).join(Competitor, ResultDetail.competitor_id==Competitor.id).\
            filter(ResultDetail.run_id == run_id,
                   ResultDetail.virtual_device_id == lastDevice.id, ResultDetail.is_first==True).\
            order_by(ResultDetail.group_id.asc(), ResultDetail.grouprank.asc()).all()

        for item in data:
            self.ws.write(self.row, 0, item[1].id)
            self.ws.write(self.row, 1, item[1].ru_firstname)
            self.ws.write(self.row, 2, item[1].ru_lastname)
            self.ws.write(self.row, 3, timeConverter(item[0].time))
            self.ws.write(self.row, 4, timeConverter(item[0].diff))
            self.ws.write(self.row, 5, item[0].grouprank)
            self.row += 1

    def save(self, path):
        self.wb.save(path)

    def get_xls_file(self):
        output = io.BytesIO()
        self.wb.save(output)
        return output.getvalue()

class ExcelLoader:
    pass