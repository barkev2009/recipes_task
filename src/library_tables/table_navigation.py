from src.utils import PostgreSQLStarter


def most_popular_author(year):
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


def fowlest_reader():
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
    print(fowlest_reader())
