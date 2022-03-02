# -*- coding: utf-8 -*-
# ##############################################################################
#
# 【プロセス可視化チャート：詳細画面処理】
#
#
#
# ##############################################################################
#
import requests
import json
from configparser import ConfigParser
import flask
from flask import Flask, jsonify, render_template, request, abort, Blueprint
import sys
import tornado.wsgi
import tornado.httpserver
import logging
import base64
import pyodbc
import os
import pandas as pd
import datetime
import logging
import logging.config
import sys
import requests
import json
from configparser import ConfigParser
import base64
from requests_toolbelt import MultipartEncoder
from datetime import datetime
from collections import Counter
import calendar


# Const
# -----------------------------------------------------------------------------
# Path: config - log
PATH_CONFIG_LOG = 'applicationlogging.ini'
# Path: config - log
PATH_CONFIG_APPLICATION = 'application.ini'
# Section config: application
SECTION_CONFIG_APPLICATION = 'default'

# Initialize logging
# -----------------------------------------------------------------------------
logging.config.fileConfig(PATH_CONFIG_LOG)
logger = logging.getLogger(__name__)
# Initialize Flask application
# -----------------------------------------------------------------------------
app_config = ConfigParser()
app_config.read(PATH_CONFIG_APPLICATION)
app_section = app_config[SECTION_CONFIG_APPLICATION]

### Blueprintでモジュールの登録 ###
ProcessEditWindow_api = Blueprint('ProcessEditWindow', __name__)

# ========================================================================
# 画像情報の取得
#
#
# ------------------------------------------------------


# ========================================================================
# プロセス可視化チャート情報を保存（更新）する
#
#
# ------------------------------------------------------

@ProcessEditWindow_api.route("/getCommentList/", methods=['GET'])
def getCommentList():

    try:
       
        # SQL
        process_edit_conn = pyodbc.connect('DRIVER={SQL Server};'
                                     'Server='+app_section.get('IP')+';'
                                     'Database=' +
                                     app_section.get('DATABASE')+';'
                                     'uid='+app_section.get('DB_USER_ID')+';'
                                     'pwd='+app_section.get('DB_PASSWORD')+';')

        process_edit_cursor = process_edit_conn.cursor()

        
        update_query = "select commentCode from ChartComment_TBL"

        process_edit_cursor.execute(update_query)
        commentList = []
        for x in process_edit_cursor:
            print("x in comment list = ",x)
            commentList.append(x[0])        
        return jsonify(commentList)
    except Exception as e:
        return "null"



# ========================================================================
# プロセス可視化チャート情報を保存（更新）する
#
#
# ------------------------------------------------------

@ProcessEditWindow_api.route("/updateChartCommentInfo/", methods=['POST'])
def updateChartCommentInfo():

    try:
        comment_code = flask.request.form['comment_code']
        print(" comment_code= ",comment_code )
        heading = flask.request.form['heading']
        print(" heading= ", heading)
        explaination = flask.request.form['explaination']
        print(" explaination= ",explaination )
        efficiency = flask.request.form['efficiency']
        print("efficiency = ", efficiency)
        ExceptionWork = flask.request.form['ExceptionWork']
        print("ExceptionWork = ", ExceptionWork)
        OperationTarget = flask.request.form['OperationTarget']
        print("OperationTarget = ",OperationTarget )
        working_hour = flask.request.form['working_hour']
        print("working_hour = ",working_hour )
        SupplementComment = flask.request.form['SupplementComment']
        print("SupplementComment = ",SupplementComment )

       
        # SQL
        delete_conn = pyodbc.connect('DRIVER={SQL Server};'
                                     'Server='+app_section.get('IP')+';'
                                     'Database=' +
                                     app_section.get('DATABASE')+';'
                                     'uid='+app_section.get('DB_USER_ID')+';'
                                     'pwd='+app_section.get('DB_PASSWORD')+';')

        update_conn = pyodbc.connect('DRIVER={SQL Server};'
                                     'Server='+app_section.get('IP')+';'
                                     'Database=' +
                                     app_section.get('DATABASE')+';'
                                     'uid='+app_section.get('DB_USER_ID')+';'
                                     'pwd='+app_section.get('DB_PASSWORD')+';')

        delete_cursor = delete_conn.cursor()        
        delete_query = "delete from ChartComment_TBL where CommentCode = '"+comment_code+"'"
        delete_cursor.execute(delete_query)
        delete_conn.commit()

        update_cursor = update_conn.cursor() 
        update_query = "insert into ChartComment_TBL values('"+comment_code+"','"+heading+"','"+explaination+"','"+efficiency+"','"+OperationTarget+"','"+working_hour+"','"+ExceptionWork+"','"+SupplementComment+"','DesignCode_20220214135920') "
        update_cursor.execute(update_query)
        update_conn.commit()
        return "success"
        
    except Exception as e:
        return "null"
