# -*- coding: utf-8 -*-
'''
// =============================================================================
// 機能名：プロセス可視化チャート：編集画面
//
// =============================================================================
// （ファイル整形）Visual Studio Code : Shift + Alt + f
// =============================================================================
'''
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
# プロセス可視化チャート情報：コメント情報を取得する
# （未設定のコメントを取り出す）
#
# ------------------------------------------------------

@ProcessEditWindow_api.route("/getCommentList/", methods=['POST'])
def getCommentList():

    try:
        commentCode = flask.request.form['commentCode']

        # SQL
        process_edit_conn = pyodbc.connect('DRIVER={SQL Server};'
                                           'Server='+app_section.get('IP')+';'
                                           'Database=' +
                                           app_section.get('DATABASE')+';'
                                           'uid=' +
                                           app_section.get('DB_USER_ID')+';'
                                           'pwd='+app_section.get('DB_PASSWORD')+';')

        process_edit_cursor = process_edit_conn.cursor()

        update_query = "" \
            " select " \
            "   commentCode" \
            " from" \
            "  ChartComment_TBL as c" \
            " WHERE" \
            " not exists(" \
            "  select" \
            "    commentCode" \
            "  from" \
            "    ChartDesign_TBL as d" \
            "  where" \
            "   d.commentCode = c.commentCode" \
            ")"

        process_edit_cursor.execute(update_query)
        commentList = []

        # その他
        for x in process_edit_cursor:
            commentList.append(x[0])

        if commentCode not in commentList:
            # 自分を追加
            commentList.append(commentCode)

        print(commentList)
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
        updateType = flask.request.form['updateType']
        chartDesignCode = flask.request.form['chartDesignCode']
        locationInfo = flask.request.form['locationInfo']

        comment_code = flask.request.form['comment_code']
        heading = flask.request.form['heading']
        explaination = flask.request.form['explaination']
        efficiency = flask.request.form['efficiency']
        ExceptionWork = flask.request.form['ExceptionWork']
        OperationTarget = flask.request.form['OperationTarget']
        working_hour = flask.request.form['working_hour']
        SupplementComment = flask.request.form['SupplementComment']

        print("updateType= ", updateType)
        print("chartDesignCode= ", chartDesignCode)

        print("comment_code= ", comment_code)
        print("heading= ", heading)

        print("explaination= ", explaination)
        print("efficiency = ", efficiency)
        print("ExceptionWork = ", ExceptionWork)
        print("OperationTarget = ", OperationTarget)
        print("working_hour = ", working_hour)
        print("SupplementComment = ", SupplementComment)

        status = {}

        if updateType == "insert":
            update_conn = pyodbc.connect('DRIVER={SQL Server};'
                                         'Server='+app_section.get('IP')+';'
                                         'Database=' +
                                         app_section.get('DATABASE')+';'
                                         'uid=' +
                                         app_section.get('DB_USER_ID')+';'
                                         'pwd='+app_section.get('DB_PASSWORD')+';')

            update_cursor = update_conn.cursor()

            # ChartDesign_TBL
            trn_sql = "UPDATE " \
                " ChartDesign_TBL " \
                " SET CommentCode = '" + comment_code + "'" \
                " WHERE " \
                "   ChartDesignCode = '" + chartDesignCode + "'" \
                " AND LocationInfo = '" + locationInfo + "'" \

            update_conn.execute(trn_sql)

            # ChartComment_TBL
            trn_sql = "INSERT INTO ChartComment_TBL " \
                " (CommentCode, Heading, Explanation, Efficiency, OperationTarget, " \
                "  WorkingHour, ExceptionWork, SupplementComment, ChartDesignCode) " \
                " VALUES (" + \
                "   '" + comment_code + "'" + \
                " , '" + heading + "'" \
                " , '" + explaination + "'" \
                " , '" + efficiency + "'" \
                " , '" + OperationTarget + "'" \
                " , '" + working_hour + "'" \
                " , '" + ExceptionWork + "'" \
                " , '" + SupplementComment + "'" \
                " , '" + chartDesignCode + "'" + \
                ") "

            update_cursor.execute(trn_sql)
            update_conn.commit()

        if updateType == "update":
            # 選択したコメントの情報を更新する
            update_conn = pyodbc.connect('DRIVER={SQL Server};'
                                         'Server='+app_section.get('IP')+';'
                                         'Database=' +
                                         app_section.get('DATABASE')+';'
                                         'uid=' +
                                         app_section.get('DB_USER_ID')+';'
                                         'pwd='+app_section.get('DB_PASSWORD')+';')

            update_cursor = update_conn.cursor()

            # ChartDesign_TBL
            trn_sql = "UPDATE " \
                " ChartDesign_TBL " \
                " SET CommentCode = '" + comment_code + "'" \
                " WHERE " \
                "   ChartDesignCode = '" + chartDesignCode + "'" \
                " AND LocationInfo = '" + locationInfo + "'" \

            update_conn.execute(trn_sql)

            update_query = "" \
                "UPDATE " \
                "  ChartComment_TBL " \
                " SET Heading = '" + heading + "'" \
                "  , Explanation = '" + explaination + "'" \
                "  , Efficiency = '" + efficiency + "'" \
                "  , OperationTarget = '" + OperationTarget + "'" \
                "  , WorkingHour = '" + working_hour + "'" \
                "  , ExceptionWork = '" + ExceptionWork + "'" \
                "  , SupplementComment = '" + SupplementComment + "'" \
                " WHERE " \
                "   CommentCode = '" + comment_code + "'" \
                " AND ChartDesignCode = '" + chartDesignCode + "'" \

            update_cursor.execute(update_query)
            update_conn.commit()

        # OK
        status['status'] = "OK"

    except Exception as e:
        update_cursor.rollback()

        print("updateChartCommentInfo save error  " + e.args)
        status['status'] = "NG"
        pass

    # end
    finally:
        print(json.dumps(status, indent=2, ensure_ascii=False))

        return jsonify(status)


# ========================================================================
# プロセス可視化チャート情報を削除する
#
#
# ------------------------------------------------------

@ProcessEditWindow_api.route("/deleteChartCommentData/", methods=['POST'])
def deleteChartCommentData():

    try:
        chartDesignCode = flask.request.form['chartDesignCode']
        locationInfo = flask.request.form['locationInfo']
        commentCode = flask.request.form['commentCode']

        print(chartDesignCode)
        print(locationInfo)
        print(commentCode)

        status = {}

        # SQL
        trn_conn = pyodbc.connect('DRIVER={SQL Server};'
                                  'Server='+app_section.get('IP')+';'
                                  'Database=' +
                                  app_section.get('DATABASE')+';'
                                  'uid='+app_section.get('DB_USER_ID')+';'
                                  'pwd='+app_section.get('DB_PASSWORD')+';')

        trn_cursor = trn_conn.cursor()

        # ChartComment_TBL
        trn_sql = "DELETE " \
            " FROM ChartComment_TBL " \
            " WHERE " + \
            "   ChartDesignCode = '" + chartDesignCode + "'" \
            " AND CommentCode = '" + commentCode + "'"

        trn_cursor.execute(trn_sql)

        trn_cursor.commit()

        # OK
        status['status'] = "OK"

    except Exception as e:
        trn_cursor.rollback()

        print("deleteChartCommentData save error  " + e.args)
        status['status'] = "NG"
        pass

    # end
    finally:
        print(json.dumps(status, indent=2, ensure_ascii=False))

        return jsonify(status)
