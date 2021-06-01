# Chat bot
Chatbot based in comments from Reddit comments in December 2017.


## Requirements
- Python 3.9.5
- Poetry
- xz decompressor

## Instructions

1. Download Reddit comments database from 2017/12 [here](http://files.pushshift.io/reddit/comments/RC_2017-12.xz) and extracts it's contents in `reddit_data/2017` directory.
```shell
curl http://files.pushshift.io/reddit/comments/RC_2017-12.xz --output RC_2017-12.xz
xz --decompress RC_2017-12.xz
mv RC_2017-12 reddit_data/2017/RC_2017-12
```

2. Install dependencies and activate virtual environment
```shell
poetry install
poetry shell
```

3. Create table in database

```shell
python 01_create_table.py
```

4. Create database
```shell
python 02_create_db.py
```

5. Split test/train database
```shell
python 03_split_test_train_database.py
```

6. Train model
```shell
python 04_train_model.py
```

7. Run chat
```shell
python 05_chat.py
```
