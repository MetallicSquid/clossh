# The script to be executed on the node as part of the "primes" example
import sys
import multiprocessing as mp

# Convert command line argument (string) to a list
numbers_string = sys.argv[1]
numbers_list = numbers_string.strip("][").replace("\'", "").replace(" ", "").split(",")

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

with mp.Pool(mp.cpu_count()) as pool:
    print(pool.map(is_prime, numbers_list))
