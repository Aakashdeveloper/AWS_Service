import flask
from flask import request, jsonify
from flask_cors import CORS, cross_origin
from sqlalchemy.orm.util import identity_key
from flask_sqlalchemy import SQLAlchemy
from psycopg2.pool import SimpleConnectionPool
import time
import random
import psycopg2
import os
import csv
from gevent.pywsgi import WSGIServer
import logging
import pandas as pd
from zipfile import ZipFile 

logger = logging.getLogger(__name__)
#logging.basicConfig(level=Parameters.logging)


application = flask.Flask(__name__)
application.config["DEBUG"] = True
CORS(application,resources={r"/*": {"origins": "*"}})
application.config['CORS_HEADERS'] = 'Content-Type'


class Apiservice():
    
    def __init__(self):
    
      print('Inside __init__')
      self.conn = psycopg2.connect(user='postgres',password='admin12345',host="database-1.cjcjgqizui8x.us-east-1.rds.amazonaws.com",port=5432,dbname='postgres')

      
    def getConnection (self):
       print('Inside getConnection')
       try:
          cur = self.conn.cursor()
          cur.execute('SELECT 1')
          cur.close()

       except Exception as exc:
          logger.error(exc)
          self.conn = psycopg2.connect(user='postgres',password='admin12345',host="database-1.cjcjgqizui8x.us-east-1.rds.amazonaws.com",port=5432,dbname='postgres')

       return self.conn

    
    def getData(self,query):
        sql_query = query
        conn = apiService.getConnection ()
        cur = conn.cursor()
        out = cur.execute(sql_query)
        context_records = cur.fetchall()
        out = jsonify(context_records)
        return context_records
    
    def postData(self,query,value):
        sql_query = query
        conn = apiService.getConnection ()
        cur = conn.cursor()
        cur.execute(sql_query,value)
        conn.commit()
        return "Data Added"
 
    @application.route('/health', methods=['GET'])
    @cross_origin('*')
    def hello():
        return "hello from API"

    @application.route('/userInfo/', methods=['GET'])
    @cross_origin('*')
    def getEntity():
        output = apiService.getData("SELECT * FROM userinfo")
        print(output)
        outArray=[]
        try:
            length = len(output)
            for i in range(length):
                userinfo={}
                userinfo["uname"]= output[i][0]
                userinfo["empid"]= output[i][1]
                userinfo["tech"]= output[i][2]
                outArray.append(userinfo)     
        except Exception as exc:
            print(exc)
        return jsonify(outArray)
    


    @application.route('/postuser/', methods=['POST'])
    @cross_origin('*')
    def postIntent():
        body = request.json
        uname= body['uname']
        empid= body['empid']
        tech= body['tech']
        sql_ins="""INSERT INTO userinfo(uname,empid,tech) VALUES (%s,%s,%s)"""
        values=(uname,empid,tech)
        out = apiService.postData(sql_ins,values)
        return out

    
    
    


    @application.route('/updateuser/', methods=['PUT'])
    @cross_origin('*')
    def updateIntent():
        body = request.json
        uname= body['uname']
        empid= body['empid']
        tech= body['tech']
        sql_upt="""Update userinfo set uname = %s, tech=%s  where empid = %s"""
        values=(uname,tech,empid)
        out = apiService.postData(sql_upt,values)
        return out

    
apiService = Apiservice ()


if __name__ == '__main__':
    #http_server = WSGIServer(('0.0.0.0', 8443), application, keyfile='/opt/epaas/certs/dkey', certfile='/opt/epaas/certs/ca-chain')
    http_server = WSGIServer(('0.0.0.0', 8005), application)
    http_server.start()
    try:
       logger.info("LDAP Service is up and running")
       http_server.serve_forever()

    except Exception as exc:
       logger.exception(exc)