from . import raceinfo
from .. import ScoreboardSender
from .models import *
from . DataViewer import timeConverter
from distutils.util import strtobool
class Scoreboard:
     def __init__(self,  resultDetail=None, run=None):
         self.competitor = db.session.query(RaceCompetitor.bib.label('bib'),
                             Competitor.en_firstname.label('firstname'),
                             Competitor.en_lastname.label('lastname'),
                             Nation.name.label('country_code')).\
         filter(RaceCompetitor.competitor_id == Competitor.id,
                Competitor.nation_code_id == Nation.id,
                RaceCompetitor.id == resultDetail.race_competitor_id).first()
         self.result = resultDetail


         self.race = db.session.query(Race.racedate.label('racedate'),
                          Race.eventname.label('eventname'),
                          Discipline.fiscode.label('discipline')).\
             filter(Race.id == run.race_id,
                    Race.discipline_id == Discipline.id).\
             first()
         self.run = run

         self.start_list = db.session.query(RunOrder.order.label('order'),
                                            RaceCompetitor.bib.label('bib'),
                                            Competitor.en_firstname.label('firstname'),
                                            Competitor.en_lastname.label('lastname')).\
             filter(RunOrder.race_competitor_id == RaceCompetitor.id,
                    RaceCompetitor.competitor_id == Competitor.id,
                    RunOrder.run_id == run.id
                    ).all()

         self.finish_list = db.session.query(ResultApproved.rank.label('rank'),
                                             RaceCompetitor.bib.label('bib'),
                                             Competitor.en_firstname.label('firstname'),
                                             Competitor.en_lastname.label('lastname'),
                                             ResultApproved.diff.label('diff')).\
             filter(ResultApproved.race_competitor_id == RaceCompetitor.id,
                    RaceCompetitor.competitor_id == Competitor.id,
                    ResultApproved.run_id == run.id
                    ).all()
         state=System.query.filter(System.key == "Scoreboard").fisrt()
         if state is None:
             self.is_active = True
         else:
             self.is_active = strtobool(state.value)

     @staticmethod
     @raceinfo.route('/scoreboard/connect')
     def connect():
         return ScoreboardSender.connect()

     @staticmethod
     @raceinfo.route('/scoreboard/active/<string:is_active>')
     def is_active(is_active):
         if is_active in ['true', 'false']:
            state = System.query.filter(System.key == "Scoreboard").first()
            if state is None:
                state = System(key='Scoreboard',
                               value=is_active)
            else:
                state.value = is_active
            db.session.add(state)
            db.session.commit()
         return ''

     @staticmethod
     @raceinfo.route('/scoreboard/status')
     def status():
         state = System.query.filter(System.key == "Scoreboard").first()
         return {'is_active': state.value}


     def new_best_time(self):
         if self.is_active:
             self.message = 'CCBestTime;%s;%s;%s;%s;!!' % (
                 self.competitor.bib,
                 (self.competitor.firstname[0] + '.' + self.competitor.lastname),
                 self.competitor.country_code,
                 timeConverter(self.result.time, '%H:%M:%S.%f')
             )

     def next_competitor(self):
         if self.is_active:
             self.message = 'CCNextCompetitor;%s;%s;%s;%s;!!' % (
                 self.competitor.bib,
                 (self.competitor.firstname[0] + '.' + self.competitor.lastname),
                 self.competitor.country_code,
                 timeConverter(self.result.time, '%H:%M:%S.%f')
             )
     def started_competitor(self):
         if self.is_active:
             self.message = 'CCStart;%s;%s;%s;%s;!!' % (
                 self.competitor.bib,
                 (self.competitor.firstname[0] + '.' + self.competitor.lastname),
                 self.competitor.country_code,
                 timeConverter(self.result.time, '%H:%M:%S.%f')
             )

     def crossed_device(self):
         if self.is_active:
             self.message = 'CCInter;%s;%s;%s;%s;%s;%s;!!' % (
                 self.competitor.bib,
                 (self.competitor.firstname[0] + '.'+self.competitor.lastname),
                 self.competitor.country_code,
                 timeConverter(self.result.time),
                 timeConverter(self.result.diff),
                 self.result.rank
             )

     def finished_competitor(self):
         self.message = "CCFinish;%s;%s;%s;%s;%s;%s;!!" % (
             self.competitor.bib,
             (self.competitor.firstname[0] + '.'+self.competitor.lastname),
             self.competitor.country_code,
             timeConverter(self.result.time),
             timeConverter(self.result.diff),
             self.result.rank
         )
     def finished_list(self):
         if self.is_active:
             self.message = "CCfinishlist;" + \
                            self.race.racedate.strftime('%d:%m:%Y') + ';' + \
                            self.race.eventname + ';' + \
                            self.race.discipline + ';' + str(self.run.number) + ';'
             for item in self.finish_list:
                 self.message += str(item.rank) + ';' + \
                 str(item.bib) + ';' + item.firstname + ';' + item.lastname + ';' + timeConverter(item.diff) + ';'
             self.message += '!!'

     def start_list(self):
         if self.is_active:
             self.message = "CCstartlist;" + \
                            self.race.racedate.strftime('%d:%m:%Y') + ';' + \
                            self.race.eventname + ';' + \
                            self.race.discipline + ';' + str(self.run.number) + ';'
             for item in self.start_list:
                 self.message += str(item.order) + ';' + \
                 str(item.bib) + ';' + item.firstname + ';' + item.lastname + ';'
             self.message += '!!'

     def send(self):
         if self.is_active:
            ScoreboardSender.send(self.message.encode())