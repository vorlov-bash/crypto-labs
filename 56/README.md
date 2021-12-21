# Secure storage app

### Info

In this app we use database with argon2i encryption. So how it's encrypting our data?

The answer is the argon2 algorithm! But in this lab we used the envelope encryption. It's encrypt our data with some DEK
key. What is it? It's just encrypted key that encrypts our data. But how we store it? Well the best solution is to store
keys in DEK storage, and KEK (key to DEK) storage. But in our solution storing in the database will be enough.

### DEK Encryption

In this solution we use an app secret key, which will be our KEK to encrypt DEK. The secret key must be 32 long due to
argon2 algorithm.

### Data encryption

On data-request we're generating a new DEK for data, and encrypt it by the KEK(secret key). This implementation gives us
to control which data whom be provided. As we know we have KEK for DEK. The cool part that we can decrypt any DEK for
any user. So, for examle we can share some user phone number to all users. Looks like vulnerability... But it's not,
because we, and only we control it (because we have access to KEK)

### Password

The app check for password length (between 8 and 64), and for simply (based on 10000 common passwords)