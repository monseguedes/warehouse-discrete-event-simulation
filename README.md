# Project of Warehouse Discrete Event Simulation
We model a toy example of the DES a warehouse in Python using the package SimPy. The model is as follows:
The warehouse is made of several sectors, where each sector has a set number of workers. When an order comes in to the system, it will be made up from products from some sectors. If there is a free worker in the needed sectors, they process the order, otherwise the order is added to the queue of the sector. Once all the sectors needed to complete an order have processed the order, the order is sent to the delivery area. If there is a free truck, the order is delivered. Otherwise, it is added to the delivery queue. 

What do we want to see with this model?
- What happens when a sector is particularly slow?
- What happends when we increase the number of workers/trucks/sectors?
- How does having orders made of fewer sectors compare to many sectors?

What are our KPIs?
- Total order processing time of orders.
- Total waiting time of orders.
- Waiting times of orders at each sector (over time and mean).
- Waiting times of orders at delivery (over time and mean).
- Waiting times of workers at each sector, and utilization ratio.
- Waiting times of trucks, and utilization ratio.

Possible extensions:
- Priority orders that go to the first position of any queue.
- Trucks that need to wait for a minimum number of orders before they leave.
- Workers that have to go to the sectors to collect the packages.  
