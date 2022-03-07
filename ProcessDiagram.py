# -*- coding: utf-8 -*-
# ##############################################################################
#
# 【プロセス可視化チャート：共通処理】
#
#    JSON データ構造を作成する
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
ProcessDiagram_api = Blueprint('ProcessDiagram', __name__)

# ========================================================================
# プロセス可視化チャート図情報を保存する
#
#
# ------------------------------------------------------


@ProcessDiagram_api.route("/saveProcessChartImagesData/", methods=['POST', 'GET'])
def saveProcessChartImagesData():

    try:
        updateUser = flask.request.form['updateUser']

        processProcedureID = flask.request.form['processProcedureID']
        processProcedureName = flask.request.form['processProcedureName']
        chartDesignCode = flask.request.form['chartDesignCode']

        permissionFlag = flask.request.form['permissionFlag']
        changeProhibitionFlag = flask.request.form['changeProhibitionFlag']

        totalWorkingTime = flask.request.form['totalWorkingTime']
        workFrequency = flask.request.form['workFrequency']
        numberOfWorkers = flask.request.form['numberOfWorkers']

        columnNumber = flask.request.form['columnNumber']
        rowsNumber = flask.request.form['rowsNumber']

        print(processProcedureID)
        print(processProcedureName)
        print(chartDesignCode)

        print(permissionFlag)
        print(changeProhibitionFlag)
        print(totalWorkingTime)
        print(workFrequency)
        print(numberOfWorkers)
        print(columnNumber)
        print(rowsNumber)

        status = {}

        # SQL
        update_conn = pyodbc.connect('DRIVER={SQL Server};'
                                     'Server='+app_section.get('IP')+';'
                                     'Database=' +
                                     app_section.get('DATABASE')+';'
                                     'uid='+app_section.get('DB_USER_ID')+';'
                                     'pwd='+app_section.get('DB_PASSWORD')+';')

        conn_cursor = update_conn.cursor()

        pFlag = "0"
        cFlag = "0"
        if permissionFlag == "true":
            pFlag = "1"
        if changeProhibitionFlag == "true":
            cFlag = "1"

        tdatetime = datetime.now()
        updateDatetime = tdatetime.strftime('%Y-%m-%d %H:%M:%S')

        # ---------------------------------------
        # プロセス可視化チャート情報（一覧情報）を更新する
        # ---------------------------------------
        update_query = \
            " UPDATE  ProcessChartData_TBL " \
            "  SET ProcessProcedureName = '" + processProcedureName + "'" \
            "  , PermissionFlag = '" + pFlag + "' " \
            "  , ChangeProhibitionFlag = '" + cFlag + "' " \
            "  , WorkFrequency = '" + workFrequency + "' " \
            "  , NumberOfWorkers = '" + numberOfWorkers + "' " \
            "  , TotalWorkingTime = '" + totalWorkingTime + "' " \
            "  , ColumnNumber = '" + columnNumber + "' " \
            "  , RowsNumber = '" + rowsNumber + "' " \
            "  , UpdateMailAddress = '" + updateUser + "'" \
            "  , UpdateDateTime  = '" + updateDatetime + "'" \
            " WHERE " \
            "  ProcessProcedureID = '" + processProcedureID + "'"

        conn_cursor.execute(update_query)
        conn_cursor.commit()

        status['status'] = "OK"

    except Exception as e:
        print("saveProcessChartImagesData save error  " + e.args)
        status['status'] = "NG"
        pass

    # end
    finally:
        print(json.dumps(status, indent=2, ensure_ascii=False))

        return jsonify(status)

# ========================================================================
# プロセス可視化チャート図情報を保存する
# 【画像】
#
# ------------------------------------------------------


@ProcessDiagram_api.route("/updateChartImg/", methods=['POST', 'GET'])
def updateChartImg():

    chartDesignCode = flask.request.form['chartDesignCode']
    imgFileName = flask.request.form['imgFileName']
    locationInfo = flask.request.form['locationInfo']
    midashi = flask.request.form['midashi']

    print(chartDesignCode)
    print(imgFileName)
    print(locationInfo)
    print(midashi)

    try:
        # イメージ名
        basename = os.path.basename(imgFileName)
        imgFileName = os.path.splitext(basename)[0]

        status = {}

        # SQL
        trn_conn = pyodbc.connect('DRIVER={SQL Server};'
                                  'Server='+app_section.get('IP')+';'
                                  'Database=' +
                                  app_section.get('DATABASE')+';'
                                  'uid='+app_section.get('DB_USER_ID')+';'
                                  'pwd='+app_section.get('DB_PASSWORD')+';')

        select_conn = pyodbc.connect('DRIVER={SQL Server};'
                                     'Server='+app_section.get('IP')+';'
                                     'Database=' +
                                     app_section.get('DATABASE')+';'
                                     'uid='+app_section.get('DB_USER_ID')+';'
                                     'pwd='+app_section.get('DB_PASSWORD')+';')

        select_conn_cursor = select_conn.cursor()

        # ---------------------------------------
        # カラム数、行数を取得する
        # ---------------------------------------
        select_query = \
            " SELECT " \
            "  ImageName ," \
            "  CommentCode " \
            " FROM " \
            "   ChartDesign_TBL " \
            " WHERE " \
            "   ChartDesignCode = '" + chartDesignCode + "'" \
            "  AND LocationInfo = '" + locationInfo + "'"

        select_conn_cursor.execute(select_query)

        imgData = []
        for x in select_conn_cursor:
            imgData.append(x[0])
            imgData.append(x[1])

        select_conn_cursor.close()

        trn_cursor = trn_conn.cursor()

        if imgFileName == "Space_001":
            if len(imgData) != 0:
                # 削除とする
                trn_sql = "DELETE " \
                    " FROM ChartDesign_TBL " \
                    " WHERE " + \
                    "   ChartDesignCode = '" + chartDesignCode + "'" \
                    " AND LocationInfo = '" + locationInfo + "'" \
                    " AND CommentCode = '" + imgData[1] + "'"

                trn_cursor.execute(trn_sql)

                # ChartComment_TBL
                trn_sql = "DELETE " \
                    " FROM ChartComment_TBL " \
                    " WHERE " + \
                    "   ChartDesignCode = '" + chartDesignCode + "'" \
                    " AND CommentCode = '" + imgData[1] + "'"

                trn_cursor.execute(trn_sql)

                trn_cursor.commit()

        else:
            if len(imgData) != 0:
                if (imgFileName != imgData[0]):
                    # 画像変更（同じ画像の場合には処理しない）
                    trn_sql = "UPDATE " \
                        " ChartDesign_TBL " \
                        " SET ImageName = '" + imgFileName + "' " \
                        " WHERE " + \
                        "   ChartDesignCode = '" + chartDesignCode + "'" \
                        " AND LocationInfo = '" + locationInfo + "'" \
                        " AND CommentCode = '" + imgData[1] + "'"

                    trn_cursor.execute(trn_sql)

                    # ChartComment_TBL
                    trn_sql = "UPDATE " \
                        " ChartComment_TBL " \
                        " SET Heading = '" + midashi + "' " \
                        " WHERE " + \
                        "   ChartDesignCode = '" + chartDesignCode + "'" \
                        " AND CommentCode = '" + imgData[1] + "'"

                    trn_cursor.execute(trn_sql)

                    trn_cursor.commit()

            else:
                tdatetime = datetime.now()
                updateDatetime = tdatetime.strftime('%Y%m%d%H%M%S.%f')
                commentCode = "Comment_" + updateDatetime

                # ChartDesign_TBL
                trn_sql = "INSERT INTO ChartDesign_TBL (ChartDesignCode, LocationInfo, ImageName, CommentCode) " \
                    " VALUES (" + \
                    "'" + chartDesignCode + "'," + \
                    "'" + locationInfo + "'," + \
                    "'" + imgFileName + "'," + \
                    "'" + commentCode + "'" + \
                    ") "

                trn_cursor.execute(trn_sql)

                # ChartComment_TBL
                trn_sql = "INSERT INTO ChartComment_TBL (CommentCode, Heading, ChartDesignCode) " \
                    " VALUES (" + \
                    "'" + commentCode + "'," + \
                    "'" + midashi + "'," + \
                    "'" + chartDesignCode + "'" + \
                    ") "

                trn_cursor.execute(trn_sql)

                trn_cursor.commit()

        # OK
        status['status'] = "OK"

    except Exception as e:
        trn_cursor.rollback()

        print("updateChartImg save error  " + e.args)
        status['status'] = "NG"
        pass

    # end
    finally:
        print(json.dumps(status, indent=2, ensure_ascii=False))

        return jsonify(status)

# ========================================================================
# プロセス可視化チャート図情報を保存する
# 【テキスト】
#
# ------------------------------------------------------


@ProcessDiagram_api.route("/updateChartComment/", methods=['POST', 'GET'])
def updateChartComment():

    chartDesignCode = flask.request.form['chartDesignCode']
    locationInfo = flask.request.form['locationInfo']
    midashi = flask.request.form['midashi']

    print(chartDesignCode)
    print(locationInfo)
    print(midashi)

    try:
        status = {}

        # SQL
        trn_conn = pyodbc.connect('DRIVER={SQL Server};'
                                  'Server='+app_section.get('IP')+';'
                                  'Database=' +
                                  app_section.get('DATABASE')+';'
                                  'uid='+app_section.get('DB_USER_ID')+';'
                                  'pwd='+app_section.get('DB_PASSWORD')+';')

        select_conn = pyodbc.connect('DRIVER={SQL Server};'
                                     'Server='+app_section.get('IP')+';'
                                     'Database=' +
                                     app_section.get('DATABASE')+';'
                                     'uid='+app_section.get('DB_USER_ID')+';'
                                     'pwd='+app_section.get('DB_PASSWORD')+';')

        select_conn_cursor = select_conn.cursor()

        # ---------------------------------------
        # カラム数、行数を取得する
        # ---------------------------------------
        select_query = \
            " SELECT " \
            "  ImageName ," \
            "  CommentCode " \
            " FROM " \
            "   ChartDesign_TBL " \
            " WHERE " \
            "   ChartDesignCode = '" + chartDesignCode + "'" \
            "  AND LocationInfo = '" + locationInfo + "'"

        select_conn_cursor.execute(select_query)

        imgData = []
        for x in select_conn_cursor:
            imgData.append(x[0])
            imgData.append(x[1])

        select_conn_cursor.close()

        trn_cursor = trn_conn.cursor()

        if len(imgData) != 0:
            # ChartComment_TBL
            trn_sql = "UPDATE " \
                " ChartComment_TBL " \
                " SET Heading = '" + midashi + "' " \
                " WHERE " + \
                "   ChartDesignCode = '" + chartDesignCode + "'" \
                " AND CommentCode = '" + imgData[1] + "'"

            trn_cursor.execute(trn_sql)

            trn_cursor.commit()

        # OK
        status['status'] = "OK"

    except Exception as e:
        trn_cursor.rollback()

        print("updateChartComment save error  " + e.args)
        status['status'] = "NG"
        pass

    # end
    finally:
        print(json.dumps(status, indent=2, ensure_ascii=False))

        return jsonify(status)
