PADDING_CHAR = "`"
BLOCK_SIZE = 3


def _pad_text(text: str) -> str:
    text = list(text)

    new_text = []

    while len(text) > BLOCK_SIZE:
        new_text.extend(text[:BLOCK_SIZE])
        text = text[BLOCK_SIZE:]
    else:
        while len(text) < BLOCK_SIZE:
            text.append(PADDING_CHAR)
        new_text.extend(text)

    return ''.join(new_text)


def _unpad_text(text: str) -> str:
    while text.endswith(PADDING_CHAR):
        text = text[:-1]

    return ''.join(text)


def sum_(n1: int, n2: int) -> int:
    return n1 + n2


def subtraction(n1: int, n2: int) -> int:
    return n1 - n2


OPERATIONS = {
    'encrypt': [sum_, subtraction],
    'decrypt': [subtraction, sum_],
}


def encrypt(text: str) -> str:
    padded_text = _pad_text(text)

    cipher_text = ""

    operations = OPERATIONS['encrypt']

    for index, char in enumerate(padded_text):
        if index % 2 == 0:
            next_operation = operations[1]
        else:
            next_operation = operations[0]

        cipher_char = chr(next_operation(ord(char), 10))
        cipher_text += cipher_char

    return cipher_text


def decrypt(cipher_text):
    operations = OPERATIONS['decrypt']

    text = ""

    for index, char in enumerate(cipher_text):
        if index % 2 == 0:
            next_operation = operations[1]
        else:
            next_operation = operations[0]

        char = chr(next_operation(ord(char), 10))
        text += char

    unpadded_text = _unpad_text(text)

    return unpadded_text


if __name__ == '__main__':
    test_words = [
        'amigo', 'Perro', 'que onda', 'así es mi estimado',
        'Espero esta práctica me ayude a no reprobar XD'
    ]

    for word in test_words:
        encrypted = encrypt(word)
        print(f"Encriptando ------- {word} -> {encrypted}")
        decrypted = decrypt(encrypted)
        print(f"Desencriptando ---- {word} -> {decrypted}")
        assert word == decrypted
        print("-" * 100)
