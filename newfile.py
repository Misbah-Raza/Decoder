import string

# Reverse Alphabet Mapping (A ↔ Z, B ↔ Y, etc.)
def reverse_alphabet(text):
    alphabet = string.ascii_uppercase
    reversed_alphabet = alphabet[::-1]
    mapping = str.maketrans(alphabet + alphabet.lower(), reversed_alphabet + reversed_alphabet.lower())
    return text.translate(mapping)

# Letter-to-Number Conversion
def letter_to_number(text):
    return [(ord(char) - ord('A')) if 'A' <= char <= 'Z' else 
            (ord(char) - ord('a')) if 'a' <= char <= 'z' else char 
            for char in text]

def number_to_letter(numbers):
    return ''.join(chr(num + ord('A')) if isinstance(num, int) and 0 <= num <= 25 else 
                   chr(num + ord('a')) if isinstance(num, int) else str(num)
                   for num in numbers)

def apply_hex_shift(numbers, shift=3):
    return [(num + shift) % 26 if isinstance(num, int) and 0 <= num <= 25 else num for num in numbers]

def reverse_hex_shift(numbers, shift=3):
    return [(num - shift) % 26 if isinstance(num, int) and 0 <= num <= 25 else num for num in numbers]

# Scrambling
def scramble(text):
    text = list(text)
    if len(text) % 2 != 0:
        text.append('X')
    for i in range(0, len(text) - 1, 2):
        text[i], text[i + 1] = text[i + 1], text[i]
    return ''.join(text)

def unscramble(text):
    # Remove padding before unscrambling
    if len(text) % 2 == 0 and text.endswith('X'):
        # Check if the 'X' was added during scrambling
        temp = scramble(text)
        if temp[-1] == 'X':
            text = text[:-1]
    # Scramble again to reverse the swapping
    unscrambled = scramble(text)
    # Remove the padding 'X' if it exists
    if len(unscrambled) % 2 == 0 and unscrambled.endswith('X'):
        return unscrambled[:-1]
    return unscrambled

# Symbol Replacement Mapping (Updated to avoid apostrophe)
symbol_map = {
    'A': '@', 'B': '#', 'C': '%', 'D': '&', 'E': '*', 'F': '!', 'G': '^', 'H': ')', 'I': '(', 'J': '_',
    'K': '=', 'L': '+', 'M': '{', 'N': '}', 'O': '[', 'P': ']', 'Q': '|', 'R': ':', 'S': ';', 'T': '"',
    'U': '-', 'V': '<', 'W': '>', 'X': '?', 'Y': '/', 'Z': '~'
}

reverse_symbol_map = {v: k for k, v in symbol_map.items()}

def replace_symbols(text):
    return ''.join(symbol_map.get(char, char) for char in text)

def restore_symbols(text):
    return ''.join(reverse_symbol_map.get(char, char) for char in text)

# Encryption Process
def encrypt(text):
    text = text.upper()
    text = reverse_alphabet(text)
    numbers = letter_to_number(text)
    shifted = apply_hex_shift(numbers)
    shifted_text = number_to_letter(shifted)
    scrambled = scramble(shifted_text)
    symbol_text = replace_symbols(scrambled)
    mirrored = symbol_text[::-1]
    return mirrored

# Decryption Process
def decrypt(text):
    unmirrored = text[::-1]
    restored_symbols = restore_symbols(unmirrored)
    unscrambled = unscramble(restored_symbols)
    numbers = letter_to_number(unscrambled)
    shifted_back = reverse_hex_shift(numbers)
    original_text = number_to_letter(shifted_back)
    final_text = reverse_alphabet(original_text)
    return final_text

# ... [keep all existing functions and mappings] ...

# Replace the existing test code starting from line:
# message = input("write here")
# down to the print statements with:

# User interface
operation = input("Choose operation:\n[E] Encode text\n[D] Decode text\n> ").upper()

if operation == 'E':
    message = input("\nEnter text to encode:\n")
    encrypted = encrypt(message)
    print("\nEncrypted Result:\n" + encrypted)
elif operation == 'D':
    cipher = input("\nEnter text to decode:\n")
    decrypted = decrypt(cipher)
    print("\nDecrypted Result:\n" + decrypted)
else:
    print("Invalid selection. Please choose 'E' or 'D'.")
# Test