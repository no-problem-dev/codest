import argparse
import sys
from .collector import create_source_document
import logging

def main():
    parser = argparse.ArgumentParser(description='Collect source code files into a single document')
    parser.add_argument('root_dir', help='Root directory to scan for source files', nargs='?', default='.')
    parser.add_argument('-o', '--output', help='Output file path')
    parser.add_argument('--max-size', type=int, default=1000,
                       help='Maximum file size in KB (default: 1000)')
    parser.add_argument('-v', '--verbose', action='store_true',
                       help='Enable verbose output')
    
    args = parser.parse_args()
    
    # Set up logging based on verbosity
    log_level = logging.DEBUG if args.verbose else logging.INFO
    logging.basicConfig(
        level=log_level,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    
    try:
        create_source_document(args.root_dir, args.output, args.max_size)
        print(f"Source code collection completed successfully!")
        return 0
    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        return 1

if __name__ == '__main__':
    sys.exit(main())
