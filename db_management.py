import sqlite3

import config

connection = sqlite3.Connection(config.DB_NAME)
cursor = connection.cursor()


def add_id(chat_id):
    query = """
        INSERT INTO CHAT_LANG 
          (chat_id)
        VALUES
          ({0});
    """.format(chat_id)
    cursor.execute(query)
    connection.commit()


def get_lang(chat_id):
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
    query = """
        UPDATE
          CHAT_LANG
        SET
          lang_txt = '{1}'
        WHERE
          chat_id = {0};
    """.format(chat_id, lang_txt,)
    q = cursor.execute(query)
    connection.commit()


def add_description(request_txt, description_txt):
    cursor.execute("""
        INSERT INTO REQUEST 
          (urban_request_txt, description_txt)
        VALUES
          ('{0}', '{1}'); 
    """.format(request_txt.lower(), description_txt))
    connection.commit()


def get_description(request_txt):
    query = """
        SELECT 
          description_txt
        FROM 
          REQUEST
        WHERE
          urban_request_txt = '{0}';
    """.format(request_txt.lower())
    response = cursor.execute(query)
    return response


def get_top(limit):
    query = """
        SELECT 
          REQUEST.urban_request_txt
        FROM 
          REQUEST
        ORDER BY
          REQUEST.frequency_cnt DESC
        LIMIT {0};
    """.format(limit,)
    return cursor.execute(query).fetchall()


if __name__ == '__main__':
    print(get_lang(1032567))
