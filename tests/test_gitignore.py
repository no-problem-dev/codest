import pytest
import os
from codest.gitignore import GitIgnoreHandler


@pytest.fixture
def temp_gitignore(tmp_path):
    """Create a temporary .gitignore file for testing"""
    gitignore_content = """
# Comment
*.log
/build/
node_modules/
.DS_Store
"""
    gitignore_path = tmp_path / '.gitignore'
    gitignore_path.write_text(gitignore_content)
    return tmp_path


def test_gitignore_parsing(temp_gitignore):
    """Test if .gitignore patterns are correctly parsed"""
    handler = GitIgnoreHandler(str(temp_gitignore))
    patterns = handler.patterns

    assert '*.log' in patterns
    assert 'build/' in patterns
    assert 'node_modules/' in patterns
    assert '.DS_Store' in patterns


def test_should_ignore(temp_gitignore):
    """Test if files are correctly ignored based on .gitignore patterns"""
    handler = GitIgnoreHandler(str(temp_gitignore))

    # Test various patterns
    assert handler.should_ignore(os.path.join(str(temp_gitignore), 'test.log'))
    assert handler.should_ignore(os.path.join(str(temp_gitignore), 'build', 'output.txt'))
    assert handler.should_ignore(os.path.join(str(temp_gitignore), 'src', 'build', 'output.txt'))
    assert handler.should_ignore(os.path.join(str(temp_gitignore), 'node_modules', 'package.json'))
    assert handler.should_ignore(os.path.join(str(temp_gitignore), '.DS_Store'))

    # Test files that should not be ignored
    assert not handler.should_ignore(os.path.join(str(temp_gitignore), 'src', 'main.py'))
    assert not handler.should_ignore(os.path.join(str(temp_gitignore), 'README.md'))


def test_missing_gitignore():
    """Test behavior when .gitignore file is missing"""
    handler = GitIgnoreHandler('/nonexistent/path')
    assert len(handler.patterns) == 0
    assert not handler.should_ignore('any/file.txt')