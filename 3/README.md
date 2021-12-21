# Casino crackers

## LCG
There some algorithm to implement the LCG for casinos (poor security):

We have 3 variables of algorithm:
* multiplier
* increment
* modulus (we have defined modulus in task, the value is 2 ^ 32)

So we just doining reverse programming to crack this algo.

Base algorithm next value: `(self.state * self.m + self.c) % self.n`

So doing some math we can figure out, what's will be the next number: `crackers/lcg.py`

But we have a problem: seed of the algorithm. The solution is to get some first states of bet's
to calculate the next value (because every next number depends on previous number)

## Mt & BetterMt
This algorithm is better as LCG, because of its complexity. In this part we doing pretty the same as in LCG cracker,
 but now the next number depends on previous 624 numbers. So doing that, we can crack the BetterMt also, because the seed is no more important! 
We just can write own Mt generator and put the 624 numbers in generator state ([mt generator](generators/mt.py)).

## Program
The program provides choose which algorithm you will be using, and how many moneys you want go generate.

## Example
### LCG
```
	(1) LCG
	(2) Mt
	(3) BetterMt
Choose algo: 1
Money to generate: 10000000
Done: 100%|██████████| 49/49 [00:02<00:00, 18.47it/s]
Your account: id='d7e26130-ef91-4dc2-b83d-6f621c306163' money=10490497 deletion_time=datetime.datetime(2021, 12, 21, 20, 12, 31, 115321, tzinfo=datetime.timezone.utc)
```

### Mt
```
	(1) LCG
	(2) Mt
	(3) BetterMt
Choose algo: 2
Money to generate: 1000000
Done: 100%|██████████| 628/628 [01:09<00:00,  8.99it/s] 
Your account: id='c68d55a2-9acf-46af-abe0-abf40726eaf4' money=1199176 deletion_time=datetime.datetime(2021, 12, 21, 20, 13, 8, 34697, tzinfo=datetime.timezone.utc)
```

### BetterMt
```
	(1) LCG
	(2) Mt
	(3) BetterMt
Choose algo: 3
Money to generate: 100000000
Done: 100%|██████████| 1024/1024 [01:47<00:00,  9.49it/s]
Your account: id='472e6e68-6fde-4ba4-a906-1f622d959caf' money=100100176 deletion_time=datetime.datetime(2021, 12, 21, 20, 15, 33, 656815, tzinfo=datetime.timezone.utc)
```