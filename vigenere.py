import string
from collections import Counter

alphabet = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'

# Генерация случайного ключа
def gen_key(length):
    from random import choices
    return ''.join(choices(alphabet, k=length))

# Шифрование сообщения
def enc(msg, key):
    enc_msg = []
    for i in range(len(msg)):
        char = msg[i]
        if char.lower() not in alphabet:
            # Нешифруемые символы оставляем без изменений
            enc_msg.append(char)
        else:
            key_char = key[i % len(key)]
            offset = alphabet.find(key_char)
            new_pos = (alphabet.find(char.lower()) + offset) % len(alphabet)
            if char.isupper():
                enc_msg.append(alphabet[new_pos].upper())
            else:
                enc_msg.append(alphabet[new_pos])

    return ''.join(enc_msg)

# Дешифрование сообщения
def dec(ciphertext, key):
    dec_msg = []
    for i in range(len(ciphertext)):
        char = ciphertext[i]
        if char.lower() not in alphabet:
            # Нешифруемые символы оставляем без изменений
            dec_msg.append(char)
        else:
            key_char = key[i % len(key)]
            offset = alphabet.find(key_char)
            new_pos = (alphabet.find(char.lower()) - offset) % len(alphabet)
            if char.isupper():
                dec_msg.append(alphabet[new_pos].upper())
            else:
                dec_msg.append(alphabet[new_pos])

    return ''.join(dec_msg)

# расчета индекса совпадения
def calc_ic(text):
    n = len(text)
    freq_sum = 0
    for char in set(text):
        count = text.count(char)
        freq_sum += count * (count - 1)
    return freq_sum / (n * (n - 1)) if n > 1 else 0

# Определение длины ключа на основе индекса совпадения
def calc_key_length(ciphertext, max_len=16):
    best_len = 1
    best_ic = 0
    for k_len in range(1, max_len + 1):
        ic_sum = 0
        for i in range(k_len):
            block = ciphertext[i::k_len]
            ic = calc_ic(block)
            ic_sum += ic
        avg_ic = ic_sum / k_len
        if avg_ic > best_ic:
            best_ic = avg_ic
            best_len = k_len
    return best_len

# Взлом
def crack(ciphertext):
    key_len = calc_key_length(ciphertext)
    best_guess = None
    max_score = 0
    possible_key = ''

    for j in range(key_len):
        freq = Counter()
        for i in range(j, len(ciphertext), key_len):
            char = ciphertext[i]
            if char.lower() in alphabet:
                freq.update([char])

        if freq:
            # Получаем 3 самых частых буквы
            most_common = freq.most_common(3)
            for common_letter, _ in most_common:
                # Пробуем каждую из самых частых букв
                possible_key += alphabet[(alphabet.find(common_letter) - alphabet.find('о')) % len(alphabet)]

                # Декодируем текст с этим ключом
                decrypted_text = dec(ciphertext, possible_key)
                score = analyze_text(decrypted_text)

                if score > max_score:
                    max_score = score
                    best_guess = (possible_key, decrypted_text)

    return best_guess

# Анализ текста на основе частоты букв
def analyze_text(text):

    letter_freqs = {
        'а': 0.08167, 'б': 0.01592, 'в': 0.04576, 'г': 0.01669, 'д': 0.03413,
        'е': 0.08477, 'ё': 0.00201, 'ж': 0.00568, 'з': 0.01764, 'и': 0.07324,
        'й': 0.01648, 'к': 0.02977, 'л': 0.04525, 'м': 0.03237, 'н': 0.06701,
        'о': 0.10977, 'п': 0.03295, 'р': 0.04573, 'с': 0.05859, 'т': 0.06224,
        'у': 0.02779, 'ф': 0.00216, 'х': 0.00858, 'ц': 0.01458, 'ч': 0.01635,
        'ш': 0.00653, 'щ': 0.00283, 'ъ': 0.00022, 'ы': 0.01968, 'ь': 0.01769,
        'э': 0.00845, 'ю': 0.00549, 'я': 0.01948
    }


    bigram_freqs = {
        'ст': 0.097, 'ен': 0.075, 'то': 0.068, 'на': 0.060, 'но': 0.051,
        'ра': 0.050, 'ов': 0.046, 'ие': 0.044, 'ни': 0.041, 'ко': 0.040,
        'ал': 0.039, 'ро': 0.036, 'ре': 0.035, 'во': 0.034, 'пр': 0.033,
        'ос': 0.032, 'не': 0.030, 'ли': 0.027, 'ло': 0.022, 'по': 0.021,
        'ка': 0.020, 'ве': 0.019, 'ла': 0.018, 'го': 0.016, 'за': 0.015,
        'со': 0.014, 'до': 0.013, 'од': 0.012, 'та': 0.011, 'мо': 0.010,
        'па': 0.009, 'те': 0.008, 'ви': 0.007, 'ва': 0.006, 'ти': 0.005,
        'ши': 0.004, 'че': 0.003, 'чу': 0.002
    }

    # Подсчитываем количество совпадающих букв
    letter_score = 0
    bigram_score = 0

    for char in text.lower():
        if char in letter_freqs:
            letter_score += letter_freqs[char]

    for i in range(len(text) - 1):
        bigram = text[i:i + 2].lower()
        if bigram in bigram_freqs:
            bigram_score += bigram_freqs[bigram]

    # Дополнительная проверка на наличие пробелов между словами
    space_check = sum(1 for char in text if char == ' ')

    return letter_score + bigram_score + space_check


def main():
    print("Меню:")
    print("1. Шифрование")
    print("2. Расшифровка")
    print("3. Взлом")
    print("0. Выход")

    while True:
        choice = input("Введите номер действия: ")

        if choice == '1':
            msg = input("Введите сообщение для шифрования: ").lower()
            length = int(input("Введите длину ключа: "))
            key = gen_key(length)
            print(f"Ключ: {key}")
            encrypted = enc(msg, key)
            print(f"Зашифрованное сообщение: {encrypted}")

        elif choice == '2':
            ciphertext = input("Введите зашифрованное сообщение: ").lower()
            key = input("Введите ключ: ")
            decrypted = dec(ciphertext, key)
            print(f"Расшифрованное сообщение: {decrypted}")

        elif choice == '3':
            ciphertext = input("Введите зашифрованное сообщение: ").lower()
            cracked = crack(ciphertext)
            if cracked is not None:
                key, plaintext = cracked
                print(f"Восстановленный ключ: {key}")
                print(f"Попытка расшифровки: {plaintext}")
            else:
                print("Не удалось взломать шифр.")

        elif choice == '0':
            break

        else:
            print("Неверный выбор. Попробуйте снова.")


if __name__ == "__main__":
    main()
