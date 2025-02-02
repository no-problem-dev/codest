import argparse
import sys
import logging
from .document_generator import DocumentGenerator
from .exceptions import CodestError


def setup_logging(verbose: bool) -> None:
    """Set up logging configuration"""
    log_level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=log_level,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )


def create_parser() -> argparse.ArgumentParser:
    """Create and configure argument parser"""
    parser = argparse.ArgumentParser(
        description='Collect source code files into a single document'
    )
    parser.add_argument(
        'root_dir',
        help='Root directory to scan for source files',
        nargs='?',
        default='.'
    )
    parser.add_argument(
        '-o', '--output',
        help='Output file path'
    )
    parser.add_argument(
        '--max-size',
        type=int,
        default=1000,
        help='Maximum file size in KB (default: 1000)'
    )
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Enable verbose output'
    )
    return parser


def main() -> int:
    """
    Main entry point for the CLI

    Returns:
        int: Exit code (0 for success, 1 for error)
    """
    parser = create_parser()
    args = parser.parse_args()

    setup_logging(args.verbose)
    logger = logging.getLogger(__name__)

    try:
        generator = DocumentGenerator(args.root_dir, args.max_size)
        output_file = generator.generate(args.output)
        logger.info(f"Source code collection completed successfully: {output_file}")
        return 0

    except CodestError as e:
        logger.error(str(e))
        return 1

    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return 1


if __name__ == '__main__':
    sys.exit(main())