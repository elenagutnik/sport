from . import db
from .models import Competitor, RunOrder, RunInfo, RunGroup, Race, VirtualDevice, ResultDetail, Status
import math
import xlwt
from .Race import timeConverter
import io

CIRCLE_LENGHT = 111.12

class RunList:
    def __init__(self, race_id):
        self.race = Race.query.filter(Race.id == race_id).first()
        self.run = None
        generateVirtualDevices(race_id)

    def builder_1st_run(self):
        competitors_list = Competitor.query.filter(Competitor.race_id == self.race.id).all()
        competitors_list = sorted([item for item in competitors_list if item.points is not None],
                                   key=lambda item: item.points) + \
                           sorted([item for item in competitors_list if item.points is None],
                                   key=lambda item: item.best_season_time)

        run = RunInfo.query.filter(RunInfo.race_id == self.race.id,
                                    RunInfo.number == 1).first()
        RunOrder.query.filter(RunOrder.run_id == run.id).delete()
        RunGroup.query.filter(RunGroup.run_id == run.id).delete()
        if run is None:
            run = RunInfo(
                number=1,
                race_id=self.race.id
            )
            db.session.add(run)
            db.session.commit()

        self.run = run
        reversed = False
        
        count = math.ceil(len(competitors_list)/self.race.competitors_in_group)

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
                reversed = not reversed
                order += 1
            elif reversed:
                group_order -= 1
            else:
                # order += 1
                group_order += 1

def generateVirtualDevices(race_id):
    race = Race.query.get(race_id)
    db.session.query(VirtualDevice).filter(VirtualDevice.race_id == race.id).delete()
    for index in range(round(race.distance/CIRCLE_LENGHT)+1):
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
        self.ws.write(0, 6, 'status')
        self.ws.write(0, 7, 'next run group')
        self.ws.write(0, 8, 'order in group')
        self.ws.write(0, 10, 'status codes')
        statusList = Status.query.all()
        coll = 10
        self.row = 1
        for index, item in enumerate(statusList):
            self.ws.write(self.row+index, 10, item.name)




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

# class ExcelLoader:
#     def race_run_startlist_upload(id, run_id):
#         filename = request.files['list'].filename
#         extension = filename.split(".")[-1]
#         content = request.files['list'].read()
#         sheet = pyexcel.get_sheet(file_type=extension, file_content=content)
#         runList = RunGroup.query.filter(RunGroup.run_id == run_id).all()
#         db.session.query(RunOrder).filter(RunOrder.run_id == run_id).delete()
#         for item in sheet.to_array()[1:]:
#             if item[6] != '':
#                 group = next((itm for itm in runList if itm.number == item[6]), None)
#                 if group is None:
#                     group = RunGroup(
#                         number=item[6],
#                         run_id=run_id
#                     )
#                     db.session.add(group)
#                     db.session.commit()
#                     runList.append(group)
#
#                 runOrder = RunOrder(
#                     group_id=group.id,
#                     order=item[7],
#                     competitor_id=item[0],
#                     run_id=run_id
#                 )
#                 db.session.add(runOrder)
#         db.session.commit()
#         return redirect(url_for('.race_run_orderlist', race_id=id, run_id=run_id, _external=True))