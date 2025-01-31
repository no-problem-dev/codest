import pytest
from codest.collector import collect_source_files, create_source_document
import os
import tempfile
import shutil
from pathlib import Path


@pytest.fixture
def temp_dir():
    temp_dir = tempfile.mkdtemp()
    yield temp_dir
    shutil.rmtree(temp_dir)


def create_test_files(base_dir):
    """テスト用のファイルを作成"""
    # Pythonファイル
    Path(base_dir, "test.py").write_text("print('test')")
    # 隠しファイル
    Path(base_dir, ".hidden").write_text("hidden")
    # サブディレクトリとファイル
    sub_dir = Path(base_dir, "subdir")
    sub_dir.mkdir()
    Path(sub_dir, "sub.py").write_text("print('sub')")
    # .gitignore
    Path(base_dir, ".gitignore").write_text("*.ignore\n")
    # 無視すべきファイル
    Path(base_dir, "test.ignore").write_text("ignore me")


def test_collect_source_files_empty_directory(temp_dir):
    """空のディレクトリからファイル収集をテスト"""
    files = collect_source_files(temp_dir)
    assert len(files) == 0


def test_collect_source_files_with_content(temp_dir):
    """ファイルが存在するディレクトリからの収集をテスト"""
    create_test_files(temp_dir)
    files = collect_source_files(temp_dir)

    # 相対パスに変換してチェック
    rel_paths = [os.path.relpath(f, temp_dir) for f in files]
    assert sorted(rel_paths) == sorted(['test.py', os.path.join('subdir', 'sub.py')])


def test_create_source_document(temp_dir):
    """ドキュメント生成をテスト"""
    create_test_files(temp_dir)
    output_file = os.path.join(temp_dir, "output.txt")

    create_source_document(temp_dir, output_file)

    assert os.path.exists(output_file)
    with open(output_file, 'r', encoding='utf-8') as f:
        content = f.read()
        assert "test.py" in content
        assert "sub.py" in content
        assert "print('test')" in content
        assert "print('sub')" in content


def test_gitignore_respect(temp_dir):
    """gitignoreパターンの適用をテスト"""
    create_test_files(temp_dir)
    files = collect_source_files(temp_dir)

    # .ignoreファイルが含まれていないことを確認
    assert not any('test.ignore' in f for f in files)


def test_invalid_directory():
    """無効なディレクトリに対するエラー処理をテスト"""
    with pytest.raises(FileNotFoundError):
        collect_source_files("/path/that/does/not/exist")