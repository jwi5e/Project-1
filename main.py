''' This code was written and tested by Jamee Wise and Nicholas Gross.'''

import random
import simpy
import matplotlib.pyplot as plt

AR = [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0,
      10.0, 11.0, 12.0, 13.0, 14.0, 15.0, 16.0,
      17.0, 18.0, 19.0, 20.0]    # Rates for cars to be generated
SERVED = 0
BALK = 0
SERVICE_TIME = 0
ORDER_WINDOWS = 1   # Number of order windows
SIM_NUM = 10        # Number of times to run the simulation
SERVED_DATA = []    # Number of people served per run
BALK_DATA = []      # Number of people who left per run
TIME_DATA = []      # Average service time per run

class Car:

    carNumber = 0

    def __init__(self, env, res):
        self.env = env
        self.res = res
        Car.carNumber += 1
        self.name = Car.carNumber

    def drive(self):
        self.arrivalTime = self.env.now
        print('Arrival::', self)
        req = self.res[0].request()
        yield req
        if (res[0].count == 7):
            roll = random.randint(0, 100)
            if (roll >= 80):
                self.res[0].release(req)
                print("homie dipped::", self)
                global BALK
                BALK += 1
                return


        order = self.res[1].request()
        yield order
        self.res[0].release(req)
        print('Start ordering::', self)
        self.orderTime = random.weibullvariate(3, 1.5)
        evt = self.env.timeout(self.orderTime)
        yield evt
        print("Finish ordering::", self)
        self.foodPrepTime = random.weibullvariate(6, 2.0)
        foodPrep = self.env.timeout(self.foodPrepTime)


        req2 = self.res[2].request()
        yield req2
        self.res[1].release(order)


        req3 = self.res[3].request()
        yield req3
        self.res[2].release(req2)
        print('Start paying::', self)
        self.payTime = random.weibullvariate(2, 1.5)
        pay = self.env.timeout(self.payTime)
        yield pay
        print("Finish paying::", self)


        req4 = self.res[4].request()
        yield req4
        self.res[3].release(req3)
        print('Waiting for pickup::', self)


        req5 = self.res[5].request()
        yield req5
        self.res[4].release(req4)
        print('Start pickup::', self)
        self.pickupTime = random.weibullvariate(2, 1.5)
        pickup = self.env.timeout(self.pickupTime)
        val = yield pickup & foodPrep # simpy.anyOf(evt,evt,evt)

        print("Finish pickup::", self)
        
        if pickup in val:
            print('food was ready waited to pay')
        elif foodPrep in val:
            print("food wasn't ready had to wait")
        else:
            print("oops")
        
        global SERVED
        SERVED += 1
        
        endTime = self.env.now
        global SERVICE_TIME
        SERVICE_TIME += endTime - self.arrivalTime
        
        self.res[5].release(req5)

    def __str__(self):
        return f'Car: {self.name:d} time: {self.env.now:.3f}'

def arrivalGen(env, res, AR):

    while True:

        c = Car(env, res)
        env.process(c.drive())
        evt = env.timeout(random.expovariate(1.0/AR))
        yield evt

for x in AR:
    for i in range(SIM_NUM):
        env = simpy.Environment()
        
        initialLine = simpy.Resource(env, 7)
        orderWindow = simpy.Resource(env, ORDER_WINDOWS)
        betweenOrderAndPay = simpy.Resource(env, 4)
        payWindow = simpy.Resource(env,1)
        betweenPayAndPickup = simpy.Resource(env, 1)
        pickupWindow = simpy.Resource(env,1)

        res = [initialLine, orderWindow, betweenOrderAndPay, payWindow, betweenPayAndPickup, pickupWindow]

        env.process(arrivalGen(env, res, x))

        env.run(until=120.0)

    SERVED_DATA.append(SERVED/SIM_NUM)
    BALK_DATA.append(BALK/SIM_NUM)
    TIME_DATA.append(SERVICE_TIME/SERVED)
    SERVED = 0
    BALK = 0
    SERVICE_TIME = 0

print('SERVED_DATA::', SERVED_DATA)
print('BALK_DATA::', BALK_DATA)
print('TIME_DATA::', TIME_DATA)

plt.plot(AR, SERVED_DATA, label = "Scenario 1")
plt.title('People Served/Arrival rate')
plt.xlabel('Arrival Rate')
plt.ylabel('People Served')
plt.show()

plt.plot(AR, BALK_DATA, label = "Scenario 1")
plt.title('People Balked/Arrival rate')
plt.xlabel('Arrival Rate')
plt.ylabel('People Balked')
plt.show()

plt.plot(AR, TIME_DATA, label = "Scenario 1")
plt.title('Average Service Time/Arrival rate')
plt.xlabel('Arrival Rate')
plt.ylabel('Average Service Time')
plt.show()
    

