import argparse
import sys
import logging

from src.codest.normalize_paths import normalize_paths, is_subdirectory
from .document_generator import DocumentGenerator
from .exceptions import CodestError

logger = logging.getLogger(__name__)


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
        'directories',
        help='Directories to scan for source files',
        nargs='+',  # 1つ以上のディレクトリを受け付ける
        default=['.']
    )
    parser.add_argument(
        '--exclude',
        help='Directories to exclude from scanning',
        nargs='*',
        default=[]
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
    parser.add_argument(
        '-c', '--clipboard',
        action='store_true',
        help='Copy output to clipboard instead of creating a file'
    )
    return parser


def main() -> int:
    """
    Main entry point for the CLI
    """
    parser = create_parser()
    args = parser.parse_args()

    setup_logging(args.verbose)
    logger = logging.getLogger(__name__)

    try:
        # パスの正規化と重複排除
        directories = normalize_paths(args.directories)
        exclude_dirs = normalize_paths(args.exclude)

        logger.debug(f"Normalized directories to scan: {directories}")
        if exclude_dirs:
            logger.debug(f"Normalized directories to exclude: {exclude_dirs}")

        # 除外ディレクトリが指定されたディレクトリのサブディレクトリであることを確認
        for exclude_dir in exclude_dirs:
            if not any(is_subdirectory(d, exclude_dir) for d in directories):
                logger.warning(f"Excluded directory '{exclude_dir}' is not a subdirectory of any specified directories")

        generator = DocumentGenerator(
            directories=directories,
            exclude_dirs=exclude_dirs,
            max_file_size_kb=args.max_size
        )

        if args.clipboard:
            content, _ = generator.generate(to_clipboard=True)
            logger.info("Source code collection copied to clipboard")
        else:
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