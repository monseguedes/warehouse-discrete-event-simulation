import numpy as np
from simpy_helpers import Entity, Resource, Source, Stats
import matplotlib.pyplot as plt
import simpy
import random

## Here is the Entity Subclass
class Order(Entity):
    def process(self):
        yield self.wait_for_resource(warehouse)
        yield self.process_at_resource(warehouse)
        self.release_resource(warehouse)

# Here is the Resource subclass
class Warehouse(Resource):
    def service_time(self, entity):
        return np.random.normal(30, 5)
        
# Here is the Source subclass
class OrderSource(Source):
    def interarrival_time(self):
        return random.expovariate(1.0 / 5) # every 5 minutes, order should arrive
    
    def build_entity(self):
        # Sections (TODO)
        return Order(env) # create a call with the chosen problem_size
    
# Now construct instances of Resource and Source.
np.random.seed(42) # set seed so random parts remain constant between simulations

env = simpy.Environment()
warehouse = Warehouse(env, capacity=2) # configure 2 employee capacity
order_source = OrderSource(env, number=20) # source will stop after 20 customers have been generated

env.process(order_source.start(debug=True)) # if you want to see printed output for simulation, set debug=True
env.run()

system_time = Stats.get_total_times()
print("total_time:", Stats.get_total_times())
print("total waiting_time:", Stats.get_waiting_times()) 
print("total processing_time:", Stats.get_processing_times(), "\n")

print("waiting time for warehouse resource", Stats.get_waiting_times(warehouse))
print("processing time for warehouse resource", Stats.get_processing_times(warehouse))
print("total time at warehouse resource", Stats.get_total_times(warehouse), "\n")

print("warehouse queue size over time", Stats.queue_size_over_time(warehouse))
print("call_cetner utilization over time", Stats.utilization_over_time(warehouse))

print("entities that were not disposed", Stats.get_total_times(attributes={"disposed": False}))

# we can use the return values from these statistics methods to create charts about our simulation's performance

plt.hist(system_time,bins=5)
# you can customize the exact tick marks on an axis
plt.yticks(range(0,3))
plt.ylabel('Frequency')
plt.xlabel('Time in System')
plt.title('Histogram of Time in System')
plt.show()

"""
Histogram of queue over time
"""
warehouse_queue = Stats.queue_size_over_time(warehouse)
plt.hist(warehouse_queue)
print(f"Average number in queue: {np.mean(warehouse_queue)}")
print(f"Max in queue: {np.max(warehouse_queue)}")
print(f"Min in queue: {np.min(warehouse_queue)}")
plt.ylabel('Frequency')
plt.xlabel('Queue Size')
plt.title('Histogram of Queue Size')
plt.show()


#------------------------------------------------------------

# ## Here is the Entity Subclass
# class Call(Entity):
#     def process(self):
#         yield self.wait_for_resource(warehouse)
#         yield self.process_at_resource(warehouse)
#         self.release_resource(warehouse)

# # Here is the Resource subclass
# class CallCenter(Resource):
#     def service_time(self, entity):
#         problem_size = entity.attributes["problem_size"]
#         if problem_size == "sm":
#             return 1
#         elif problem_size == "md":
#             return 3
#         else:  # size must be lg at this point
#             return 10

# # Here is the Source subclass
# class CallSource(Source):
#     def interarrival_time(self):
#         return 1 # every 1 minute, call should arrive to the simulation
    
#     def build_entity(self):
#         # choose problem_size for this entity based on distribution in scenario.
#         problem_size = np.random.choice(["sm", "md", "lg"], p=[0.5, 0.35, 0.15])
#         attributes = {
#             "problem_size": problem_size
#         }
#         return Call(env, attributes) # create a call with the chosen problem_size
    
# # Now construct instances of Resource and Source.
# np.random.seed(42) # set seed so random parts remain constant between simulations

# env = simpy.Environment()
# warehouse = CallCenter(env, capacity=2) # configure 2 employee capacity
# call_source = CallSource(env, number=20) # source will stop after 20 customers have been generated

# env.process(call_source.start(debug=True)) # if you want to see printed output for simulation, set debug=True
# env.run()