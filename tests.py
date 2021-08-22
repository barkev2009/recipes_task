from src.library_tables.table_navigation import most_popular_author, foulest_reader


def test_most_popular_author_2021():
    assert 'J.K. Rowling' in most_popular_author(2021)


def test_most_popular_author_2020():
    assert 'Bram Stoker' in most_popular_author(2020)


def test_foulest_reader():
    assert 'Greg Kovshov' in foulest_reader()
