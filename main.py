import math
import lzma
import gzip
import bz2


def CodeToBase64(file):
    # таблиця символів Base64
    base64_chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"

    # читаємо вміст файлу у вигляді байтів
    with open(file, "rb") as f:
        file_bytes = f.read()

    # створюємо порожній рядок для зберігання закодованого тексту
    base64_text = ""

    # докладаємо додаткові нульові байти, якщо кількість байтів не кратна 3
    while len(file_bytes) % 3 != 0:
        file_bytes += bytes([0])

    # перетворюємо послідовність трійок байтів у послідовність чотирьох символів Base64
    for i in range(0, len(file_bytes), 3):
        # розбиваємо поточну трійку байтів на окремі байти
        b1, b2, b3 = file_bytes[i:i + 3]

        # розбиваємо поточний байт на дві частини
        # використовуємо зсуви на 2 та 4 розряди, щоб отримати дві шестнадцяткові цифри
        c1 = (b1 & 0xfc) >> 2
        c2 = ((b1 & 0x03) << 4) | ((b2 & 0xf0) >> 4)
        c3 = ((b2 & 0x0f) << 2) | ((b3 & 0xc0) >> 6)
        c4 = b3 & 0x3f

        # додаємо чотири символи Base64 до результуючого тексту
        base64_text += base64_chars[c1]
        base64_text += base64_chars[c2]
        base64_text += base64_chars[c3]
        base64_text += base64_chars[c4]

    # замінюємо останні два символи Base64 на знак дорівнює, якщо було додано додаткові нульові байти
    if len(file_bytes) % 3 == 1:
        base64_text = base64_text[:-2] + "=="
    elif len(file_bytes) % 3 == 2:
        base64_text = base64_text[:-1] + "="

    with open(f'{fileName}_base64', "w") as f:
        f.write(base64_text)


def calculate_entropy(char_probs):
    entropy = 0
    for prob in char_probs.values():
        entropy += - prob * math.log2(prob)

    print("Середня ентропія алфавіту: {:.2f} біт на символ".format(entropy))
    return entropy

def calculate_information(entropy, text):
    text_length = len(text)
    information = entropy * text_length
    print("Кількість інформації: {:.2f} біт".format(information))
    return information

def Compressions():
    # Стискаємо текст різними алгоритмами стиснення
    with gzip.open(f'{fileName}.gz', 'wb') as gz:
        gz.write(bytes(text, 'utf-8'))

    with bz2.BZ2File(f'{fileName}.bz2', 'w') as bz:
        bz.write(bytes(text, 'utf-8'))

    with lzma.open(f'{fileName}.xz', 'w') as xz:
        xz.write(bytes(text, 'utf-8'))

    # отримуємо розміри файлів
    text_size = len(text)
    compressed_size_zip = len(open(f"{fileName}.zip", "rb").read())
    compressed_size_7z = len(open(f"{fileName}.7z", "rb").read())
    compressed_size_gz = len(open(f"{fileName}.gz", "rb").read())
    compressed_size_bz2 = len(open(f"{fileName}.bz2", "rb").read())
    compressed_size_xz = len(open(f"{fileName}.xz", "rb").read())

    print("Розмір текстового файлу: {} байт".format(text_size))
    print("Розмір стисненого файлу zip: {} байт".format(compressed_size_zip))
    print("Розмір стисненого файлу 7z: {} байт".format(compressed_size_7z))
    print("Розмір стисненого файлу gz: {} байт".format(compressed_size_gz))
    print("Розмір стисненого файлу bz2: {} байт".format(compressed_size_bz2))
    print("Розмір стисненого файлу xz: {} байт".format(compressed_size_xz))

def FrequencyOfSymbols(text):
    char_counts = {}

    for char in text:
        if char in char_counts:
            char_counts[char] += 1
        else:
            char_counts[char] = 1

    total_chars = len(text)
    char_frequency = {char: count / total_chars for char, count in char_counts.items()}

    for key in char_frequency.keys():
        print(f"ймовірність появи символу '{key}' - {char_frequency[key]}")

    return  char_frequency

fileName = "text3"
filePath = f"{fileName}.txt"

fileBase64Path = f'{fileName}_base64'
filebz2Base64Path = f'{fileName}.bz2_base64'

with open(filebz2Base64Path, encoding="utf-8") as file:
    text = file.read()

char_frequency = FrequencyOfSymbols(text)
print('\n')
entropy = calculate_entropy(char_frequency)
print('\n')
information = calculate_information(entropy, text)
print('\n')

text_size = len(text)
print("Розмір текстового файлу: {} байт".format(text_size))

#Compressions()

CodeToBase64(filePath)