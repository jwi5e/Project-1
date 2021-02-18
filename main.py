import random
import simpy

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
        req =  self.res[0].request()
        yield req
        print('Start ordering::', self)
        self.orderTime = random.expovariate(1.0/12.0)
        evt = self.env.timeout(self.orderTime)
        yield evt
        print("Finish ordering::", self)

        self.foodPrepTime = 3.0 #random.expovariate(1.0/5.0)
        foodPrep = self.env.timeout(self.foodPrepTime)

        self.res[0].release(req)

        print('Waiting for pickup::', self)

        req =  self.res[2].request()
        yield req

        print('Start pickup::', self)
        self.pickupTime = 2.0 #random.expovariate(1.0/3.0)
        pickup = self.env.timeout(self.pickupTime)

        val = yield pickup & foodPrep  # simpy.anyOf(evt,evt,evt)

        print("Finish pickup::", self)

        if pickup in val:
            print('food was ready waited to pay')
        elif foodPrep in val:
            print("food wasn't ready had to wait")
        else:
            print("oops")

        self.res[2].release(req)


    def __str__(self):
        return f'Car: {self.name:d} time: {self.env.now:.3f}'

def arrivalGen(env, res):

    while True:

        c = Car(env, res)
        env.process(c.drive())
        evt = env.timeout(random.expovariate(1.0/10.0))
        yield evt


env = simpy.Environment()
orderWindow = simpy.Resource(env, 1)
payWindow = simpy.Resource(env,1)
pickupWindow = simpy.Resource(env,1)

res = [orderWindow, payWindow, pickupWindow]

env.process(arrivalGen(env, res))

env.run(until = 100.0)