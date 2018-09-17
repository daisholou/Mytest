import pandas as pd

import pymysql

conn = pymysql.connect(host="localhost", user="root", passwd="*****", db="test", charset="utf8")

# read

sql = "select * from user limit 3"

df = pd.read_sql(sql, conn, index_col="id")

print df


# write

cur = conn.cursor()

cur.execute("drop table if exists user")

cur.execute('create table user(id int,name varchar(20))')

pd.io.sql.write_frame(df, "user", conn)
