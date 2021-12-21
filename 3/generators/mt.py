import ctypes

_i32_ = lambda v: ctypes.c_int32(v).value


class _MTConstants:
    W = 32
    N = 624
    M = 397
    R = 31
    A = 0x9908b0df
    U = 11
    D = 0xffffffff
    S = 7
    B = 0x9d2c5680
    T = 15
    C = 0xefc60000
    L = 18
    F = 1812433253
    L_MASK = (1 << 31) - 1
    U_MASK = 1 << 31


class MTGenerator:

    def __init__(self, seed):
        self.state = [0 for _ in range(_MTConstants.N)]
        self.current_index = 0

        self.init_seed(seed)

    def init_seed(self, seed: int):
        self.state[0] = seed

        for i in range(1, _MTConstants.N):
            self.state[i] = (_MTConstants.F *
                             (self.state[i - 1] ^
                              (self.state[i - 1] >> (_MTConstants.W - 2))) + i) & \
                            ((1 << _MTConstants.W) - 1)

    # https://jazzy.id.au/2010/09/22/cracking_random_number_generators_part_3.html#:~:text=next%20624%20integers.-,Generating%20the%20next%20state,-The%20algorithm%20for
    def generate_states(self):
        for i in range(_MTConstants.N):
            x = (
                    (self.state[i] & _MTConstants.U_MASK) +
                    (self.state[(i + 1) % _MTConstants.N] & _MTConstants.L_MASK)
            )

            x_a = x >> 1
            if x % 2 != 0:
                x_a = x_a ^ _MTConstants.A
            self.state[i] = self.state[(i + _MTConstants.M) % _MTConstants.N] ^ x_a
        self.current_index = 0

    def twist(self):
        for i in range(_MTConstants.N):
            x = (
                    (self.state[i] & _MTConstants.U_MASK) +
                    (self.state[(i + 1) % _MTConstants.N] & _MTConstants.L_MASK)
            )

            x_a = x >> 1
            if x % 2 != 0:
                x_a = x_a ^ _MTConstants.A
            self.state[i] = self.state[(i + _MTConstants.M) % _MTConstants.N] ^ x_a
        self.current_index = 0

    # https://jazzy.id.au/2010/09/22/cracking_random_number_generators_part_3.html#:~:text=Obtaining%20the%20next%20number
    def next(self):
        if self.current_index >= _MTConstants.N:
            self.twist()

        y = self.state[self.current_index]
        # print('y0', y)
        y = y ^ ((y >> _MTConstants.U) & _MTConstants.D)
        # print('y1', y)

        y = y ^ ((y << _MTConstants.S) & _MTConstants.B)
        # print('y2', y)

        y = y ^ ((y << _MTConstants.T) & _MTConstants.C)
        # print('y3', y)

        y = y ^ (y >> _MTConstants.L)
        # print('y4', y)

        self.current_index += 1
        return y & ((1 << _MTConstants.W) - 1)

    def set_state_with_index(self, state, i):
        self.state = state
        self.current_index = i
