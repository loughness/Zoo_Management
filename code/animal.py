import uuid 
import datetime
from flask import jsonify

class Animal: 
    def __init__ (self, species_name, common_name, age): 
        self.animal_id = str(uuid.uuid4())
        self.species_name = species_name 
        self.common_name = common_name 
        self.age = age 
        self.feeding_record = [] 
        self.enclosure = None 
        self.care_taker = None
        self.vet_record = []
        self.next_check_up = None
        self.next_feed = None
        self.area_needed = 28 # minimum space needed per animal
        # add more as required here 
        
    # simply store the current system time when this method is called    
    def feed(self):
        # getting todays date for check
        today = datetime.datetime.now().date()
        # if there is something in the feed record
        if self.feeding_record != []:
            feeding_record = str(self.feeding_record[-1])
            # if the last feed_rec is the same date as the next feed, then
            # it shouldn't be fed again
            if feeding_record != str(self.next_feed):
                return jsonify(f"Animal {self.animal_id} has already been fed,"
                               f" next feed on {self.next_feed}")
                print("Animal has already been fed")
            else:  # if feeding rec is either next_feed or another date
                self.feeding_record.append(today)
                self.next_feed = today + datetime.timedelta(days=2)
                return jsonify(f"Animal {self.animal_id} is being fed,"
                               f" next feed on {self.next_feed}")
                print("Animal is being fed")
        else:  # if feeding rec is either next feed or another date
            self.feeding_record.append(today)
            self.next_feed = today + datetime.timedelta(days=2)
            return jsonify(f"Animal {self.animal_id} is being fed,"
                           f" next feed on {self.next_feed}")
            print("Animal is being fed")

    def vet(self):
        # getting todays date for check
        today = datetime.datetime.now().date()
        # if there is nothing in the vet record
        if self.vet_record != []:
            vet_record = str(self.vet_record[-1])
            # if the last vet record is the same date as the next check up, then
            # it shouldn't be checked again
            if vet_record != str(self.next_check_up):
                # return jsonify(f"Animal {self.animal_id} has already been checked up,"
                #                f" next check up on {self.next_check_up}")
                print("Animal already checked")
            else: # if vet record is either next_check_up or another date
                self.vet_record.append(today)
                self.next_check_up = today + datetime.timedelta(days=3)
                # return jsonify(f"Animal {self.animal_id} is being checked up,"
                #                f" next check up on {self.next_check_up}")
                print("Animal being checked")
        else: # if vet record is either next_check_up or another date
            self.vet_record.append(today)
            self.next_check_up = today + datetime.timedelta(days=3)
            # return jsonify(f"Animal {self.animal_id} is being checked up,"
            #                f" next check up on {self.next_check_up}")
            print("Animal is being checked")
# a = Animal("asd","asd",12)
#
# a.vet()
# a.vet()
# print(a.vet_record)