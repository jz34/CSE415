# CSE 415 hw1 part a


# 1. four_x_cubed_plus_1(2) -> 33
def four_x_cubed_plus_1(num):
    return 4 * (num ** 3) + 1


# 2. mystery_code('abc Iz th1s Secure? n0, no, 9!', 17) -> 'PQR xO IW1H hTRJGT? C0, CD, 9!'
def mystery_code(str, num):
    result = ''
    for char in str:
        if char.isalpha():
            if char.islower():
                if ord(char) + 32 - num <= 122:
                    result += chr(ord(char) + 32 - num).upper()
                else:
                    result += chr(ord(char) + 32 - num - 26).upper()
            else:
                if ord(char) + 32 - num <= 90:
                    result += chr(ord(char) + 32 - num).lower()
                else:
                    result += chr(ord(char) + 32 - num - 26).lower()
        else:
            result += char

    return result


# 3. quintuples([2, 5, 1.5, 100, 3, 8, 7, 1, 1, 0, -2, -5])  ->  [[2, 5, 1.5, 100, 3], [8, 7, 1, 1, 0], [-2, -5]]
def quintuples(li):
    res = []
    while len(li) > 5:
        res.append(li[0:5])
        li = li[5:]
    res.append(li)

    return res


# 4. past_tense(['program', 'debug', 'execute', 'crash', 'repeat', 'eat']) ->
# ['programmed', 'debugged', 'executed', 'crashed', 'repeated', 'ate']

def past_tense(li):
    vowels = ['a', 'e', 'i', 'o', 'u']
    res = []
    for verb in li:
        last_letter = verb[len(verb) - 1]
        second_last = verb[len(verb) - 2]
        third_last = verb[len(verb) - 3]
        if isirreg(verb):
            res.append(irreg(verb))
        elif last_letter == 'e':
            res.append(verb + 'd')
        elif second_last in vowels and last_letter not in vowels and not last_letter == 'y' \
                and not last_letter == 'w' and third_last not in vowels:
            res.append(verb + last_letter + 'ed')
        elif last_letter == 'y' and second_last not in vowels:
            res.append(verb[:len(verb) - 1] + 'ied')
        else:
            res.append(verb + 'ed')
    return res


def isirreg(verb):
    irreg_verb = ['have', 'be', 'eat', 'go']
    return verb in irreg_verb


def irreg(verb):
    if verb == 'have':
        return 'had'
    elif verb == 'be':
        return 'was'
    elif verb == 'eat':
        return 'ate'
    elif verb == 'go':
        return 'went'














