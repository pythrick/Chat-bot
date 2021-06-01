from chatbot.services import create_table, create_connection

DB_NAME = "2017-12"


if __name__ == '__main__':
    # create connection
    conn, cur = create_connection(DB_NAME)

    # create table
    create_table(conn, cur)
