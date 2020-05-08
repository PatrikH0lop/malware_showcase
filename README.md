![license](https://img.shields.io/badge/License-MIT-green)
![version](https://img.shields.io/badge/Version-1.1-blue)
![dev](https://img.shields.io/badge/Dev-Python3-brightgreen)
![types](https://img.shields.io/badge/Malware%20Types-7%20-red)

# Malware Showcase

<img align="middle" src="https://github.com/PatrikH0lop/malware_showcase/blob/master/logo.svg">

This repository contains explanatory examples of malicious behavior like _file infection_ or _remote code execution_. It's supposed to demonstrate and explain 
the nature of malicious software with practical examples in Python.

**Note:** _This repository contains examples of malicious files. It should be used for educational purposes only. Usage of files in this repository for any other purpose might cause you legal issues, even though the provided examples are very simple. It is advised to follow the instructions._

### Showcase structure

- **File infector** - This kind of malware infects other files. Common example of such behavior is _code injection_. Malicious code is injected into targeted files and might be later executed. This allows the file infectors to spread. The purpose of their payload might differ, from harmless to destructive behavior.
  - [Simple file infector in Python (with explanation)](https://github.com/PatrikH0lop/malware_showcase/tree/master/file_infection)
- **Trojan (trojan horse)** - This kind of malware tries to look like a legitimate software and the malicious activity is hidden from the victim. Common example of such behaviour is _spying on victims_. Trojans can be more precisely classified by a purpose of the malicious segment. They were named after the Greek story, in which the city of Troy has accepted a statue of wooden horse as a gift from their enemies, while the enemy soldiers were hidden inside.
  - [Simple trojan in Python (with explanation)](https://github.com/PatrikH0lop/malware_showcase/tree/master/trojan)
- **Worm** - This kind of malware tries to spread on the network and does not need a host file to spread. Worms might contain malicious payload and execute commands on the compromised systems or just consume the network bandwidth to jam the communication.
  - [Simple worm in Python (with explanation)](https://github.com/PatrikH0lop/malware_showcase/tree/master/worm)
- **Spyware** - This kind of malware tries to spy on the victim and steal his or her data. There exist various ways of spying on the victim, for example scanning the pressed keys on the keyboard. In comparison with the trojan horse, spyware stays often hidden from the sight of the victim. 
  - [Simple keylogger in Python (with explanation)](https://github.com/PatrikH0lop/malware_showcase/tree/master/spyware)
- **Ransomware** - This kind of malware tries to encrypt your files or even restrict your access to the system until a financial ransom is paid. It might continuously remove your files to increase the threat and force you to submit. Ransomwares became very popular in the recent years.
  - [Simple ransomware in Python (with explanation)](https://github.com/PatrikH0lop/malware_showcase/tree/master/ransomware)
- **Adware** - This kind of malware tries to aggressively show ads to the victims. Usually it is just an annoying software that does not have any harmful intentions. Adware might try various methods to make the advertising more persistent.
  - [Simple adware in Python (with explanation)](https://github.com/PatrikH0lop/malware_showcase/tree/master/adware)
- **Dropper** - This kind of malware attemps to download or dump malicious code to the target system. The malware can be secretly embedded in the dropper itself or downloaded from a remote server. It often tries to avoid detection by obfuscation and encryption.
  - [Simple dropper in Python (with explanation)](https://github.com/PatrikH0lop/malware_showcase/tree/master/dropper)

### Installation

Make sure that you have installed [Python3](https://www.python.org/download/), system package `python3-dev` and Python package `wheel`. 
```console
sudo apt install python3-dev
pip3 install wheel
python3 setup.py bdist_wheel  # You might need to run this command as well.
```

To setup a virtual environment, run the following command:
```console
source setup_env.sh
```
Or you can install required Python packages listed in `requirements.txt` on your own.
If something goes wrong during the installation, the script should provide you information 
about possible failures. You can then focus on the problematic steps in `setup_env.sh` and
fix the problem. 
