import sys
import json
import argparse
import jsonbrotliminifyer


def main() -> None:
    parser = argparse.ArgumentParser(
        description="JSON Brotli compression/decompression tool."
    )
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Compress command
    compress_parser = subparsers.add_parser("compress", help="Compress JSON data")
    compress_parser.add_argument(
        "-i", "--input-file", type=str, help="Input JSON file to compress"
    )
    compress_parser.add_argument(
        "-o", "--output-file", type=str, help="Output compressed file"
    )
    compress_parser.add_argument(
        "-q", "--quality", type=int, default=11, help="Compression quality (0-11)"
    )

    # Decompress command
    decompress_parser = subparsers.add_parser("decompress", help="Decompress JSON data")
    decompress_parser.add_argument(
        "-i", "--input-file", type=str, help="Input compressed file to decompress"
    )
    decompress_parser.add_argument(
        "-o", "--output-file", type=str, help="Output JSON file"
    )

    args = parser.parse_args()

    if args.command == "compress":
        if args.input_file:
            if not args.output_file:
                print(
                    "Error: --output-file is required when using --input-file",
                    file=sys.stderr,
                )
                sys.exit(1)
            jsonbrotliminifyer.compress_json_file(
                args.input_file, args.output_file, args.quality
            )
            print(f"Compressed {args.input_file} to {args.output_file}")
        else:
            # Read from stdin
            try:
                data = json.load(sys.stdin)
            except json.JSONDecodeError as e:
                print(f"Error: Invalid JSON input: {e}", file=sys.stderr)
                sys.exit(1)
            compressed = jsonbrotliminifyer.compress_json(data, args.quality)
            if args.output_file:
                with open(args.output_file, "wb") as f:
                    f.write(compressed)
                print(f"Compressed to {args.output_file}")
            else:
                sys.stdout.buffer.write(compressed)

    elif args.command == "decompress":
        if args.input_file:
            if not args.output_file:
                print(
                    "Error: --output-file is required when using --input-file",
                    file=sys.stderr,
                )
                sys.exit(1)
            jsonbrotliminifyer.decompress_json_file(args.input_file, args.output_file)
            print(f"Decompressed {args.input_file} to {args.output_file}")
        else:
            # Read from stdin
            compressed = sys.stdin.buffer.read()
            try:
                data = jsonbrotliminifyer.decompress_json(compressed)
            except ValueError as e:
                print(f"Error: {e}", file=sys.stderr)
                sys.exit(1)
            if args.output_file:
                with open(args.output_file, "w") as f:
                    json.dump(data, f, indent=2)
                print(f"Decompressed to {args.output_file}")
            else:
                json.dump(data, sys.stdout, indent=2)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
