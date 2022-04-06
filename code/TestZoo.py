import pytest
import requests
import json

from animal import Animal


@pytest.fixture
def baseURL ():
    return "http://127.0.0.1:7890"

@pytest.fixture
def tiger1 ():
    return Animal("tiger mum", "btiger1", 21)

@pytest.fixture
def tiger2 ():
    return Animal("tiger child", "btiger2", 2)

@pytest.fixture
def post_tiger1 (baseURL, tiger1):
    tiger1_data = {"species": tiger1.species_name, "name": tiger1.common_name, "age": tiger1.age}
    requests.post(baseURL + "/animal", data=tiger1_data)

class Testzoo ():


    def test_one(self, baseURL, post_tiger1):
        x = requests.get (baseURL+"/animals")
        js =  x.content
        animals = json.loads(js)
        assert (len(animals)==1)




