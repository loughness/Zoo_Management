import pytest

from animal import Animal
from zoo import Zoo


@pytest.fixture
def tiger1 ():
    return Animal ("tiger", "ti", 12)

@pytest.fixture
def tiger2 ():
    return Animal ("tiger2", "ti", 2)

@pytest.fixture
def zoo1 ():
    return Zoo ()

def test_addingAnimal(zoo1, tiger1):
    zoo1.addAnimal(tiger1)
    assert (tiger1 in zoo1.animals)
    zoo1.addAnimal(tiger2)
    assert (len(zoo1.animals)==2)

def test_feedingAnimal(zoo1, tiger1):
    zoo1.addAnimal(tiger1)
    assert (tiger1 in zoo1.animals)
    tiger1.feed()
    assert (len(tiger1.feeding_record)==1)
    tiger1.feed()
    assert (len(tiger1.feeding_record)==1)
    assert (tiger1.next_feed != None)

def test_vettingAnimal(tiger1,tiger2):
    tiger2.vet()
    assert (len(tiger2.vet_record)==1)
    assert (tiger2.next_check_up != None)
    tiger1.vet()
    assert (len(tiger1.vet_record) == 1)
    assert (tiger1.next_check_up != None)
    tiger1.vet()
    assert (len(tiger1.vet_record) == 1)
    assert (tiger1.next_check_up != None)

