import sqlite3
import datetime

import matplotlib.pyplot
import numpy

import config


def language_frequency(chat_id=0):
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
        for k, v in cursor.execute(query).fetchall():
            percantage.append(round(k * 100, 0))
            langs.append(v.upper())
        extended_cnt = len(langs)
        pos = numpy.arange(extended_cnt)
        matplotlib.pyplot.barh(pos, percantage, color='blue', edgecolor='black')
        matplotlib.pyplot.yticks(pos, langs)
        matplotlib.pyplot.xlabel("%", fontsize=extended_cnt * 4)
        matplotlib.pyplot.ylabel("", fontsize=extended_cnt * 4)
        matplotlib.pyplot.title("", fontsize=extended_cnt * 5)
        pic_name = 'tmp/{}.png'.format(str(datetime.datetime.now()) + str(chat_id))
        matplotlib.pyplot.savefig(pic_name)
        return pic_name
