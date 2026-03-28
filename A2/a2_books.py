"""CSC108: Winter 2026 -- Assignment 2: Books

This code is provided solely for the personal and private use of students
taking the CSC271H1 course at the University of Toronto. Copying for purposes
other than this use is expressly prohibited. All forms of distribution of
this code, whether as given or with any changes, are expressly prohibited.

All of the files in this directory and all subdirectories are:
Copyright (c) 2026 CSC271H1 Teaching Team
"""

import re
import requests
from bs4 import BeautifulSoup
import pandas as pd
import matplotlib.pyplot as plt

############
# Constants
############

BASE_BOOK_URL = 'http://books.toscrape.com/catalogue/'

BASE_CATEGORY_URL = 'http://books.toscrape.com/catalogue/category/books/'

NAME_TO_CODE = {'Travel': 'travel_2', 
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
                'Health': 'health_47'}

RATINGS = {'One': 1,
           'Two': 2,
           'Three': 3,
           'Four': 4,
           'Five': 5}

# Column/key names
UPC = 'UPC'
PRICE = 'Price'
AVAILABILITY = 'Availability'
RATING = 'Rating'
TITLE = 'Title'
CATEGORY = 'Category'

############################
# Provided Helper Functions
############################

def fetch_soup(url: str) -> BeautifulSoup | None:
    """Return a BeautifulSoup object if url is successfully fetched,
    and None otherwise.
    """

    response = requests.get(url)
    if response.status_code == 200:
        return BeautifulSoup(response.text, 'html.parser')
    return None


def get_books_from_categories(category_names: list[str]) -> pd.DataFrame:
    """Return book records for all categories with names in category_names,
    or an empty DataFrame if category_names is empty.

    Precondition: each item in category_names is in NAME_TO_CODE.keys()
    """

    all_records = pd.DataFrame()

    for category_name in category_names:
        df_category = get_books_in_category(category_name)
        all_records = pd.concat([all_records, df_category], ignore_index=True)

    return all_records


#######################################
# Task 1: complete the functions below
#######################################

def extract_price(text: str) -> float:
    """Return the numeric price extracted from text. If no valid price
    is found, return 0.0.

    >>> extract_price('Now only £12.99!')
    12.99
    >>> extract_price('Price not available')
    0.0
    """
    check = re.search(r'£\s*(\d+\.\d{2})', text)
    return float(check.group(1)) if check else 0.0

def extract_availability(text: str) -> int:
    """Return the number of book copies available from text. If no quantity
     is found, return 0.

    >>> extract_availability('In stock (19 available)')
    19
    >>> extract_availability('Out of stock')
    0
    """
    check = re.search(r'(\d+)\s?available', text)
    return int(check.group(1)) if check else 0

def reformat_text(text: str) -> str:
    """Return a new string that is the same as text but with all letters in 
    lowercase, punctuation removed, leading and trailing whitespace removed, 
    and internal whitespace sequences collapsed to a single space.

    >>> reformat_text("    Harry Potter:   The \\n  Philosopher's  Stone\\n\\n")
    'harry potter the philosophers stone'
    """
    text = text.lower()                       
    text = re.sub(r"[^\w\s]", "", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()

def get_quantity(category_name: str) -> int:
    """Return the number of books in the category named category_name, 
    or -1 if the request is unsuccessful.
    
    Precondition: category_name in NAME_TO_CODE.keys()

    >>> get_quantity('Business')
    12
    """

    # Starter code
    url = BASE_CATEGORY_URL + NAME_TO_CODE[category_name]
    soup = fetch_soup(url)
    if soup == None:
        return -1

    # Complete the function
    form = soup.find("form", class_="form-horizontal")
    if form is None:
        return -1
    strong = form.find("strong")
    return int(strong.text.strip()) if strong else -1

def get_quantity_per_category(category_names: list[str]) -> dict[str, int]:
    """Return a dictionary where the keys are the category names from
    category_names the corresponding values are the number of books in
    each category.
     
    Precondition: each item in category_names is in NAME_TO_CODE.keys()

    >>> result = get_quantity_per_category(['Mystery', 'Travel'])
    >>> result == {'Mystery': 32, 'Travel': 11}
    True
    """
    result = {}

    for name in category_names:
        result[name] = get_quantity(name)

    return result


def get_book_details(book_url: str) -> dict:
    """Return a dictionary with keys named according to the constants UPC,
    PRICE, and AVAILABILITY and values corresponding to the data at the url
    book_url, or -1 if data cannot be fetched from book_url.

    >>> url = 'https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html'
    >>> result = get_book_details(url)
    >>> result == {'UPC': 'a897fe39b1053632', 'Price': 51.77, 'Availability': 22}
    True
    """

    # Starter code
    soup = fetch_soup(book_url)
    if soup == None:
        return -1
    
    # Complete the function
    table = soup.find('table')
    rows = table.find_all('tr')

    upc = ''
    for row in rows:
        header = row.find('th').text.strip()
        if header == 'UPC':
            upc = row.find('td').text.strip()

    price_text = soup.find('p', class_='price_color').text
    price = extract_price(price_text)

    availability_text = soup.find('p', class_='instock availability').text
    availability = extract_availability(availability_text)

    return {
        UPC: upc,
        PRICE: price,
        AVAILABILITY: availability
    }

def get_books_in_category(category_name: str) -> pd.DataFrame:
    """Return a pandas DataFrame with columns UPC, PRICE, AVAILABILITY,
    RATING, TITLE, and CATEGORY, and entries for all books on the first
    webpage for the category named category_name, or an empty DataFrame
    if the url for the category page is not successfully fetched.
    """
    
    # Starter code
    soup = fetch_soup(BASE_CATEGORY_URL + NAME_TO_CODE[category_name])
    if soup == None:
        return pd.DataFrame()

    # Complete the function
    rating_map = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}
    records = []

    for article in soup.select("article.product_pod"):
        a_tag = article.find("h3").find("a")
        title = a_tag.get("title", "").strip()

        rating_tag = article.find("p", class_="star-rating")
        rating_word = next((c for c in rating_tag.get("class", []) if c != "star-rating"), "")
        rating = rating_map.get(rating_word, 0)

        book_url = urljoin("https://books.toscrape.com/", a_tag.get("href", ""))

        details = get_book_details(book_url)
        if details == -1:
            continue

        records.append({
            UPC: details[UPC],
            PRICE: details[PRICE],
            AVAILABILITY: details[AVAILABILITY],
            RATING: rating,
            TITLE: title,
            CATEGORY: category_name
        })

    return pd.DataFrame(records, columns=[UPC, PRICE, AVAILABILITY, RATING, TITLE, CATEGORY])

######################################
# Task 2: complete the function below
######################################

def plot_ratings_by_category(df: pd.DataFrame,
                             name1: str,
                             name2: str) -> plt.Figure:
    """Return a figure containing side-by-side histograms of book ratings for
    the two book categories from df with names name1 and name2.
    """
    r1 = df[df[CATEGORY] == name1][RATING]
    r2 = df[df[CATEGORY] == name2][RATING]

    fig, axes = plt.subplots(1, 2, figsize=(12, 5), sharey=True)

    bins = [0.5, 1.5, 2.5, 3.5, 4.5, 5.5]

    axes[0].hist(r1, bins=bins, color="pink", edgecolor="white")
    axes[0].set_title(name1)
    axes[0].set_xlabel("Rating (Stars)")
    axes[0].set_ylabel("Number of Books")
    axes[0].set_xticks([1, 2, 3, 4, 5])

    axes[1].hist(r2, bins=bins, color="brown", edgecolor="white")
    axes[1].set_title(name2)
    axes[1].set_xlabel("Rating (Stars)")
    axes[1].set_xticks([1, 2, 3, 4, 5])

    fig.suptitle("Rating Distribution by Category")

    return fig

if __name__ == '__main__':
    pass

    import doctest
    doctest.testmod()