import sqlite3

import config


def add_id(chat_id):
    with sqlite3.Connection(config.DB_NAME) as connection:
        cursor = connection.cursor()
        query = """
            INSERT INTO CHAT_LANG 
              (chat_id)
            VALUES
              ({0});
        """.format(chat_id)
        cursor.execute(query)
        connection.commit()


def get_lang(chat_id):
    with sqlite3.Connection(config.DB_NAME) as connection:
        cursor = connection.cursor()
        query = """
            SELECT 
              lang_txt
            FROM 
              CHAT_LANG
            WHERE
              chat_id = {0};
        """.format(chat_id)
        response = cursor.execute(query).fetchone()
        if response is None:
            add_id(chat_id)
            return get_lang(chat_id)
        else:
            return response[0]


def set_lang(chat_id, lang_txt):
    with sqlite3.Connection(config.DB_NAME) as connection:
        cursor = connection.cursor()
        query = """
            UPDATE
              CHAT_LANG
            SET
              lang_txt = '{1}'
            WHERE
              chat_id = {0};
        """.format(chat_id, lang_txt,)
        cursor.execute(query)
        connection.commit()


def add_description(request_txt, description_txt):
    with sqlite3.Connection(config.DB_NAME) as connection:
        cursor = connection.cursor()
        cursor.execute("""
            INSERT INTO REQUEST 
              (urban_request_txt, description_txt)
            VALUES
              ('{0}', '{1}'); 
        """.format(request_txt.lower(), description_txt))
        connection.commit()


def update_cnt(request_txt):
    with sqlite3.Connection(config.DB_NAME) as connection:
        cursor = connection.cursor()
        query = """
            UPDATE 
              REQUEST
            SET
              frequency_cnt = frequency_cnt + 1
            WHERE
              urban_request_txt = '{0}';
        """.format(request_txt.lower(),)
        cursor.execute(query)
        connection.commit()


def get_description(request_txt):
    with sqlite3.Connection(config.DB_NAME) as connection:
        cursor = connection.cursor()
        query = """
            SELECT 
              description_txt
            FROM 
              REQUEST
            WHERE
              urban_request_txt = '{0}';
        """.format(request_txt.lower())
        response = cursor.execute(query).fetchone()
        if response is None:
            return None
        else:
            update_cnt(request_txt)
            return response[0]


def get_top(limit):
    with sqlite3.Connection(config.DB_NAME) as connection:
        cursor = connection.cursor()
        query = """
            SELECT 
              urban_request_txt
            FROM 
              REQUEST
            ORDER BY
              frequency_cnt DESC
            LIMIT {0};
        """.format(limit,)
        return cursor.execute(query).fetchall()
