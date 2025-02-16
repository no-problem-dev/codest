import os
import io
import logging
from datetime import datetime
from typing import Union, TextIO, Tuple, List
import pyperclip
from .file_collector import FileCollector
from .exceptions import DocumentGenerationError
from .constants import MARKDOWN_LANGUAGE_MAP

logger = logging.getLogger(__name__)


class DocumentGenerator:
    def __init__(
            self,
            directories: Union[str, List[str]],
            exclude_dirs: List[str] = None,
            max_file_size_kb: int = 1000,
            collector: FileCollector = None
    ):
        """
        DocumentGeneratorの初期化

        Args:
            directories (Union[str, List[str]]): プロジェクトのディレクトリまたはディレクトリリスト
            exclude_dirs (List[str], optional): 除外するディレクトリリスト
            max_file_size_kb (int, optional): 最大ファイルサイズ（KB）
            collector (FileCollector, optional): カスタムFileCollector
        """
        if isinstance(directories, str):
            directories = [directories]

        self.directories = [os.path.abspath(d) for d in directories]
        self.max_file_size_kb = max_file_size_kb
        self.collector = collector or FileCollector(
            directories=directories,
            exclude_dirs=exclude_dirs
        )

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
                output_file = f'source_code_{timestamp}.md'  # 拡張子を.mdに変更

            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(content)

            logger.info(f"Output written to: {output_file}")
            return output_file

        except Exception as e:
            raise DocumentGenerationError(f"Failed to generate document: {str(e)}")

    def _write_header(self, file: TextIO, total_files: int) -> None:
        """
        ドキュメントヘッダーを書き込み

        Args:
            file (TextIO): 出力先のファイルオブジェクト
            total_files (int): 収集されたファイルの総数
        """
        # タイトルセクション
        file.write("# Source Code Collection\n\n")

        # メタ情報セクション
        file.write("## Meta Information\n\n")
        file.write(f"- **Generated at**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        file.write(f"- **Total files**: {total_files}\n")

        # ディレクトリ情報セクション
        file.write("\n## Target Directories\n\n")
        for directory in self.directories:
            file.write(f"- `{directory}`\n")

        # セパレータ
        file.write("\n---\n\n")
        file.write("## Source Files\n\n")

    def _process_file(self, output_file: TextIO, file_path: str) -> None:
        """
        単一ファイルを処理して書き込み

        Args:
            output_file (TextIO): 出力先のファイルオブジェクト
            file_path (str): 処理対象のファイルパス
        """
        # ファイルパスを最も近い収集対象ディレクトリからの相対パスで表示
        shortest_rel_path = None
        shortest_prefix_len = float('inf')

        for directory in self.directories:
            try:
                rel_path = os.path.relpath(file_path, directory)
                prefix_len = len(os.path.commonpath([directory, file_path]))
                if prefix_len < shortest_prefix_len:  # Changed from > to <
                    shortest_rel_path = rel_path
                    shortest_prefix_len = prefix_len
            except ValueError:
                continue

        if shortest_rel_path is None:
            shortest_rel_path = os.path.basename(file_path)  # Use basename as fallback

        logger.debug(f"Processing file: {shortest_rel_path}")

        file_size_kb = os.path.getsize(file_path) / 1024
        if file_size_kb > self.max_file_size_kb:
            self._write_skipped_file(output_file, shortest_rel_path, file_size_kb)
            return

        try:
            self._write_file_content(output_file, file_path, shortest_rel_path)
        except Exception as e:
            self._write_error_file(output_file, shortest_rel_path, str(e))

    def _write_skipped_file(self, output_file: TextIO, rel_path: str, file_size_kb: float) -> None:
        """
        スキップされたファイル情報を書き込み

        Args:
            output_file (TextIO): 出力先のファイルオブジェクト
            rel_path (str): ファイルの相対パス
            file_size_kb (float): ファイルサイズ（KB）
        """
        logger.warning(f"Skipping large file: {rel_path} ({file_size_kb:.1f}KB)")
        output_file.write(f"\n### `{rel_path}`\n\n")
        output_file.write(
            f"> ⚠️ **File skipped**: Size ({file_size_kb:.1f}KB) exceeds limit of {self.max_file_size_kb}KB\n\n")

    def _write_file_content(self, output_file: TextIO, file_path: str, rel_path: str) -> None:
        """
        ファイル内容を書き込み

        Args:
            output_file (TextIO): 出力先のファイルオブジェクト
            file_path (str): ファイルの絶対パス
            rel_path (str): ファイルの相対パス
        """
        with open(file_path, 'r', encoding='utf-8') as source_file:
            content = source_file.read()
            # ファイル名をコードブロックで装飾
            output_file.write(f"\n### `{rel_path}`\n\n")

            # 拡張子を取得
            ext = os.path.splitext(file_path)[1].lower()

            if ext == '.md':
                # マークダウンファイルの場合は特別な処理
                self._write_markdown_content(output_file, content)
            else:
                # 通常のファイルは従来通りの処理
                lang = MARKDOWN_LANGUAGE_MAP.get(ext, ext[1:] if ext else '')
                output_file.write("```" + lang + "\n")
                output_file.write(content)
                output_file.write("\n```\n")

    def _write_markdown_content(self, output_file: TextIO, content: str) -> None:
        """
        マークダウンファイルの内容を書き込み
        コードブロックを適切にエスケープして書き込む

        Args:
            output_file (TextIO): 出力先のファイルオブジェクト
            content (str): マークダウンファイルの内容
        """
        # <details>タグを使用してマークダウンコンテンツを折りたたみ可能にする
        output_file.write("<details>\n<summary>Markdown content (click to expand)</summary>\n\n")

        # マークダウンの内容をコードブロックとして表示
        output_file.write("```markdown\n")
        output_file.write(content)
        output_file.write("\n```\n")

        # レンダリングされたマークダウンを表示
        output_file.write("\nRendered markdown:\n\n")
        output_file.write(content)
        output_file.write("\n</details>\n")

    def _write_error_file(self, output_file: TextIO, rel_path: str, error: str) -> None:
        """
        エラー情報を書き込み

        Args:
            output_file (TextIO): 出力先のファイルオブジェクト
            rel_path (str): ファイルの相対パス
            error (str): エラーメッセージ
        """
        logger.error(f"Error reading file {rel_path}: {error}")
        output_file.write(f"\n### `{rel_path}`\n\n")
        output_file.write(f"> ❌ **Error**: Failed to read file: {error}\n\n")