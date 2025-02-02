import os
import logging
from typing import List, Set
from .gitignore import GitIgnoreHandler
from .constants import DEFAULT_IGNORE_PATTERNS, DEFAULT_IGNORE_DIRS, DEFAULT_FILE_EXTENSIONS
from .exceptions import FileCollectionError

logger = logging.getLogger(__name__)


class FileCollector:
    def __init__(
            self,
            root_dir: str,
            ignore_patterns: Set[str] = None,
            ignore_dirs: Set[str] = None,
            file_extensions: Set[str] = None
    ):
        """
        FileCollectorの初期化

        Args:
            root_dir (str): 収集対象のルートディレクトリ
            ignore_patterns (Set[str], optional): 無視するパターン
            ignore_dirs (Set[str], optional): 無視するディレクトリ
            file_extensions (Set[str], optional): 収集対象の拡張子
        """
        self.root_dir = os.path.abspath(root_dir)
        self.ignore_patterns = ignore_patterns or DEFAULT_IGNORE_PATTERNS
        self.ignore_dirs = ignore_dirs or DEFAULT_IGNORE_DIRS
        self.file_extensions = file_extensions or DEFAULT_FILE_EXTENSIONS
        self.gitignore = GitIgnoreHandler(self.root_dir)

    def should_ignore(self, path: str) -> bool:
        """
        指定されたパスを無視すべきかを判定

        Args:
            path (str): チェックするパス

        Returns:
            bool: 無視すべき場合はTrue
        """
        parts = path.split(os.sep)

        if any(part in self.ignore_dirs for part in parts):
            logger.debug(f"Ignoring directory: {path}")
            return True

        if any(pattern in path for pattern in self.ignore_patterns):
            logger.debug(f"Ignoring file due to pattern match: {path}")
            return True

        return self.gitignore.should_ignore(path)

    def collect_files(self) -> List[str]:
        """
        ルートディレクトリからソースファイルを収集

        Returns:
            List[str]: 収集されたファイルパスのリスト

        Raises:
            FileCollectionError: ファイル収集に失敗した場合
        """
        if not os.path.exists(self.root_dir):
            raise FileCollectionError(f"Directory not found: {self.root_dir}")

        if not os.path.isdir(self.root_dir):
            raise FileCollectionError(f"Path is not a directory: {self.root_dir}")

        logger.info(f"Starting to collect files from: {self.root_dir}")
        logger.debug(f"File extensions to collect: {self.file_extensions}")

        source_files = []

        try:
            for dirpath, dirnames, filenames in os.walk(self.root_dir):
                logger.debug(f"Scanning directory: {dirpath}")
                if self.should_ignore(dirpath):
                    dirnames.clear()
                    continue

                for filename in filenames:
                    full_path = os.path.join(dirpath, filename)
                    if any(filename.endswith(ext) for ext in self.file_extensions):
                        if not self.should_ignore(full_path):
                            logger.debug(f"Found source file: {full_path}")
                            source_files.append(full_path)

            return sorted(source_files)

        except Exception as e:
            raise FileCollectionError(f"Error collecting files: {str(e)}")
