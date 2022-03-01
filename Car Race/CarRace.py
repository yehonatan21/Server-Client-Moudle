import turtle
import random
import sys 
# from Factory import Factory

#create interface called "iborad" including the metonds create_board, create_racers, race
#to learn module
#app structure in python - https://realpython.com/python-application-layouts/ - Application with Internal Packages
#turn CarRace and Factory to an instance

sys.path.append('/Users/macbook/Desktop/Python Projects/Cars/Server') #FIXME: Change this to be more portable

class CarRace():

    def __init__(self, racers_num, width=500, height=500):
        self.__width = width or 500
        self.__height = height or 500
        self.__racers = []
        self.__vehicles = []
        self.__vehicles = Factory.create_vehicles(racers_num)
        
    def draw_board(self):
        self.__create_board()
        self.__fill_board()
        self.__draw_start_line()
        self.__draw_finish_line()
        self.__init_racers(self.__vehicles)  

    def __create_board(self):
        screen = turtle.Screen()
        screen.setup(self.__width, self.__height)
        screen.bgcolor("lightsteelblue")
        screen.title("The Coolest Game!")
        
    def __fill_board(self):
        draw = turtle.Turtle()
        draw.color("chocolate")
        draw.penup()
        draw.goto(((-(self.__width//2))+20,-(self.__height//2-10)))
        draw.pendown()
        draw.begin_fill()
        for i in range(2):
            draw.forward(self.__width-20)
            draw.left(90)
            draw.forward(self.__height-30)
            draw.left(90)
        draw.end_fill()
        draw.color("lightsteelblue")

    def __draw_start_line(self):
        draw = turtle.Turtle()
        draw.penup()
        draw.goto((-self.__width//2+20) ,-self.__height//2 + 12)
        draw.pendown()
        draw.forward(self.__width-10)
        draw.color("lightsteelblue")

    def __draw_finish_line(self):
        fin = turtle.Turtle()
        gap_size = 20
        fin.shape("square")
        fin.penup()
        gap_space = ((self.__width-20)//40)

        fin.color("white")
        adding = 0
        if (((self.__width-20)%40)>0):
            adding = 1
        for i in range(gap_space+adding):
            fin.goto((-(self.__width//2))+30 + (i *gap_size*2),self.__height//2-20)
            fin.stamp()

        fin.color("black")
        for i in range(gap_space):
            fin.goto((-(self.__width//2))+30 + gap_size+(i * gap_size * 2),self.__height//2-20)
            fin.stamp()
        
        fin.color("black")
        for i in range(gap_space+adding):
            fin.goto((-(self.__width//2))+30 + (i *gap_size*2),self.__height//2-40)
            fin.stamp()

        fin.color("white")
        for i in range(gap_space):
            fin.goto((-(self.__width//2))+30 + gap_size+(i * gap_size * 2),self.__height//2-40)
            fin.stamp()

    def __init_racers(self,new_vehicles):
        spacing = self.__width//(len(new_vehicles)+1)
        i = 0
        for i in range(len(new_vehicles)):
            racer = turtle.Turtle()
            racer.shape(new_vehicles[i].vehicle_shape)
            racer.color(new_vehicles[i].color)
            racer.speed = random.randrange(1, 20)# take the vehicle speed insted the random function. distans function.
            racer.left(90)
            racer.penup()
            i=i+1
            racer.setpos((-self.__width//2) + spacing * i ,-self.__height//2 + 20)
            racer.pendown()
            self.__racers.append(racer)

    def race(self):  
        while True:
            for racer in self.__racers:
                racer.forward(racer.speed)

                if racer.ycor() >= self.__height // 2 - 60:
                    for i in range(144):
                        racer.right(5)
                        racer.shapesize(2)

                    for vehicle in self.__vehicles:
                        if racer._fillcolor == vehicle.color:
                            return vehicle
