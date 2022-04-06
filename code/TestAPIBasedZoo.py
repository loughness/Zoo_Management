import pytest
import requests
import json

@pytest.fixture
def baseURL ():
    return "http://127.0.0.1:7890/"

@pytest.fixture
def zooWithOneAnimal(baseURL):
    requests.post (baseURL+"/animal", {"species":"tiger", "name":"btiger", "age":3})
    response = requests.get(baseURL + "/animals")

    return response.content

def test_zoo1 (zooWithOneAnimal):
    jo = json.loads(zooWithOneAnimal)

    print (jo)

    assert jo[0]["common_name"] =="btiger"
    assert (len(jo) == 1)

