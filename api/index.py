from flask import Flask, render_template, request, jsonify
from num2words import num2words
from text2digits import text2digits
import base64
import re

app = Flask(__name__)

def text_to_number(text):
    """Convert English text number to integer"""
    import re
    
    # Check for negative words first
    if any(word in text.lower() for word in ['negative', 'minus']):
        raise ValueError("Negative numbers are not supported")
    
    # First try text2digits
    try:
        t2d = text2digits.Text2Digits()
        result = t2d.convert(text)
        
        # Check if result contains negative indicators
        if any(word in result.lower() for word in ['negative', 'minus', '-']):
            raise ValueError("Negative numbers are not supported")
        
        # Extract the number from the converted text
        numbers = re.findall(r'\d+', result)  # Only positive numbers
        if numbers:
            number = int(numbers[0])
            return number
    except ValueError:
        raise  # Re-raise our custom errors
    except:
        pass  # Fall through to manual implementation
    
    text_clean = re.sub(r'[^a-zA-Z\s]', '', text.lower().strip())
    
    if text_clean in ['zero', 'nil']:
        return 0
    
    # Handle basic words
    ones = {"one": 1, "two": 2, "three": 3, "four": 4, "five": 5,
            "six": 6, "seven": 7, "eight": 8, "nine": 9, "ten": 10,
            "eleven": 11, "twelve": 12, "thirteen": 13, "fourteen": 14, "fifteen": 15,
            "sixteen": 16, "seventeen": 17, "eighteen": 18, "nineteen": 19}
    
    tens = {"twenty": 20, "thirty": 30, "forty": 40, "fifty": 50,
            "sixty": 60, "seventy": 70, "eighty": 80, "ninety": 90}
    
    # Handle compound numbers like "forty two"
    words = text_clean.split()
    if len(words) == 2 and words[0] in tens and words[1] in ones:
        return tens[words[0]] + ones[words[1]]
    elif len(words) == 1 and words[0] in ones:
        return ones[words[0]]
    elif len(words) == 1 and words[0] in tens:
        return tens[words[0]]
    
    raise ValueError("Unable to convert text to number")

def number_to_text(number):
    """Convert integer to English text"""
    try:
        return num2words(number)
    except:
        raise ValueError("Unable to convert number to text")

def base64_to_number(b64_str):
    """Convert base64 to integer"""
    try:
        # Decode base64 to bytes, then convert bytes to integer using little-endian
        decoded_bytes = base64.b64decode(b64_str)
        return int.from_bytes(decoded_bytes, byteorder='little')
    except:
        raise ValueError("Invalid base64 input")

def number_to_base64(number):
    """Convert integer to base64"""
    try:
        # Handle negative numbers
        if number < 0:
            raise ValueError("Cannot convert negative numbers to base64")
        
        # Special case for zero - encode as single zero byte
        if number == 0:
            number_bytes = b'\x00'
        else:
            # Convert integer to bytes using little-endian, then encode to base64
            byte_count = (number.bit_length() + 7) // 8
            number_bytes = number.to_bytes(byte_count, byteorder='little')
        
        return base64.b64encode(number_bytes).decode('utf-8')
    except Exception as e:
        raise ValueError(f"Unable to convert to base64: {str(e)}")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert():
    try:
        data = request.get_json()
        input_value = data['input']
        input_type = data['inputType']
        output_type = data['outputType']
        
        # Pre-validate for negative inputs BEFORE conversion
        if input_type in ['binary', 'octal', 'decimal', 'hexadecimal']:
            if input_value.strip().startswith('-'):
                raise ValueError("Negative numbers are not supported")
        
        # Additional input validation
        if input_type == 'binary':
            # Binary should only contain 0 and 1
            if not all(c in '01' for c in input_value.strip()):
                raise ValueError("Invalid binary input - only 0 and 1 allowed")
        elif input_type == 'octal':
            # Octal should only contain 0-7
            if not all(c in '01234567' for c in input_value.strip()):
                raise ValueError("Invalid octal input - only 0-7 allowed")
        
        # Convert input to integer based on input type
        if input_type == 'text':
            number = text_to_number(input_value)
        elif input_type == 'binary':
            number = int(input_value, 2)
        elif input_type == 'octal':
            number = int(input_value, 8)
        elif input_type == 'decimal':
            number = int(input_value)
        elif input_type == 'hexadecimal':
            number = int(input_value, 16)
        elif input_type == 'base64':
            number = base64_to_number(input_value)
        else:
            raise ValueError("Invalid input type")
        
        # Design choice: Validate non-negative for all conversions
        if number < 0:
            raise ValueError("Negative numbers are not supported")
            
        # Convert integer to output type
        if output_type == 'text':
            result = number_to_text(number)
        elif output_type == 'binary':
            result = bin(number)[2:]  # Remove '0b' prefix
        elif output_type == 'octal':
            result = oct(number)[2:]  # Remove '0o' prefix
        elif output_type == 'decimal':
            result = str(number)
        elif output_type == 'hexadecimal':
            result = hex(number)[2:] # Remove '0x' prefix
        elif output_type == 'base64':
            result = number_to_base64(number)
        else:
            raise ValueError("Invalid output type")
            
        return jsonify({'result': result, 'error': None})
    except Exception as e:
        return jsonify({'result': None, 'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)
