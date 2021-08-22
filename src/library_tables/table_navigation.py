from src.utils import PostgreSQLStarter


def most_popular_author(year: int) -> tuple:
    """
    Calculates the most popular author within a year

    :param year: a year to search the most popular author in
    :return: a tuple of the most popular author and the number of times
            his/her books were taken by students within a given year
    """
    cursor.execute("""  SELECT
                            author, count(author)
                        FROM
                            students
                        JOIN
                            books
                        ON
                            students.book_taken_id=books.id
                        WHERE
                            EXTRACT(YEAR FROM date_taken) = {}
                        GROUP BY
                            author
                        ORDER BY
                            count(author)
                            DESC
                        """.format(year))
    return cursor.fetchone()


def foulest_reader() -> tuple:
    """
    Calculates "the foulest" reader among students

    :return: a tuple with the full name of "the foulest" reader
            and the number of days of not returning books in time
    """
    sum_of_days_without_return_sub_query = """
        SUM(
            GREATEST(
                ROUND(
                    EXTRACT(EPOCH FROM date_returned - date_taken)/(60 * 60 * 24) - trial_period
                    ),
                    0
                )
            )
        """
    full_names_sub_query = """TRIM(CONCAT(first_name, ' ', last_name))"""
    cursor.execute("""  SELECT
                            {}, {}
                        FROM
                            students
                        GROUP BY
                            {}
                        ORDER BY
                           {}
                            DESC
                    """.format(sum_of_days_without_return_sub_query,
                               full_names_sub_query,
                               full_names_sub_query,
                               sum_of_days_without_return_sub_query))
    return cursor.fetchone()


conn, cursor = PostgreSQLStarter().get_connection_and_cursor()
if __name__ == '__main__':
    print(most_popular_author(2021))
    print(most_popular_author(2020))
    print(foulest_reader())
