from src.table_navigation import most_popular_author, fowlest_reader


def test_most_popular_author():
    assert 'J.K. Rowling' in most_popular_author()


def test_fowlest_reader():
    assert 'Greg Kovshov' in fowlest_reader()
