from django.db import models
from django.contrib.auth.models import User

# Create your models here.

alphabet = []
for i in range(1213):
    alphabet.append(chr(i))


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


def encrypt(input_text, e, n):
    text_nums = to_nums(input_text)
    encrypted_text_nums = [0] * len(text_nums)
    for i in range(len(encrypted_text_nums)):
        encrypted_text_nums[i] = pow(text_nums[i], to_bin(e), n)

    result = ''
    for i in range(len(encrypted_text_nums)):
        result += str(encrypted_text_nums[i])
        result += ' '
    print(result)

    return result


def decrypt(text_nums, d, n):
    new_enc_txt = []
    encrypted_text = text_nums.split()
    print(encrypted_text)
    for el in range(len(encrypted_text)):
        new_enc_txt.append(int(encrypted_text[el]))

    print(new_enc_txt)

    decrypted_text_nums = [0] * len(new_enc_txt)
    for i in range(len(decrypted_text_nums)):
        decrypted_text_nums[i] = pow(new_enc_txt[i], to_bin(d), n)

    decrypted_text = to_letters(decrypted_text_nums)
    print(decrypted_text_nums)
    return decrypted_text




class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    reciever = models.ForeignKey(User, related_name='to_reciever', on_delete = models.DO_NOTHING)
    message_text = models.TextField('Текст сообщения')
    message_time = models.DateTimeField('Время отправления')
    sender_visibility = models.BooleanField('Отображение у отправителя', default=True)
    reciever_visibility = models.BooleanField('Отображение у получателя', default=True)
    is_readed = models.BooleanField('Прочитано', default=False)

    def __str__(self):
        return str(self.sender) + ' to ' + str(self.reciever)

    def encrypt_message(self, text):
        e = 1213
        n = 1032247
        self.message_text = encrypt(text, e, n)


    def decrypt_message(self):
        d = 13589
        n = 1032247
        self.message_text = decrypt(self.message_text, d, n)

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'


