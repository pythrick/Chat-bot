from chatbot.services import create_connection, get_pairs_count, select_pairs


def write_files(name: str):
    with open(f"{name}.from", "a") as test_from_file, open(f"{name}.to", "a") as test_to_file:
        for question, answer in pairs:
            test_from_file.write(f"{question}\n")
            test_to_file.write(f"{answer}\n")


if __name__ == '__main__':
    DB_NAME = "2017-12"
    conn, cur = create_connection(DB_NAME)
    pairs_count = get_pairs_count(conn, cur)
    test_size = int(pairs_count * 0.2)
    limit = 10000
    offset = 0
    while pairs := select_pairs(conn, cur, limit, offset):
        if offset <= test_size:
            write_files("test")
        else:
            write_files("train")
        offset += limit


