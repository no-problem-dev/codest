import os
import logging
from typing import List, Set
from .gitignore import GitIgnoreHandler
from .constants import DEFAULT_IGNORE_PATTERNS, DEFAULT_IGNORE_DIRS, DEFAULT_FILE_EXTENSIONS
from .exceptions import FileCollectionError
from .normalize_paths import normalize_paths, is_subdirectory

logger = logging.getLogger(__name__)


class FileCollector:
    def __init__(
            self,
            directories: List[str],
            exclude_dirs: List[str] = None,
            ignore_patterns: Set[str] = None,
            ignore_dirs: Set[str] = None,
            file_extensions: Set[str] = None
    ):
        """
        FileCollectorの初期化

        Args:
            directories (List[str]): 収集対象のディレクトリリスト
            exclude_dirs (List[str], optional): 除外するディレクトリリスト
            ignore_patterns (Set[str], optional): 無視するパターン
            ignore_dirs (Set[str], optional): 無視するディレクトリ
            file_extensions (Set[str], optional): 収集対象の拡張子

        Raises:
            FileCollectionError: ディレクトリが存在しない場合
        """
        # 存在チェックを初期化時に行う
        for directory in directories:
            abs_path = os.path.abspath(directory)
            if not os.path.exists(abs_path):
                raise FileCollectionError(f"Directory not found: {directory}")
            if not os.path.isdir(abs_path):
                raise FileCollectionError(f"Path is not a directory: {directory}")

        self.directories = [os.path.abspath(d) for d in directories]
        self.exclude_dirs = set(os.path.abspath(d) for d in (exclude_dirs or []))
        self.ignore_patterns = ignore_patterns or DEFAULT_IGNORE_PATTERNS
        self.ignore_dirs = ignore_dirs or DEFAULT_IGNORE_DIRS
        self.file_extensions = file_extensions or DEFAULT_FILE_EXTENSIONS

        # GitIgnoreHandlerの初期化
        self.gitignore_handlers = {}
        for directory in self.directories:
            try:
                self.gitignore_handlers[directory] = GitIgnoreHandler(directory)
            except Exception as e:
                logger.warning(f"Failed to initialize GitIgnoreHandler for {directory}: {e}")
                self.gitignore_handlers[directory] = GitIgnoreHandler(".")

    def should_ignore(self, path: str, base_dir: str) -> bool:
        """指定されたパスを無視すべきかを判定"""
        abs_path = os.path.abspath(path)

        # 除外ディレクトリのチェック
        if any(os.path.commonpath([exclude_dir, abs_path]) == exclude_dir
               for exclude_dir in self.exclude_dirs):
            logger.debug(f"Ignoring excluded directory: {path}")
            return True

        parts = path.split(os.sep)

        if any(part in self.ignore_dirs for part in parts):
            logger.debug(f"Ignoring directory: {path}")
            return True

        if any(pattern in path for pattern in self.ignore_patterns):
            logger.debug(f"Ignoring file due to pattern match: {path}")
            return True

        return self.gitignore_handlers[base_dir].should_ignore(path)

    def collect_files(self) -> List[str]:
        """
        ファイルを収集

        Returns:
            List[str]: 重複のない収集されたファイルパスのリスト
        """
        collected_files = set()  # 重複を防ぐためにsetを使用

        for directory in self.directories:
            if not os.path.exists(directory):
                raise FileCollectionError(f"Directory not found: {directory}")

            if not os.path.isdir(directory):
                raise FileCollectionError(f"Path is not a directory: {directory}")

            logger.info(f"Starting to collect files from: {directory}")
            logger.debug(f"File extensions to collect: {self.file_extensions}")

            try:
                for dirpath, dirnames, filenames in os.walk(directory):
                    logger.debug(f"Scanning directory: {dirpath}")
                    if self.should_ignore(dirpath, directory):
                        dirnames.clear()
                        continue

                    for filename in filenames:
                        full_path = os.path.abspath(os.path.join(dirpath, filename))
                        if any(filename.endswith(ext) for ext in self.file_extensions):
                            if not self.should_ignore(full_path, directory):
                                logger.debug(f"Found source file: {full_path}")
                                collected_files.add(full_path)

            except Exception as e:
                raise FileCollectionError(f"Error collecting files in {directory}: {str(e)}")

        return sorted(collected_files)