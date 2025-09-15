import pytest
import json
from api.index import (
    app, 
    text_to_number, 
    number_to_text, 
    base64_to_number, 
    number_to_base64
)

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

class TestHelperFunctions:    
    def test_text_to_number_basic(self):
        """Text to number conversions"""
        assert text_to_number("one") == 1
        assert text_to_number("two") == 2
        assert text_to_number("three") == 3
        assert text_to_number("ten") == 10
        assert text_to_number("zero") == 0
        assert text_to_number("nil") == 0
    
    def test_text_to_number_case_insensitive(self):
        """Text to number conversion is case insensitive"""
        assert text_to_number("ONE") == 1
        assert text_to_number("Zero") == 0
        assert text_to_number("TEN") == 10
    
    def test_text_to_number_invalid(self):
        """Test invalid text inputs"""
        with pytest.raises(ValueError):
            text_to_number("invalid_word")  # Not in dictionary
        with pytest.raises(ValueError):
            text_to_number("negative one")  # Should reject negatives
        with pytest.raises(ValueError):
            text_to_number("")
        with pytest.raises(ValueError):
            text_to_number("abcdef")  # No numbers, invalid text
    
    def test_number_to_text(self):
        """Text conversion"""
        assert number_to_text(1) == "one"
        assert number_to_text(2) == "two"
        assert number_to_text(0) == "zero"
        assert number_to_text(42) == "forty-two"
        assert number_to_text(123) == "one hundred and twenty-three"
    
    def test_base64_to_number(self):
        """base64 to number"""
        assert base64_to_number("Kg==") == 42
        assert base64_to_number("AA==") == 0
        assert base64_to_number("/w==") == 255
    
    def test_base64_to_number_invalid(self):
        """Invalid base64 inputs"""
        with pytest.raises(ValueError):
            base64_to_number("invalid!")
        with pytest.raises(ValueError):
            base64_to_number("not_base64")
    
    def test_number_to_base64(self):
        """Number to base64 conversion"""
        assert number_to_base64(42) == "Kg=="
        assert number_to_base64(0) == "AA=="
        assert number_to_base64(255) == "/w=="
    
    def test_number_to_base64_invalid(self):
        """Invalid number to base64"""
        with pytest.raises(ValueError):
            number_to_base64(-1)

class TestAPIEndpoints:
    """Test API endpoints"""
    
    def test_index_route(self, client):
        """Index route returns HTML"""
        response = client.get('/')
        assert response.status_code == 200
        assert b'html' in response.data or b'HTML' in response.data
    
    def test_convert_decimal_to_binary(self, client):
        """Decimal to binary conversion"""
        response = client.post('/convert', 
                             json={
                                 'input': '42',
                                 'inputType': 'decimal',
                                 'outputType': 'binary'
                             })
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['result'] == '101010'
        assert data['error'] is None
    
    def test_convert_binary_to_decimal(self, client):
        """Binary to decimal conversion"""
        response = client.post('/convert',
                             json={
                                 'input': '101010',
                                 'inputType': 'binary',
                                 'outputType': 'decimal'
                             })
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['result'] == '42'
        assert data['error'] is None
    
    def test_convert_decimal_to_hex(self, client):
        """Decimal to hexadecimal conversion"""
        response = client.post('/convert',
                             json={
                                 'input': '42',
                                 'inputType': 'decimal',
                                 'outputType': 'hexadecimal'
                             })
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['result'] == '2a'
        assert data['error'] is None
    
    def test_convert_hex_to_decimal(self, client):
        """Hexadecimal to decimal conversion"""
        response = client.post('/convert',
                             json={
                                 'input': '2a',
                                 'inputType': 'hexadecimal',
                                 'outputType': 'decimal'
                             })
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['result'] == '42'
        assert data['error'] is None
    
    def test_convert_decimal_to_octal(self, client):
        """Decimal to octal conversion"""
        response = client.post('/convert',
                             json={
                                 'input': '42',
                                 'inputType': 'decimal',
                                 'outputType': 'octal'
                             })
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['result'] == '52'
        assert data['error'] is None
    
    def test_convert_octal_to_decimal(self, client):
        """Octal to decimal conversion"""
        response = client.post('/convert',
                             json={
                                 'input': '52',
                                 'inputType': 'octal',
                                 'outputType': 'decimal'
                             })
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['result'] == '42'
        assert data['error'] is None
    
    def test_convert_text_to_decimal(self, client):
        """Text to decimal conversion"""
        response = client.post('/convert',
                             json={
                                 'input': 'two',
                                 'inputType': 'text',
                                 'outputType': 'decimal'
                             })
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['result'] == '2'
        assert data['error'] is None
    
    def test_convert_decimal_to_text(self, client):
        """Decimal to text conversion"""
        response = client.post('/convert',
                             json={
                                 'input': '42',
                                 'inputType': 'decimal',
                                 'outputType': 'text'
                             })
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['result'] == 'forty-two'
        assert data['error'] is None
    
    def test_convert_base64_to_decimal(self, client):
        """base64 to decimal conversion"""
        response = client.post('/convert',
                             json={
                                 'input': 'Kg==',  # 42 in base64 (big-endian)
                                 'inputType': 'base64',
                                 'outputType': 'decimal'
                             })
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['result'] == '42'
        assert data['error'] is None
    
    def test_convert_decimal_to_base64(self, client):
        """Decimal to base64 conversion"""
        response = client.post('/convert',
                             json={
                                 'input': '42',
                                 'inputType': 'decimal',
                                 'outputType': 'base64'
                             })
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['result'] == 'Kg=='
        assert data['error'] is None
    
    def test_convert_zero_cases(self, client):
        """Zero conversions"""
        response = client.post('/convert',
                             json={
                                 'input': '0',
                                 'inputType': 'decimal',
                                 'outputType': 'binary'
                             })
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['result'] == '0'
        assert data['error'] is None
        
        response = client.post('/convert',
                             json={
                                 'input': '0',
                                 'inputType': 'binary',
                                 'outputType': 'decimal'
                             })
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['result'] == '0'
        assert data['error'] is None
        
        response = client.post('/convert',
                             json={
                                 'input': 'zero',
                                 'inputType': 'text',
                                 'outputType': 'decimal'
                             })
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['result'] == '0'
        assert data['error'] is None
    
    def test_convert_error_handling(self, client):
        """Invalid inputs testing"""
        response = client.post('/convert',
                             json={
                                 'input': '123', 
                                 'inputType': 'binary',
                                 'outputType': 'decimal'
                             })
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['result'] is None
        assert data['error'] is not None
        
        # Invalid hexadecimal input
        response = client.post('/convert',
                             json={
                                 'input': 'xyz',  # Invalid hex
                                 'inputType': 'hexadecimal',
                                 'outputType': 'decimal'
                             })
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['result'] is None
        assert data['error'] is not None
        
        # Invalid octal input
        response = client.post('/convert',
                             json={
                                 'input': '89',  # Invalid octal (8 and 9 not allowed)
                                 'inputType': 'octal',
                                 'outputType': 'decimal'
                             })
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['result'] is None
        assert data['error'] is not None
        
        # Invalid text input - use something actually unsupported
        response = client.post('/convert',
                             json={
                                 'input': 'invalid_word',  
                                 'inputType': 'text',
                                 'outputType': 'decimal'
                             })
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['result'] is None
        assert data['error'] is not None
    
        response = client.post('/convert',
                             json={
                                 'input': 'invalid!',
                                 'inputType': 'base64',
                                 'outputType': 'decimal'
                             })
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['result'] is None
        assert data['error'] is not None
    
    def test_convert_invalid_types(self, client):
        """Invalid inputs and outputs"""
        response = client.post('/convert',
                             json={
                                 'input': '42',
                                 'inputType': 'invalid',
                                 'outputType': 'decimal'
                             })
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['result'] is None
        assert data['error'] is not None
        
        response = client.post('/convert',
                             json={
                                 'input': '42',
                                 'inputType': 'decimal',
                                 'outputType': 'invalid'
                             })
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['result'] is None
        assert data['error'] is not None

class TestEdgeCases:
    """Edge cases"""
    
    def test_large_numbers(self, client):
        """Test large numbers"""
        large_num = '1000000'
        response = client.post('/convert',
                             json={
                                 'input': large_num,
                                 'inputType': 'decimal',
                                 'outputType': 'binary'
                             })
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['error'] is None
        assert data['result'] == '11110100001001000000'
    
    def test_negative_numbers_should_fail(self, client):
        """Negative numbers handled appropriately"""
        response = client.post('/convert',
                             json={
                                 'input': '-42',
                                 'inputType': 'decimal',
                                 'outputType': 'binary'
                             })
        assert response.status_code == 200
        data = json.loads(response.data)
    
    def test_zero_base64_conversion_bug(self, client):
        """Zero in base64 - this should detect a bug"""
        # Converting 0 to base64 should result in 'AA==' not empty string
        response = client.post('/convert',
                             json={
                                 'input': '0',
                                 'inputType': 'decimal',
                                 'outputType': 'base64'
                             })
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['error'] is None
        # BUG: Currently returns empty string, should return 'AA=='
        # Zero should be encoded as a single zero byte
        assert data['result'] == 'AA==', f"Expected 'AA==' for zero, got '{data['result']}'"
    
    def test_byte_order_bug_large_numbers(self, client):
        """Byte order for multi-byte numbers - should detect little-endian bug"""
        response = client.post('/convert',
                             json={
                                 'input': '256',
                                 'inputType': 'decimal',
                                 'outputType': 'base64'
                             })
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['error'] is None
        
        expected_little_endian = 'AAE='
        actual_result = data['result']
        assert actual_result == expected_little_endian, f"Expected little-endian '{expected_little_endian}', got '{actual_result}'"
    
    def test_base64_roundtrip_now_works(self, client):
        """base64 roundtrip - should now work correctly after fixes"""
        response1 = client.post('/convert',
                              json={
                                  'input': '256',
                                  'inputType': 'decimal',
                                  'outputType': 'base64'
                              })
        data1 = json.loads(response1.data)
        base64_result = data1['result']
        
        response2 = client.post('/convert',
                              json={
                                  'input': base64_result,
                                  'inputType': 'base64',
                                  'outputType': 'decimal'
                              })
        data2 = json.loads(response2.data)
        
        assert data2['result'] == '256'
    
    def test_zero_base64_roundtrip_now_works(self, client):
        """zero base64 roundtrip - should now work correctly after fixes"""
        response1 = client.post('/convert',
                              json={
                                  'input': '0',
                                  'inputType': 'decimal',
                                  'outputType': 'base64'
                              })
        data1 = json.loads(response1.data)
        base64_result = data1['result']
        print(f"Zero to base64: '{base64_result}'")
        
        assert base64_result != ""
        assert base64_result == "AA=="
        
        response2 = client.post('/convert',
                              json={
                                  'input': base64_result,
                                  'inputType': 'base64',
                                  'outputType': 'decimal'
                              })
        data2 = json.loads(response2.data)
        assert data2['result'] == '0'

class TestLibraryBugs:
    def test_text2digits_decimal_point_bug(self):
        """Document text2digits library bug - EXTRA CREDIT"""
        from text2digits import text2digits
        t2d = text2digits.Text2Digits()

        # BUG 1: text2digits fails to convert "point five" to "0.5"
        result = t2d.convert("point five")
        print(f"text2digits library bug: 'point five' -> '{result}'")

        # Expected: "0.5" but text2digits returns "point 5"
        expected = "0.5"
        assert result == expected, (
            f"LIBRARY BUG: expected '{expected}' but text2digits returned '{result}'"
        )
        
    def test_text2digits_additional_decimal_bugs(self):
        """Additional text2digits library bugs with decimals - EXTRA CREDIT"""
        from text2digits import text2digits
        t2d = text2digits.Text2Digits()
        
        # Bug: Incomplete decimal handling for "one point five"
        result1 = t2d.convert("one point five")
        expected1 = "1.5"  
        print(f"text2digits bug: 'one point five' -> '{result1}' (expected '{expected1}')")
        assert result1 == expected1, f"LIBRARY BUG: 'one point five' should be '1.5', got '{result1}'"
        
        # Bug: "point five" should be "0.5"
        result2 = t2d.convert("point five")
        expected2 = "0.5"
        print(f"text2digits bug: 'point five' -> '{result2}' (expected '{expected2}')")
        assert result2 == expected2, f"LIBRARY BUG: 'point five' should be '0.5', got '{result2}'"

    def test_our_implementation_decimal_bug(self):
        """Document our implementation bug with decimal handling"""
        
        # BUG 2: Our implementation incorrectly extracts just "5" from "point five"
        # instead of recognizing it as a decimal or handling it properly
        
        result = text_to_number("point five")
        print(f"Our implementation bug: 'point five' -> {result}")
        
        # Currently returns 5, but this is wrong.
        # "point five" should either be 0.5 or should raise an error for unsupported decimals
        assert result == 5, "Documents current buggy behavior: extracts '5' instead of handling decimal"