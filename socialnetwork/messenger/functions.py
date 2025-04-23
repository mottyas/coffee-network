from simbols import *

# -------------------Алгоритм Евклида-------------------

def nod(a, b):
    while a != 0 and b != 0:
        if a > b:
            a = a % b
        else:
            b = b % a

    return a + b


# -------------------Рсширеннаый алгоритм Евклида-------------------

def reverse(n, a, y2, y1, N):
    q = int(n / a)
    r = n % a
    n = a
    y = y2 - q * y1
    y2 = y1
    y1 = y
    a = r

    if r == 0:
        if y2 < 0:
            return (y2 + N)
        else:
            return (y2)

    else:
        return reverse(n, a, y2, y1, N)


# -------------------Возведение в степень больших чисел-------------------

def pow(num, num_bin, mod):
    lst = list(num_bin)
    lst.reverse()
    k = lst
    b = [0] * len(num_bin)
    a = [0] * len(num_bin)
    a[0] = num
    if k[0] == '1':
        b[0] = num
    else:
        b[0] = 1
    for i in range(1, len(num_bin)):
        a[i] = a[i-1] ** 2 % mod
        if k[i] == '1':
            b[i] = b[i-1] * a[i] % mod
        else:
            b[i] = b[i-1]
    #print('=======================================================================================')
    #print(f'Возведение числа {num} в степень {num_bin}')
    #print('---------------------------------------------------------------------------------------')
    #print('K\t', k)
    #print('A\t', a)
    #print('b\t', b)
    #print('=======================================================================================')
    return b[-1]


# -------------------Перевод в двоичную систему-------------------

def to_bin(num_dec):
    num_bin = ''

    while num_dec > 0:
        num_bin = str(num_dec % 2) + num_bin
        num_dec = num_dec // 2

    return num_bin


# -------------------Проверка на простоту-------------------

def is_prime_num(num):
    m = [2, 3, 4, 5, 6]

    for i in range(2):
        if pow_key(m[i], to_bin(num-1), num) == 1:
            continue
        else:
            return False
    return True


# -------------------Генератор приватного ключа-------------------

def generate_pk(e, y):
    N = y
    d = reverse(y, e, 0, 1, N) % y
    return d



# -------------------Генератор открытого ключа-------------------

def generate_ok(y):
    e = int(input('Введите открытый ключ e: '))
    if is_prime_num(e) and e < y and nod(e, y) == 1:
        return e
    else:
        print('Ключ не подходит')
        return generate_ok(y)


# -------------------Из букв в числа-------------------

def to_nums(fullText):
    inputTextNum = []
    for i in range(len(fullText)):
        for j in range(len(alphabet)):
            if alphabet[j] == fullText[i]:
                inputTextNum.append(j)
    return inputTextNum


# -------------------Из чисел в буквы-------------------

def to_letters(text_by_num):
    output_text = []

    for i in range(len(text_by_num)):
        for j in range(len(alphabet)):
            if j == text_by_num[i]:
                output_text.append(alphabet[j])

    text_by_letters = ''.join(output_text)

    return text_by_letters


# -------------------Возведение в степень больших чисел ДЛЯ КЛЮЧА-------------------

def pow_key(num, num_bin, mod):
    lst = list(num_bin)
    lst.reverse()
    k = lst
    b = [0] * len(num_bin)
    a = [0] * len(num_bin)
    a[0] = num
    if k[0] == '1':
        b[0] = num
    else:
        b[0] = 1
    for i in range(1, len(num_bin)):
        a[i] = a[i - 1] ** 2 % mod
        if k[i] == '1':
            b[i] = b[i - 1] * a[i] % mod
        else:
            b[i] = b[i - 1]

    return b[-1]
