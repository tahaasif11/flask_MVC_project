import pymysql


def openDbconnection():
  try:
    connection = pymysql.connect(host='localhost', user='admin', passwd='Taha.Asif', db='flask_blog_project')
    cursor = connection.cursor(pymysql.cursors.DictCursor)
    return connection, cursor

  except Exception as e:
    print(e)
    return False

connection, cursor = openDbconnection()
