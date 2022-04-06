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

    def home(self, animal_id, enclosure_id):
        current_animal = self.getAnimal(animal_id)
        for animal in self.animals:
            if animal.animal_id == animal_id:
                if current_animal.enclosure:
                    old_enclosure_id = animal.enclosure
                    old_enclosure = self.getEnclosure(old_enclosure_id)
                    old_enclosure.animals.remove(animal_id)
                for enclosure in self.enclosures:
                    if enclosure.enclosure_id == enclosure_id:
                        enclosure.animals.append(animal_id)
                        animal.enclosure = enclosure_id
                        return jsonify(animal_id,enclosure_id)

    def birth(self, mother_id):
        mother = self.getAnimal(mother_id)
        species = mother.species_name
        name = mother.common_name
        new_born = Animal(species, name, 0)
        self.addAnimal(new_born)

        if mother.enclosure:
            enclosure_id = mother.enclosure
            self.home(new_born.animal_id, enclosure_id)
        return jsonify(new_born)

    def death(self,animal_id):
        animal = self.getAnimal(animal_id)
        if animal.enclosure:
            enclosure_id = animal.enclosure
            self.leaveEnclosure(animal_id,enclosure_id)

        self.removeAnimal(animal)
        return jsonify(f"Animal {animal_id} has left the building...")

    def animalStats(self):
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
        # print(ave_num_animals_per_enclosure, " Number of animals per enclosure")

        # number of enclosures with different species and the available space left
        enclo_list = []
        diff_species = []
        available_space = {}
        for enclosure in self.enclosures:
            enclo_list.append(enclosure.enclosure_id)
            species_counter = 0
            available_space.update({enclosure.enclosure_id: round(enclosure.area / len(enclosure.animals))})
            for animal in enclosure.animals:
                animal = self.getAnimal(animal) # returns full ANIMAL
                ani_species = animal.species_name
                species_set = set()# this might not be the best place to put it
                species_set.add(ani_species)
                species_counter = len(species_set)
            if species_counter > 1:
                diff_species.append(species_counter)
        # print(f"The number of enclosures with multiple species is {len(diff_species)}")
        # print(f"The available space per animal is {available_space}")

        return jsonify(f"The average number of animals per enclosure is: {ave_num_animals_per_enclosure}, "
                       f"the number of enclosures with multiple species is: {len(diff_species)}, "
                       f"the available space per animal in each enclosure is: {available_space}")

        # available space per animal in enclosure



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
        animal = self.getAnimal(animal_id)
        if animal.care_taker == None:
            animal.care_taker = employee_id
        else:
            old_careTaker_id = animal.care_taker
            old_careTaker = self.getEmployee(old_careTaker_id)
            old_careTaker.animals.remove(animal_id)
            animal.care_taker = employee_id

        employee = self.getEmployee(employee_id)
        employee.animals.append(animal_id)

        return jsonify(f"Employee {employee_id} now takes care of animal {animal_id}")

    def deleteEmployee(self,employee_id):
        employee = self.getEmployee(employee_id)
        if len(self.employees) > 1:
            if employee.animals:
                animal_list = []
                for animal in employee.animals:
                    animal_list.append(animal) # animal ID
                    # assign animals new care taker

                self.employees.remove(employee)
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


    def employeeStats(self):
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
        # getting the employee with the most amount of aimals
        emp_with_max_animals = max(totes,key=totes.get)
        # getting the corresponding max value of animals
        max_value = totes[emp_with_max_animals]
        # getting the average amount of animals
        ave_num_animals = sum(ani_len) / len(ani_len)

        return jsonify(f"The employee with the least amount of animals is {emp_with_min_animals} and has {min_value}, "
                       f"the employee with the most amount of animals is {emp_with_max_animals} and has {max_value},"
                       f"the average amount of animals per person is {ave_num_animals} ~ roughly {round(ave_num_animals)}")

        # print(f"Emp with min animals {emp_with_min_animals} has {min_value}")
        # print(f"Emp with max animals is {emp_with_max_animals} and has {max_value}")
        # print(f"The average amount of animals per person is {ave_num_animals} ~ roughly {round(ave_num_animals)}")


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
        enclosure = self.getEnclosure(enclosure_id)
        enclosure.animals.remove(animal_id)

    def clean(self, enclosure_id):
        enclosure = self.getEnclosure(enclosure_id)
        if not enclosure:
            return jsonify(f"Enclosure with ID {enclosure_id} was not found")
        enclosure.clean_record.append(datetime.datetime.now())
        return jsonify(enclosure)

    def removeEnclosure(self, enclosure_id):
        enclosure = self.getEnclosure(enclosure_id)
        if len(self.enclosures) > 1:
            if enclosure.animals:
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

        else:
            self.enclosures.remove(enclosure)

        return jsonify(f"Enclosure {enclosure_id} was removed!")

    def clean(self, enclosure_id):
        enclosure = self.getEnclosure(enclosure_id)
        clean = datetime.datetime.now().date()
        enclosure.clean_record.append(clean)
        next_clean = clean + datetime.timedelta(days=3)
        enclosure.next_clean = next_clean
        return jsonify(f"Enclosure {enclosure_id} was cleaned, next cleaning will be on {next_clean}")

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
        cleaning_list = []
        for enclosure in self.enclosures:
            # get cleaning time
            if enclosure.clean_record == []:
                # then the next_clean will be NONE
                next_cleaning = datetime.datetime.now().date()
                enclosure.next_clean = next_cleaning
                cleaning_list.append(f"The next cleaning time for {enclosure.enclosure_id} is {enclosure.next_clean}")
                # next_cleaning = next_cleaning.datetime.date()
                # return jsonify(cleaning_list)

            else:
                # This means the next_clean will have something
                # therefore the next_clean in enclosure will have the next clean
                next_cleaning = enclosure.next_clean # getting the next cleaning record date
                cleaning_list.append(f"The next cleaning time for {enclosure.enclosure_id} is {next_cleaning}")
        return (cleaning_list)

    def medicalSchedule(self):
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
                medical_list.append(f"The next feed for {animal.animal_id} is {next_checkup}")
        return (medical_list)

# zoo = Zoo()
# e = Employee("Liam", "vienna")
# e2 = Employee("Liam", "vienna")
# zoo.addEmployee(e2)
# zoo.addEmployee(e)
#
# a = Animal("Bird", "Parrot",12)
# a2 = Animal("Ape", "gorilla",12)
# a3 = Animal("Ape", "gorilla",12)
# a4 = Animal("Ape", "gorilla",12)
# a5 = Animal("Ape", "gorilla",12)
# a6 = Animal("Ape", "gorilla",12)
# zoo.addAnimal(a)
# zoo.addAnimal(a2)
# zoo.addAnimal(a3)
# zoo.addAnimal(a4)
# zoo.addAnimal(a5)
# zoo.addAnimal(a6)
#
# zoo.careTaker(e.employee_id,a.animal_id)
# zoo.careTaker(e.employee_id,a2.animal_id)
# zoo.careTaker(e.employee_id,a3.animal_id)
# zoo.careTaker(e.employee_id,a4.animal_id)
# zoo.careTaker(e.employee_id,a5.animal_id)
# zoo.careTaker(e2.employee_id,a6.animal_id)
#
# enclo = Enclosure("Chill zone", 100)
# enclo2 = Enclosure("Chill zone", 100)
# enclo3 = Enclosure("Chill zone", 100)
# zoo.addEnclosure(enclo)
# zoo.addEnclosure(enclo2)
# zoo.addEnclosure(enclo3)
#
# zoo.home(a.animal_id,enclo.enclosure_id)
# zoo.home(a2.animal_id,enclo.enclosure_id)
# zoo.home(a3.animal_id,enclo.enclosure_id)
# zoo.home(a4.animal_id,enclo2.enclosure_id)
# zoo.home(a5.animal_id,enclo2.enclosure_id)
# zoo.home(a6.animal_id,enclo3.enclosure_id)
#
# zoo.animalStats()
#

# print(f"First Employee {e.employee_id}")
# print(len(e.animals))
# zoo.employeeStats()