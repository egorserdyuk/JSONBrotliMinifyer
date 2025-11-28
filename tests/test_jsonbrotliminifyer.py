import unittest
import jsonbrotliminifyer
import tempfile
import os
import json
import brotli
import subprocess
import sys
from unittest.mock import patch, Mock


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

    @patch("jsonbrotliminifyer.os.rename")
    def test_compress_json_file_atomic_write_failure(self, mock_rename: Mock) -> None:
        """Test that if atomic rename fails, output file is not created."""
        mock_rename.side_effect = OSError("Rename failed")
        original = {"test": "data"}
        with tempfile.TemporaryDirectory() as temp_dir:
            input_file = os.path.join(temp_dir, "input.json")
            output_file = os.path.join(temp_dir, "output.br")

            # Write input file
            with open(input_file, "w") as f:
                json.dump(original, f)

            # Attempt compression, should fail on rename
            with self.assertRaises(ValueError) as cm:
                jsonbrotliminifyer.compress_json_file(input_file, output_file)
            self.assertIn("Error writing to output file", str(cm.exception))

            # Output file should not exist
            self.assertFalse(os.path.exists(output_file))

    @patch("jsonbrotliminifyer.os.rename")
    def test_decompress_json_file_atomic_write_failure(self, mock_rename: Mock) -> None:
        """Test that if atomic rename fails, output file is not created."""
        mock_rename.side_effect = OSError("Rename failed")
        data = {"test": "data"}
        compressed = jsonbrotliminifyer.compress_json(data)
        with tempfile.TemporaryDirectory() as temp_dir:
            input_file = os.path.join(temp_dir, "input.br")
            output_file = os.path.join(temp_dir, "output.json")

            # Write compressed file
            with open(input_file, "wb") as f:
                f.write(compressed)

            # Attempt decompression, should fail on rename
            with self.assertRaises(ValueError) as cm:
                jsonbrotliminifyer.decompress_json_file(input_file, output_file)
            self.assertIn("Error writing to output file", str(cm.exception))

            # Output file should not exist
            self.assertFalse(os.path.exists(output_file))


class TestCli(unittest.TestCase):
    def test_compress_stdin(self) -> None:
        data = {"test": "data"}
        input_json = json.dumps(data).encode()
        result = subprocess.run(
            [sys.executable, "-m", "jsonbrotliminifyer", "compress"],
            input=input_json,
            capture_output=True,
        )
        self.assertEqual(result.returncode, 0)
        compressed = result.stdout
        decompressed = jsonbrotliminifyer.decompress_json(compressed)
        self.assertEqual(decompressed, data)

    def test_compress_files(self) -> None:
        data = {"file": "test"}
        with tempfile.TemporaryDirectory() as temp_dir:
            input_file = os.path.join(temp_dir, "input.json")
            output_file = os.path.join(temp_dir, "output.br")
            with open(input_file, "w") as f:
                json.dump(data, f)
            result = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "jsonbrotliminifyer",
                    "compress",
                    "-i",
                    input_file,
                    "-o",
                    output_file,
                ],
                capture_output=True,
                text=True,
            )
            self.assertEqual(result.returncode, 0)
            self.assertIn("Compressed", result.stdout)
            with open(output_file, "rb") as f:
                compressed = f.read()
            decompressed = jsonbrotliminifyer.decompress_json(compressed)
            self.assertEqual(decompressed, data)

    def test_decompress_stdin(self) -> None:
        data = {"stdin": "decompress"}
        compressed = jsonbrotliminifyer.compress_json(data)
        result = subprocess.run(
            [sys.executable, "-m", "jsonbrotliminifyer", "decompress"],
            input=compressed,
            capture_output=True,
        )
        self.assertEqual(result.returncode, 0)
        output = result.stdout.decode()
        decompressed = json.loads(output)
        self.assertEqual(decompressed, data)

    def test_decompress_files(self) -> None:
        data = {"file": "decompress"}
        compressed = jsonbrotliminifyer.compress_json(data)
        with tempfile.TemporaryDirectory() as temp_dir:
            input_file = os.path.join(temp_dir, "input.br")
            output_file = os.path.join(temp_dir, "output.json")
            with open(input_file, "wb") as f:
                f.write(compressed)
            result = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "jsonbrotliminifyer",
                    "decompress",
                    "-i",
                    input_file,
                    "-o",
                    output_file,
                ],
                capture_output=True,
                text=True,
            )
            self.assertEqual(result.returncode, 0)
            self.assertIn("Decompressed", result.stdout)
            with open(output_file, "r") as f:
                decompressed = json.load(f)
            self.assertEqual(decompressed, data)

    def test_compress_invalid_quality(self) -> None:
        data = {"test": "quality"}
        input_json = json.dumps(data)
        result = subprocess.run(
            [sys.executable, "-m", "jsonbrotliminifyer", "compress", "-q", "12"],
            input=input_json,
            capture_output=True,
            text=True,
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Error", result.stderr)

    def test_compress_missing_output_file(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            input_file = os.path.join(temp_dir, "input.json")
            with open(input_file, "w") as f:
                json.dump({"test": "missing"}, f)
            result = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "jsonbrotliminifyer",
                    "compress",
                    "-i",
                    input_file,
                ],
                capture_output=True,
                text=True,
            )
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("required", result.stderr)

    def test_help(self) -> None:
        result = subprocess.run(
            [sys.executable, "-m", "jsonbrotliminifyer", "--help"],
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 0)
        self.assertIn("JSON Brotli compression", result.stdout)

    def test_invalid_command(self) -> None:
        result = subprocess.run(
            [sys.executable, "-m", "jsonbrotliminifyer", "invalid"],
            capture_output=True,
            text=True,
        )
        self.assertNotEqual(result.returncode, 0)
        # For invalid subcommand, argparse shows help or error


if __name__ == "__main__":
    unittest.main()
