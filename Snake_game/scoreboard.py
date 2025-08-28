from turtle import Turtle
class Scoreboard(Turtle):
    def __init__(self):
        super().__init__()
        self.score=0
        with open("data.txt") as data:
            self.high_score =int(data.read())
        self.color("white")
        self.penup()
        self.goto(0, 270)  # to move the scoreboard to the top
        self.update_scoreboard() #to display score on screen
        self.hideturtle() #to not display the cursor turtle


    def update_scoreboard(self):
        self.clear()
        self.write(f"Score: {self.score} High Score: {self.high_score}", align="center", font=("Arial", 24, "normal")) #to display score on screen

    def reset(self):
        if self.score>self.high_score:
            self.high_score=self.score
            with open("data.txt",mode="w") as data:
                data.write(f"{self.high_score}")
        self.score=0
        self.update_scoreboard()

    #def game_over(self):
     #   self.goto(0,0) #to display game over at center
      #  self.write(f"Game Over", align="center", font=("Arial", 24, "normal"))

    def increase_score(self): #to increase the score
        self.score +=1
        #self.clear() #to clear the previous scoreboard after score has been increased
        self.update_scoreboard()

