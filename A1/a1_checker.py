"""Student checker for a1_functions.py
"""

from checker_generic import (
    check_type,
    check_constants,
    run_pyta,
    TARGET_LEN,
    SEP
)

import pytest
import pandas as pd

try:
    import a1_functions as a1
except ImportError:
    pass


PYTA_CONFIG = 'a1_pyta.json'
FILENAME = 'a1_functions.py'


CONSTANTS = {
    'DATE': 'Date',
    'REGION': 'Region',
    'MODE': 'Mode',
    'VOLUME': 'Volume',
    'PORT_ID': 'Port ID',
    'PORT_NAME': 'Port Name'
}


################################################################################
################################################################################

@pytest.fixture
def raw_region_df():
    """Sample DataFrame with region misspellings."""
    return pd.DataFrame({
        CONSTANTS['REGION']: ['QuÈbec Region', 'Quebec Region', 'Ontario Region'],
        CONSTANTS['VOLUME']: [100, 200, 300]
    })

@pytest.fixture
def raw_volume_df():
    """Sample DataFrame with volume column to rename and clean."""
    return pd.DataFrame({
        CONSTANTS['DATE']: ['2024-01-01', '2024-01-02', '2024-01-03'],
        'Sum of Volume': [100, 200, 300]
    })

@pytest.fixture
def raw_port_df():
    """Sample DataFrame with Port of Entry to split."""
    return pd.DataFrame({
        'Port of Entry': ['123 - Toronto', '456 - Montreal', '789 - Vancouver'],
        'Volume': [100, 200, 300]
    })

@pytest.fixture
def raw_full_df():
    """Sample DataFrame for full cleaning."""
    return pd.DataFrame({
        CONSTANTS['DATE']: ['2024-01-01', '2024-01-02', '2024-01-03'],
        CONSTANTS['REGION']: ['QuÈbec Region', 'Ontario Region', 'Quebec Region'],
        'Port of Entry': ['123 - Toronto', '456 - Montreal', '789 - Vancouver'],
        'Sum of Volume': [100, 200, 300]
    })


@pytest.fixture
def analysis_df():
    """Sample DataFrame, fully cleaned."""
    return pd.DataFrame({
        CONSTANTS['DATE']: pd.to_datetime(['2023-01-15', '2023-02-20', '2023-03-10',
                              '2024-01-10', '2024-02-14', '2024-03-05']),
        CONSTANTS['REGION']: ['Ontario', 'Ontario', 'Québec', 'Québec', 'Québec', 'Ontario'],
        CONSTANTS['PORT_ID']: [123, 456, 789, 123, 789, 456],
        CONSTANTS['PORT_NAME']: ['Toronto', 'Ottawa', 'Montreal', 'Toronto', 'Montreal', 'Ottawa'],
        CONSTANTS['VOLUME']: pd.array([100, 200, 0, 150, 300, 250], dtype='Int64')
    })

################################################################################
################################################################################

class TestChecker:
    """Test data processing functions."""

    def test_clean_region_type(self, raw_region_df):
        """Verify clean_region returns None."""
        success, result = check_type(a1.clean_region, [raw_region_df], type(None))
        assert success, result

    def test_clean_volume_type(self, raw_volume_df):
        """Verify clean_volume returns None."""
        success, result = check_type(a1.clean_volume, [raw_volume_df], type(None))
        assert success, result

    def test_clean_port_type(self, raw_port_df):
        """Verify clean_port returns None."""
        success, result = check_type(a1.clean_port, [raw_port_df], type(None))
        assert success, result

    def test_clean_data_type(self, raw_full_df):
        """Verify clean_data returns None."""
        success, result = check_type(a1.clean_data, [raw_full_df], type(None))
        assert success, result

    def test_filter_with_volume_type(self, analysis_df):
        """Verify filter_by_volume returns a DataFrame."""
        success, result = check_type(
            a1.filter_with_volume,
            [analysis_df, CONSTANTS['REGION'], 'Ontario', 100],
            pd.DataFrame
        )
        assert success, result

    def test_get_mean_volume_by_type(self, analysis_df):
        """Verify get_mean_volume_by returns a Series."""
        success, result = check_type(
            a1.get_mean_volume_by,
            [analysis_df, CONSTANTS['REGION']],
            pd.Series
        )
        assert success, result

    def test_get_top_n_by_volume_type(self, analysis_df):
        """Verify get_top_n_by_volume returns a Series."""
        success, result = check_type(
            a1.get_top_n_by_volume,
            [analysis_df, CONSTANTS['REGION'], 1],
            pd.Series
        )
        assert success, result

    def test_compute_volume_by_type(self, analysis_df):
        """Verify compute_volume_by_time returns a Series."""
        success, result = check_type(
            a1.compute_volume_by_time,
            [analysis_df, CONSTANTS['REGION'], 2024, -1],
            pd.Series
        )
        assert success, result

    def test_calculate_volume_change_type(self, analysis_df):
        """Verify calculate_volume_change returns a Series."""
        success, result = check_type(
            a1.calculate_volume_change,
            [analysis_df, CONSTANTS['REGION'], 2023, 2024, -1, -1],
            pd.Series
        )
        assert success, result

    def test_check_constants(self) -> None:
        """Values of constants."""
        check_constants(CONSTANTS, a1)

################################################################################
################################################################################

print(''.center(TARGET_LEN, SEP))
print(' Start: checking coding style '.center(TARGET_LEN, SEP))
run_pyta(FILENAME, PYTA_CONFIG)
print(' End checking coding style '.center(TARGET_LEN, SEP))

print(' Start: checking type contracts '.center(TARGET_LEN, SEP))
pytest.main([__file__, '-v'])
print(' End checking type contracts '.center(TARGET_LEN, SEP))

print('\nScroll up to see ALL RESULTS:')
print('  - checking coding style')
print('  - checking type contract\n')
