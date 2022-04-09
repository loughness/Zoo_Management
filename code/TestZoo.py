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
    # requests.post(baseURL + "/animal", data=tiger1_data)
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    requests.post(baseURL + "/animal", data=json.dumps(tiger1_data), headers=headers)

class Testzoo ():
    def test_one(self, baseURL, post_tiger1):
        x = requests.get (baseURL+"/animals")
        js = x.content
        animals = json.loads(js)
        assert (len(animals)==1)



# url = "http://127.0.0.1:7890/animal"
# data={"name":"asd","species":"asd","age":12}
# headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
# r = requests.post(url, data=json.dumps(data), headers=headers)
#
# print(r.content)
