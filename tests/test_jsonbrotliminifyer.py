import unittest
import jsonbrotliminifyer


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


if __name__ == '__main__':
    unittest.main()
