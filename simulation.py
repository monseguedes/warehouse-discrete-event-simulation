"""
Warehouse example.

Scenario:
  Orders arrive to a warehouse with several sections with a number of employees. 
  Each order needs products from a subset of the sections. Once the order is ready,
  it moves to the delivery section. There, if there is a free truck, the order is
  dispatched. Otherwise, the order is queued.

"""

import simpy
import random
import itertools

RANDOM_SEED = 42
NUM_TRUCKS = 2  # Number of trucks in the warehouse
NUM_EMPLOYEES = 1  # Number of employees in each section
NUM_SECTORS = 3  # Number of sections in the warehouse
DELIVERY_TIME = {
    "MEAN_ORDER_TIME": 20,
    "SD_ORDER_TIME": 0,
}  # Minutes it takes to deliver an order
PROCESSING_TIME = {
    "MEAN_ORDER_TIME": 10,
    "SD_ORDER_TIME": 2,
}  # Minutes it takes to prepare an order
ORDER_TIME = 5  # Create a new order every ~5 minutes
SIM_TIME = 30  # Simulation time in minutes


class Sector:
    """
    A sector has a limited number of employees (``num_employees``) to
    work in parallel. Orders have to be assigned to one of the employees. 
    When they got one, they can start the preparation processes (which takes 
    ``preparation_time``minutes).
    """

    def __init__(
        self, env, name, num_employees, preparation_time
    ):  # env is inherited from simpy
        self.env = env
        self.name = name
        self.employee = simpy.Resource(env, num_employees)
        self.preparation_time = random.gauss(
            preparation_time["MEAN_ORDER_TIME"], preparation_time["SD_ORDER_TIME"]
        )

    def handling(self):
        """
        The handling processes.
        """

        yield self.env.timeout(self.preparation_time)

class Warehouse:
    """
    A warehouse has a limited number of sectors (``num_sectors``) to
    dispatch in parallel.
    """

    def __init__(self, env, num_sectors):
        self.env = env
        self.num_sectors = num_sectors
        self.sectors = [Sector(env, i, NUM_EMPLOYEES, PROCESSING_TIME) for i in range(num_sectors)]

    def handle_order(self, order_id, sector_ids):
        sectors = []
        for sec_id in sector_ids:
            sectors.append(self.env.process(self.process_in_sector(order_id, self.sectors[sec_id])))
        
        yield simpy.events.AllOf(env, sectors)

    def process_in_sector(self, order_id, sector):
        with sector.employee.request() as request:
            print(f"{order_id} arrives at {env.now:.2f} at the queue of sector {sector.name}.")
            yield request
            print(f"There is an employee available in sector {sector.name} at {self.env.now:.2f} to do {order_id}.")
            yield self.env.process(sector.handling())
            print(f"{order_id} is processed in sector {sector.name} at {self.env.now:.2f}.")


class DeliveryArea:
    """
    A delivery area has a limited number of trucks (``NUM_TRUCKS``) to
    dispatch in parallel. Orders have to be assigned to one of the trucks. 
    When they got one, they can start the delivery processes (which takes 
    ``delivery_time``minutes).
    """

    def __init__(self, env, num_trucks, delivery_time):  # env is inherited from simpy
        self.env = env
        self.truck = simpy.Resource(env, num_trucks)
        self.delivery_time = random.gauss(
            delivery_time["MEAN_ORDER_TIME"], delivery_time["SD_ORDER_TIME"]
        )

    def deliver(self, order):
        """
        The delivey processes. 
        """

        yield self.env.timeout(self.delivery_time)
        print(f"{order} delivered at {self.env.now:.2f}")


def deliver(env, name, delivery_area):
    """
    The delivery process. An order arrives at the delivery area
    and requests a truck.

    It then starts the delivery process, waits for it to finish and
    leaves to never come back ...

    """

    with delivery_area.truck.request() as request:
        yield request

        print(f"{name} starts to be delivered at {env.now:.2f}.")
        yield env.process(delivery_area.deliver(name))
        print(f"{name} is delivered at {env.now:.2f}.")


def prepare_order(env, name, warehouse):
    """
    The order process. A new order for each section is created for
    a specific order.

    """

    indices_sectors = random.sample(range(NUM_SECTORS), random.randint(1, NUM_SECTORS))
    print(f"{name} needs products from sectors {indices_sectors}.")
    yield env.process(warehouse.handle_order(name, indices_sectors))


def order_journey(
    env, name, warehouse, delivery_area
):
    """
    Main setup process. Orders are created

    """

    # Prepare order, and only after it is prepared, deliver it
    yield env.process(prepare_order(env, name, warehouse))
    print(f"{name} is processed and ready to be delivered at {env.now:.2f}.")
    yield env.process(deliver(env, name, delivery_area))

    order_data = {}

    return order_data 


def main_setup(
    env, num_employees, preparation_time, num_trucks, delivery_time, t_inter
):
    """
    Main setup process. Orders are created

    """

    order_count = itertools.count()

    # Create the warehouse
    warehouse = Warehouse(env, NUM_SECTORS)

    # Create the delivery area
    delivery_area = DeliveryArea(env, num_trucks, delivery_time)

    data = {}

    while True:
        arrival_time = random.expovariate(1.0 / t_inter)
        yield env.timeout(arrival_time)
        name = f"Order {next(order_count)}"
        order_data = env.process(
            order_journey(
                env,
                name,
                warehouse,
                delivery_area,
            )
        )
        data[name] = order_data

    


# Setup and start the simulation
print("Warehouse")
random.seed(RANDOM_SEED)  # This helps to reproduce the results

# Create an environment and start the setup process
env = simpy.Environment()
env.process(
    main_setup(
        env, NUM_EMPLOYEES, PROCESSING_TIME, NUM_TRUCKS, DELIVERY_TIME, ORDER_TIME
    )
)

# Execute!
env.run(until=SIM_TIME)
