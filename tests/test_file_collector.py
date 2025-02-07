import os
import pytest
from codest.file_collector import FileCollector
from codest.exceptions import FileCollectionError


@pytest.fixture
def temp_project(tmp_path):
    """テスト用のプロジェクト構造を作成"""
    # ソースディレクトリ
    src = tmp_path / 'src'
    src.mkdir()
    (src / 'main.py').write_text('print("Hello")')
    (src / 'test.py').write_text('def test(): pass')

    # テストディレクトリ
    tests = tmp_path / 'tests'
    tests.mkdir()
    (tests / 'test_main.py').write_text('def test_main(): pass')

    # buildディレクトリ（除外対象）
    build = tmp_path / 'build'
    build.mkdir()
    (build / 'output.txt').write_text('build artifact')

    return tmp_path


def test_collect_single_directory(temp_project):
    """単一ディレクトリからのファイル収集をテスト"""
    collector = FileCollector([str(temp_project / 'src')])
    files = collector.collect_files()

    file_names = [os.path.basename(f) for f in files]
    assert sorted(file_names) == ['main.py', 'test.py']


def test_collect_multiple_directories(temp_project):
    """複数ディレクトリからのファイル収集をテスト"""
    collector = FileCollector([
        str(temp_project / 'src'),
        str(temp_project / 'tests')
    ])
    files = collector.collect_files()

    file_names = [os.path.basename(f) for f in files]
    assert sorted(file_names) == ['main.py', 'test.py', 'test_main.py']


def test_exclude_directories(temp_project):
    """ディレクトリ除外機能のテスト"""
    collector = FileCollector(
        directories=[str(temp_project)],
        exclude_dirs=[str(temp_project / 'tests')]
    )
    files = collector.collect_files()

    # testsディレクトリのファイルが除外されていることを確認
    assert not any('test_main.py' in f for f in files)
    # srcディレクトリのファイルは含まれていることを確認
    assert any('main.py' in f for f in files)


def test_ignore_patterns(temp_project):
    """無視パターンのテスト"""
    # 一時ファイルを作成
    (temp_project / 'src' / '.DS_Store').write_text('')
    (temp_project / 'src' / 'test.pyc').write_text('')

    collector = FileCollector([str(temp_project / 'src')])
    files = collector.collect_files()

    file_names = [os.path.basename(f) for f in files]
    assert '.DS_Store' not in file_names
    assert 'test.pyc' not in file_names
    assert 'main.py' in file_names


def test_file_extensions(temp_project):
    """ファイル拡張子フィルタのテスト"""
    # 異なる拡張子のファイルを作成
    (temp_project / 'src' / 'style.css').write_text('body {}')
    (temp_project / 'src' / 'data.json').write_text('{}')
    (temp_project / 'src' / 'readme.txt').write_text('readme')

    collector = FileCollector(
        [str(temp_project / 'src')],
        file_extensions={'.py', '.css', '.json'}
    )
    files = collector.collect_files()

    file_names = [os.path.basename(f) for f in files]
    assert 'style.css' in file_names
    assert 'data.json' in file_names
    assert 'readme.txt' not in file_names


def test_directory_not_found():
    """存在しないディレクトリのテスト"""
    with pytest.raises(FileCollectionError):
        collector = FileCollector(['/nonexistent/path'])
        collector.collect_files()


def test_empty_directory(tmp_path):
    """空のディレクトリのテスト"""
    collector = FileCollector([str(tmp_path)])
    files = collector.collect_files()
    assert len(files) == 0


def test_nested_directories(temp_project):
    """ネストされたディレクトリ構造のテスト"""
    # ネストされたディレクトリを作成
    nested = temp_project / 'src' / 'nested'
    nested.mkdir()
    (nested / 'nested.py').write_text('print("nested")')

    collector = FileCollector([str(temp_project / 'src')])
    files = collector.collect_files()

    file_names = [os.path.basename(f) for f in files]
    assert 'nested.py' in file_names
    assert 'main.py' in file_names


def test_duplicate_directories(temp_project):
    """重複するディレクトリの指定をテスト"""
    src_path = str(temp_project / 'src')
    collector = FileCollector([src_path, src_path])
    files = collector.collect_files()

    # 重複して収集されていないことを確認
    file_names = [os.path.basename(f) for f in files]
    assert file_names.count('main.py') == 1


def test_overlapping_directories(temp_project):
    """重なり合うディレクトリの指定をテスト"""
    collector = FileCollector([
        str(temp_project),
        str(temp_project / 'src')
    ])
    files = collector.collect_files()

    # ファイルが重複して収集されていないことを確認
    file_names = [os.path.basename(f) for f in files]
    assert file_names.count('main.py') == 1
