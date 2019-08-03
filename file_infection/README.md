# File infection

Our **file infector** is implemented in the file `infector.py`. It infects all files in the same directory with its own code that allows it to spread in the future. When the targeted file is executed, it should perform the same malicious infection on other files as our own **file infector**.

#### Demonstration of behavior

Observe `target_file.ext` before the execution of **file infector**. It is a simple file located in the same directory as our **file infector**. To see the behavior of **file infector**, simply execute it in this folder (```./infector.py```). You should see something like this:
```
DEBUG:user:Infecting file: ./target_file.ext
DEBUG:user:Infecting file: ./infector.py
INFO:user:Number of infected files: 1
```
Our **file infector** has tried to infect every file in this folder, even itself, but has successfully infected only `target_file.ext` (explained below). Now move the infected file into folder `target_folder/` and execute it the same way as we have executed our **file infector** (`./target_file.ext`). You should see similar information as above but this time we have successfully infected `target_file_2.ext` by using the infected `target_file.ext`.

Creation of **file infector** is very simple process as it is described below and anyone can do it just with basic knowledge of programming and understandment of operating systems. That's why we should be always cautious when we execute any uncommon or not trusted file.

#### How does it work?

- Firstly, we create our **file infector** and give it a name. <br>
  ```python
  code_injector = FileInfector('SimpleFileInfector')
  ```
- Then we must **choose a folder** with files we want to infect. We call function *infect_files_in_folder*
  that is provided by our **file infector** and pass the path to the folder as an argument. This function 
  returns the number of infected files. <br>
   ```python
  number_infected_files = code_injector.infect_files_in_folder(path)
  ```
- The first thing that needs to be done is a lookup for all filenames in the same directory. This implementation ignores _README_ files, because **file infector** would infect this file as well if you execute it.
- The second step is to check whether the file has been already infected. If you run our **file infector** multiple times, you can see that it ignores files that it has already infected. This might be done by using some sort of mark left in the infected file together with injected code. In this case it is a string `INJECTION SIGNATURE` in the module docstring. Our **file infector** reads the content of the targeted file and if it contains this signature, malware continues with other files. <br>
  ```python
  """ Implementation of file infector in Python.
      INJECTION SIGNATURE 
  """ 
  ```
- Because we expect the injected code to be executed, we must be sure that the targeted file has valid permissions for execution. To learn more about permissions, see [the guide to Linux permissions](https://www.linux.com/learn/understanding-linux-file-permissions).<br>
  ```python
  os.chmod(file, 777)
  ```
- The last step is to write the code of **our own file** into the targeted file.
  ```python
   with open(file, 'w') as infected_file:
      infected_file.write(self.malicious_code)
  ```
- To obtain the **code of our own application**, we can simply read the source file. A name of the file is always passed as the first argument before the execution. We should obtain the name from this argument, because the infected files might have various names and the code should work in all of them. Because _malicious_code_ is a **cached property**, we
  would access the source file only once.
  ```python
  malicious_file = sys.argv[0]
  with open(malicious_file, 'r') as file:
      malicious_code = file.read()
  ```
 
