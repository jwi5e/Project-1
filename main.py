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
        req = self.res[0].request()
        yield req
        print(res[0].count)


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


        req = self.res[2].request()
        yield req
        self.res[1].release(order)

        ##yield foodPrep



        req = self.res[3].request()
        yield req
        self.res[2].release(req)
        print('Start paying::', self)
        self.payTime = random.weibullvariate(2, 1.5)
        pay = self.env.timeout(self.payTime)
        yield pay
        print("Finish paying::", self)


        req = self.res[4].request()
        yield req
        self.res[3].release(req)
        print('Waiting for pickup::', self)


        req = self.res[5].request()
        yield req
        self.res[4].release(req)
        print('Start pickup::', self)
        self.pickupTime = random.weibullvariate(2, 1.5)
        pickup = self.env.timeout(self.pickupTime)
        yield pickup
        val = yield pickup & foodPrep # simpy.anyOf(evt,evt,evt)

        print("Finish pickup::", self)

        ##if pickup in val:
            ##print('food was ready waited to pay')
        ##elif foodPrep in val:
            ##print("food wasn't ready had to wait")
        ##else:
            ##print("oops")

        self.res[5].release(req)

    def __str__(self):
        return f'Car: {self.name:d} time: {self.env.now:.3f}'


def arrivalGen(env, res):

    while True:

        c = Car(env, res)
        env.process(c.drive())
        evt = env.timeout(random.expovariate(1.0/10.0))
        yield evt


env = simpy.Environment()
initialLine = simpy.Resource(env, 7)
orderWindow = simpy.Resource(env, 1)
betweenOrderAndPay = simpy.Resource(env, 4)
payWindow = simpy.Resource(env,1)
betweenPayAndPickup = simpy.Resource(env, 1)
pickupWindow = simpy.Resource(env,1)


res = [initialLine, orderWindow, betweenOrderAndPay, payWindow, betweenPayAndPickup, pickupWindow]

env.process(arrivalGen(env, res))

env.run(until=100.0)
