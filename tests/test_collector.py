import pytest
from codest.collector import collect_source_files, create_source_document
import os
import tempfile
import shutil

@pytest.fixture
def temp_dir():
    temp_dir = tempfile.mkdtemp()
    yield temp_dir
    shutil.rmtree(temp_dir)

def test_collect_source_files_empty_directory(temp_dir):
    files = collect_source_files(temp_dir)
    assert len(files) == 0

def test
