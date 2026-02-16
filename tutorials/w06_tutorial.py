import pandas as pd
import requests
from bs4 import BeautifulSoup
import re

def fetch_soup(url: str) -> BeautifulSoup | None:
    """Return a BeautifulSoup object if url is successfully fetched,
    and None otherwise.
    """

    response = requests.get(url)
    if response.status_code == 200:
        return BeautifulSoup(response.text, 'html.parser')
    return None


def get_email_address(url: str) -> str:
    """Return the email address from the website url or an empty string if the
    page does not exist.

    >>> url = 'https://www.cs.toronto.edu/~campbell/csc271/csc271-w06-tutorial.html'
    >>> get_email_address(url)
    'owner@example.com'
    """

    # Starter code
    soup = fetch_soup(url)

    if not soup:
        return ''

    for a in soup.find_all('a', href=True):
        href = a['href']
        if href.lower().startswith('mailto:'):
            email = href.split(':', 1)[1].split('?')[0]
            return email.strip()

    text = soup.get_text(separator=' ')
    match = re.search(r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}', text)
    if match:
        return match.group(0)

    return ''
    


def get_total_episodes(url: str) -> int:
    """Return the total number of episodes for all podcasts listed on the
    webpage url or -1 if the page does not exist.

    >>> url = 'https://www.cs.toronto.edu/~campbell/csc271/csc271-w06-tutorial.html'
    >>> get_total_episodes(url)
    442
    """

    # Starter code
    soup = fetch_soup(url)

    if not soup:
        return -1

    total = 0
    for h in soup.find_all('h2'):
        e = h
        found = False
        for _ in range(5):
            e = e.next_sibling
            if e is None:
                break
            text = ''
            if getattr(e, 'get_text', None):
                text = e.get_text()
            else:
                text = str(e)
            m = re.search(r"(\d+)", text)
            if m:
                total += int(m.group(1))
                found = True
                break
        if not found:
            continue

    return total
    

def get_podcast_names(url: str) -> list[str]:
    """Return a sorted list of the podcast names from the website url or an empty list
    if the page does not exist.

    >>> url = 'https://www.cs.toronto.edu/~campbell/csc271/csc271-w06-tutorial.html'
    >>> get_podcast_names(url)
    ['History Uncovered', 'Science Weekly', 'Tech Today']
    """

    # Starter code
    soup = fetch_soup(url)

    if not soup:
        return []

    names: list[str] = []
    for h in soup.find_all('h2'):
        e = h
        found = False
        for _ in range(5):
            e = e.next_sibling
            if e is None:
                break
            text = ''
            if getattr(e, 'get_text', None):
                text = e.get_text()
            else:
                text = str(e)
            if re.search(r"\d+", text):
                found = True
                break
        if found:
            names.append(h.get_text().strip())

    return sorted(names)
    


if __name__ == '__main__':
    pass
    
    import doctest
    doctest.testmod() 