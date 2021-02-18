# -*- coding: utf-8 -*-

import random

import simpy


RANDOM_SEED = 1431221
NEW_CUSTOMERS = 20  # Total number of customers
INTERVAL_CUSTOMERS = 10.0  # Generate new customers roughly every x seconds


def source(env, number, interval, counter):
    """Source generates customers randomly"""
    for i in range(number):
        c = customer(env, f'Customer{i:2d}', counter, meanServiceTime=15.0)
        env.process(c)
        t = random.expovariate(1.0 / interval)
        yield env.timeout(t)


def customer(env, name, teller, meanServiceTime):
    """Customer arrives, is served and leaves."""
    arrive = env.now
    print(f'Time: {arrive:0.3f} Customer: {name:s}')

    req = teller.request()

    yield req

    wait = env.now - arrive

    print(f'Time: {env.now:0.3f} Customer: {name:s} Waited: {wait:0.3f}')

    serviceTime = random.expovariate(1.0 / meanServiceTime)

    yield env.timeout(serviceTime)

    print(f'Time: {env.now:0.3f} Customer: {name:s} leaves')

    teller.release(req)


# Setup and start the simulation
print('Simply single server queue')
random.seed(RANDOM_SEED)

env = simpy.Environment()
# Start processes and run
teller = simpy.Resource(env, capacity=1)
env.process(source(env, NEW_CUSTOMERS, INTERVAL_CUSTOMERS, teller))

env.run()