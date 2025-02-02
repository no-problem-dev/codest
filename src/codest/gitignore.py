import os
import fnmatch
import logging
from typing import Set
from .exceptions import GitIgnoreError

logger = logging.getLogger(__name__)


class GitIgnoreHandler:
    def __init__(self, root_dir: str):
        """
        GitIgnoreHandlerの初期化

        Args:
            root_dir (str): プロジェクトのルートディレクトリ
        """
        self.root_dir = root_dir
        self.patterns = self._parse_gitignore()

    def _parse_gitignore(self) -> Set[str]:
        """
        .gitignoreファイルを解析してパターンのセットを返す

        Returns:
            Set[str]: 無視パターンのセット

        Raises:
            GitIgnoreError: .gitignoreの解析に失敗した場合
        """
        patterns = set()
        gitignore_path = os.path.join(self.root_dir, '.gitignore')

        if not os.path.exists(gitignore_path):
            logger.debug("No .gitignore file found")
            return patterns

        try:
            with open(gitignore_path, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#'):
                        # パターンの正規化
                        if line.startswith('/'):
                            line = line[1:]
                        patterns.add(line)

            logger.debug(f"Loaded {len(patterns)} patterns from .gitignore")
            return patterns

        except Exception as e:
            raise GitIgnoreError(f"Failed to parse .gitignore: {str(e)}")

    def should_ignore(self, path: str) -> bool:
        """
        指定されたパスが.gitignoreパターンによって無視すべきかを判定

        Args:
            path (str): チェックするパス

        Returns:
            bool: 無視すべき場合はTrue
        """
        rel_path = os.path.relpath(path, self.root_dir)
        path_parts = rel_path.split(os.sep)

        for pattern in self.patterns:
            # ディレクトリパターン（末尾が/）の処理
            if pattern.endswith('/'):
                pattern_name = pattern.rstrip('/')
                # パスの各部分でマッチをチェック
                for part in path_parts:
                    if fnmatch.fnmatch(part, pattern_name):
                        return True
            else:
                # ファイルパターンの処理
                # 1. 完全パスでのマッチ
                if fnmatch.fnmatch(rel_path, pattern):
                    return True
                # 2. ベースネームでのマッチ（ディレクトリを含まないパターン）
                if '/' not in pattern and fnmatch.fnmatch(os.path.basename(path), pattern):
                    return True
                # 3. パスの一部としてのマッチ
                for part in path_parts:
                    if fnmatch.fnmatch(part, pattern):
                        return True

        return False