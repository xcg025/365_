from datetime import datetime,date

class WeekDay:
    @classmethod
    def isWeekend(cls):
        theDayOfWeek = datetime.now().weekday()
        if theDayOfWeek == 4 or theDayOfWeek == 5 or theDayOfWeek == 6:
            return True
        return False

