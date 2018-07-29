from . import raceinfo
from .. import ScoreboardSender
from .models import *
from . DataViewer import timeConverter
from distutils.util import strtobool
from .. import socketio
import json

class Scoreboard:
     def __init__(self, raceHandler):
         self.raceHandler = raceHandler
         # self.competitor = db.session.query(RaceCompetitor.bib.label('bib'),
         #                     Competitor.en_firstname.label('firstname'),
         #                     Competitor.en_lastname.label('lastname'),
         #                     Nation.name.label('country_code')).\
         # filter(RaceCompetitor.competitor_id == Competitor.id,
         #        Competitor.nation_code_id == Nation.id,
         #        RaceCompetitor.id == resultDetail.race_competitor_id).first()
         # self.result = resultDetail
         #
         #
         # self.race = db.session.query(Race.racedate.label('racedate'),
         #                  Race.eventname.label('eventname'),
         #                  Discipline.fiscode.label('discipline')).\
         #     filter(Race.id == run.race_id,
         #            Race.discipline_id == Discipline.id).\
         #     first()
         # self.run = run
         #
         # self.start_list = db.session.query(RunOrder.order.label('order'),
         #                                    RaceCompetitor.bib.label('bib'),
         #                                    Competitor.en_firstname.label('firstname'),
         #                                    Competitor.en_lastname.label('lastname')).\
         #     filter(RunOrder.race_competitor_id == RaceCompetitor.id,
         #            RaceCompetitor.competitor_id == Competitor.id,
         #            RunOrder.run_id == run.id
         #            ).all()
         #
         # self.finish_list = db.session.query(ResultApproved.rank.label('rank'),
         #                                     RaceCompetitor.bib.label('bib'),
         #                                     Competitor.en_firstname.label('firstname'),
         #                                     Competitor.en_lastname.label('lastname'),
         #                                     ResultApproved.diff.label('diff')).\
         #     filter(ResultApproved.race_competitor_id == RaceCompetitor.id,
         #            RaceCompetitor.competitor_id == Competitor.id,
         #            ResultApproved.run_id == run.id,
         #            ResultApproved.is_finish == True
         #            ).all()
         state = System.query.filter(System.key == "Scoreboard").first()
         if state is None:
             state = System(key='Scoreboard', value=False)
             self.is_active = False
             db.session.add(state)
         else:
             self.is_active = strtobool(state.value)
         is_connected = System.query.filter(System.key == "ScoreboardConnect").first()
         if is_connected is None:
             is_connected = System(key='ScoreboardConnect', value=False)
             self.is_connected = False
             db.session.add(is_connected)
         db.session.commit()

     @staticmethod
     @socketio.on('ScoreboardConnect')
     def connect():
         status = System.query.filter(System.key == "ScoreboardConnect").first()
         if status is None:
             status = System(key='ScoreboardConnect')
         if ScoreboardSender.connect():
             status.value = 'True'
         else:
             status.value = 'False'
         db.session.add(status)
         db.session.commit()
         socketio.emit('ScoreboardStatus', json.dumps({'is_connected': strtobool(status.value)}))


     @staticmethod
     @socketio.on('ScoreboardDisconnect')
     def close():
         ScoreboardSender.close()
         status = System.query.filter(System.key == "ScoreboardConnect").first()
         if status is None:
             status = System(key='ScoreboardConnect')
         status.value = 'False'
         db.session.add(status)
         db.session.commit()
         socketio.emit('ScoreboardStatus', json.dumps({'is_connected': strtobool(status.value)}))

     @staticmethod
     @socketio.on('ScoreboardActive')
     def is_active(is_active):
         is_connected = System.query.filter(System.key == "ScoreboardConnect").first()
         if is_active in ['true', 'false']:
             state = System.query.filter(System.key == "Scoreboard").first()
             if state is None:
                 state = System(key='Scoreboard', value=is_active)
             else:
                 state.value = is_active
             db.session.add(state)
             db.session.commit()
             socketio.emit('ScoreboardStatus', json.dumps({'is_active': strtobool(state.value), 'is_connected': strtobool(is_connected.value)}))

     @staticmethod
     @socketio.on('GetScoreboardStatus')
     def status():
         state = System.query.filter(System.key == "Scoreboard").first()
         is_connected = System.query.filter(System.key == "ScoreboardConnect").first()
         socketio.emit('ScoreboardStatus', json.dumps({'is_active': strtobool(state.value),
                                                       'is_connected': is_connected.value}))


     def new_best_time(self):
         if self.is_active:
             competitor = self.raceHandler.get_competitor_info()
             self.message = 'CCBestTime;%s;%s;%s;%s;!!' % (
                 competitor.bib,
                 (competitor.firstname[0] + '.' + competitor.lastname),
                 competitor.country_code,
                 timeConverter(self.raceHandler.result.time, '%H:%M:%S.%f')
             )

     def next_competitor(self):
         if self.is_active:
             competitor = self.raceHandler.get_competitor_info()
             self.message = 'CCNextCompetitor;%s;%s;%s;%s;!!' % (
                 competitor.bib,
                 (competitor.firstname[0] + '.' + competitor.lastname),
                 competitor.country_code,
                 timeConverter(self.raceHandler.result.time, '%H:%M:%S.%f')
             )
     def started_competitor(self):
         if self.is_active:
             competitor = self.raceHandler.get_competitor_info()
             self.message = 'CCStart;%s;%s;%s;%s;!!' % (
                 competitor.bib,
                 (competitor.firstname[0] + '.' + competitor.lastname),
                 competitor.country_code,
                 timeConverter(self.raceHandler.result.time, '%H:%M:%S.%f')
             )

     def crossed_device(self):
         if self.is_active:
             competitor = self.raceHandler.get_competitor_info()
             self.message = 'CCInter;%s;%s;%s;%s;%s;%s;!!' % (
                 competitor.bib,
                 (competitor.firstname[0] + '.'+competitor.lastname),
                 competitor.country_code,
                 timeConverter(self.raceHandler.result.time),
                 timeConverter(self.raceHandler.result.diff),
                 self.raceHandler.result.rank
             )

     def finished_competitor(self):
         if self.is_active:
             competitor = self.raceHandler.get_competitor_info()
             self.message = "CCFinish;%s;%s;%s;%s;%s;%s;!!" % (
                 competitor.bib,
                 (competitor.firstname[0] + '.'+competitor.lastname),
                 competitor.country_code,
                 timeConverter(self.raceHandler.result.time),
                 timeConverter(self.raceHandler.result.diff),
                 self.raceHandler.result.rank
             )
     def finished_list(self):
         if self.is_active:
             self.message = "CCfinishlist;" + \
                            self.raceHandler.race.racedate.strftime('%d:%m:%Y') + ';' + \
                            self.raceHandler.race.eventname + ';' + \
                            self.raceHandler.discipline.name + ';' + str(self.raceHandler.run.number) + ';'
             for item in self.raceHandler.finish_list_info():
                 self.message += str(item.rank) + ';' + \
                 str(item.bib) + ';' + item.firstname + ';' + item.lastname + ';' + timeConverter(item.diff) + ';'
             self.message += '!!'

     def start_list(self):
         if self.is_active:
             self.message = "CCstartlist;" + \
                            self.raceHandler.race.racedate.strftime('%d:%m:%Y') + ';' + \
                            self.raceHandler.race.eventname + ';' + \
                            self.raceHandler.race.discipline + ';' + str(self.raceHandler.run.number) + ';'
             # for item in self.raceHandler.finish_list_info():
             #     self.message += str(item.order) + ';' + \
             #     str(item.bib) + ';' + item.firstname + ';' + item.lastname + ';'
             # self.message += '!!'

     def send(self):
         if self.is_active:
             try:
                 ScoreboardSender.send(self.message.encode())
             except:
                 is_connected = System.query.filter(System.key == "ScoreboardConnect").first()
                 is_connected.value = False
                 Scoreboard.status()

