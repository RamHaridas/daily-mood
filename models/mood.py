from db import db
from datetime import date

class MoodModel(db.Model):
    __tablename__ = 'mood'
    mood_id = db.Column(db.Integer,primary_key=True)
    email = db.Column(db.String(101))
    day_status = db.Column(db.String(101))
    sleep_status = db.Column(db.String(101))
    time_spending = db.Column(db.String(101))
    eat_status = db.Column(db.String(101))
    activities = db.Column(db.String(101))
    entry_date = db.Column(db.Date())

    def __init__(self,email,day_status,sleep_status,time_spending,eat_status,activities,entry_date):
        self.email = email
        self.day_status = day_status
        self.sleep_status = sleep_status
        self.time_spending = time_spending
        self.eat_status = eat_status
        self.activities = activities
        self.entry_date = entry_date

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def json(self):
        string = self.entry_date.strftime("%Y/%m/%d")
        return {'email':self.email,'day_status':self.day_status,'sleep_status':self.sleep_status,'time_spending':self.time_spending,'eat_status':self.eat_status,'activites':self.activities,'date':string}

    @classmethod
    def find_by_email_and_date(cls,email,entry_date):
        return cls.query.filter_by(email = email,entry_date = entry_date).all()

    @classmethod
    def check_by_email_and_date(cls,email,entry_date):
        return cls.query.filter_by(email = email,entry_date = entry_date).first()

    @classmethod
    def analyze_weekly_status(cls,moodlist):
        day_stat = []
        sleep_stat = []
        time_stat = []
        eat_stat = []
        activity = []
        for mood in moodlist:
            day_stat.append(mood.day_status)
            sleep_stat.append(mood.sleep_status)
            time_stat.append(mood.time_spending)
            eat_stat.append(mood.eat_status)
            activity.append(mood.activities)
        


        return {'great':day_stat.count('GREAT'),'normal':day_stat.count('NORMAL'),'sad':day_stat.count('SAD'),
                'sleep early':sleep_stat.count('sleep early'),'sleep good':sleep_stat.count('sleep good'),'sleep medium':sleep_stat.count('sleep medium'),'sleep bad':sleep_stat.count('sleep bad'),
                'family':time_stat.count('family'),'friend':time_stat.count('friend'),
                'eat healty':eat_stat.count('eat healthy'),'eat_homemade':eat_stat.count('eat homemade'),'eat_fastfood':eat_stat.count('eat fastfood'),'eat soda':eat_stat.count('eat soda'),'eat sweets':eat_stat.count('eat sweets'),
                'read':activity.count('read'),'gaming':activity.count('gaming'),'movie':activity.count('movie'),'party':activity.count('party'),'workout':activity.count('workout')
                }

    @classmethod
    def analyze_user_statistics(cls,moodlist):

        day_stat = []
        sleep_stat = []
        time_stat = []
        eat_stat = []
        activity = []
        min_values = []
        #iterating over moodlist to fetch each mood data or row
        for mood in moodlist:
            #day_stat.append(mood.day_status)
            sleep_stat.append(mood.sleep_status)
            time_stat.append(mood.time_spending)
            eat_stat.append(mood.eat_status)
            activity.append(mood.activities)

       #craeting dictionary of each stat in order to store their individual count 
        sleep_dict = {'sleep early':sleep_stat.count('sleep early'),
                      'sleep good':sleep_stat.count('sleep good'),
                      'sleep medium':sleep_stat.count('sleep medium'),
                      'sleep bad':sleep_stat.count('sleep bad')
        }
        time_dict = {
            'family':time_stat.count('family'),
            'friend':time_stat.count('friend')
        }
        eat_dict = {
            'eat healty':eat_stat.count('eat healthy'),
            'eat homemade':eat_stat.count('eat homemade'),
            'eat fastfood':eat_stat.count('eat fastfood'),
            'eat soda':eat_stat.count('eat soda'),
            'eat sweets':eat_stat.count('eat sweets')
        }
        activity_dict = {
            'read':activity.count('read'),
            'gaming':activity.count('gaming'),
            'movie':activity.count('movie'),
            'party':activity.count('party'),
            'workout':activity.count('workout')
        }
        #appending the min values of each dictionary in min_values list
        min_values.append(min(sleep_dict,key=sleep_dict.get))
        min_values.append(min(time_dict,key=time_dict.get))
        min_values.append(min(eat_dict,key=eat_dict.get))
        min_values.append(min(activity_dict,key=activity_dict.get)) 
        
        return {'min':min_values}
