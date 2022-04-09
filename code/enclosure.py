import uuid
import datetime

class Enclosure:
    def __init__(self, name, area):
        self.name = name
        self.area = area
        self.enclosure_id = str(uuid.uuid4())
        self.animals = [] # stored as ID's!
        self.clean_record = []
        # YYYY-MM-DD
        # HH:MM:SS
        self.next_clean = None
        self.diff_species = 0

# e = Enclosure("asd", 12)
# e.clean_record.append(datetime.datetime.now())
#
# print(e.clean_record)
# e.clean_record.append(datetime.datetime.now())
# print(e.clean_record)
# d = e.clean_record[-1].date()
# print(d)
# z = d + datetime.timedelta(days=2)
# print(z)