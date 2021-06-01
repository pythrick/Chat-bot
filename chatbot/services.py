import sqlite3


def create_connection(db_name: str):
    connection = sqlite3.connect(f"{db_name}.db", timeout=60, check_same_thread=False)
    cursor = connection.cursor()
    return connection, cursor


def create_table(conn, cur):
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS parent_reply(
          comment_id TEXT,
          parent_id TEXT, 
          parent TEXT, 
          comment TEXT
        )
    """
    )
    conn.commit()


def create_indexes(conn, cur):
    cur.execute("CREATE INDEX comment_id_idx ON parent_reply (comment_id)")
    cur.execute("CREATE INDEX parent_id_idx ON parent_reply (parent_id)")
    conn.commit()


def link_comments_parents(conn, cur):
    sql = """
    UPDATE parent_reply
    SET parent = (
        SELECT pr.comment 
        FROM parent_reply AS pr 
        WHERE pr.comment_id == parent_reply.parent_id
    )"""
    cur.execute(sql)
    conn.commit()


def delete_orphan_comments(conn, cur):
    sql = "DELETE FROM parent_reply WHERE parent IS NULL"
    cur.execute(sql)
    conn.commit()


def get_pairs_count(conn, cur):
    sql = f"""
    SELECT COUNT(*) 
    FROM parent_reply as p1
    INNER JOIN parent_reply AS p2 ON (p1.parent_id = p2.comment_id)
      """
    cur.execute(sql)
    return cur.fetchone()[0]


def select_pairs(conn, cur, limit: int = 100, offset: int = 0):
    sql = """
    SELECT p2.comment as question, p1.comment as answer
    FROM parent_reply as p1
    INNER JOIN parent_reply AS p2 ON (p1.parent_id = p2.comment_id)
    LIMIT ? OFFSET ?
    """
    cur.execute(sql, (limit, offset))
    return cur.fetchall()
