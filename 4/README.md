# Passwords generator


## Part 1
This app generates the 100k set of passwords:
* 10% - human like passwords (c0m2merasscutg)
* 70% - most common user passwords (123456)
* 20% - really random, but human understandable (OuvDlDNj301315)

These passwords we hash with:
* md5 without salt `-->` weak_hashes.csv
* argon2i with memory limit 16384 `-->` strong_hashes.csv

## Part 2
### MD5 without salt
To crack md5 hashes we use **hashcat** with command

`.\hashcat.exe -m 0 .\test-passwords\in\weak_hashes.csv .\test-passwords\rockyou.txt -d 1`

Out if 100k hashed we cracked 43718 passwords only in 1 minute with Nvidia GTX 970

```
Started: Sat Dec 25 12:16:49 2021
Stopped: Sat Dec 25 12:17:42 2021
```

### Argon2i with memory limit 16 KB (default 65000KB)
To crack argon2i we use john the ripper. The key feature of argon hashes that it hard to bruteforce, because of argon specific.
Use:
`.\john.exe --format=argon2 .\test-passwords\strong_passwords.csv --wordlist=.\test-passwords\rockyou.txt`

Well, we don't have much time to crack all 100k passwords, so we only generate 10, and see on performance.
So, out of 10 hashes we cracked 6 in 12 minutes with Intel I7 6700k.

## Conclusion
Arhon2 is way better than md5, because of algorithm specific (bruteforce defence). If we doing some math, we figured out that
to crack one argon password took us 2 minutes with memory limit 16KB, but with 65000KB that took us approximately 25 hours, and to crack one md5 hash took us 0,001 second (120000x faster than argon)