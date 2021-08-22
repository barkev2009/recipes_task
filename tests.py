from src.library_tables.table_navigation import most_popular_author, fowlest_reader


def test_most_popular_author_2021():
    assert 'J.K. Rowling' in most_popular_author(2021)


def test_most_popular_author_2020():
    assert 'Bram Stoker' in most_popular_author(2020)


def test_fowlest_reader():
    assert 'Greg Kovshov' in fowlest_reader()
