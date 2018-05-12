import datetime
import sqlite3
import tkinter

import matplotlib

matplotlib.use('Agg')
import matplotlib.pyplot
import numpy

import config
import db_manager


def language_frequency(chat_id):
    query = '''
      WITH total AS (
        SELECT 
          count(*) AS cnt
        FROM
          CHAT_LANG
      )
      SELECT 
        cast(count(*) AS float) / (SELECT cnt FROM total) AS freq,
        lang_txt
      FROM
        CHAT_LANG
      GROUP BY
        lang_txt
      ORDER BY
        freq DESC;
    '''
    with sqlite3.connect(config.DB_NAME) as connection:
        cursor = connection.cursor()
        langs, percantage = [], []
        for part, explanation in cursor.execute(query).fetchall():
            percantage.append(round(part * 100, 0))
            langs.append(explanation.upper())
        extended_cnt = len(langs)
        pos = numpy.arange(extended_cnt)
        matplotlib.pyplot.barh(pos, percantage, color='blue', edgecolor='black')
        matplotlib.pyplot.yticks(pos, langs)
        matplotlib.pyplot.xlabel("%", fontsize=extended_cnt * 4)
        matplotlib.pyplot.ylabel("", fontsize=extended_cnt * 4)
        matplotlib.pyplot.title("", fontsize=extended_cnt * 5)
        pic_name = 'tmp/lang_{}.png'.format(str(datetime.datetime.now()) + str(chat_id)).replace(' ', '')
        matplotlib.pyplot.savefig(pic_name)
        matplotlib.pyplot.clf()
        return pic_name


def request_frequency(chat_id):
    requests, frequences = [], []
    for _, request, cnt in db_manager.get_top(10):
        requests.append(request)
        frequences.append(cnt)
    extended_cnt = len(requests)
    pos = numpy.arange(extended_cnt)
    matplotlib.pyplot.barh(pos, frequences, color='blue', edgecolor='black')
    matplotlib.pyplot.yticks(pos, requests)
    matplotlib.pyplot.xlabel("", fontsize=extended_cnt)
    matplotlib.pyplot.ylabel("", fontsize=extended_cnt)
    matplotlib.pyplot.title("", fontsize=extended_cnt)
    pic_name = 'tmp/req_{}.png'.format(str(datetime.datetime.now()) + str(chat_id))
    matplotlib.pyplot.savefig(pic_name)
    matplotlib.pyplot.clf()
    return pic_name
