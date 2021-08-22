from library.utils.utils import PostgreSQLStarter


def most_popular_author():
    cursor.execute("""  SELECT 
                            author, count(author) 
                        FROM 
                            students 
                        JOIN 
                            books
                        ON
                            students.book_taken_id=books.id 
                        GROUP BY 
                            author 
                        ORDER BY 
                            count(author) 
                            DESC
                        """)
    return cursor.fetchone()
    # print(*cursor.fetchall(), sep='\n')


def fowlest_reader():
    cursor.execute("""  SELECT 
                            SUM(
                                GREATEST(
                                    ROUND(
                                        EXTRACT(EPOCH FROM date_returned - date_taken)/(60 * 60 * 24) - trial_period
                                        ), 
                                        0
                                    )
                                ), 
                            TRIM(CONCAT(first_name, ' ', last_name))
                        FROM 
                            students 
                        GROUP BY
                            TRIM(CONCAT(first_name, ' ', last_name))
                        ORDER BY
                           SUM(
                                GREATEST(
                                    ROUND(
                                        EXTRACT(EPOCH FROM date_returned - date_taken)/(60 * 60 * 24) - trial_period
                                        ), 
                                        0
                                    )
                                )
                            DESC 
                    """)
    return cursor.fetchone()


conn, cursor = PostgreSQLStarter().get_connection_and_cursor()
if __name__ == '__main__':
    most_popular_author()
    fowlest_reader()