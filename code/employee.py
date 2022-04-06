import uuid

class Employee:
    def __init__(self, name, address):
        self.name = name
        self.address = address
        self.employee_id = str(uuid.uuid4())
        self.animals = [] # animal ID!
