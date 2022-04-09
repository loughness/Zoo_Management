import uuid
import datetime

class Enclosure:
    def __init__(self, name, area):
        self.name = name
        self.area = area
        self.enclosure_id = str(uuid.uuid4())
        self.animals = [] # stored as ID's!
        self.clean_record = [] # YYYY-MM-DD HH:MM:SS
        self.next_clean = None
        self.diff_species = 0
