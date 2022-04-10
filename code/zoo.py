import random
from flask import jsonify
import datetime
from enclosure import Enclosure
from animal import Animal
from employee import Employee
from collections import Counter

class Zoo:
    def __init__ (self):
        self.animals = []
        self.enclosures = []
        self.employees = []
        self.emp_min_animals = 0
        self.emp_max_animals = 0
        self.ave_animals = 0
        self.ave_num_of_animals_per_enclosure = 0
        self.enclo_with_diff_species = 0
        self.avail_space_per_animal = 0
        self.num_ani_per_species = {}

# ---------------------------------------
#               Animal
# ---------------------------------------
    def addAnimal(self, animal):
        self.animals.append(animal)

    def removeAnimal(self, animal):
        self.animals.remove(animal)

    def getAnimal(self, animal_id):
        for animal in self.animals:
            if animal.animal_id == animal_id:
                return animal
            else:
                return jsonify("Animal not found")

    def home(self, animal_id, enclosure_id):
        # getting the target animal
        current_animal = self.getAnimal(animal_id)
        # Not allowing an animal to assigned if there are no enclosures
        if self.enclosures == []:
            return jsonify("There aren't any enclosures to assign animals to")
        else:
            # if there is an enclosure:
            for animal in self.animals:
                if animal.animal_id == animal_id:
                    if current_animal.enclosure:
                        # getting the animals old enclosure if the animal was previously in one
                        old_enclosure_id = animal.enclosure
                        old_enclosure = self.getEnclosure(old_enclosure_id)
                        # removing the animal from that enclosure
                        # otehrwise old enclosure will still think that animal lives in it
                        old_enclosure.animals.remove(animal_id)
                    for enclosure in self.enclosures:
                        # finding the new enclosure
                        if enclosure.enclosure_id == enclosure_id:
                            # adding the target animal to the new enclosure
                            enclosure.animals.append(animal_id)
                            animal.enclosure = enclosure_id
                            return jsonify(f"Animal {animal_id} is now in enclosure {enclosure_id}")
                            print("home sorted")

    def birth(self, mother_id):
        # getting the details of the mother animal
        mother = self.getAnimal(mother_id)
        species = mother.species_name
        name = mother.common_name
        # creating a new animal with the mothers details
        new_born = Animal(species, name, 0)
        self.addAnimal(new_born)
        # if the mother was in an enclosure - adding the child to mothers' enclosure
        if mother.enclosure:
            enclosure_id = mother.enclosure
            self.home(new_born.animal_id, enclosure_id)
        return jsonify(new_born)
        print("Baby born")

    def death(self,animal_id):
        # getting the dead animal
        animal = self.getAnimal(animal_id)
        # if the animal was in an enclosure - remove it
        if animal.enclosure != None:
            enclosure_id = animal.enclosure
            self.leaveEnclosure(animal_id,enclosure_id)
        # if the animal had a caretaker - remove it
        if animal.care_taker != None:
            caretaker_id = animal.care_taker
            self.loseAnimal(caretaker_id,animal_id)
        self.removeAnimal(animal)
        return jsonify(f"Animal {animal_id} has left the building...")

    def animalStats(self):
        if self.animals == [] or self.enclosures == []:
            return jsonify("There aren't enough entries to calculate statistics yet")
        else:
            # getting animals per species
            species_list = []
            for animal in self.animals:
                species = animal.species_name
                species_list.append(species)

            tally_species = dict(Counter(species_list))
            tally_species = str(tally_species).replace("{","")
            tally_species = str(tally_species).replace("}", "")
            print(tally_species)

            # getting average number of animals in enclosures
            num_enclosures = len(self.enclosures)
            num_animals = len(self.animals)
            ave_num_animals_per_enclosure = num_animals / num_enclosures
            self.ave_num_of_animals_per_enclosure = ave_num_animals_per_enclosure # setting for test purposes

            # number of enclosures with different species and the available space left
            enclo_list = []
            diff_species = []
            species_set = set()
            available_space = {}
            enclo_species_counter = 0
            for enclosure in self.enclosures:
                enclo_list.append(enclosure.enclosure_id)
                species_counter = 0
                try:
                    available_space.update({enclosure.enclosure_id: round(enclosure.area / len(enclosure.animals))})
                    self.avail_space_per_animal = (round(enclosure.area / len(enclosure.animals)))
                except ZeroDivisionError:
                    available_space.update({enclosure.enclosure_id: enclosure.area})
                    self.avail_space_per_animal = enclosure.area
                for animal in enclosure.animals:
                    animal = self.getAnimal(animal) # returns full ANIMAL
                    ani_species = animal.species_name
                    if ani_species not in self.num_ani_per_species.keys():
                        self.num_ani_per_species.update({f'{ani_species}': 1})
                    else:
                        self.num_ani_per_species[f'{ani_species}'] += 1
                    # this might not be the best place to put it
                    species_set.add(ani_species)
                    # species_counter = len(species_set)
                # if species_counter > 1:
                #     diff_species.append(species_counter)
                #     self.num_of_diff_species = species_counter # setting for test purposes
                enclosure.diff_species = len(species_set)
                if enclosure.diff_species > 1 :
                    enclo_species_counter +=1
                    self.enclo_with_diff_species = enclo_species_counter
                else:
                    self.enclo_with_diff_species = 0

            return jsonify(f"The total number of animals per species is: {self.num_ani_per_species}"
                           f"The average number of animals per enclosure is: {ave_num_animals_per_enclosure}, "
                           f"the number of enclosures with multiple species is: {enclo_species_counter}, "
                           f"the available space per animal in each enclosure is: {available_space}")

# ---------------------------------------
#               Employee
# ---------------------------------------
    def addEmployee(self, employee):
        self.employees.append(employee)

    def getEmployee(self, employee_id):
        for employee in self.employees:
            if employee.employee_id == employee_id:
                return employee

    def careTaker(self, employee_id, animal_id):
        # getting the target animal
        animal = self.getAnimal(animal_id)
        # if there aren't any employees - don't allow action
        if self.employees == []:
            return jsonify("There aren't any employees, hire some more before assignment")
        else:
            # if the animal doesn't have a care taker - assign it the new one
            if animal.care_taker == None:
                animal.care_taker = employee_id
            else:
                # if the caretaker has an employee
                # remove the animal from old employee
                # assign new care taker
                old_careTaker_id = animal.care_taker
                old_careTaker = self.getEmployee(old_careTaker_id)
                old_careTaker.animals.remove(animal_id)
                animal.care_taker = employee_id
            # assigning the animal to the care taker
            employee = self.getEmployee(employee_id)
            employee.animals.append(animal_id)

            return jsonify(f"Employee {employee_id} now takes care of animal {animal_id}")

    def deleteEmployee(self,employee_id):
        employee = self.getEmployee(employee_id)
        # if there is only one employee - don't allow
        # as this will then leave the animals stranded
        if len(self.employees) == 1:
            return jsonify("You only have one employee, "
                           "you cannot delete this one otherwise the animals will be left unattended")
        else:
            # if there are more employees
            if len(self.employees) > 1:
                if employee.animals:
                    animal_list = []
                    for animal in employee.animals:
                        animal_list.append(animal) # animal ID
                        # assign animals new care taker
                    self.employees.remove(employee)
                    # choosing a new employee for the animals
                    new_care_taker = random.choice(self.employees)
                    for animal in animal_list:
                        ani = self.getAnimal(animal)
                        ani.care_taker = new_care_taker.employee_id
                        # assigning animals to caretaker
                        new_care_taker.animals.append(animal)
                return jsonify(f"Employee {employee_id} was removed!")
            else:
                self.employees.remove(employee)
                return jsonify(f"Employee {employee_id} was removed!")

            return jsonify(f"Employee {employee_id} was removed!")

    def loseAnimal(self, employee_id, animal_id):
        # used in conjuction with the death of an animal
        # removing animal from care taker
        employee = self.getEmployee(employee_id)
        employee.animals.remove(animal_id)


    def employeeStats(self):
        if self.employees == [] or self.animals == []:
            return jsonify("There aren't enough entries to calculate statistics")
        # lists to hold emp_id's and the amount of animals they look after
        emp_list = []
        ani_len = []
        # going through all the employees
        for employee in self.employees:
            # appending the employee_id and their corresponding amount of animals
            emp_list.append(employee.employee_id)
            ani_len.append(len(employee.animals))
        # constructing the dictionary with key=emp_id, val=number_of_animals
        totes = dict(zip(emp_list,ani_len))
        # getting the employee with the least amount of animals
        emp_with_min_animals = min(totes,key=totes.get)
        # getting the corresponding minimum values of animals
        min_value = totes[emp_with_min_animals]
        self.emp_min_animals = min_value # setting for test purposes
        # getting the employee with the most amount of aimals
        emp_with_max_animals = max(totes,key=totes.get)
        # getting the corresponding max value of animals
        max_value = totes[emp_with_max_animals]
        self.emp_max_animals = max_value # setting for test purposes
        # getting the average amount of animals
        ave_num_animals = sum(ani_len) / len(ani_len)
        self.ave_animals = ave_num_animals # setting for test purposes

        return jsonify(f"The employee with the least amount of animals is {emp_with_min_animals} and has {min_value}, "
                       f"the employee with the most amount of animals is {emp_with_max_animals} and has {max_value},"
                       f"the average amount of animals per person is {ave_num_animals} ~ roughly {round(ave_num_animals)}")

# ---------------------------------------
#               Enclosure
# ---------------------------------------
    def addEnclosure(self, enclosure):
        self.enclosures.append(enclosure)

    def getEnclosure(self, enclosure_id):
        for enclosure in self.enclosures:
            if enclosure.enclosure_id == enclosure_id:
                return enclosure

    def leaveEnclosure(self, animal_id, enclosure_id):
        # if an animal is to leave an enclosure
        enclosure = self.getEnclosure(enclosure_id)
        enclosure.animals.remove(animal_id)

    def clean(self, enclosure_id):
        enclosure = self.getEnclosure(enclosure_id)
        if not enclosure:
            return jsonify(f"Enclosure with ID {enclosure_id} was not found")
        enclosure.clean_record.append(datetime.datetime.now())
        return jsonify(enclosure)

    def removeEnclosure(self, enclosure_id):
        # getting target enclosure to remove
        enclosure = self.getEnclosure(enclosure_id)
        # if there are more than 1 enclosures
        # animals need to be moved to another enclosure
        if len(self.enclosures) > 1:
            if enclosure.animals != []:
                animal_list = []
                for animal in enclosure.animals:
                    # making list of animals for the next enclosure
                    animal_list.append(animal)
                    # assign new enclosure its new animals
                self.enclosures.remove(enclosure)
                new_enclosure = random.choice(self.enclosures)
                for animal in animal_list:
                    # assign new animals to new enclosure
                    # appending - because animals in enclosures are stored as ID's not ANIMALS
                    new_enclosure.animals.append(animal)

                # assign the new animals a new home
                for animal in new_enclosure.animals:
                    # assigning a home to each animal(ID)
                    ani = self.getAnimal(animal)
                    ani.enclosure = new_enclosure.enclosure_id
        # if the enclosure never had any animals
        if enclosure.animals == []:
            self.enclosures.remove(enclosure)

        return jsonify(f"Enclosure {enclosure_id} was removed!")

    def clean(self, enclosure_id):
        enclosure = self.getEnclosure(enclosure_id)
        # getting todays date for check
        today = datetime.datetime.now().date()
        # if there is nothing in the feed record
        if enclosure.clean_record != []:
            clean_record = str(enclosure.clean_record[-1])
            # if the last feed_rec is the same date as the next feed, then
            # it shouldn't be fed again
            if clean_record != str(enclosure.next_clean):
                return jsonify(f"Enclosure {enclosure_id} has already been cleaned,"
                               f" next clean on {enclosure.next_clean}")
            else:  # if feeding rec is either next_feed or another date
                enclosure.clean_record.append(today)
                enclosure.next_clean = today + datetime.timedelta(days=2)
                return jsonify(f"Enclosure {enclosure_id} is being cleaned,"
                               f" next clean on {enclosure.next_clean}")
        else:  # if feeding rec is either next feed or another date
            enclosure.clean_record.append(today)
            enclosure.next_clean = today + datetime.timedelta(days=2)
            return jsonify(f"Enclosure {enclosure_id} is being cleaned,"
                           f" next clean on {enclosure.next_clean}")

# ---------------------------------------
#               Tasks
# ---------------------------------------
    def cleaningSchedule(self):
        # creating the list to display which enclosures
        # and their clean dates
        cleaning_list = []
        for enclosure in self.enclosures:
            # get cleaning time
            if enclosure.clean_record == []:
                # then the next_clean will be NONE
                next_cleaning = datetime.datetime.now().date()
                enclosure.next_clean = next_cleaning
                cleaning_list.append(f"The next cleaning time for {enclosure.enclosure_id} is {enclosure.next_clean}")
                # next_cleaning = next_cleaning.datetime.date()
                return jsonify(cleaning_list)

            else:
                # This means the next_clean will have something
                # therefore the next_clean in enclosure will have the next clean
                next_cleaning = enclosure.next_clean # getting the next cleaning record date
                cleaning_list.append(f"The next cleaning time for {enclosure.enclosure_id} is {next_cleaning}")
        return (cleaning_list)

    def medicalSchedule(self):
        # creating list to display when the animals medical schedule
        medical_list = []
        for animal in self.animals:
            # getting check up date
            if animal.vet_record == []:
                # meaning the medical has nothing in it yet
                next_checkup = datetime.datetime.now().date()
                animal.next_check_up = next_checkup
                medical_list.append(f"The next check up for {animal.animal_id} is {animal.next_check_up}")
            else:
                next_checkup = animal.next_check_up
                medical_list.append(f"The next check for {animal.animal_id} is {next_checkup}")
        return (medical_list)

    def feedingSchedule(self):
        # creating list to display animals feeding schedule
        feeding_list = []
        for animal in self.animals:
            # getting the feeding date
            if animal.feeding_record == []:
                # the next feed will be NONE
                next_feeding = datetime.datetime.now().date()
                animal.next_feed = next_feeding
                feeding_list.append(f"The next feeding time for {animal.animal_id} is {animal.next_feed}")
            else:
                next_feeding = animal.next_feed
                feeding_list.append(f"The next feeding time for {animal.animal_id} is {next_feeding }")
            return (feeding_list)
