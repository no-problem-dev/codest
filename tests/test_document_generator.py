import fnmatch
import logging
import pytest
import os
from codest.document_generator import DocumentGenerator

logger = logging.getLogger(__name__)


@pytest.fixture
def temp_project(tmp_path):
    src_dir = tmp_path / 'src'
    src_dir.mkdir()
    (src_dir / 'main.py').write_text('print("Hello")')
    (src_dir / 'large_file.py').write_text('x' * (2 * 1024 * 1024))  # 2MB file
    return tmp_path


def test_generate_document(temp_project):
    generator = DocumentGenerator(str(temp_project), max_file_size_kb=1000)
    output_file = generator.generate('test_output.txt')
    assert os.path.exists(output_file)
    with open(output_file, 'r', encoding='utf-8') as f:
        content = f.read()
        assert '# Project Source Code Collection' in content
        assert 'main.py' in content
        assert 'print("Hello")' in content
        assert '[SKIPPED]' in content and 'large_file.py' in content


# src/codest/gitignore.py の GitIgnoreHandler クラスの should_ignore メソッドを修正
class GitIgnoreHandler:
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
            # ディレクトリパターンの処理
            if pattern.endswith('/'):
                pattern_without_slash = pattern[:-1]
                if pattern_without_slash in path_parts:
                    return True
            # 通常のパターンの処理
            elif fnmatch.fnmatch(rel_path, pattern) or \
                    fnmatch.fnmatch(os.path.basename(path), pattern) or \
                    any(fnmatch.fnmatch(part, pattern) for part in path_parts):
                logger.debug(f"Ignoring file due to .gitignore pattern '{pattern}': {path}")
                return True

        return False