# Salsa 20 encoded message

## Problem
We have a couple salsa20-encoded messages. We need to encode it.

## Solution
The main vulnerability of salsa20, that it uses the xor algorithm. As we knows the "XOR" is working on two sides.
So we can just xor 2 messages and xor it with some english word (text of these messages on english lang). Let's look
to the most popular words in english texts:
1. the
2. be
3. to
4. of
5. and
6. a
7. in
8. that
9. have

So we can xor our popular words with some lines of this text. 
Lets try "The". Ok, but which lines we will be xor-ing?
We need to doing some research. Let's have a look to our salsa encoded strings:

Line 3 have the same beginning as line 4. Moreover, the length of these bytes are 4!
This means that we have 4-length word or 3-length word with space character. Let's pick "The" with space character.

## Usage
The program is taking your source line index, keyword and xor-ing it with all encoded lines.

* Decoded lines (output) - saved decoded lines in json file
* Source index (input) - the source index of which line we will be xor-ing
* Keyword (input) - word which will be xor-ed with our xor-ed lines
* Apply (input) - prompt to save the xor result to json, or not

## Example
Start of decoding:
```
Source index: 2
Keyword: The

index #0, result: For
index #1, result: Th'
index #2, result: The
index #3, result: The
index #4, result: Tha
index #5, result: Whe
index #6, result: Wit
index #7, result: To 
index #8, result: But
index #9, result: The
index #10, result: No 
index #11, result: And
index #12, result: Tha
index #13, result: Thu
index #14, result: And
index #15, result: Is 
index #16, result: And
index #17, result: Wit
index #18, result: And
```

Some time after decoding:
```
Source index: 0
Keyword: For who would bear the

index #0, result: For who would bear the
index #1, result: Th'oppressor's wrong, 
index #2, result: The pangs of dispriz'd
index #3, result: The insolence of offic
index #4, result: That patient merit of 
index #5, result: When he himself might 
index #6, result: With a bare bodkin? Wh
index #7, result: To grunt and sweat und
index #8, result: But that the dread of 
index #9, result: The undiscovere'd coun
index #10, result: No traveller returns, 
index #11, result: And makes us rather be
index #12, result: Than fly to others tha
index #13, result: Thus conscience doth m
index #14, result: And thus the native hu
index #15, result: Is sicklied o'er with 
index #16, result: And enterprises of gre
index #17, result: With this regard their
index #18, result: And lose the name of a
```

After some googling we figured out that it was Shakespeare's text!