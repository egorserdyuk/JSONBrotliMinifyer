import unittest
import jsonbrotliminifyer
import tempfile
import os
import json


class TestJsonBrotliMinifyer(unittest.TestCase):

    def test_compress_decompress_dict(self):
        original = {"key": "value", "number": 42, "list": [1, 2, 3]}
        compressed = jsonbrotliminifyer.compress_json(original)
        decompressed = jsonbrotliminifyer.decompress_json(compressed)
        self.assertEqual(original, decompressed)

    def test_compress_decompress_list(self):
        original = [1, "string", {"nested": True}]
        compressed = jsonbrotliminifyer.compress_json(original)
        decompressed = jsonbrotliminifyer.decompress_json(compressed)
        self.assertEqual(original, decompressed)

    def test_compress_decompress_string(self):
        original = "simple string"
        compressed = jsonbrotliminifyer.compress_json(original)
        decompressed = jsonbrotliminifyer.decompress_json(compressed)
        self.assertEqual(original, decompressed)

    def test_compress_decompress_number(self):
        original = 12345
        compressed = jsonbrotliminifyer.compress_json(original)
        decompressed = jsonbrotliminifyer.decompress_json(compressed)
        self.assertEqual(original, decompressed)

    def test_compress_decompress_file(self):
        original = {"test": "data", "array": [1, 2, 3]}
        with tempfile.TemporaryDirectory() as temp_dir:
            input_file = os.path.join(temp_dir, 'input.json')
            compressed_file = os.path.join(temp_dir, 'compressed.br')
            output_file = os.path.join(temp_dir, 'output.json')

            # Write original JSON to file
            with open(input_file, 'w') as f:
                json.dump(original, f)

            # Compress file
            jsonbrotliminifyer.compress_json_file(input_file, compressed_file)

            # Decompress file
            jsonbrotliminifyer.decompress_json_file(
                compressed_file, output_file)

            # Read decompressed file and compare
            with open(output_file, 'r') as f:
                decompressed = json.load(f)
            self.assertEqual(original, decompressed)


if __name__ == '__main__':
    unittest.main()
