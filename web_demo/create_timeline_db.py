# coding=utf-8
import sqlite3

if __name__ == '__main__':
    dbfile = "fmachine_demo.db"
    conn = sqlite3.connect(dbfile, detect_types=sqlite3.PARSE_DECLTYPES)
    c = conn.cursor()
    c.execute('CREATE TABLE titem (\
        timestamp TIMESTAMP NOT NULL,\
        title TEXT NOT NULL,\
        content   TEXT,\
    PRIMARY KEY(timestamp,title)\
    )')
    conn.commit()
    c.close()
    conn.close()
