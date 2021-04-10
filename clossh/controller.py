##### General Cluster Controls #####
import os
import paramiko as pk
import json
import asyncio


### Task Class ###
class Task():
    """
        A class that represents a Task, an action to be performed by a given Node in a Cluster.

        Methods
        -------
        process()
            Runs the script (specified by script_path) on the Node. """
    def __init__(self, node, inputs=None):
        """
            Sets up the command to be run by the Task.

            Parameters
            ----------
            node: Node (or sub-class of Node)
                The Node that performs the Task.
            script_path: str
                The path to the script that will be performed in the Task.
            inputs: list
                The variable(s) to be passed to the script. """
        self.node = node

    def node_process(self, node_path):
        """
            Runs the script (specified by script_path) on the Node.

            Returns a tuple containing the script's output in the form (stdin, stdout, stderr). """
        
        if inputs == None:
            command = f'python3 {script_path}'
        else:
            command = f'python3 {script_path} "{inputs}"'

        stdin, stdout, stderr = self.node.client.exec_command(command)
        return (stdin, stdout, stderr)

    def control_process(self, control_path):
        """
            Runs a local (on the control node) script on the Node.

            Returns a tuple containing the script's output in the form (stdin, stdout, stderr). """
        

        node.control_node_copy(node.sftp, control_path, to_path) 
        pass

### Node Class ###
class Node():
    """
        A class that represents a Node, a "computer" in a Cluster that performs one or more Tasks.

        Methods
        -------
        node_control_copy(sftp_client, from_path, to_path)
            Copy a file or directory from a Node to the controller.
        control_node_copy(sftp_client, from_path, to_path)
            Copy a file or directory from the controller to a Node. """
    def __init__(self, username, hostname, password=None):
        """
            Sets up an SSH and SFTP connection between the controller and a Node.

            Parameters
            ----------
            username: str
                The Node's username (necessary to establish SSH / SFTP).
            hostname: str
                The Node's hostname (necessary to establish SSH / SFTP).
            password: str
                The Node's password (necessary to establish SSH / SFTP). """
        self.username = username
        self.hostname = hostname
        client = pk.SSHClient()
        client.load_system_host_keys()
        client.set_missing_host_key_policy(pk.WarningPolicy)
        client.connect(hostname=hostname, username=username, password=password)
        self.client = client
        self.sftp = client.open_sftp()

    def node_control_copy(self, sftp_client, from_path, to_path):
        """
            Copy a file or directory from a Node to the controller.

            Parameters
            ----------
            sftp_client: .SFTPClient object
                The SFTP connection object through which file / directory transfers are controlled.
            from_path: str
                The path of the file / directory to be transferred from.
            to_path: str
                The destination path for the file / directory to be transferred to. """
        from_path_exist_check = self.client.exec_command("ls {from_path}")
        print("TEST - From path:", from_path_exist_check)
        from_path_exists = True
        if from_path_exist_check == None:
            raise OSError(f"Path {from_path} does not exist on node ({self.username}@{self.hostname})")

        from_path_is_file = True
        if from_path[-1] == "/":
            from_path_is_file = False

        if os.path.exists(to_path):
            if from_path_is_file and os.path.isfile(to_path):
                sftp_client.get(from_path, to_path)
            elif not from_path_is_file and os.path.isdir(to_path):
                for file_name in sftp_client.listdir(from_path):
                    sftp_client.get(from_path+file_name, to_path+file_name)
            else:
                raise OSError(f"Path type for either {from_path} or {to_path} is ambiguous")
        else:
            raise OSError(f"Path {to_path} does not exist")

    def control_node_copy(self, sftp_client, from_path, to_path):
        """
            Copy a file or directory from the controller to a Node.

            Parameters
            ----------
            sftp_client: .SFTPClient object
                The SFTP connection object through which file / directory transfers are controlled.
            from_path: str
                The path of the file / directory to be transferred from.
            to_path: str
                The destination path for the file / directory to be transferred to. """
        to_path_exist_check = self.client.exec_command("ls {to_path}")[2]
        print("TEST - To path: ", to_path_exist_check)
        to_path_exists = True
        if to_path_exist_check == None:
            raise OSError(f"Path {to_path} does not exist on node ({self.username}@{self.hostname})")
        
        to_path_is_file = True
        if to_path[-1] == "/":
            to_path_is_file = False

        if os.path.exists(from_path):
            if os.path.isfile(from_path) and to_path_is_file: 
                sftp_client.put(from_path, to_path)
            elif os.path.isdir(from_path) and not to_path_is_file:
                for file_name in sftp_client.listdir(from_path):
                    sftp_client.put(from_path+file_name, to_path+file_name)
            else:
                raise OSError(f"Path type for either {from_path} or {to_path} is ambiguous")
        else:
            raise OSError(f"Path {from_path} does not exist")

    def find_safe_node_path(self, from_path, target_dir):
        """
        Find a safe (non-conflicting) path in the target_dir to copy a file to a Node from the controller.

        Parameters
        ----------
        from_path: str
            The path of the file to be tranferred.
        target_dir: str
            The target directory within which the file is to be copied to. """
        if not os.path.exists(from_path):
           raise OSError(f"Path {from_path} does not exist")
        
        ls_target_dir = self.client.exec_command("ls {target_dir}")[2]
        print("TEST - Target dir: ", target_dir_exist_check)
        target_dir_exists = True
        if ls_target_dir == None:
            raise OSError(f"Directory {target_dir} does not exist")

        original_filename = os.path.basename(from_path)
        print(original_filename)


### Cluster Class ###
class Cluster():
    """
        A class that represents a Cluster, a collection of Nodes co-ordinated by a controller, which perform one or more Tasks.

        Methods
        -------
        equal_distribute(input_list, task)
           Distribute the elements in a list equally among the Nodes controlled by the controller and perform a Task on each element. """
    def __init__(self, nodes):
        """
            Accepts a list of Nodes (or Node-based sub-classes) to be collected as a Cluster.

           Parameters
           ----------
           nodes: list
               A list of Nodes (or Node-based sub-classes) to be controlled as a Cluster. """
        self.nodes = nodes

    def equal_distribute(self, input_list, task):
        """
            Distibute the elements in a list equally among the Nodes controlled by the controller and perform a Task on each element.

            Parameters
            ----------
            input_list: list
                A list of elements to be distributed among the Nodes in the Cluster.
            task: Task (or Task-based sub-class)
                The Task to be performed on each of the elements of the input_list. """
        lower = 0
        split = upper = int(round(len(input_list) / len(self.nodes), 0))
        for node in self.nodes:
            if len(input_list) >= upper:
                node.task_alloc = input_list[lower:upper]
                lower = upper
                upper += split
            else:
                node.task_alloc = input_list[upper:]

        async def main():
            tasks = []
            for node in self.nodes:
                tasks.append(task(node, node.task_alloc))
            await asyncio.gather(*tasks)

        loop = asyncio.get_event_loop()
        loop.run_until_complete(main())
