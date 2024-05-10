from numpy.linalg import qr
from database import Database
import datetime

class MeasureMonthlyDataJob:
    db = Database().get_database()

    def __init__(self, name, description):
        self.name = name
        self.description = description

    def execute(self):
        today = datetime.datetime.now()
