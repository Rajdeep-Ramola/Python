from turtle import  Turtle
import random
class Food(Turtle): #food class is inheriting turtle class
    def __init__(self):
        super().__init__() #for accessing methods of superclass in subclass
        self.shape("circle")
        self.penup()
        self.shapesize(0.5,0.5)
        self.color("red")
        self.speed("fastest")
        self.refresh()


    def refresh(self): #to move food to another location after snake eats it
        random_x = random.randint(-280, 280)
        random_y = random.randint(-280, 280)
        self.goto(random_x, random_y)

