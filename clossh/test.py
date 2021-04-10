##### File for testing new functionality #####

import paramiko as pk
from clossh.controller import Task, Node, Cluster

cluster = Cluster(Node("pi", "compute1"), Node("pi", "compute2"), Node("pi", "compute3"))

class CopyNode(Node):
    def copy_task():
        print("Testing Control -> Node Copy...")
        self.control_node_copy(self.sftp, "~/server.txt", "~/server.txt")
        print("...Control -> Node Copy Successful")
        print("Testing Node -> Control Copy...")
        if self.hostname == "compute1":
            self.node_control_copy(self.sftp, "~/compute1.txt", "~/compute1.txt")
        elif self.hostname == "compute2":
            self.node_control_copy(self.sftp, "~/compute2.txt", "~/compute2.txt")
        else:
            self.node_control_copy(self.sftp, "~/compute3.txt", "~/compute3.txt")
        print("...Node -> Control Copy Successful")

cluster.equal_distribute([], CopyNode.copy_task)
