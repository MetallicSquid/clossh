##### SSH Handling #####
import os
import paramiko as pk

def generate_rsa(key_password=None, key_path=None, bits=1024):
    """
        Generate RSA key pair on the controller, at a specified directory.

        Parameters
        ---------
        key_password: str
            Password to be assigned to the RSA key pair.
        key_path: str
            Path of the file allocated to the RSA key pair.
        bits: int
            The number of bits to generate the RSA key pair with."""
    key_directory = ""
    if key_path == None:
        key_directory = os.path.join(os.environ["HOME"], ".ssh/")
        key_path = os.path.join(key_directory, "id_rsa")
    else:
        key_directory = os.path.dirname(key_path)

    print(f"Generating private & public RSA key pair, with {bits} bits at `{key_path}` and `{key_path}.pub` respectively...\n")
    os.system(f"mkdir {key_directory}")
    private = pk.RSAKey.generate(bits=bits)
    private.write_private_key_file(key_path, password=key_password)
    public = pk.RSAKey(filename=key_path, password=key_password)
    with open(f"{key_path}.pub", "w") as public_file:
        public_file.write(f"{public.get_name()} {public.get_base64()}")
    print("... RSA key pair generated!")

def generate_dss(key_password=None, key_path=None, bits=1024):
    """
        Generate DSS key pair on the controller, at a specified directory.

        Parameters
        ---------
        key_password: str
            Password to be assigned to the DSS key pair.
        key_path: str
            Path of the file allocated to the DSS key pair.
        bits: int
            The number of bits to generate the DSS key pair with."""
    if key_path == None:
        key_directory = os.path.join(os.environ["HOME"], ".ssh/")
        key_path = os.path.join(key_directory, "id_dsa")
    else:
        key_directory = os.path.dirname(key_path)

    print(f"Generating private & public DSS key pair, with {bits} bits at `{key_path}` and `{key_path}.pub` respectively...\n")
    os.system(f"mkdir {key_directory}")
    private = pk.DSSKey.generate(bits=bits)
    private.write_private_key_file(key_path, password=key_password)
    public = pk.DSSKey(filename=key_path, password=key_password)
    with open(f"{key_path}.pub", "w") as public_file:
        public_file.write(f"{public.get_name()} {public.get_base64()}")
    print("... DSS key pair generated!")

def generate_ecdsa(key_password=None, key_path=None, bits=521):
		"""
        Generate ECDSA key pair on the controller, at a specified directory.

        Parameters
        ---------
        key_password: str
            Password to be assigned to the ECDSA key pair.
        key_path: str
            Path of the file allocated to the ECDSA key pair.
        bits: int
            The number of bits to generate the ECDSA key pair with."""
		if key_path == None:
				key_directory = os.path.join(os.environ["HOME"], ".ssh/")
				key_path = os.path.join(key_directory, "id_ecdsa")
		else:
				key_directory = os.path.dirname(key_path)
		
		if bits != 256 and bits != 384 and bits != 521:
				print("ECDSA keys can only take sizes of 256, 384 or 521 bits. Defaulting to 521 bits.")
				bits = 521
	
		print(f"Generating private & public ECDSA key pair, with {bits} at `{key_path}` and `{key_path}.pub` respectively...\n")
		os.system(f"mkdir {key_directory}")
		private = pk.ECDSAKey.generate(bits=bits)
		private.write_private_key(key_path, password=key_password)
		public = pk.ECDSAKey(filename=key_path, password=key_password)
		with open(f"{key_path}.pub", "w") as public_file:
				public_file.write(f"{public.get_name()} {public.get_base64()}")
		print("... ECDSA key pair generated!")

def generate_ed25519(key_password=None, key_path=None, bits=1024):
    """
        Generate DSS key pair on the controller, at a specified directory.

        Parameters
        ---------
        key_password: str
            Password to be assigned to the ED25519 key pair.
        key_path: str
            Path of the file allocated to the ED25519 key pair.
        bits: int
            The number of bits to generate the ED25519 key pair with."""
    if key_path == None:
        key_directory = os.path.join(os.environ["HOME"], ".ssh/")
        key_path = os.path.join(key_directory, "id_ed25519")
    else:
        key_directory = os.path.dirname(key_path)

    print(f"Generating private & public ED25519 key pair, with {bits} bits at `{key_path}` and `{key_path}.pub` respectively...\n")
    os.system(f"mkdir {key_directory}")
    private = pk.Ed25519Key.generate(bits=bits)
    private.write_private_key_file(key_path, password=key_password)
    public = pk.Ed25519Key(filename=key_path, password=key_password)
    with open(f"{key_path}.pub", "w") as public_file:
        public_file.write(f"{public.get_name()} {public.get_base64()}")
    print("... ED25519 key pair generated!")


def authorize_controller(node, pub_key_path=None, ssh_path=None):
    """
        Add the controller's public key to the .ssh/authorized_keys file in a given Node.

        Parameters
        ----------
        node: Node (or Node-based sub-class)
            The Node on which the controller is to be authorized.
        pub_key_path: str
            Path to the controller's public key file.
        ssh_path: str
            Path to the Node's .ssh directory."""
    key = ""
    if pub_key_path == None:
        pub_key_path = os.path.join(os.environ["HOME"], ".ssh", "id_rsa.pub")
    with open(pub_key_path, "r") as pub_file:
        key = pub_file.read()

    if ssh_path == None:
        home = node.client.exec_command("echo $HOME")[1]
        ssh_path = os.path.join(home.read().decode('utf-8').replace("\n", ""), ".ssh/")
        auth_path = os.path.join(ssh_path, "authorized_keys")

    _touch_auth_keys = node.client.exec_command(f"touch {auth_path}")
    _echo_auth_keys = node.client.exec_command(f"echo '{key}' >> {auth_path}")
