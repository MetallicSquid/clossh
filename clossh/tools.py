import os
import getpass
from clossh.controller import Node
from clossh.ssh import generate_rsa, generate_dss, authorize_controller

def setup_cluster_ssh():
    """
        A script to set up SSH keys for a controller and its Nodes (as a Cluster). Requires user interaction.
        
        THIS IS A WIP, USE AT YOUR OWN PERIL!"""
    controller_status = input("Does the controller (this machine) currently have a valid SSH key pair? (y/N): ").lower()
    if controller_status == "" or controller_status == "n":
        key_pair_type = input("What SSH key pair algorithm do you want to use? ([R]sa/[d]ss): ").lower()
        key_bits = int(input("How many bits would you like your key pair to have? (1024 by default): "))
        ssh_path = input("Where do you want the .ssh directory to be? (~/.ssh by default): ")
        key_password = getpass.getpass("What password would you like your key pair to have? (leave blank for none): ")

        if key_bits == "":
            key_bits = 1024
        if ssh_path == "":
            ssh_path = os.path.expanduser("~/.ssh")
        if key_password == "":
            key_password = None

        if key_pair_type == "" or key_pair_type == "r":
            verify = input(f"Making an RSA key pair at {ssh_path} on the controller (this machine). Is this ok? (Y/n)").lower()
            key_path = os.path.join(ssh_path, "id_rsa")
            if verify == "" or verify == "y":
                generate_rsa(key_password, key_path, key_bits)
            else:
                exit()
        elif key_pair_type == "d":
            verify = input(f"Making an DSS key pair at {ssh_path} on the controller (this machine). Is this ok? (Y/n)").lower()
            key_path = os.path.join(ssh_path, "id_dsa")
            if verify == "" or verify == "y":
                generate_dss(key_password, key_path, key_bits)
            else:
                exit()
        else:
            exit()
    
    node_amount = int(input("How many nodes do you want to have in this cluster? "))
    public_key_path = input("What is the path to the controller's (this machine's) public key? (~/.ssh/id_rsa.pub by default): ")

    if public_key_path == "":
        public_key_path = os.path.expanduser("~/.ssh/id_rsa.pub")

    for node in range(node_amount):
        node += 1
        node_username = input(f"What is the username for node {node}? ")
        node_hostname = input(f"What is the hostname for node {node}? ")
        node_password = getpass.getpass(f"What is the password for node {node}? (leave blank for none): ")
        node_ssh_path = input(f"Where is the .ssh directory for node {node}? (~/.ssh by default): ")

        if node_password == "":
            node_password = None
        if node_ssh_path == "":
            node_ssh_path = None

        verify = input(f"Authorizing controller (this machine) with public key from {public_key_path} on node {node}. Is this ok? (Y/n)").lower()
        if verify == "" or verify == "y":
            authorize_controller(Node(username=node_username, hostname=node_hostname, password=node_password))
        else:
            exit()

    print("All done!")
        
