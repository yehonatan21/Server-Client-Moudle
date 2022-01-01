from CarRace import CarRace
import time

#1 main for all the program in the App.

def main():
    # for i in range(2):
    racers_num = None
    while racers_num not in range(2,10):
        try:
            racers_num = int(input("please select number of racers btween 2-9:\n"))
        except:
            pass
    #race = CarRace(-1,-1)
    race = CarRace(racers_num)
    race.draw_board()
    time.sleep(1)
    winner = race.race()
    print(winner.color)
    print (winner.vehicle_shape)
    time.sleep(3)

def test():
    # racers_num = CarRace.racers_num()
    # racers = Factory.create_vehicles(racers_num)
    CarRace.__create_board()
    CarRace.__fill_board()
    CarRace.__draw_finish_line()
    CarRace.__draw_start_line()
    time.sleep(3)

if __name__ == "__main__": #module
    if False:
        test()
    else:
        main()  