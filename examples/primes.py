# Check the first 10000 integers for primes over the cluster
from clossh.controller import Task, Node, Cluster

# Make a list of numbers to check for "prime-ness"
number_list = []
for i in range(10000):
    number_list.append(i)

# A simple function to check whether a given number is prime
def is_prime(number):
    if number == 1:
        return False

    i = 2
    while i*i <= number:
        if number % i == 0:
            return False
        i += 1
    
    return True

class PrimeNode(Node):
    def prime_task(self, input_list):
        prime_process = Task(self, input_list)
        print(prime_process.function_process()[1].read().decode("utf-8"))

# Define your cluster
cluster = Cluster([PrimeNode("pi", "compute1"), PrimeNode("pi", "compute2"), PrimeNode("pi", "compute3")])
cluster.equal_distribute(number_list, PrimeNode.prime_task)
