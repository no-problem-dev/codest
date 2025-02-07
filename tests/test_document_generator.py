import pytest
import os
import pyperclip
from codest.document_generator import DocumentGenerator


@pytest.fixture
def temp_project(tmp_path):
    """テスト用の一時プロジェクト構造を作成"""
    src_dir = tmp_path / 'src'
    src_dir.mkdir()

    # Python ファイルの作成
    (src_dir / 'main.py').write_text('print("Hello")')

    # マークダウンファイルの作成
    (src_dir / 'README.md').write_text('# Test Project\n\n```python\nprint("test")\n```')

    # 大きなファイルの作成（2MB）
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
    output_file = generator.generate('test_output.md')

    # 出力ファイルの存在確認
    assert os.path.exists(output_file)
    assert output_file.endswith('.md')

    # 出力内容の検証
    with open(output_file, 'r', encoding='utf-8') as f:
        content = f.read()
        # ヘッダーの確認
        assert '# Source Code Collection' in content
        assert '## Meta Information' in content
        assert '## Target Directories' in content
        # Python ファイルの確認
        assert 'src/main.py' in content
        assert '```python' in content
        assert 'print("Hello")' in content
        # マークダウンファイルの確認
        assert 'src/README.md' in content
        assert '<details>' in content
        # 大きなファイルがスキップされていることの確認
        assert 'large_file.py' in content
        assert '⚠️ **File skipped**' in content


def test_generate_to_clipboard(temp_project):
    """クリップボードへの出力テスト"""
    generator = DocumentGenerator(
        directories=[str(temp_project)],
        max_file_size_kb=1000
    )
    content, _ = generator.generate(to_clipboard=True)

    # 生成された内容の検証
    assert '# Source Code Collection' in content
    assert '```python' in content
    assert 'print("Hello")' in content
    assert '<details>' in content  # マークダウンファイルの処理を確認

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
    output_file = generator.generate('test_multiple.md')

    with open(output_file, 'r', encoding='utf-8') as f:
        content = f.read()
        # 両方のディレクトリのファイルが含まれていることを確認
        assert 'main.py' in content
        assert 'test_main.py' in content
        # ターゲットディレクトリの確認
        assert f'`{src_dir}`' in content
        assert f'`{test_dir}`' in content


def test_generate_with_excluded_directory(temp_project):
    """除外ディレクトリを指定した生成テスト"""
    test_dir = str(temp_project / 'tests')

    generator = DocumentGenerator(
        directories=[str(temp_project)],
        exclude_dirs=[test_dir],
        max_file_size_kb=1000
    )
    output_file = generator.generate('test_exclude.md')

    with open(output_file, 'r', encoding='utf-8') as f:
        content = f.read()
        # メインのソースファイルは含まれている
        assert 'src/main.py' in content
        # テストファイルは除外されている
        assert 'test_main.py' not in content


def test_generate_with_max_size_zero(temp_project):
    """最大サイズ0でのテスト（すべてのファイルがスキップされる）"""
    generator = DocumentGenerator(
        directories=[str(temp_project)],
        max_file_size_kb=0
    )
    output_file = generator.generate('test_size_zero.md')

    with open(output_file, 'r', encoding='utf-8') as f:
        content = f.read()
        # すべてのファイルセクションにスキップメッセージが含まれていることを確認
        sections = [s for s in content.split('### `') if s.strip()]
        assert len(sections) > 0
        for section in sections:
            if not section.startswith('#'):  # ヘッダーセクションをスキップ
                assert '⚠️ **File skipped**' in section


def test_generate_empty_directory(tmp_path):
    """空のディレクトリでのテスト"""
    generator = DocumentGenerator(
        directories=[str(tmp_path)],
        max_file_size_kb=1000
    )
    output_file = generator.generate('test_empty.md')

    with open(output_file, 'r', encoding='utf-8') as f:
        content = f.read()
        assert '# Source Code Collection' in content
        assert '**Total files**: 0' in content