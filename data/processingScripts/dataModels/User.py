import json

class User:
    def __init__(self, userId, name, city, street):
        self.userId = userId
        self.name = name
        self.city = city
        self.street = street

    def print(self):
        print('userId: '+str(self.userId) +'\n'+
              'name:   '+self.name +'\n'+
              'city:   '+self.city +'\n'+
              'street: '+self.street +'\n')