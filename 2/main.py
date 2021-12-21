import json


def get_encoded_hex_lines():
    with open('salsa20_encoded.txt', 'r') as file:
        lines = []
        for line in file.readlines():
            lines.append(bytearray.fromhex(line))
    return lines


def xor_lines(a, b):
    res = []
    for i, el in enumerate(a):
        res.append(el ^ (0 if len(b) < i + 1 else b[i]))
    return bytearray.fromhex(bytearray(res).hex())


def str_to_hex(raw_str):
    return bytearray.fromhex(''.join(hex(ord(s))[2:] for s in raw_str))


def dump_lines_result_to_file(result):
    with open('result.json', 'w') as file:
        json.dump(result, file, indent=2)


def read_lines_result_from_file():
    try:
        with open('result.json', 'r') as file:
            return json.load(file)
    except:
        return {}


if __name__ == '__main__':
    decoded = read_lines_result_from_file()
    hex_lines = get_encoded_hex_lines()

    while True:
        print('Decoded lines:')
        for k, v in decoded.items():
            print(f'index #{k}, decoded: {v}')
        print('\n')

        try:
            source = int(input('Source index: '))
            word = input('Keyword: ')

            temp_decoded = {}
            for i in range(len(hex_lines)):
                res = xor_lines(xor_lines(hex_lines[source], hex_lines[i]), str_to_hex(word))
                print(f'index #{i}, result: {res[:len(word)].decode("utf-8")}')
                temp_decoded[str(i)] = res
            apply = bool(int(input('Apply? (0 or 1): ')))

            if apply:
                for k, v in temp_decoded.items():
                    decoded[str(k)] = v[:len(word)].decode('utf-8')
                dump_lines_result_to_file(decoded)
        except Exception as e:
            print(f'Error: {e}\n')
