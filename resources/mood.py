from flask_restful import Resource,reqparse
from models.mood import MoodModel
from datetime import date,timedelta

class Mood(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument(
        'email',
        type=str,
        required=True,
        help = 'email is mandatory'
    )
    parser.add_argument(
        'day_status',
        type=str,
        required=True,
        help = 'day_status is mandatory'
    )
    parser.add_argument(
        'sleep_status',
        type=str,
        required=True,
        help = 'sleep_status is mandatory'
    )
    parser.add_argument(
        'time_spending',
        type=str,
        required=True,
        help = 'time_spending is mandatory'
    )
    parser.add_argument(
        'eat_status',
        type=str,
        required=True,
        help = 'eat_status is mandatory'
    )
    parser.add_argument(
        'activities',
        type=str,
        required=True,
        help = 'activities is mandatory'
    )
    

    def post(self):
        data = Mood.parser.parse_args()
        new = date.today()
        mood = MoodModel.check_by_email_and_date(data['email'],new)
        
        if mood:                                                    
            mood.sleep_status = data['sleep_status']                #updating current data   
            mood.day_status = data['day_status']
            mood.time_spending = data['time_spending']
            mood.eat_status = data['eat_status']
            mood.activities = data['activities']
            
        else:
            mood = MoodModel(**data,entry_date=new)  #save all data at once  

        mood.save()

        return mood.json()


    def get(self):
        local = reqparse.RequestParser()
        local.add_argument(
            'email',
            type=str,
            required=True,
            help='email is mandatory'
        )

        data = local.parse_args()

        moodlist = []
        today = date.today()
        for i in range(0,7):
            #print (today - timedelta(days=i))
            for mood in MoodModel.find_by_email_and_date(data['email'],(today - timedelta(days=i))):
                moodlist.append(mood)

        return MoodModel.analyze_weekly_status(moodlist)

    #this function is not to be used
    def delete(self):
        
        local = reqparse.RequestParser()
        local.add_argument(
            'email',
            type=str,
            required=True,
            help='email is mandatory'
        )
        local.add_argument(
            'ram',
            type=str,
            required=True,
            help='ram haridas knows this stuff, ask him'
        )
        
        data = local.parse_args()
        if data['ram'] != 'force':
            return{'msg':'koshish kiya tumne, par jama nahi'}
        today = date.today()
        for i in range(0,7):
            #print (today - timedelta(days=i))
            for mood in MoodModel.find_by_email_and_date(data['email'],(today - timedelta(days=i))):
                if mood:
                    mood.delete()

        return{'msg': 'deleted'}


class UserMoodStatus(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        'email',
        type=str,
        required=True,
        help = 'email is mandatory'
    )

    def get(self):

        data = UserMoodStatus.parser.parse_args()
        moodlist = []
        today = date.today()
        for i in range(0,7):
            for mood in MoodModel.find_by_email_and_date(data['email'],(today - timedelta(days=i))):
                moodlist.append(mood.json())

        return {'moods':moodlist}


class MoodSuggestion(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        'email',
        type=str,
        required=True,
        help = 'email is mandatory'
    )
    
    def get(self):
        data = MoodSuggestion.parser.parse_args()
        today = date.today()
        moodlist = []
        for i in range(0,7):
            for mood in MoodModel.find_by_email_and_date(data['email'],(today - timedelta(days=i))):
                moodlist.append(mood)

        return MoodModel.analyze_user_statistics(moodlist)
        