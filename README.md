# Numeric Converter - cs1060-hw2-base

A web-based application that converts numbers between different formats including:
- English text (e.g., "one hundred twenty-three")
- Binary
- Octal
- Decimal
- Hexadecimal
- Base64

## Setup

1. Install the required dependencies. We recommend following the best Python practice of a virtual environment. (This assumes Python3.)
```bash
python3 -m venv "hw2-env"
. hw2-env/bin/activate
pip3 install -r requirements.txt
```

2. Run the application:
```bash
python api/index.py
```

3. Open your web browser and navigate to `http://localhost:5000`

## Usage

1. Enter your input value in the text box
2. Select the input format from the dropdown menu
3. Select the desired output format from the second dropdown menu
4. Click "Convert" to see the result

## Examples

- Convert decimal to binary: Input "42" with input type "decimal" and output type "binary"
- Convert text to decimal: Input "forty two" with input type "text" and output type "decimal"
- Convert hexadecimal to text: Input "2a" with input type "hexadecimal" and output type "text"

# Deploying
The application should deploy to [Vercel](https://vercel.com?utm_source=github&utm_medium=readme&utm_campaign=vercel-examples) 
out of the box.

Just Add New... > Project, import the Git repository, and off you go.
Note that Vercel's Hobby plan means your private repository needs to be
in your personal GitHub account, not the organizational account.


--------------------------------------------------------------------

# Some bugs that I fixed

1. Converting 0 to formats, such base64, returned an empty string. I fixed this to properly return the correct representation of 0.

2. I fixed the byte order to use little-endian instead of big-endian.

3. Our old text parsing only supported one digit numbers, so converting "forty two" or "eleven" to decimal wasn't possible. I updated this so we can do this now.

4. Perhaps not a bug per se, but I updated our stance on negative number handling. We now reject negatives across the board.

# Extra Credit (and another bug documentation)

During testing, I found an implementation bug where decimal text inputs like "point five" were incorrectly converted to 5 instead of 0.5. Additioanlly, I also discovered a bug in the text2digits library, which fails to handle decimals correctly (e.g., "point five" returns "point 5" instead of "0.5"). Note that text2digits on "point five" returns 5 in my case, which doesn't match the intended behavior so this is a bug in my implementation as well. 

My test suite documents both issues (we fail the tests related to text2digits and decimals), ensuring consistent behavior while highlighting limitations in the external library.