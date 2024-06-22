import datetime

class DateTimeUtils:
    def __init__(self, year, month, day):
        self.year = year
        self.month = month
        self.day = day

    @staticmethod
    def get_current_week_range ():
        today = datetime.datetime.now()
        start = today - datetime.timedelta(days=today.weekday())
        end = start + datetime.timedelta(days=6)
        return start, end

    @staticmethod
    def get_current_month_range ():
        today = datetime.datetime.now()
        start = today.replace(day=1)
        end = today.replace(day=1, month=today.month+1) - datetime.timedelta(days=1)
        return start, end
    
    def get_days_of_week_range (week_range):
        days = []
        for i in range(7):
            days.append(week_range[0] + datetime.timedelta(days=i))
        return days

    def get_days_of_month_range (month_range):
        days = []
        
        for i in range((month_range[1] - month_range[0]).days + 1):
            days.append(month_range[0] + datetime.timedelta(days=i))
