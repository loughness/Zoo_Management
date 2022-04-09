from flask import Flask, jsonify
from flask_restx import Api, reqparse, Resource
from zoo_json_utils import ZooJsonEncoder 
from zoo import Zoo

from animal import Animal
from enclosure import Enclosure
from employee import Employee

my_zoo = Zoo()

zooma_app = Flask(__name__)
# need to extend this class for custom objects, so that they can be jsonified
zooma_app.json_encoder = ZooJsonEncoder 
zooma_api = Api(zooma_app)

# ---------------------------------------------------------------
# for ANIMALS
animal_parser = reqparse.RequestParser()
animal_parser.add_argument('species', type=str, required=True, help='The scientific name of the animal, e,g. Panthera tigris')
animal_parser.add_argument('name', type=str, required=True, help='The common name of the animal, e.g., Tiger')
animal_parser.add_argument('age', type=int, required=True, help='The age of the animal, e.g., 12')
@zooma_api.route('/animal')
class AddAnimalAPI(Resource):
    @zooma_api.doc(parser=animal_parser)
    def post(self):
        # get the post parameters 
        args = animal_parser.parse_args()
        name = args['name']
        species = args['species']
        age = args['age']
        # create a new animal object 
        new_animal = Animal(species, name, age)
        #add the animal to the zoo
        my_zoo.addAnimal(new_animal)
        return jsonify(new_animal) 

@zooma_api.route('/animal/<animal_id>')
class Animal_ID(Resource):
     def get(self, animal_id):
        search_result = my_zoo.getAnimal(animal_id)
        return jsonify(search_result) # this is automatically jsonified by flask-restx
    
     def delete(self, animal_id):
        targeted_animal = my_zoo.getAnimal(animal_id)
        if not targeted_animal: 
            return jsonify("Animal with ID {animal_id} was not found")
        my_zoo.removeAnimal(targeted_animal)
        return jsonify("Animal with ID {animal_id} was removed") 

@zooma_api.route('/animals')
class AllAnimals(Resource):
     def get(self):
        return jsonify( my_zoo.animals)  

@zooma_api.route('/animals/<animal_id>/feed')
class FeedAnimal(Resource):
     def post(self, animal_id):
        targeted_animal  = my_zoo.getAnimal(animal_id)
        if not targeted_animal: 
            return jsonify(f"Animal with ID {animal_id} was not found")
        return targeted_animal.feed()

@zooma_api.route('/animal/<animal_id>/vet')
class VetCheckUp(Resource):
    def post(self, animal_id):
        target_animal = my_zoo.getAnimal(animal_id)
        if not target_animal:
            return jsonify(f"Animal with ID {animal_id} was not found")
        return target_animal.vet()

home_parser = reqparse.RequestParser()
home_parser.add_argument('enclosure_id', type=str, required=True, help='enclosure_id')
@zooma_api.route('/animal/<animal_id>/home')
class AnimalHome(Resource):
    @zooma_api.doc(parser=home_parser)
    def post(self, animal_id):
        args = home_parser.parse_args()
        enclosure_id = args['enclosure_id']
        target_enclousre = my_zoo.getEnclosure(enclosure_id)
        if not target_enclousre:
            return jsonify(f"Enclosure {enclosure_id} doesn't exist")
        return my_zoo.home(animal_id, enclosure_id)

mother_parser = reqparse.RequestParser()
mother_parser.add_argument('mother_id', type=str, required=True)
@zooma_api.route('/animal/birth')
class Birth(Resource):
    @zooma_api.doc(parser=mother_parser)
    def post(self):
        args = mother_parser.parse_args()
        mother_id = args['mother_id']
        return my_zoo.birth(mother_id)

death_parser = reqparse.RequestParser()
death_parser.add_argument('animal_id', type=str, required=True, help='The animal that died')
@zooma_api.route('/animal/death')
class Death(Resource):
    @zooma_api.doc(parser=death_parser)
    def post(self):
        args = death_parser.parse_args()
        animal_id = args['animal_id']
        return my_zoo.death(animal_id)

@zooma_api.route('/animal/stat')
class AnimalStats(Resource):
    def get(self):
        return my_zoo.animalStats()

# ---------------------------------------------------------------
# for ENCLOSURES
enclosure_parser = reqparse.RequestParser()
enclosure_parser.add_argument('name', type=str, required=True, help='The name of the enclosure.')
enclosure_parser.add_argument('area', type=int, required=True, help='The area (size) of the enclosure in m^2.')
@zooma_api.route('/enclosure')
class AddEnclosure(Resource):
    @zooma_api.doc(parser=enclosure_parser)
    def post(self):
        # get the post parameters
        args = enclosure_parser.parse_args()
        name = args['name']
        area = args['area']
        # create a new enclosure object
        new_enclosure = Enclosure(name, area)
        # add the enclosure to the zoo
        my_zoo.addEnclosure(new_enclosure)
        return jsonify(new_enclosure)

@zooma_api.route('/enclosures')
class GetEnclosures(Resource):
    def get(self):
        return jsonify(my_zoo.enclosures)

@zooma_api.route('/enclosures/<enclosure_id>/clean')
class CleanEnclosure(Resource):
    def post(self,enclosure_id):
        return my_zoo.clean(enclosure_id)

@zooma_api.route('/enclosures/<enclosure_id>/animals')
class GetEnclosureAnimals(Resource):
    def get(self, enclosure_id):
        enclosure = my_zoo.getEnclosure(enclosure_id)
        if not enclosure:
            return jsonify(f"Enclosure with ID {enclosure_id} was not found")
        animals = enclosure.animals
        animal_list = []
        for animal in animals:
            animal_list.append(my_zoo.getAnimal(animal))
        return jsonify(animal_list)

@zooma_api.route('/enclosure/<enclosure_id>')
class deleteEnclosure(Resource):
    def delete(self,enclosure_id):
        enclosure = my_zoo.getEnclosure(enclosure_id)
        if not enclosure:
            return jsonify(f"Enclosure with ID {enclosure_id} was not found")
        if len(my_zoo.enclosures) == 1:
            return jsonify("There is only one enclosure, the animals will not have anywhere to live if you get rid of this one")
        if enclosure.animals == []:
            my_zoo.removeEnclosure(enclosure_id)
            return jsonify("Enclosure was removed")

# ---------------------------------------------------------------
# for EMPLOYEES
employee_parser = reqparse.RequestParser()
employee_parser.add_argument('name', type=str, required=True)
employee_parser.add_argument('address', type=str, required=True)
@zooma_api.route('/employee')
class AddEmployee(Resource):
    @zooma_api.doc(parser=employee_parser)
    def post(self):
        args = employee_parser.parse_args()
        name = args['name']
        address = args['address']
        new_employee = Employee(name,address)
        my_zoo.addEmployee(new_employee)
        return jsonify(new_employee)

@zooma_api.route('/employees')
class GetEmployees(Resource):
    def get(self):
        return jsonify(my_zoo.employees)

@zooma_api.route('/employee/<employee_id>/care/<animal_id>/')
class CareTaker(Resource):
    def post(self, employee_id, animal_id):
        employee = my_zoo.getEmployee(employee_id)
        animal = my_zoo.getAnimal(animal_id)
        if not employee and not animal:
            return jsonify(f"Animal with ID: '{animal_id}', and Employee with ID: '{employee_id}' were not found!")
        elif not animal:
            return jsonify(f"Animal with ID: '{animal_id}' was not found!")
        elif not employee:
            return jsonify(f"Employee with ID: '{employee_id}' was not found!")
        return my_zoo.careTaker(employee_id,animal_id)

@zooma_api.route('/employee/<employee_id>/care/animals')
class EmployeeAnimals(Resource):
    def get(self,employee_id):
        employee = my_zoo.getEmployee(employee_id)
        animal_list = []
        for animal in employee.animals:
            ani = my_zoo.getAnimal(animal)
            animal_list.append(ani)
        return jsonify(animal_list)

@zooma_api.route('/employee/<employee_id>')
class DeleteEmployee(Resource):
    def delete(self,employee_id):
        employee = my_zoo.getEmployee(employee_id)
        if not employee:
            return jsonify(f"That employee {employee_id} was not found")
        return my_zoo.deleteEmployee(employee_id)

@zooma_api.route('/employee/stats')
class EmployeeStats(Resource):
    def get(self):
        return my_zoo.employeeStats()

# ---------------------------------------------------------------
# for TASKS
@zooma_api.route('/tasks/cleaning/')
class CleaningSchedule(Resource):
    def get(self):
        return my_zoo.cleaningSchedule()
@zooma_api.route('/tasks/medical/')
class MedicalSchedule(Resource):
    def get(self):
        return my_zoo.medicalSchedule()

@zooma_api.route('/tasks/feeding')
class FeedingSchedule(Resource):
    def get(self):
        return my_zoo.feedingSchedule()


if __name__ == '__main__':
    zooma_app.run(debug = False, port = 7890)