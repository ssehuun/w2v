#!/usr/bin/env python
# coding=utf-8

import sys
import pymysql
import logging
from collections import OrderedDict

class MysqlPython(object):

    __instance   = None
    __host       = None
    __user       = None
    __password   = None
    __database   = None
    __session    = None
    __connection = None

    def __init__(self, host='localhost', user='root', password='', database=''):
        self.__host     = host
        self.__user     = user
        self.__password = password
        self.__database = database
    ## End def __init__

    def open(self):
        self.__open()

    def __open(self):
        try:
            cnx = pymysql.connect(self.__host, self.__user, self.__password, self.__database)
            self.__connection = cnx
            self.__session    = cnx.cursor()
            self.__session.execute('SET NAMES utf8;')
            # self.__session.execute('SET CHARACTER SET utf8;')
            # self.__session.execute("set character_set_connection=utf8;")
            # self.__session.execute("set character_set_server=utf8;")
            # self.__session.execute("set character_set_client=utf8;")
            # self.__session.execute("set character_set_results=utf8;")
            # self.__session.execute("set character_set_database=utf8;")
            # self.__session.execute('insert ignore into sentences (sentence)  values (%s);', (x.encode('utf-8'))
        except pymysql.Error as e:
            logging.error("%d: %s" % (e.args[0],e.args[1]))
    ## End def __open

    def close(self):
        self.__close()

    def __close(self):
        self.__session.close()
        self.__connection.close()
    ## End def __close

    def select(self, table, where=None, *args, **kwargs):
        result = None
        query = 'SELECT '
        keys = args
        values = tuple(kwargs.values())
        l = len(keys) - 1

        for i, key in enumerate(keys):
            query += "`"+key+"`"
            if i < l:
                query += ","
        ## End for keys

        query += 'FROM %s' % table

        if where:
            query += " WHERE %s" % where
        ## End if where

        self.__open()
        self.__session.execute(query, values)
        number_rows = self.__session.rowcount
        number_columns = len(self.__session.description)

        if number_rows >= 1 and number_columns > 1:
            result = [item for item in self.__session.fetchall()]
        else:
            result = [item[0] for item in self.__session.fetchall()]
        self.__close()

        return result
    ## End def select


    def select_count(self, table, where=None, *args, **kwargs):
        result = None
        query = 'SELECT '
        keys = args
        values = tuple(kwargs.values())
        l = len(keys) - 1

        for i, key in enumerate(keys):
            query += "`" + key + "`"
            if i < l:
                query += ","
        ## End for keys

        query += 'FROM %s' % table

        if where:
            query += " WHERE %s" % where
            ## End if where

        self.__open()
        self.__session.execute(query, values)
        number_rows = self.__session.rowcount
        self.__close()

        return number_rows
        ## End def select


    def update(self, table, where=None, *args, **kwargs):
        query  = "UPDATE %s SET " % table
        keys   = kwargs.keys()
        values = tuple(kwargs.values()) + tuple(args)
        l = len(keys) - 1
        for i, key in enumerate(keys):
            query += "`"+key+"` = %s"
            if i < l:
                query += ","
            ## End if i less than 1
        ## End for keys
        query += " WHERE %s" % where

        self.__open()
        self.__session.execute(query, values)
        self.__connection.commit()

        # Obtain rows affected
        update_rows = self.__session.rowcount
        self.__close()

        return update_rows
    ## End function update

    def addslashes(self, s):
        l = ["\\", '"', "'", "\0", ]
        for i in l:
            if i in s:
                s = s.replace(i, '\\' + i)
        return s

    # def insert_news(self, id, category, date, link, has_vod, source, title_txt, title_len, content_txt, content_len):
    #     table = "daum_news_"+category
    #     query = "INSERT INTO %s " % table
    #     query += "(id, category, date, link, has_vod, source, title, title_len, content, content_len) VALUES ('"+id+"','"+category+"','"+date+"','"+link+"',"+has_vod+",'"+source+"','"+self.addslashes(title_txt)+"',"+str(title_len)+",'"+self.addslashes(content_txt)+"',"+str(content_len)+")"
    #     self.__open()
    #     self.__session.execute(query.encode('utf8'))
    #     self.__connection.commit()
    #     self.__close()
    #     return self.__session.lastrowid

    def insert_news(self, id, category, date, link, has_vod, source, title_len, content_len):
        table = "daum_news_" + category
        query = "INSERT INTO %s " % table
        query += "(id, category, date, link, has_vod, source, title_len, content_len) VALUES ('" + id + "','" + category + "','" + date + "','" + link + "'," + has_vod + ",'" + source + "'," + str(title_len) + "," + str(content_len) + ")"
        self.__open()
        self.__session.execute(query.encode('utf8'))
        self.__connection.commit()
        self.__close()
        return self.__session.lastrowid


    def insert(self, table, *args, **kwargs):
        values = None
        query = "INSERT INTO %s " % table
        if kwargs:
            keys = kwargs.keys()
            values = tuple(kwargs.values())
            query += "(" + ",".join(["`%s`"] * len(keys)) %  tuple (keys) + ") VALUES (" + ",".join(["%s"]*len(values)) + ")"
        elif args:
            values = args
            query += " VALUES(" + ",".join(["%s"]*len(values)) + ")"

        self.__open()
        self.__session.execute(query, values)
        self.__connection.commit()
        self.__close()
        return self.__session.lastrowid
    ## End def insert

    def delete(self, table, where=None, *args):
        query = "DELETE FROM %s" % table
        if where:
            query += ' WHERE %s' % where

        values = tuple(args)

        self.__open()
        self.__session.execute(query, values)
        self.__connection.commit()

        # Obtain rows affected
        delete_rows = self.__session.rowcount
        self.__close()

        return delete_rows
    ## End def delete

    def select_advanced(self, sql, *args):
        od = OrderedDict(args)
        query = sql
        values = tuple(od.values())
        self.__open()
        self.__session.execute(query, values)
        number_rows = self.__session.rowcount
        number_columns = len(self.__session.description)

        if number_rows >= 1 and number_columns > 1:
            result = [item for item in self.__session.fetchall()]
        else:
            result = [item[0] for item in self.__session.fetchall()]

        self.__close()
        return result
    ## End def select_advanced
## End class




