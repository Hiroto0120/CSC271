"""Student checker for a2_functions.py
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
import matplotlib.pyplot as plt

try:
    import a2_books as a2
except ImportError:
    pass


PYTA_CONFIG = 'a2_pyta.json'
FILENAME = 'a2_books.py'


CONSTANTS = {
    'BASE_BOOK_URL': 'http://books.toscrape.com/catalogue/',
    'BASE_CATEGORY_URL': 'http://books.toscrape.com/catalogue/category/books/',
    'NAME_TO_CODE': {'Travel': 'travel_2',
                     'Science': 'science_22',
                     'Mystery': 'mystery_3',
                     'Fiction': 'fiction_10',
                     'Historical Fiction': 'historical-fiction_4',
                     'Business': 'business_35',
                     'Biography': 'biography_36',
                     'Thriller': 'thriller_37',
                     'Contemporary': 'contemporary_38',
                     'Short Stories': 'short-stories_45',
                     'Novels': 'novels_46',
                     'Health': 'health_47'},
    'RATINGS': {'One': 1, 'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5}
}


################################################################################
# Test Fixtures
################################################################################

@pytest.fixture
def sample_price_text():
    """Sample price text for testing."""
    return "£19.99"


@pytest.fixture
def sample_avail_text():
    """Sample availability text for testing."""
    return "In stock (19 available)"


@pytest.fixture
def sample_title():
    """Sample book title for testing."""
    return "The Great Adventure: A Novel!"


@pytest.fixture
def sample_category():
    """Sample category name for testing."""
    return "Travel"


@pytest.fixture
def sample_categories():
    """Sample list of categories for testing."""
    return ["Travel", "Science"]


@pytest.fixture
def sample_book_url():
    """Sample book URL for testing."""
    return "http://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html"


@pytest.fixture
def sample_dataframe():
    """Sample DataFrame with book data for plotting."""
    return pd.DataFrame({
        'Title': ['Full Moon over Noahâs Ark: An Odyssey to Mount Ararat and Beyond', 
                  'The Great Railway Bazaar',
                  'Sample Fiction Book'],
        'Category': ['Travel', 'Travel', 'Fiction'],
        'Rating': [4, 1, 5],
        'Price': [49.43, 30.54, 25.00],
        'Availability': [15, 6, 10]
    })


################################################################################
# Test Class
################################################################################

class TestChecker:
    """Test book scraping and analysis functions."""

    def test_extract_price_type(self, sample_price_text):
        """Verify extract_price returns a float."""
        success, result = check_type(
            a2.extract_price,
            [sample_price_text],
            float
        )
        assert success, result

    def test_extract_availability_type(self, sample_avail_text):
        """Verify extract_availability returns an int."""
        success, result = check_type(
            a2.extract_availability,
            [sample_avail_text],
            int
        )
        assert success, result

    def test_reformat_text_type(self, sample_title):
        """Verify reformat_text returns a string."""
        success, result = check_type(
            a2.reformat_text,
            [sample_title],
            str
        )
        assert success, result

    def test_get_quantity_type(self, sample_category):
        """Verify get_quantity returns an int."""
        success, result = check_type(
            a2.get_quantity,
            [sample_category],
            int
        )
        assert success, result

    def test_get_quantity_per_category_type(self, sample_categories):
        """Verify get_quantity_per_category returns a dict."""
        success, result = check_type(
            a2.get_quantity_per_category,
            [sample_categories],
            dict
        )
        assert success, result

    def test_get_book_details_type(self, sample_book_url):
        """Verify get_book_details returns a dict."""
        success, result = check_type(
            a2.get_book_details,
            [sample_book_url],
            dict
        )
        assert success, result

    def test_get_books_in_category_type(self, sample_category):
        """Verify get_books_in_category returns a DataFrame."""
        success, result = check_type(
            a2.get_books_in_category,
            [sample_category],
            pd.DataFrame
        )
        assert success, result

    def test_plot_ratings_by_category_type(self, sample_dataframe):
        """Verify plot_ratings_by_category returns a Figure."""
        success, result = check_type(
            a2.plot_ratings_by_category,
            [sample_dataframe, 'Fiction', 'Travel'],
            plt.Figure
        )
        if success:
            plt.close(result)
        assert success, result

    def test_check_constants(self) -> None:
        """Values of constants."""
        check_constants(CONSTANTS, a2)


################################################################################
# Main Execution
################################################################################

if __name__ == '__main__':
    print(''.center(TARGET_LEN, SEP))
    print(' Start: checking coding style '.center(TARGET_LEN, SEP))
    run_pyta(FILENAME, PYTA_CONFIG)
    print(' End checking coding style '.center(TARGET_LEN, SEP))

    print(' Start: checking type contracts '.center(TARGET_LEN, SEP))
    pytest.main([
        '--show-capture',
        'no',
        '--disable-warnings',
        '--tb=short',
        __file__,
        "--capture=sys",
        "-W",
        "ignore:Module already imported:pytest.PytestWarning"]
    )
    print(' End checking type contracts '.center(TARGET_LEN, SEP))

    print('\nScroll up to see ALL RESULTS:')
    print('  - checking coding style')
    print('  - checking type contract\n')