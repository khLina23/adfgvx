class ADFGVX:
    def __init__(self):
        self.symbols = "АДФГВХ"
        self.alphabet = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ0123456789" # Русский алфавит + цифры
        self.square = None
        self.key_subst = None # ключевая фраза
        self.key_transp = None # ключ столбцов

    """ Установка ключа подстановки. Ключевая фраза для создания Полибиева квадрата  """
    def set_key_subst(self, key_subst):
        if self.create_square(key_subst):
            self.key_subst = key_subst

    """ Установка ключа транспозиции """
    def set_key_transp(self, key_transp):
        self.key_transp = key_transp

    """ Создание Полибиева квадрата на основе ключевой фразы """
    def create_square(self, key):
        # Удаление дубликатов и приведение всех букв к верхнему регистру
        key = "".join(sorted(set(key.upper()), key=key.upper().index))
        # Добавление оставшихся символов русского алфавита и цифр
        remaining_chars = [char for char in self.alphabet if char not in key]
        remaining_chars = "".join(remaining_chars)
        # Объединение ключевых символов и остальных символов
        self.square = key + remaining_chars
        # Вывод Полибиева квадрата
        print("Полибиев квадрат:")
        for i in range(6):
            print(self.square[i * 6 : (i + 1) * 6])
        return True

    """ Шифрование текста """
    def encrypt(self, text):
        encrypted_text = ""
        # Подстановка (использование Полибиева квадрата)
        for char in text:
            if char.upper() in self.square: # Проверка наличия символа в квадрате
                index = self.square.index(char.upper()) # Нахождение индекса символа
                row = self.symbols[index // 6] # Определение строки
                col = self.symbols[index % 6] # Определение столбца
                encrypted_text += row + col # Добавляем пару символов в зашифрованный текст

        # Транспозиция (перестановка столбцов)
        transposed_text = [""] * len(self.key_transp)
        for i in range(len(encrypted_text)):
            transposed_text[i % len(self.key_transp)] += encrypted_text[i]

        # Индексация ключей для сортировки
        indexed_keys = [(char, i) for i, char in enumerate(self.key_transp)]
        # Сортировка столбцов по ключу транспозиции
        transposed_text = [x for _, x in sorted(zip(indexed_keys, transposed_text), key=lambda pair: pair[0])]

        return "".join(transposed_text)

    """ Расшифровка текста, зашифрованного """
    def decrypt(self, encrypted_text):
        # Определяем количество полных столбцов
        full_cols = len(encrypted_text) % len(self.key_transp)
        # Определяем количество символов на каждый столбец
        chars_per_col = len(encrypted_text) // len(self.key_transp)
        # Создаем список для хранения столбцов
        cols = [""] * len(self.key_transp)
        # Индексация ключа транспозиции
        indexed_keys = [(char, i) for i, char in enumerate(self.key_transp)]
        # Распределение символов по столбцам
        i = 0
        for key in sorted(indexed_keys):
            length = (chars_per_col + 1) if indexed_keys.index(key) < full_cols else chars_per_col
            cols[indexed_keys.index(key)] = encrypted_text[i:i + length]
            i += length

        # Объединение столбцов для восстановления исходной строки
        decrypted_text = ""
        max_len = max(len(col) for col in cols)
        for i in range(max_len):
            for col in cols:
                if i < len(col):
                    decrypted_text += col[i]

        # Декодирование пар символов
        final_text = ""
        for i in range(0, len(decrypted_text), 2):
            row = decrypted_text[i]
            col = decrypted_text[i + 1]
            index = self.symbols.index(row) * 6 + self.symbols.index(col)
            if index < len(self.square):
                final_text += self.square[index]

        return final_text

    """ Взлом  """
    def crack(self, encrypted_text):
        results = []
        for subst_key in self.alphabet:
            for transp_key in self.alphabet:
                self.set_key_subst(subst_key)
                self.set_key_transp(transp_key)
                decrypted_text = self.decrypt(encrypted_text)
                results.append((subst_key, transp_key, decrypted_text))
        return results


def main():
    cipher = ADFGVX()

    while True:
        print("\nВыберите действие:")
        print("1. Шифрование")
        print("2. Дешифрование")
        print("3. Взлом")
        print("4. Выход")
        choice = input("Ваш выбор: ")  # Получаем ввод пользователя

        if choice == '1':
            plaintext = input("Введите текст для шифрования: ")
            subst_key = input("Введите ключ для подстановки: ")
            cipher.set_key_subst(subst_key)
            transp_key = input("Введите ключ для транспозиции: ")
            cipher.set_key_transp(transp_key)
            encrypted_text = cipher.encrypt(plaintext)
            print(f"Зашифрованный текст {encrypted_text}")
        elif choice == '2':
            encrypted_text = input("Введите текст для дешифрования: ")
            subst_key = input("Введите ключ для подстановки: ")
            cipher.set_key_subst(subst_key)
            transp_key = input("Введите ключ для транспозиции: ")
            cipher.set_key_transp(transp_key)
            decrypted_text = cipher.decrypt(encrypted_text)
            print(f"Дешифрованный текст: {decrypted_text}")
        elif choice == '3':
            encrypted_text = input("Введите текст для взлома: ")
            results = cipher.crack(encrypted_text)
            print("\nВозможные варианты расшифровки:")
            for subst_key, transp_key, decrypted_text in results:
                print(f"Ключ подстановки: {subst_key}, Ключ транспозиции: {transp_key}, Text: {decrypted_text}")
        elif choice == '4':
            print("Выход из программы.")
            break
        else:
            print("Некорректный выбор. Пожалуйста, попробуйте снова.")

if __name__ == "__main__":
    main()