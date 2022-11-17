from pathlib import Path

import pytest


@pytest.fixture
def test_data_directory() -> Path:
    return Path(__file__).parent / 'test_data'


@pytest.fixture
def align_log_file(test_data_directory) -> Path:
    return test_data_directory / 'align.log'


@pytest.fixture
def xf_file(test_data_directory) -> Path:
    return test_data_directory / 'xf_file.xf'