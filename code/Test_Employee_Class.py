import pytest
from employee import Employee
from zoo import Zoo

@pytest.fixture
def employee1():
    return Employee("Liam", "Vienna")

@pytest.fixture
def employee2():
    return Employee("Misi", "Krems")

@pytest.fixture
def zoo1():
    return Zoo()

def test_addEmployee(zoo1,employee1):
    zoo1.addEmployee(employee1)
    assert (employee1 in zoo1.employees)
    zoo1.addEmployee(employee2)
    assert (employee2 in zoo1.employees)
    assert (len(zoo1.employees)==2)
    