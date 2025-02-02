import pytest
import os
from codest.file_collector import FileCollector
from codest.exceptions import FileCollectionError


@pytest.fixture
def temp_project(tmp_path):
    # Create test project structure
    (tmp_path / 'src').mkdir()
    (tmp_path / 'src' / 'main.py').write_text('print("Hello")')
    (tmp_path / 'src' / 'test.py').write_text('def test(): pass')
    (tmp_path / 'build').mkdir()
    (tmp_path / 'build' / 'output.txt').write_text('build artifact')
    return tmp_path


def test_collect_files(temp_project):
    collector = FileCollector(str(temp_project))
    files = collector.collect_files()

    # Convert to relative paths for easier comparison
    rel_paths = [os.path.relpath(f, str(temp_project)) for f in files]
    assert sorted(rel_paths) == sorted([
        os.path.join('src', 'main.py'),
        os.path.join('src', 'test.py')
    ])


def test_ignore_patterns(temp_project):
    collector = FileCollector(
        str(temp_project),
        ignore_patterns={'test.py'}
    )
    files = [os.path.relpath(f, str(temp_project)) for f in collector.collect_files()]
    assert os.path.join('src', 'test.py') not in files
    assert os.path.join('src', 'main.py') in files


def test_invalid_directory():
    with pytest.raises(FileCollectionError):
        collector = FileCollector('/nonexistent/path')
        collector.collect_files()