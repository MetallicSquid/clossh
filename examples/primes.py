# Check the first 10000 integers for primes over the cluster
from clossh.controller import Task, Node, Cluster

# Make a list of numbers to check for "prime-ness"
number_list = []
for i in range(10000):
    number_list.append(i)

class PrimeNode(Node):
    def prime_task(self, input_list):
        prime_process = Task(self, input_list)
        print(prime_process.control_process()[1].read().decode("utf-8"))

# Define your cluster
cluster = Cluster([PrimeNode("pi", "compute1"), PrimeNode("pi", "compute2"), PrimeNode("pi", "compute3")])
cluster.equal_distribute(number_list, PrimeNode.prime_task)
