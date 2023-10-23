from flask import Flask, render_template, request
import sqlite3

class Person:
    amountofpeople = 0
    def __init__(self, name="", description="", age=0, major="", GPA=0.0, gradYear=0, fsuID=""):
        self.__name = name
        self.__description = description
        self.__age = age
        self.__major = major
        self.__GPA = GPA
        self.__gradYear = gradYear
        self.__fsuID = fsuID
        Person.amountofpeople += 1

    #GETTERS
    def getName(self):
        return self.__name
    
    def getDescription(self):
        return self.__description
    
    def getAge(self):
        return self.__age
    
    def getMajor(self):
        return self.__major

    def getGPA(self):
        return self.__GPA
    
    def getGradYear(self):
        return self.__gradYear
    
    def getID(self):
        return self.__fsuID
    
    #SETTERS
    def setName(self, name):
        self.__name = name
    
    def setDescription(self, desc):
        self.__description = desc
    
    def setAge(self, age):
        self.__age = age
    
    def setMajor(self, major):
        self.__major = major

    def setGPA(self, GPA):
        self.__GPA = GPA
    
    def setGradYear(self, year):
        self.__gradYear = year
    
    def setID(self, ID):
        self.__fsuID = ID

    @staticmethod
    def getAmountOfPeople():
        return Person.amountofpeople

    def getPersonByFSUId(self, id):
        conn = sqlite3.connect('database.db')
        with sqlite3.connect('database.db') as con:
                cur = con.cursor("SELECT * FROM users WHERE id = ?", ())




#child classes of Person (app tiers)
class Bronze(Person):
    def __init__(self):
        super().__init__()
      
    def getTier(self):
        return "Bronze"


class Silver(Person):
    def __init__(self):
        super().__init__()
      
    def getTier(self):
        return "Silver"  
    
    
class Gold(Person):
    def __init__(self):
        super().__init__()
      
    def getTier(self):
        return "Gold" 
