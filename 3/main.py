from crackers.lcg import LcgCracker
from crackers.mt import MTCracker
import uuid

if __name__ == '__main__':
    crack_type_input = int(input('\t(1) LCG\n'
                                 '\t(2) Mt\n'
                                 '\t(3) BetterMt\n'
                                 'Choose algo: '))
    money_count = int(input('Money to generate: '))
    acc = None
    if crack_type_input == 1:
        acc = LcgCracker(str(uuid.uuid4()), 2 ** 32).crack(money_count)
    elif crack_type_input == 2:
        acc = MTCracker(str(uuid.uuid4()), 'Mt').crack(money_count)
    elif crack_type_input == 3:
        acc = MTCracker(str(uuid.uuid4()), 'BetterMt').crack(money_count)

    if acc:
        print(f'Your account: {acc}')
