##### File for testing new functionality #####

# Working on simplified key authentification
import paramiko as pk
from clossh.controller import Task, Node, Cluster

node = Node("pi", "server", "gCm2816R")

client = pk.SSHClient()

system_keys = node.client.load_system_host_keys()
host_keys = node.client.get_host_keys()

print(system_keys)
print(host_keys)

