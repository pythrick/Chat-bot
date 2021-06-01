import os
import multiprocessing as mp
from contextlib import suppress

import orjson

from chatbot.preprocessing import is_acceptable
from chatbot.services import create_connection, create_indexes

CORES = mp.cpu_count()
FILE_PATH = "reddit_data/2017/RC_2017-12"
DB_NAME = "2017-12"


def process(line: str):
    row = orjson.loads(line)
    comment_id = row["id"].split("_")[-1]
    parent_id = row["parent_id"].split("_")[-1]
    comment = row["body"].replace("\n", " ").replace("\r", " ").replace('"', "'")
    score = row["score"]

    if not is_acceptable(comment) or score <= 1:
        raise ValueError("Invalid line")

    sql = """
        INSERT INTO 
            parent_reply (
                parent_id, 
                comment_id,
                comment
            ) 
        VALUES (?, ?, ?)"""

    return sql, (parent_id, comment_id, comment)


def process_wrapper(chunk_start, chunk_size):
    conn, cur = create_connection(DB_NAME)
    cur.execute("BEGIN TRANSACTION")
    with open(FILE_PATH) as f:
        f.seek(chunk_start)
        lines = f.read(chunk_size).splitlines()
        for line in lines:
            with suppress(ValueError):
                sql, params = process(line)
                cur.execute(sql, params)
    conn.commit()


def generate_chunk_file(file_name, size=1024 * 1024):
    file_end = os.path.getsize(file_name)
    with open(file_name, "rb") as f:
        chunk_end = f.tell()
        while True:
            chunk_start = chunk_end
            f.seek(size, 1)
            f.readline()
            chunk_end = f.tell()
            yield chunk_start, chunk_end - chunk_start
            if chunk_end > file_end:
                break


if __name__ == '__main__':
    # init objects
    pool = mp.Pool(CORES)
    jobs = []

    # create jobs
    for ck_start, ck_size in generate_chunk_file(FILE_PATH):
        jobs.append(pool.apply_async(process_wrapper, (ck_start, ck_size)))

    # wait for all jobs to finish
    for job in jobs:
        job.get()

    # clean up
    pool.close()

    conn, cur = create_connection(DB_NAME)
    create_indexes(conn, cur)
