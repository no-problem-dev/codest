# tests/test_path_handling.py
import os
import pytest
from codest.normalize_paths import normalize_paths, is_subdirectory
from codest.file_collector import FileCollector


@pytest.fixture
def temp_project_structure(tmp_path):
    """複雑なプロジェクト構造を作成するフィクスチャ"""
    # メインディレクトリ
    src = tmp_path / 'src'
    src.mkdir()
    (src / 'main.py').write_text('print("main")')
    (src / 'utils.py').write_text('def util(): pass')

    # サブディレクトリ
    frontend = src / 'frontend'
    frontend.mkdir()
    (frontend / 'app.js').write_text('console.log("app")')

    # テストディレクトリ
    tests = tmp_path / 'tests'
    tests.mkdir()
    (tests / 'test_main.py').write_text('def test_main(): pass')

    # buildディレクトリ（除外対象）
    build = tmp_path / 'build'
    build.mkdir()
    (build / 'output.txt').write_text('build output')

    return tmp_path


def test_normalize_paths_basic():
    """基本的なパス正規化のテスト"""
    paths = ['src', 'tests', 'src']
    normalized = normalize_paths(paths)
    assert len(normalized) == 2  # 重複が排除される
    assert all(os.path.isabs(p) for p in normalized)  # すべて絶対パス


def test_normalize_paths_with_current_dir(temp_project_structure):
    """カレントディレクトリを含むパスの正規化"""
    os.chdir(str(temp_project_structure))
    paths = ['.', 'src']
    normalized = normalize_paths(paths)
    assert len(normalized) == 2  # '.'とsrcは別のパスとして扱われる
    assert normalized[0] == str(temp_project_structure)  # カレントディレクトリ
    assert normalized[1] == os.path.join(str(temp_project_structure), 'src')  # srcディレクトリ


def test_normalize_paths_with_parent_dirs(temp_project_structure):
    """親子関係のあるディレクトリの正規化"""
    src_path = str(temp_project_structure / 'src')
    frontend_path = str(temp_project_structure / 'src' / 'frontend')

    paths = [src_path, frontend_path]
    normalized = normalize_paths(paths)
    assert len(normalized) == 1  # 親ディレクトリのみ残る
    assert normalized[0] == src_path


def test_normalize_paths_with_relative_paths(temp_project_structure):
    """相対パスの正規化"""
    os.chdir(str(temp_project_structure))
    paths = ['./src', 'src']
    normalized = normalize_paths(paths)
    assert len(normalized) == 1  # 同じパスを指している場合は1つにまとめられる
    assert normalized[0] == os.path.join(str(temp_project_structure), 'src')


def test_is_subdirectory_cases(temp_project_structure):
    """is_subdirectoryの各ケースのテスト"""
    root = str(temp_project_structure)
    src = str(temp_project_structure / 'src')
    frontend = str(temp_project_structure / 'src' / 'frontend')
    tests = str(temp_project_structure / 'tests')

    # 直接の親子関係
    assert is_subdirectory(root, src)
    assert is_subdirectory(src, frontend)

    # 間接的な親子関係
    assert is_subdirectory(root, frontend)

    # 親子関係のない場合
    assert not is_subdirectory(src, tests)
    assert not is_subdirectory(tests, src)

    # 同じディレクトリ
    assert not is_subdirectory(src, src)


def test_file_collector_multiple_dirs(temp_project_structure):
    """FileCollectorの複数ディレクトリ処理のテスト"""
    root = str(temp_project_structure)
    src = str(temp_project_structure / 'src')
    tests = str(temp_project_structure / 'tests')

    # 重複を含む指定
    collector = FileCollector([root, src, root, tests])
    files = collector.collect_files()

    # ファイル数の検証
    assert len(files) == 4  # main.py, utils.py, app.js, test_main.py

    # 各ファイルが含まれていることを確認
    file_names = [os.path.basename(f) for f in files]
    assert 'main.py' in file_names
    assert 'utils.py' in file_names
    assert 'app.js' in file_names
    assert 'test_main.py' in file_names


def test_file_collector_with_excludes(temp_project_structure):
    """FileCollectorの除外ディレクトリ処理のテスト"""
    root = str(temp_project_structure)
    src_frontend = str(temp_project_structure / 'src' / 'frontend')
    tests = str(temp_project_structure / 'tests')

    # 除外ディレクトリを指定
    collector = FileCollector(
        directories=[root],
        exclude_dirs=[src_frontend, tests]
    )
    files = collector.collect_files()

    # 除外されたファイルの確認
    file_names = [os.path.basename(f) for f in files]
    assert 'main.py' in file_names
    assert 'utils.py' in file_names
    assert 'app.js' not in file_names  # frontend内のファイルは除外される
    assert 'test_main.py' not in file_names  # tests内のファイルは除外される


def test_file_collector_with_dot_dirs(temp_project_structure):
    """FileCollectorのドット表記ディレクトリの処理テスト"""
    os.chdir(str(temp_project_structure))

    # ドット表記を含むパス指定
    collector = FileCollector(
        directories=['.', './src']
    )
    files = collector.collect_files()

    # すべてのファイルが含まれることを確認
    file_names = [os.path.basename(f) for f in files]
    assert 'main.py' in file_names
    assert 'utils.py' in file_names
    assert 'app.js' in file_names
    assert 'test_main.py' in file_names


def test_file_collector_gitignore_handling(temp_project_structure):
    """FileCollectorの.gitignore処理テスト"""
    # .gitignoreファイルの作成
    gitignore_content = """
    *.log
    build/
    src/frontend/
    """
    gitignore_path = temp_project_structure / '.gitignore'
    gitignore_path.write_text(gitignore_content)

    # テスト用のログファイル作成
    (temp_project_structure / 'debug.log').write_text('log content')

    collector = FileCollector([str(temp_project_structure)])
    files = collector.collect_files()

    # .gitignoreの設定が反映されていることを確認
    file_names = [os.path.basename(f) for f in files]
    assert 'debug.log' not in file_names
    assert 'app.js' not in file_names  # frontend/内のファイル
    assert 'main.py' in file_names  # 通常のソースファイル