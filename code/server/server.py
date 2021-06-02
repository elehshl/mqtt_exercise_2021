
import time
Car = [["1","Taxi4","0,4","free"],["2","Taxi5","0,-1","free"]]
gpsUser = "0,1"




def findnextCar(Car,gpsUser):

        for i in range(int(gpsUser.split(",")[0]), 4):
            print("i ist:"+str(i))
            for j in range((i-1), i+1):
                time.sleep(2)
                print("j ist:"+str(j))
                for c in range(0,len(Car)):
                    print("car"+str(c))
                    if Car[c][2] == gpsUser:
                        print("same")
                        return Car[c]
                    elif int(Car[c][2].split(",")[0]) == -i and int(Car[c][2].split(",")[1]) == j:
                        print("Car[c][2].split(',')[0] == -i and Car[c][2].split(',')[0] == j")
                        return Car[c]
                    elif int(Car[c][2].split(',')[0]) == i and int(Car[c][2].split(',')[0]) == j:
                        print("Car[c][2].split(',')[0] == i and Car[c][2].split(',')[0] == j")
                        return Car[c]
                    elif int(Car[c][2].split(',')[0]) == j and int(Car[c][2].split(',')[0]) == -i:
                        print("Car[c][2].split(',')[0] == j and Car[c][2].split(',')[0] == -i:")
                        return Car[c]
                    elif int(Car[c][2].split(',')[0]) == j and int(Car[c][2].split(',')[0]) == i:
                        print("Car[c][2].split(',')[0] == j and Car[c][2].split(',')[0] == i:")
                        return Car[c]
