import pytest
import os
import pyperclip
from codest.document_generator import DocumentGenerator


@pytest.fixture
def temp_project(tmp_path):
    """テスト用の一時プロジェクト構造を作成"""
    src_dir = tmp_path / 'src'
    src_dir.mkdir()

    # main.pyの作成
    (src_dir / 'main.py').write_text('print("Hello")')

    # large_file.pyの作成（2MB）
    (src_dir / 'large_file.py').write_text('x' * (2 * 1024 * 1024))

    # テストファイルの作成
    test_dir = tmp_path / 'tests'
    test_dir.mkdir()
    (test_dir / 'test_main.py').write_text('def test_main(): pass')

    return tmp_path


def test_generate_document(temp_project):
    """ドキュメント生成の基本機能テスト"""
    generator = DocumentGenerator(
        directories=[str(temp_project)],
        max_file_size_kb=1000
    )
    output_file = generator.generate('test_output.txt')

    # 出力ファイルの存在確認
    assert os.path.exists(output_file)

    # 出力内容の検証
    with open(output_file, 'r', encoding='utf-8') as f:
        content = f.read()
        # ヘッダーの確認
        assert '# Project Source Code Collection' in content
        # ファイル内容の確認
        assert 'main.py' in content
        assert 'print("Hello")' in content
        # 大きなファイルがスキップされていることの確認
        assert '[SKIPPED]' in content
        assert 'large_file.py' in content


def test_generate_to_clipboard(temp_project):
    """クリップボードへの出力テスト"""
    generator = DocumentGenerator(
        directories=[str(temp_project)],
        max_file_size_kb=1000
    )
    content, _ = generator.generate(to_clipboard=True)

    # 生成された内容の検証
    assert '# Project Source Code Collection' in content
    assert 'main.py' in content
    assert 'print("Hello")' in content
    assert '[SKIPPED]' in content
    assert 'large_file.py' in content

    # クリップボードの内容を検証
    clipboard_content = pyperclip.paste()
    assert clipboard_content == content


def test_generate_with_multiple_directories(temp_project):
    """複数ディレクトリからの生成テスト"""
    src_dir = str(temp_project / 'src')
    test_dir = str(temp_project / 'tests')

    generator = DocumentGenerator(
        directories=[src_dir, test_dir],
        max_file_size_kb=1000
    )
    output_file = generator.generate('test_multiple.txt')

    with open(output_file, 'r', encoding='utf-8') as f:
        content = f.read()
        # 両方のディレクトリのファイルが含まれていることを確認
        assert 'main.py' in content
        assert 'test_main.py' in content


def test_generate_with_excluded_directory(temp_project):
    """除外ディレクトリを指定した生成テスト"""
    test_dir = str(temp_project / 'tests')

    generator = DocumentGenerator(
        directories=[str(temp_project)],
        exclude_dirs=[test_dir],
        max_file_size_kb=1000
    )
    output_file = generator.generate('test_exclude.txt')

    with open(output_file, 'r', encoding='utf-8') as f:
        content = f.read()
        # メインのソースファイルは含まれている
        assert 'main.py' in content
        # テストファイルは除外されている
        assert 'test_main.py' not in content


def test_generate_with_max_size_zero(temp_project):
    """最大サイズ0でのテスト（すべてのファイルがスキップされる）"""
    generator = DocumentGenerator(
        directories=[str(temp_project)],
        max_file_size_kb=0
    )
    output_file = generator.generate('test_size_zero.txt')

    with open(output_file, 'r', encoding='utf-8') as f:
        content = f.read()
        assert '[SKIPPED]' in content
        assert all(f'[SKIPPED]' in line for line in content.split('\n')
                   if 'File:' in line and not line.startswith('#'))


def test_generate_empty_directory(tmp_path):
    """空のディレクトリでのテスト"""
    generator = DocumentGenerator(
        directories=[str(tmp_path)],
        max_file_size_kb=1000
    )
    output_file = generator.generate('test_empty.txt')

    with open(output_file, 'r', encoding='utf-8') as f:
        content = f.read()
        assert '# Total files found: 0' in content