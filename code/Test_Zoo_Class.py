import pytest
from employee import Employee
from enclosure import Enclosure
from animal import Animal
from zoo import Zoo

@pytest.fixture
def zoo1 ():
    return Zoo()

@pytest.fixture
def animal1():
    return Animal("Ape","Gorilla", 12)

@pytest.fixture
def animal2():
    return Animal("Ape", "Monkey", 23)

@pytest.fixture
def animal3():
    return Animal("Bird", "Parrot", 2)

@pytest.fixture
def animal4():
    return Animal("Bird","Parrot", 5)

@pytest.fixture
def animal5():
    return Animal("Rodent","Rat", 3)

@pytest.fixture
def employee1():
    return Employee("Liam", "Vienna")

@pytest.fixture
def employee2():
    return Employee("Misi", "Krems")

@pytest.fixture
def enclosure1():
    return Enclosure("Monkey Zone", 100)

@pytest.fixture
def enclosure2():
    return Enclosure("Flight Zone", 300)

# _______________________________________________________
#               Animal Testing
# -------------------------------------------------------
@pytest.fixture
def adding_removing_home_birth_feed_vet_ANIMALS(zoo1,animal1,animal2,employee1,employee2,enclosure1,enclosure2):
    zoo1.addAnimal(animal1)
    zoo1.addAnimal(animal2)
    # 2 animals
    zoo1.removeAnimal(animal2)
    # 1 animal
    zoo1.addEnclosure(enclosure1)
    zoo1.addEnclosure(enclosure2)
    # 2 enclosures
    zoo1.home(animal1.animal_id,enclosure1.enclosure_id)
    zoo1.birth((animal1.animal_id))
    # 2 animals
    animal1.feed()
    animal1.vet()
    zoo1.animalStats()

def test_animal(adding_removing_home_birth_feed_vet_ANIMALS,zoo1, animal1,animal2):
    assert (len(zoo1.animals)==2)
    assert (len(zoo1.enclosures)==2)
    assert (len(animal1.vet_record)==1)
    assert (len(animal1.vet_record)==1)

def test_animal_stats(zoo1,animal1,animal2,animal3,animal4,animal5,employee1,employee2,enclosure1,enclosure2):
    zoo1.addAnimal(animal1)
    zoo1.addAnimal(animal2)
    zoo1.addAnimal(animal3)
    zoo1.addAnimal(animal4)
    zoo1.addAnimal(animal5)
    zoo1.addEnclosure(enclosure1)
    zoo1.addEnclosure(enclosure2)
    zoo1.home(animal1.animal_id,enclosure1.enclosure_id)
    zoo1.home(animal5.animal_id,enclosure1.enclosure_id)
    # enclosure 1 now has 2 diff species
    zoo1.home(animal3.animal_id,enclosure2.enclosure_id)
    zoo1.home(animal4.animal_id,enclosure2.enclosure_id)
    # enclosure 2 only has 1 species
    zoo1.home(animal2.animal_id,enclosure2.enclosure_id)
    #enclosure 2 now has 2 diff species - 3 animals
    zoo1.animalStats()
    assert zoo1.enclo_with_diff_species == 2
    assert zoo1.ave_num_of_animals_per_enclosure == 2.5
    assert zoo1.num_ani_per_species["Ape"] == 2
    assert zoo1.num_ani_per_species["Rodent"] == 1

# _______________________________________________________
#               Enclosure Testing
# -------------------------------------------------------
@pytest.fixture
def add_remove_leave_clean_ENCLOSURE(zoo1,animal1,animal2,employee1,employee2,enclosure1,enclosure2):
    zoo1.addAnimal(animal1)
    zoo1.addAnimal(animal2)
    # 2 animals
    zoo1.addEnclosure(enclosure1)
    zoo1.addEnclosure(enclosure2)
    # 2 enclosures
    zoo1.home(animal1.animal_id,enclosure1.enclosure_id)
    zoo1.home(animal2.animal_id,enclosure2.enclosure_id)
    # 1 animal in each enclosure
    zoo1.leaveEnclosure(animal1.animal_id,enclosure1.enclosure_id)
    # 0 animals in enclosure 1
    zoo1.removeEnclosure(enclosure2.enclosure_id)
    # deleted enclosure2
    # only one enclosure left -> enclosure1
    # with 2 animals now
    zoo1.birth(animal2.animal_id)
    # 3 animals
    # 2 animals in enclosure 1

def test_enclosure(add_remove_leave_clean_ENCLOSURE,zoo1,animal1,animal2,employee1,employee2,enclosure1,enclosure2):
    assert (len(zoo1.animals)==3)
    assert (len(zoo1.enclosures)==1)
    assert (enclosure1 in zoo1.enclosures)
    assert (enclosure2 not in zoo1.enclosures)
    assert (len(enclosure1.animals)==2)

# _______________________________________________________
#               Employee Testing
# -------------------------------------------------------

@pytest.fixture
def add_remove_careTake_EMPLOYEE(zoo1,animal1,animal2,employee1,employee2,enclosure1,enclosure2):
    zoo1.addAnimal(animal1)
    zoo1.addAnimal(animal2)
    # 2 animals
    zoo1.addEmployee(employee1)
    zoo1.addEmployee(employee2)
    # 2 employees
    zoo1.careTaker(employee1.employee_id,animal1.animal_id)
    zoo1.careTaker(employee1.employee_id,animal2.animal_id)
    # employee 1 now looks after 2 animals
    zoo1.deleteEmployee(employee1.employee_id)
    # 1 employee
    # employee 2 now looks after 2 animals
    zoo1.employeeStats()


def test_employee(add_remove_careTake_EMPLOYEE,zoo1,animal1,animal2,employee1,employee2,enclosure1,enclosure2):
    assert (len(zoo1.employees)==1)
    assert (len(zoo1.animals)==2)
    assert (len(employee2.animals)==2)

def test_employee_stats(add_remove_careTake_EMPLOYEE,zoo1,animal1,animal2,employee1,employee2,enclosure1,enclosure2):
   assert zoo1.emp_min_animals == 2
   assert zoo1.emp_max_animals == 2
   assert zoo1.ave_animals == 2









