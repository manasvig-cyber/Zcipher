import numpy as np

def caesar_cipher(text, shift):
    result = ""
    for char in text.upper():
        if char.isalpha():
            result += chr(((ord(char) - 65 + shift) % 26) + 65)
        else:
            result += char
    return result

def hill_cipher_encrypt(text, matrix):
    def mod_inverse_matrix(matrix, mod=26):
        try:
            determinant = int(round(np.linalg.det(matrix)))
            determinant_inv = pow(determinant, -1, mod)
            matrix_mod_inv = determinant_inv * np.round(determinant * np.linalg.inv(matrix)).astype(int) % mod
            return matrix_mod_inv
        except Exception as e:
            print("Matrix not invertible:", e)
            return None

    text = text.upper().replace(" ", "")
    while len(text) % 2 != 0:
        text += 'X'
    vectorized = [ord(c) - 65 for c in text]
    matrix = np.array(matrix)
    ciphertext = ""

    for i in range(0, len(vectorized), 2):
        pair = np.array(vectorized[i:i+2])
        result = matrix.dot(pair) % 26
        ciphertext += ''.join(chr(i + 65) for i in result)
    return ciphertext

def vigenere_cipher(text, key):
    result = ""
    key = key.upper()
    key_index = 0
    for char in text.upper():
        if char.isalpha():
            shift = ord(key[key_index % len(key)]) - 65
            result += chr(((ord(char) - 65 + shift) % 26) + 65)
            key_index += 1
        else:
            result += char
    return result

def monoalphabetic_cipher(text, substitution_alphabet):
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    result = ""
    for char in text.upper():
        if char.isalpha():
            result += substitution_alphabet[alphabet.index(char)]
        else:
            result += char
    return result

def polygram_cipher(text, mapping):
    result = ""
    i = 0
    while i < len(text):
        found = False
        for length in sorted(mapping.keys(), key=lambda x: -x):
            chunk = text[i:i+length].upper()
            if chunk in mapping[length]:
                result += mapping[length][chunk]
                i += length
                found = True
                break
        if not found:
            result += text[i]
            i += 1
    return result

def playfair_cipher(text, key):
    def create_matrix(key):
        key = ''.join(sorted(set(key), key=key.index)).upper().replace('J', 'I')
        matrix = []
        for char in key:
            if char not in matrix and char.isalpha():
                matrix.append(char)
        for char in 'ABCDEFGHIKLMNOPQRSTUVWXYZ':
            if char not in matrix:
                matrix.append(char)
        return [matrix[i:i+5] for i in range(0, 25, 5)]

    def find_position(matrix, letter):
        for i in range(5):
            for j in range(5):
                if matrix[i][j] == letter:
                    return i, j

    def process_digraphs(text):
        text = text.upper().replace("J", "I").replace(" ", "")
        digraphs = []
        i = 0
        while i < len(text):
            a = text[i]
            b = text[i+1] if i+1 < len(text) else 'X'
            if a == b:
                b = 'X'
                i += 1
            else:
                i += 2
            digraphs.append((a, b))
        return digraphs

    matrix = create_matrix(key)
    digraphs = process_digraphs(text)
    result = ""

    for a, b in digraphs:
        row1, col1 = find_position(matrix, a)
        row2, col2 = find_position(matrix, b)
        if row1 == row2:
            result += matrix[row1][(col1 + 1) % 5] + matrix[row2][(col2 + 1) % 5]
        elif col1 == col2:
            result += matrix[(row1 + 1) % 5][col1] + matrix[(row2 + 1) % 5][col2]
        else:
            result += matrix[row1][col2] + matrix[row2][col1]
    return result

def menu():
    print("\nSelect a Cipher:\n")
    print("1. Caesar Cipher")
    print("2. Hill Cipher")
    print("3. Vigenère Cipher (Polyalphabetic)")
    print("4. Polygram Substitution Cipher")
    print("5. Monoalphabetic Cipher")
    print("6. Playfair Cipher")
    print("7. Exit")

    choice = int(input("Enter your choice (1-7): "))
    return choice

while True:
    choice = menu()
    if choice == 1:
        plaintext = input("Enter plaintext: ")
        shift = int(input("Enter shift value: "))
        print("Ciphertext:", caesar_cipher(plaintext, shift))
    elif choice == 2:
        plaintext = input("Enter plaintext: ")
        matrix = [[3, 3], [2, 5]]
        print("Ciphertext:", hill_cipher_encrypt(plaintext, matrix))
    elif choice == 3:
        plaintext = input("Enter plaintext: ")
        key = input("Enter keyword: ")
        print("Ciphertext:", vigenere_cipher(plaintext, key))
    elif choice == 4:
        plaintext = input("Enter plaintext: ")
        mapping = {
            2: {"HE": "XM", "LL": "ZP"},
            1: {"O": "A"}
        }
        print("Ciphertext:", polygram_cipher(plaintext, mapping))
    elif choice == 5:
        plaintext = input("Enter plaintext: ")
        shuffled = "QWERTYUIOPASDFGHJKLZXCVBNM"
        print("Ciphertext:", monoalphabetic_cipher(plaintext, shuffled))
    elif choice == 6:
        plaintext = input("Enter plaintext: ")
        key = input("Enter Playfair keyword: ")
        print("Ciphertext:", playfair_cipher(plaintext, key))
    elif choice == 7:
        break
    else:
        print("Invalid option. Try again.")
