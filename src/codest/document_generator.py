import os
import logging
from datetime import datetime
from typing import TextIO
from .file_collector import FileCollector
from .exceptions import DocumentGenerationError

logger = logging.getLogger(__name__)


class DocumentGenerator:
    def __init__(
            self,
            root_dir: str,
            max_file_size_kb: int = 1000,
            collector: FileCollector = None
    ):
        """
        DocumentGeneratorの初期化

        Args:
            root_dir (str): プロジェクトのルートディレクトリ
            max_file_size_kb (int, optional): 最大ファイルサイズ（KB）
            collector (FileCollector, optional): カスタムFileCollector
        """
        self.root_dir = root_dir
        self.max_file_size_kb = max_file_size_kb
        self.collector = collector or FileCollector(root_dir)

    def generate(self, output_file: str = None) -> str:
        """
        ソースコードドキュメントを生成

        Args:
            output_file (str, optional): 出力ファイルパス

        Returns:
            str: 生成されたファイルのパス

        Raises:
            DocumentGenerationError: ドキュメント生成に失敗した場合
        """
        if output_file is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            output_file = f'source_code_{timestamp}.txt'

        try:
            logger.info(f"Output will be written to: {output_file}")
            source_files = self.collector.collect_files()

            with open(output_file, 'w', encoding='utf-8') as f:
                self._write_header(f, len(source_files))

                for file_path in source_files:
                    self._process_file(f, file_path)

            return output_file

        except Exception as e:
            raise DocumentGenerationError(f"Failed to generate document: {str(e)}")

    def _write_header(self, file: TextIO, total_files: int) -> None:
        """
        ドキュメントヘッダーを書き込み

        Args:
            file (TextIO): 出力ファイルオブジェクト
            total_files (int): 処理対象のファイル総数
        """
        file.write(f"# Project Source Code Collection\n")
        file.write(f"# Generated at: {datetime.now().isoformat()}\n")
        file.write(f"# Root directory: {self.root_dir}\n")
        file.write(f"# Total files found: {total_files}\n\n")

    def _process_file(self, output_file: TextIO, file_path: str) -> None:
        """
        単一ファイルを処理して書き込み

        Args:
            output_file (TextIO): 出力ファイルオブジェクト
            file_path (str): 処理対象のファイルパス
        """
        rel_path = os.path.relpath(file_path, self.root_dir)
        logger.debug(f"Processing file: {rel_path}")

        file_size_kb = os.path.getsize(file_path) / 1024
        if file_size_kb > self.max_file_size_kb:
            self._write_skipped_file(output_file, rel_path, file_size_kb)
            return

        try:
            self._write_file_content(output_file, file_path, rel_path)
        except Exception as e:
            self._write_error_file(output_file, rel_path, str(e))

    def _write_skipped_file(self, output_file: TextIO, rel_path: str, file_size_kb: float) -> None:
        """
        スキップされたファイル情報を書き込み

        Args:
            output_file (TextIO): 出力ファイルオブジェクト
            rel_path (str): 対象ファイルの相対パス
            file_size_kb (float): ファイルサイズ（KB）
        """
        logger.warning(f"Skipping large file: {rel_path} ({file_size_kb:.1f}KB)")
        output_file.write(f"\n### File: {rel_path}\n")
        output_file.write(
            f"# [SKIPPED] File size ({file_size_kb:.1f}KB) exceeds limit of {self.max_file_size_kb}KB\n\n")

    def _write_file_content(self, output_file: TextIO, file_path: str, rel_path: str) -> None:
        """
        ファイル内容を書き込み

        Args:
            output_file (TextIO): 出力ファイルオブジェクト
            file_path (str): 対象ファイルの完全パス
            rel_path (str): 対象ファイルの相対パス

        Raises:
            IOError: ファイルの読み込みに失敗した場合
        """
        with open(file_path, 'r', encoding='utf-8') as source_file:
            content = source_file.read()
            output_file.write(f"\n### File: {rel_path}\n")
            output_file.write("```" + os.path.splitext(file_path)[1][1:] + "\n")
            output_file.write(content)
            output_file.write("\n```\n")

    def _write_error_file(self, output_file: TextIO, rel_path: str, error: str) -> None:
        """
        エラー情報を書き込み

        Args:
            output_file (TextIO): 出力ファイルオブジェクト
            rel_path (str): 対象ファイルの相対パス
            error (str): エラーメッセージ
        """
        logger.error(f"Error reading file {rel_path}: {error}")
        output_file.write(f"\n### File: {rel_path}\n")
        output_file.write(f"# [ERROR] Failed to read file: {error}\n\n")