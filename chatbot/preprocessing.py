
def is_acceptable(data: str) -> bool:
    acceptable_conditions = (
        len(data.split(" ")) <= 50,
        len(data) > 1,
        len(data) <= 1000,
        data != "[deleted]",
        data != "[removed]",
    )
    return all(acceptable_conditions)


async def sql_insert(
    parent_id: str,
    comment_id: str,
    comment: str,
    subreddit: str,
    time_utc: int,
    score: int,
) -> tuple:
    sql = """
        INSERT INTO 
            parent_reply (
                parent_id, 
                comment_id,
                comment
            ) 
        VALUES (?, ?, ?)"""

    return sql, (parent_id, comment_id, comment)


async def persist_transactions(db, sql_transactions):
    await db.execute("BEGIN TRANSACTION")
    for s, p in sql_transactions:
        try:
            await db.execute(s, p)
        except Exception as e:
            print(s, p, e)
    await db.commit()
    print(f"{len(sql_transactions)} rows affected.")