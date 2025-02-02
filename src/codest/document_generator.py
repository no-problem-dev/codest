import os
import io
import logging
import pyperclip
from datetime import datetime
from typing import Union, TextIO, Tuple
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

    def generate(self, output_file: str = None, to_clipboard: bool = False) -> Union[str, Tuple[str, str]]:
        """
        ソースコードドキュメントを生成

        Args:
            output_file (str, optional): 出力ファイルパス
            to_clipboard (bool, optional): クリップボードにコピーするかどうか

        Returns:
            Union[str, Tuple[str, str]]:
                to_clipboard=Falseの場合: 生成されたファイルのパス
                to_clipboard=Trueの場合: (生成された内容, ファイルパス) のタプル

        Raises:
            DocumentGenerationError: ドキュメント生成に失敗した場合
        """
        try:
            logger.info("Starting document generation")
            source_files = self.collector.collect_files()

            # メモリ上にコンテンツを生成
            with io.StringIO() as content_buffer:
                self._write_header(content_buffer, len(source_files))

                for file_path in source_files:
                    self._process_file(content_buffer, file_path)

                content = content_buffer.getvalue()

            # クリップボードにコピーする場合
            if to_clipboard:
                pyperclip.copy(content)
                logger.info("Content copied to clipboard")
                return content, output_file if output_file else None

            # ファイルに出力する場合
            if output_file is None:
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                output_file = f'source_code_{timestamp}.txt'

            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(content)

            logger.info(f"Output written to: {output_file}")
            return output_file

        except Exception as e:
            raise DocumentGenerationError(f"Failed to generate document: {str(e)}")

    def _write_header(self, file: TextIO, total_files: int) -> None:
        """ドキュメントヘッダーを書き込み"""
        file.write(f"# Project Source Code Collection\n")
        file.write(f"# Generated at: {datetime.now().isoformat()}\n")
        file.write(f"# Root directory: {self.root_dir}\n")
        file.write(f"# Total files found: {total_files}\n\n")

    def _process_file(self, output_file: TextIO, file_path: str) -> None:
        """単一ファイルを処理して書き込み"""
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
        """スキップされたファイル情報を書き込み"""
        logger.warning(f"Skipping large file: {rel_path} ({file_size_kb:.1f}KB)")
        output_file.write(f"\n### File: {rel_path}\n")
        output_file.write(
            f"# [SKIPPED] File size ({file_size_kb:.1f}KB) exceeds limit of {self.max_file_size_kb}KB\n\n")

    def _write_file_content(self, output_file: TextIO, file_path: str, rel_path: str) -> None:
        """ファイル内容を書き込み"""
        with open(file_path, 'r', encoding='utf-8') as source_file:
            content = source_file.read()
            output_file.write(f"\n### File: {rel_path}\n")
            output_file.write("```" + os.path.splitext(file_path)[1][1:] + "\n")
            output_file.write(content)
            output_file.write("\n```\n")

    def _write_error_file(self, output_file: TextIO, rel_path: str, error: str) -> None:
        """エラー情報を書き込み"""
        logger.error(f"Error reading file {rel_path}: {error}")
        output_file.write(f"\n### File: {rel_path}\n")
        output_file.write(f"# [ERROR] Failed to read file: {error}\n\n")