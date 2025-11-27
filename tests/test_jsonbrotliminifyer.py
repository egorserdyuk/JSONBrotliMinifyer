import unittest
import jsonbrotliminifyer
import tempfile
import os
import json
import brotli


class TestJsonBrotliMinifyer(unittest.TestCase):
    def test_compress_decompress_dict(self) -> None:
        original = {"key": "value", "number": 42, "list": [1, 2, 3]}
        compressed = jsonbrotliminifyer.compress_json(original)
        decompressed = jsonbrotliminifyer.decompress_json(compressed)
        self.assertEqual(original, decompressed)

    def test_compress_decompress_list(self) -> None:
        original = [1, "string", {"nested": True}]
        compressed = jsonbrotliminifyer.compress_json(original)
        decompressed = jsonbrotliminifyer.decompress_json(compressed)
        self.assertEqual(original, decompressed)

    def test_compress_decompress_string(self) -> None:
        original = "simple string"
        compressed = jsonbrotliminifyer.compress_json(original)
        decompressed = jsonbrotliminifyer.decompress_json(compressed)
        self.assertEqual(original, decompressed)

    def test_compress_decompress_number(self) -> None:
        original = 12345
        compressed = jsonbrotliminifyer.compress_json(original)
        decompressed = jsonbrotliminifyer.decompress_json(compressed)
        self.assertEqual(original, decompressed)

    def test_compress_quality_levels(self) -> None:
        # Large data to see compression difference
        original = {"data": "x" * 1000}
        compressed_low = jsonbrotliminifyer.compress_json(original, quality=0)
        compressed_high = jsonbrotliminifyer.compress_json(original, quality=11)
        # Higher quality should generally give smaller or equal size
        self.assertLessEqual(len(compressed_high), len(compressed_low))
        # Both should decompress correctly
        self.assertEqual(jsonbrotliminifyer.decompress_json(compressed_low), original)
        self.assertEqual(jsonbrotliminifyer.decompress_json(compressed_high), original)

    def test_compress_quality_invalid(self) -> None:
        with self.assertRaises(ValueError):
            jsonbrotliminifyer.compress_json({"test": "data"}, quality=12)
        with self.assertRaises(ValueError):
            jsonbrotliminifyer.compress_json({"test": "data"}, quality=-1)

    def test_compress_decompress_file(self) -> None:
        original = {"test": "data", "array": [1, 2, 3]}
        with tempfile.TemporaryDirectory() as temp_dir:
            input_file = os.path.join(temp_dir, "input.json")
            compressed_file = os.path.join(temp_dir, "compressed.br")
            output_file = os.path.join(temp_dir, "output.json")

            # Write original JSON to file
            with open(input_file, "w") as f:
                json.dump(original, f)

            # Compress file
            jsonbrotliminifyer.compress_json_file(input_file, compressed_file)

            # Decompress file
            jsonbrotliminifyer.decompress_json_file(compressed_file, output_file)

            # Read decompressed file and compare
            with open(output_file, "r") as f:
                decompressed = json.load(f)
            self.assertEqual(original, decompressed)

    def test_decompress_invalid_brotli(self) -> None:
        with self.assertRaises(ValueError) as cm:
            jsonbrotliminifyer.decompress_json(b"invalid brotli data")
        self.assertIn("Invalid Brotli-compressed data", str(cm.exception))

    def test_decompress_invalid_json(self) -> None:
        invalid_json_bytes = b"not valid json"
        compressed = brotli.compress(invalid_json_bytes)
        with self.assertRaises(ValueError) as cm:
            jsonbrotliminifyer.decompress_json(compressed)
        self.assertIn("Decompressed data is not valid JSON", str(cm.exception))

    def test_compress_json_file_input_not_found(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            input_file = os.path.join(temp_dir, "nonexistent.json")
            output_file = os.path.join(temp_dir, "output.br")
            with self.assertRaises(ValueError) as cm:
                jsonbrotliminifyer.compress_json_file(input_file, output_file)
            self.assertIn("Input file does not exist", str(cm.exception))

    def test_compress_json_file_invalid_json(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            input_file = os.path.join(temp_dir, "invalid.json")
            output_file = os.path.join(temp_dir, "output.br")
            with open(input_file, "w") as f:
                f.write("not valid json")
            with self.assertRaises(ValueError) as cm:
                jsonbrotliminifyer.compress_json_file(input_file, output_file)
            self.assertIn("Input file contains invalid JSON", str(cm.exception))

    def test_decompress_json_file_input_not_found(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            input_file = os.path.join(temp_dir, "nonexistent.br")
            output_file = os.path.join(temp_dir, "output.json")
            with self.assertRaises(ValueError) as cm:
                jsonbrotliminifyer.decompress_json_file(input_file, output_file)
            self.assertIn("Input file does not exist", str(cm.exception))


if __name__ == "__main__":
    unittest.main()
