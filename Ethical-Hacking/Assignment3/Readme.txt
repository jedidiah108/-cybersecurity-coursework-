#Ransomware

Step 1 — Create a dummy my_secrets.txt file

Command:

echo "This is a harmless test secret for lab purposes" > my_secrets.txt

Step 2 — Create a test RSA keypair and extract public.pem

Command:

openssl genpkey -algorithm RSA -out private.pem -pkeyopt rsa_keygen_bits:2048
openssl rsa -in private.pem -pubout -out public.pem


-------------------------------------------------------------------------------------

Now you have:

* private.pem → RSA private key (used to decrypt later)

* public.pem → RSA public key (used by your script to encrypt key.txt)


-------------------------------------------------------------------------------------

Step 3 — run ransomware.py 

Command: 

python3 ransomware.py

-------------------------------------------------------------------------------------

After running:

* my_secrets.txt → deleted

* key.txt → deleted

* data_cipher.txt → Encrypted version of my_secrets.txt (base64)

* key_cipher.txt → Encrypted symmetric key (base64)

* public.pem → Deleted by your script

* Ransom message → Printed on screen 

>>>> Your file my_secrets.txt is encrypted. To decrypt it, send key_cipher.txt and $1,000 to me.


-----------------------------------------------------------------------------------------------------

*** I also provide you the screenshots of ***
-ransomware.png of the result
-data_cipher.png
-key_cipher.png