"""
Warehouse toy example.

Scenario:
  We have a limited number os trucks and orders arrive
  to trucks with some probability. If there is a free
  truck, the order is dispatched (takes some time). 
  Otherwise, the order is queued. 

"""

import simpy
import random
import itertools

RANDOM_SEED = 42
NUM_TRUCKS = 2  # Number of trucks in the warehouse
DELIVERY_TIME = {"MEAN_ORDER_TIME": 20, "SD_ORDER_TIME": 4}  # Minutes it takes to deliver an order
ORDER_TIME = 5  # Create a new order every ~5 minutes
SIM_TIME = 60  # Simulation time in minutes


class Warehouse:
    """A warehouse has a limited number of trucks (``NUM_TRUCKS``) to
    dispatch in parallel.

    Orders have to be assigned to one of the trucks. When they got one,
    they can start the delivery processes and wait for it to finish (which
    takes ``delivery_time`` minutes).

    """

    def __init__(self, env, num_trucks, delivery_time):  # env is inherited from simpy
        self.env = env
        self.truck = simpy.Resource(env, num_trucks)
        self.delivery_time = random.gauss(
            delivery_time["MEAN_ORDER_TIME"], delivery_time["SD_ORDER_TIME"]
        )

    def deliver(self, order):
        """
        The delivery processes. It takes an ``order`` processes and tries
        to deliver it.
        """
        yield self.env.timeout(self.delivery_time)


def order(env, name, warehouse):
    """The order process (each order has a ``name``) arrives at the warehouse
    (``warehouse``) and requests a truck.

    It then starts the delivery process, waits for it to finish and
    leaves to never come back ...

    """
    print(f"{name} arrives at the warehouse at {env.now:.2f}.")
    with warehouse.truck.request() as request:
        yield request

        print(f"{name} starts to be delivered at {env.now:.2f}.")
        yield env.process(warehouse.deliver(name))

        print(f"{name} is delivered at {env.now:.2f}.")


def setup(env, num_trucks, delivery_time, t_inter):
    """Create a warehouse, a number of initial orders and keeps creating orders
    approx. every ``t_inter`` minutes."""
    # Create the warehouse
    warehouse = Warehouse(env, num_trucks, delivery_time)

    order_count = itertools.count()

    # Create orders while the simulation is running
    while True:
        yield env.timeout(
            random.expovariate(1.0 / t_inter)
        )
        env.process(order(env, f"Order {next(order_count)}", warehouse))


# Setup and start the simulation
print("Warehouse")
random.seed(RANDOM_SEED)  # This helps to reproduce the results

# Create an environment and start the setup process
env = simpy.Environment()
env.process(setup(env, NUM_TRUCKS, DELIVERY_TIME, ORDER_TIME))

# Execute!
env.run(until=SIM_TIME)

def summary_table(env):
    """
    Sum
    """
    # Processing time of each order

    # Waiting time of trucks

    # Utilization time of trucks






