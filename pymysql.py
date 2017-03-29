# -*- coding:utf-8 -*-
# python mysql基本操作

"""
# testcase1 : 连接数据库, 取得 MYSQL 的版本
import MySQLdb as mdb
con = None
try:
    # 连接 mysql 的方法： connect('ip','user','password','dbname')
    con = mdb.connect('localhost', 'root', '1234', 'db_admin')

    # 所有的查询，都在连接 con 的一个模块 cursor 上面运行的
    cur = con.cursor()

    # 执行一个查询
    cur.execute("SELECT VERSION()")

    # 取得上个查询的结果，是单个结果
    data = cur.fetchone()
    print "Database version : %s " % data

finally:
    # 无论如何，连接记得关闭
    if con:
        con.close()


# testcase2 : 创建一个表并且插入数据
import MySQLdb as mdb

# 将 con 设定为全局连接
con = mdb.connect('localhost', 'root', '1234', 'db_admin');
with con:
    # 获取连接的 cursor，只有获取了 cursor，我们才能进行各种操作
    cur = con.cursor()

    # 创建一个数据表 writers(id,name)
    cur.execute("CREATE TABLE IF NOT EXISTS Writers(Id INT PRIMARY KEY AUTO_INCREMENT, Name VARCHAR(25))")

    # 以下插入了 5 条数据
    cur.execute("INSERT INTO Writers(Name) VALUES('Jack London')")
    cur.execute("INSERT INTO Writers(Name) VALUES('Honore de Balzac')")
    cur.execute("INSERT INTO Writers(Name) VALUES('Lion Feuchtwanger')")
    cur.execute("INSERT INTO Writers(Name) VALUES('Emile Zola')")
    cur.execute("INSERT INTO Writers(Name) VALUES('Truman Capote')")

con.close()


# testcase3 : python 使用 slect 获取 mysql 的数据并遍历
import MySQLdb as mdb
con = mdb.connect('localhost', 'root', '1234', 'db_admin');
with con:
    cur = con.cursor()
    cur.execute("SELECT * FROM Writers")
    rows = cur.fetchall()
    for row in rows:
        print row
con.close()


# testcase4 : python 使用 slect 获取 mysql 的数据并遍历
import MySQLdb as mdb
con = mdb.connect('localhost', 'root', '1234', 'db_admin');
with con:
    cur = con.cursor()
    cur.execute("SELECT * FROM Writers")
    numrows = int(cur.rowcount)
    for i in range(numrows):
        row = cur.fetchone()
        print row[0], row[1]


# testcase5 : 使用字典 cursor 取得结果集（可以使用表字段名字访问值）
import MySQLdb as mdb
con = mdb.connect('localhost', 'root', '1234', 'db_admin');
with con:
    cur = con.cursor(mdb.cursors.DictCursor)
    cur.execute("SELECT * FROM Writers")
    rows = cur.fetchall()
    for row in rows:
        print "%s %s" % (row["Id"], row["Name"])


# testcase6 : 获取单个表的字段名和信息的方法
import MySQLdb as mdb
con = mdb.connect('localhost', 'root', '1234', 'db_admin');
with con:
    cur = con.cursor()
    cur.execute("SELECT * FROM Writers")
    rows = cur.fetchall()
    desc = cur.description
    print 'cur.description:', desc
    print "%s %3s" % (desc[0][0], desc[1][0])
    for row in rows:
        print "%2s %3s" % row


# testcase7 : 使用 Prepared statements 执行查询（更安全方便）
import MySQLdb as mdb
con = mdb.connect('localhost', 'root', '1234', 'db_admin');
with con:
    cur = con.cursor()
    cur.execute("UPDATE Writers SET Name = %s WHERE Id = %s",
                ("Guy de Maupasant", "4"))
    print "Number of rows updated: %d" % cur.rowcount

# testcase7 : 把图片用二进制存入 MYSQL
import MySQLdb as mdb
import sys
try:
    fin = open("37.jpg")
    img = fin.read()
    fin.close()
except IOError, e:
    print "Error %d: %s" % (e.args[0], e.args[1])
    sys.exit(1)

try:
    conn = mdb.connect(host='localhost', user='root', passwd='1234',
                       db='db_admin')
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS Images(Id INT PRIMARY KEY AUTO_INCREMENT, Data LONGBLOB)")
    cursor.execute("INSERT INTO Images SET Data='%s'" % mdb.escape_string(img))
    conn.commit()
    cursor.close()
    conn.close()
except mdb.Error, e:
    print "Error %d: %s" % (e.args[0], e.args[1])
    sys.exit(1)
"""

import MySQLdb as mdb
import sys
try:
    conn = mdb.connect('localhost', 'root', '1234', 'db_admin');
    cursor = conn.cursor()
    cursor.execute("SELECT Data FROM Images LIMIT 1")
    fout = open('image.jpg','wb')
    fout.write(cursor.fetchone()[0])
    fout.close()
    cursor.close()
    conn.close()
except IOError, e:
    print "Error %d: %s" % (e.args[0], e.args[1])
    sys.exit(1)










