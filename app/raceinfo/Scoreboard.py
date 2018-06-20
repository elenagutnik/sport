from . import raceinfo
from .. import ScoreboardSender

class Scoreboard:
     time = None
     def __init__(self, bib, firstname, lastname, country_code, time=0):
         self.bib = str(bib)
         self.firstname = firstname
         self.lastname = lastname
         self.country_code = country_code
         self.time = str(time)


     @staticmethod
     @raceinfo.route('/scoreboard/connect')
     def connect():
         ScoreboardSender.connect()
         return '0'

     def new_best_time(self):
         return ('CCBestTime;%s;%s;%s;%s;!!' % (
             self.bib,
             (self.firstname[0] + '.'+self.lastname),
             self.country_code,
             self.time
         )).encode()

     def next_competitor(self):
         return ('CCNextCompetitor;%s;%s;%s;%s;!!' % (
             self.bib,
             (self.firstname[0] + '.'+self.lastname),
             self.country_code,
             self.time
         )).encode()

     def started_competitor(self):
         return ('CCStart;%s;%s;%s;%s;!!' % (
             self.bib,
             (self.firstname[0] + '.'+self.lastname),
             self.country_code,
             self.time
         )).encode()

     def crossed_device(self):
         return ('CCInter;%s;%s;%s;%s;!!' % (
             self.bib,
             (self.firstname[0] + '.'+self.lastname),
             self.country_code,
             self.time
         )).encode()

     def finished_competitor(self):
         return ("CCFinish;%s;%s;%s;%s;!!" % (
             self.bib,
             (self.firstname[0] + '.'+self.lastname),
             self.country_code,
             self.time
         )).encode()

     @staticmethod
     def send(msg):
         ScoreboardSender.send(msg)