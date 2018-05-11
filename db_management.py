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
          CHAT_LANG.lang_txt
        FROM 
          CHAT_LANG
        WHERE
          CHAT_LANG.chat_id = {0};
    """.format(chat_id)
    response = cursor.execute(query)
    return response


def set_lang(chat_id, lang_txt):
    query = """
        UPDATE
          CHAT_LANG
        SET
          CHAT_LANG.lang_txt = {1}
        WHERE
          CHAT_LANG.chat_id = {0};
    """.format(chat_id, lang_txt)
    cursor.execute(query)
    connection.commit()


def add_description(request_txt, description_txt):
    cursor.execute("""
        INSERT INTO REQUEST 
          (urban_request_txt, description_txt)
        VALUES
          ({0}, {1}); 
    """.format(request_txt.lower(), description_txt))
    connection.commit()


def get_description(request_txt):
    query = """
        SELECT 
          REQUEST.description_txt
        FROM 
          REQUEST
        WHERE
          REQUEST.urban_request_txt = {0};
    """.format(request_txt.lower())
    response = cursor.execute(query)
    return response



