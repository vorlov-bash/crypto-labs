Params:
* buffer size = 64B
* garbage size = `76 (ebp-0x4c) - 64 = 12B`
* ebp size = 4B

So padding = 80

The return address must not have `0xbf..`, so we just use ret2libc technique. It gives us the opportunity to call system functions which located outside esp stack. So what we need:
* `system` function - calls shell commands
* `/bin/sh` address - located in libc functions

We must to pass /bin/sh address argument to "system" function, the padding will be esp+0x8. Why esp+0x8? Simple.
Because right before function argument, there will be the return address of the function (where we should go after execution).
So we know that return address is 4 bytes, so we must add 8 bytes to ebp pointer to overwrite the func argument.

Call schema:
```
high
ebp + 0x8 [---/bin/sh address ---] <-- find by: 
             |                     * "strings -a -t x /lib/libc-2.11.2.so | grep /bin/sh" the /bin/sh padding (0x11f3bf)
             |                     * "info proc map" in gdb. The start address of /lib/libc-2.11.2.so (0xb7e97000)
             |                     If we add this addresses we can get actually /bin/sh address
             |
             |
ebp + 0x4 [-----return address-----] <-- actually does not matter, because we dont care 
             |                           what will be return address after calling system() 
             |                           (random 4 bytes)
             |
ebp       [-ebp of "system" function-] <-- find by calling "p system" in gdb
low
```
