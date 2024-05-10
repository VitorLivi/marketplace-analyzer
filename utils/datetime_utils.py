import datetime

class DateTimeUtils:
    def __init__(self, year, month, day):
        self.year = year
        self.month = month
        self.day = day

    @staticmethod
    def getCurrentWeekRange ():
        today = datetime.datetime.now()
        start = today - datetime.timedelta(days=today.weekday())
        end = start + datetime.timedelta(days=6)
        return start, end
    
    def getDaysOfWeekRange (week_range):
        days = []
        for i in range(7):
            days.append(week_range[0] + datetime.timedelta(days=i))
        return days
