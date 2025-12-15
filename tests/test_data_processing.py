
import pytest
import pandas as pd
from data_processing import merge_datasets
import os

@pytest.fixture
def create_test_csv_files(tmp_path):
    """Creates dummy CSV files for testing."""
    file1_path = tmp_path / "file1.csv"
    file2_path = tmp_path / "file2.csv"

    df1 = pd.DataFrame({'col1': [1, 2], 'col2': ['a', 'b']})
    df2 = pd.DataFrame({'col1': [3, 4], 'col2': ['c', 'd']})

    df1.to_csv(file1_path, index=False)
    df2.to_csv(file2_path, index=False)

    return str(file1_path), str(file2_path)

def test_merge_datasets(create_test_csv_files, tmp_path):
    """Tests the merging of two CSV files."""
    file1_path, file2_path = create_test_csv_files
    output_path = tmp_path / "merged.csv"

    merge_datasets.main(file1_path, file2_path, str(output_path))

    assert os.path.exists(output_path)

    merged_df = pd.read_csv(output_path)

    expected_df = pd.DataFrame({
        'col1': [1, 2, 3, 4],
        'col2': ['a', 'b', 'c', 'd']
    })

    pd.testing.assert_frame_equal(merged_df, expected_df)
