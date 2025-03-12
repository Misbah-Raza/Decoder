import string
from flask import Flask, request, render_template_string

app = Flask(__name__)

# ========== Existing Encryption/Decryption Functions ==========
def reverse_alphabet(text):
    alphabet = string.ascii_uppercase
    reversed_alphabet = alphabet[::-1]
    mapping = str.maketrans(alphabet + alphabet.lower(), reversed_alphabet + reversed_alphabet.lower())
    return text.translate(mapping)

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

def scramble(text):
    text = list(text)
    if len(text) % 2 != 0:
        text.append('X')
    for i in range(0, len(text) - 1, 2):
        text[i], text[i + 1] = text[i + 1], text[i]
    return ''.join(text)

def unscramble(text):
    if len(text) % 2 == 0 and text.endswith('X'):
        temp = scramble(text)
        if temp[-1] == 'X':
            text = text[:-1]
    unscrambled = scramble(text)
    if len(unscrambled) % 2 == 0 and unscrambled.endswith('X'):
        return unscrambled[:-1]
    return unscrambled

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

def decrypt(text):
    unmirrored = text[::-1]
    restored_symbols = restore_symbols(unmirrored)
    unscrambled = unscramble(restored_symbols)
    numbers = letter_to_number(unscrambled)
    shifted_back = reverse_hex_shift(numbers)
    original_text = number_to_letter(shifted_back)
    final_text = reverse_alphabet(original_text)
    return final_text

# ========== Web Interface ==========
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CipherVault Pro</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body {
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
            min-height: 100vh;
            color: #fff;
        }
        .nav-tabs .nav-link {
            color: #4ecdc4;
            border: none;
        }
        .nav-tabs .nav-link.active {
            background: transparent;
            color: #fff;
            border-bottom: 2px solid #4ecdc4;
        }
        .card {
            background: rgba(255, 255, 255, 0.05);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 15px;
        }
        .form-control {
            background: rgba(255, 255, 255, 0.1);
            border: none;
            color: #fff;
        }
        .form-control:focus {
            background: rgba(255, 255, 255, 0.2);
            color: #fff;
            box-shadow: none;
        }
        .result-box {
            background: rgba(0, 0, 0, 0.3);
            border-radius: 8px;
            word-wrap: break-word;
        }
        .gradient-text {
            background: linear-gradient(45deg, #4ecdc4, #45b7af);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
    </style>
</head>
<body>
    <div class="container py-5">
        <div class="text-center mb-5">
            <h1 class="gradient-text display-4 fw-bold">CipherVault Pro</h1>
            <p class="lead">Military-grade encryption for your sensitive data</p>
        </div>

        <ul class="nav nav-tabs justify-content-center mb-4" id="myTab" role="tablist">
            <li class="nav-item" role="presentation">
                <button class="nav-link active" id="encode-tab" data-bs-toggle="tab" 
                    data-bs-target="#encode" type="button" role="tab">Encode</button>
            </li>
            <li class="nav-item" role="presentation">
                <button class="nav-link" id="decode-tab" data-bs-toggle="tab" 
                    data-bs-target="#decode" type="button" role="tab">Decode</button>
            </li>
        </ul>

        <div class="tab-content">
            <div class="tab-pane fade show active" id="encode" role="tabpanel">
                <form method="POST" action="/encode">
                    <div class="card p-4 mb-4">
                        <div class="mb-3">
                            <label class="form-label">Text to Encode</label>
                            <textarea class="form-control" name="text" rows="3" 
                                placeholder="Enter your secret message" required></textarea>
                        </div>
                        <button type="submit" class="btn btn-primary w-100">
                            Encrypt Message
                        </button>
                    </div>
                </form>
                {% if encode_result %}
                <div class="card p-4">
                    <h5 class="mb-3">Encrypted Result</h5>
                    <div class="result-box p-3">
                        {{ encode_result }}
                    </div>
                </div>
                {% endif %}
            </div>

            <div class="tab-pane fade" id="decode" role="tabpanel">
                <form method="POST" action="/decode">
                    <div class="card p-4 mb-4">
                        <div class="mb-3">
                            <label class="form-label">Text to Decode</label>
                            <textarea class="form-control" name="text" rows="3" 
                                placeholder="Enter encrypted message" required></textarea>
                        </div>
                        <button type="submit" class="btn btn-primary w-100">
                            Decrypt Message
                        </button>
                    </div>
                </form>
            </div>
        </div>
    </div>
</body>
</html>
'''

@app.route('/', methods=['GET'])
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route('/encode', methods=['POST'])
def handle_encode():
    text = request.form['text']
    encrypted = encrypt(text)
    return render_template_string(HTML_TEMPLATE, encode_result=encrypted)

@app.route('/decode', methods=['POST'])
def handle_decode():
    text = request.form['text']
    decrypted = decrypt(text)
    return render_template_string(HTML_TEMPLATE, decode_result=decrypted)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
