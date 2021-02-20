import random
import simpy
import matplotlib


class Car:
    carNumber = 0


    def __init__(self, env, res):
        self.env = env
        self.res = res
        Car.carNumber += 1
        self.name = Car.carNumber


    def drive(self, SERVED, LEFT, SERVICETIME, RUNS):
        RUNS.append("1")
        self.arrivalTime = self.env.now
        print('Arrival::', self)
        req = self.res[0].request()
        yield req
        if (res[0].count == 7):
            roll = random.randint(0, 100)
            if (roll >= 80):
                self.res[0].release(req)
                print("homie dipped::", self)
                LEFT.append("1")
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

        ##yield foodPrep



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
        ###yield pickup
        val = yield pickup & foodPrep # simpy.anyOf(evt,evt,evt)

        print("Finish pickup::", self)
        self.leaveTime = self.env.now

        if pickup in val:
            print('food was ready waited to pay')
        elif foodPrep in val:
            print("food wasn't ready had to wait")
        else:
            print("oops")

        SERVICETIME.append(self.leaveTime - self.arrivalTime)
        self.res[5].release(req5)
        SERVED.append("1")

        print(SERVED, LEFT, SERVICETIME, RUNS)

    def __str__(self):
        return f'Car: {self.name:d} time: {self.env.now:.3f}'


def arrivalGen(env, res, SERVED, LEFT, SERVICETIME, RUNS):

    while True:

        c = Car(env, res)
        env.process(c.drive(SERVED, LEFT, SERVICETIME, RUNS))
        evt = env.timeout(random.expovariate(1.0/10.0))
        yield evt


env = simpy.Environment()
initialLine = simpy.Resource(env, 7)
orderWindow = simpy.Resource(env, 2)
betweenOrderAndPay = simpy.Resource(env, 4)
payWindow = simpy.Resource(env,1)
betweenPayAndPickup = simpy.Resource(env, 1)
pickupWindow = simpy.Resource(env,1)

SERVED = []
LEFT = []
SERVICETIME = []
RUNS = []

res = [initialLine, orderWindow, betweenOrderAndPay, payWindow, betweenPayAndPickup, pickupWindow]
env.process(arrivalGen(env, res, SERVED, LEFT, SERVICETIME, RUNS))


env.run(until=120.0)

