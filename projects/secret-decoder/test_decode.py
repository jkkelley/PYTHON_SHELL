import unittest
from unittest.mock import patch, MagicMock
from io import StringIO

# Import the main function from your script
# Assuming your main file is named decode.py
from decode import decode_secret_message

class TestSecretDecoder(unittest.TestCase):
    def setUp(self):
        # Mock HTML payload that represents the letter 'F'
        # Top bar: (0,2), (1,2), (2,2)
        # Middle bar: (0,1), (1,1)
        # Bottom stem: (0,0)
        self.mock_html = """
        <html>
            <body>
                <table>
                    <tr><th>x-coordinate</th><th>Character</th><th>y-coordinate</th></tr>
                    <tr><td>0</td><td>█</td><td>2</td></tr>
                    <tr><td>1</td><td>█</td><td>2</td></tr>
                    <tr><td>2</td><td>█</td><td>2</td></tr>
                    <tr><td>0</td><td>█</td><td>1</td></tr>
                    <tr><td>1</td><td>█</td><td>1</td></tr>
                    <tr><td>0</td><td>█</td><td>0</td></tr>
                </table>
            </body>
        </html>
        """
        
        # The expected terminal output (Y=2 down to Y=0)
        self.expected_output = (
            "███\n"  # y=2
            "██ \n"  # y=1
            "█  \n"  # y=0
        )

    @patch('decode.requests.get')
    @patch('sys.stdout', new_callable=StringIO)
    def test_decode_secret_message_prints_correctly(self, mock_stdout, mock_requests_get):
        # 1. Setup the mock response object to return our mock HTML
        mock_response = MagicMock()
        mock_response.text = self.mock_html
        mock_response.raise_for_status.return_value = None
        mock_requests_get.return_value = mock_response

        # 2. Execute the function with a dummy URL
        dummy_url = "https://docs.google.com/document/d/dummy/pub"
        decode_secret_message(dummy_url)

        # 3. Assert the network call was made with the exact argument
        mock_requests_get.assert_called_once_with(dummy_url)

        # 4. Assert the printed output matches the expected 'F' graphic perfectly
        actual_output = mock_stdout.getvalue()
        self.assertEqual(actual_output, self.expected_output)

if __name__ == '__main__':
    unittest.main()

# podman run --rm --entrypoint "python" secret-decoder test_decode.py