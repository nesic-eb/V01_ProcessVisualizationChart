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
#　【名称を変更する】
#
# ------------------------------------------------------


@ProcessDiagram_api.route("/saveProcessChartImagesData/", methods=['POST', 'GET'])
def saveProcessChartImagesData():

    try:
        updateUser = flask.request.form['updateUser']

        processProcedureID = flask.request.form['processProcedureID']
        processProcedureName = flask.request.form['processProcedureName']
        chartDesignCode = flask.request.form['chartDesignCode']

        print(processProcedureID)
        print(processProcedureName)
        print(chartDesignCode)

        status = {}

        # SQL
        update_conn = pyodbc.connect('DRIVER={SQL Server};'
                                     'Server='+app_section.get('IP')+';'
                                     'Database=' +
                                     app_section.get('DATABASE')+';'
                                     'uid='+app_section.get('DB_USER_ID')+';'
                                     'pwd='+app_section.get('DB_PASSWORD')+';')

        conn_cursor = update_conn.cursor()

        tdatetime = datetime.now()
        updateDatetime = tdatetime.strftime('%Y-%m-%d %H:%M:%S')

        # ---------------------------------------
        # プロセス可視化チャート情報（一覧情報）を更新する
        # ---------------------------------------
        update_query = \
            " UPDATE  ProcessChartData_TBL " \
            "  SET ProcessProcedureName = '" + processProcedureName + "'" \
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
# 【枠数を変更する】
#
# ------------------------------------------------------


@ProcessDiagram_api.route("/changeToProcessChartColumnRow/", methods=['POST', 'GET'])
def changeToProcessChartColumnRow():

    try:
        processProcedureID = flask.request.form['processProcedureID']
        chartDesignCode = flask.request.form['chartDesignCode']

        columnNumber = flask.request.form['columnNumber']
        rowsNumber = flask.request.form['rowsNumber']

        print(processProcedureID)
        print(chartDesignCode)

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

        # ---------------------------------------
        # プロセス可視化チャート情報（一覧情報）を更新する
        # ---------------------------------------
        update_query = \
            " UPDATE  ProcessChartData_TBL " \
            "  SET ColumnNumber = '" + columnNumber + "' " \
            "  , RowsNumber = '" + rowsNumber + "' " \
            " WHERE " \
            "  ProcessProcedureID = '" + processProcedureID + "'"

        conn_cursor.execute(update_query)
        conn_cursor.commit()

        status['status'] = "OK"

    except Exception as e:
        print("changeToProcessChartColumnRow save error  " + e.args)
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

    try:
        chartDesignCode = flask.request.form['chartDesignCode']
        imgFileName = flask.request.form['imgFileName']
        locationInfo = flask.request.form['locationInfo']
        midashi = flask.request.form['midashi']

        print(chartDesignCode)
        print(imgFileName)
        print(locationInfo)
        print(midashi)

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
                trn_sql = "INSERT INTO ChartComment_TBL (CommentCode, Heading, Efficiency, ChartDesignCode) " \
                    " VALUES (" + \
                    "'" + commentCode + "'," + \
                    "'" + midashi + "'," + \
                    "'0'," + \
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

# ========================================================================
# プロセス可視化チャート図情報を保存する
# 【全カラムの更新】
#
# ------------------------------------------------------


@ProcessDiagram_api.route("/saveAllChartDesign/", methods=['POST', 'GET'])
def saveAllChartDesign():

    status = {}

    try:
        json_data = flask.request.data

        d = json.loads(json_data)

        # print(sendList)

        chartDesignCode = d['chartDesignCode']

        saveDesignData = []

        for i in range(len(d['userInfoList'])):
            wkData = d['userInfoList'][i]
            wkData['resut'] = "0"

            print("-- " + str(i) + " -----------------")
            print(wkData['img'])
            print(wkData['text'])
            print(wkData['location'])

            saveDesignData.append(wkData)

        # 登録情報を集める
        select_conn = pyodbc.connect('DRIVER={SQL Server};'
                                     'Server='+app_section.get('IP')+';'
                                     'Database=' +
                                     app_section.get('DATABASE')+';'
                                     'uid='+app_section.get('DB_USER_ID')+';'
                                     'pwd='+app_section.get('DB_PASSWORD')+';')

        select_conn_cursor = select_conn.cursor()

        # ChartDesign_TBLを退避する
        ChartDesignTBLData = []

        select_query = \
            " SELECT " \
            "  LocationInfo, " \
            "  ImageName, " \
            "  CommentCode " \
            " FROM " \
            "   ChartDesign_TBL " \
            " WHERE " \
            "   ChartDesignCode = '" + chartDesignCode + "'" \
            " order by LocationInfo"

        select_conn_cursor.execute(select_query)

        for x in select_conn_cursor:
            wkData = {}
            wkData['resut'] = "0"
            wkData['LocationInfo'] = x[0]
            wkData['ImageName'] = x[1]
            wkData['CommentCode'] = x[2]

            # 保存
            ChartDesignTBLData.append(wkData)

        # ChartComment_TBL を退避する
        ChartCommentTBLData = []

        select_query = \
            " SELECT " \
            " CommentCode " \
            " , ISNULL(Heading, '') " \
            " , ISNULL(Explanation, '') " \
            " , ISNULL(Efficiency, '') " \
            " , ISNULL(OperationTarget, '') " \
            " , ISNULL(WorkingHour, '') " \
            " , ISNULL(ExceptionWork, '') " \
            " , ISNULL(SupplementComment, '') " \
            " , ISNULL(ChartDesignCode, '') " \
            " FROM " \
            "   ChartComment_TBL " \
            " WHERE " \
            "   ChartDesignCode = '" + chartDesignCode + "'"

        select_conn_cursor.execute(select_query)

        for x in select_conn_cursor:
            wkData = {}
            wkData['resut'] = "0"
            wkData['CommentCode'] = x[0]
            wkData['Heading'] = x[1]
            wkData['Explanation'] = x[2]
            wkData['Efficiency'] = x[3]
            wkData['OperationTarget'] = x[4]
            wkData['WorkingHour'] = x[5]
            wkData['ExceptionWork'] = x[6]
            wkData['SupplementComment'] = x[7]
            wkData['ChartDesignCode'] = x[8]

            # 保存
            ChartCommentTBLData.append(wkData)

        select_conn_cursor.close()

        # ----------------------------------------------------
        # 更新処理
        # ----------------------------------------------------
        trn_conn = pyodbc.connect('DRIVER={SQL Server};'
                                  'Server='+app_section.get('IP')+';'
                                  'Database=' +
                                  app_section.get('DATABASE')+';'
                                  'uid='+app_section.get('DB_USER_ID')+';'
                                  'pwd='+app_section.get('DB_PASSWORD')+';')

        trn_cursor = trn_conn.cursor()

        # 該当テーブル削除

        # ChartDesign_TBL
        trn_sql = "DELETE " \
            " ChartDesign_TBL " \
            " WHERE " + \
            "   ChartDesignCode = '" + chartDesignCode + "'"

        trn_cursor.execute(trn_sql)

        trn_sql = "DELETE " \
            " ChartComment_TBL " \
            " WHERE " + \
            "   ChartDesignCode = '" + chartDesignCode + "'"

        trn_cursor.execute(trn_sql)

        # ChartDesign_TBLに追加する
        for saveItem in saveDesignData:
            # ChartDesign_TBL
            for location in ChartDesignTBLData:
                if location['LocationInfo'] == saveItem['location']:
                    # 画像ファイルを差しかえる
                    location['ImageName'] = saveItem['img']
                    # 使用
                    location['resut'] = "1"
                    # 指定データ
                    saveItem['resut'] = "1"

                    # ChartComment_TBL
                    for comment in ChartCommentTBLData:
                        if comment['CommentCode'] == location['CommentCode']:
                            # 見出しを差しかえる
                            comment['Heading'] = saveItem['text']
                            # 使用
                            comment['resut'] = "1"

        # 使用だけを登録する
        # （更新情報）
        for location in ChartDesignTBLData:
            if location['resut'] == "1":
                print("-- ChartDesignTBL 再登録 ---------------------------")
                print(location['CommentCode'])
                print(location['LocationInfo'])
                print(location['ImageName'])

                # ChartDesign_TBL
                trn_sql = "INSERT INTO ChartDesign_TBL (ChartDesignCode, LocationInfo, ImageName, CommentCode) " \
                    " VALUES (" + \
                    "'" + chartDesignCode + "'," + \
                    "'" + location['LocationInfo'] + "'," + \
                    "'" + location['ImageName'] + "'," + \
                    "'" + location['CommentCode'] + "'" + \
                    ") "

                trn_cursor.execute(trn_sql)

        # 使用だけを登録する
        for comment in ChartCommentTBLData:
            if comment['resut'] == "1":
                print("-- ChartCommentTBL 再登録 ---------------------------")
                print(comment['CommentCode'])
                print(comment['Heading'])

                # ChartComment_TBL
                trn_sql = "INSERT INTO ChartComment_TBL (CommentCode, Heading, Explanation, Efficiency, OperationTarget, WorkingHour, ExceptionWork, SupplementComment, ChartDesignCode) " \
                    " VALUES (" + \
                    "'" + comment['CommentCode'] + "'," + \
                    "'" + comment['Heading'] + "'," + \
                    "'" + comment['Explanation'] + "'," + \
                    "'" + comment['Efficiency'] + "'," + \
                    "'" + comment['OperationTarget'] + "'," + \
                    "'" + comment['WorkingHour'] + "'," + \
                    "'" + comment['ExceptionWork'] + "'," + \
                    "'" + comment['SupplementComment'] + "'," + \
                    "'" + comment['ChartDesignCode'] + "' " + \
                    ") "

                trn_cursor.execute(trn_sql)

        # 未登録を登録する
        for entryData in saveDesignData:
            if entryData['resut'] == "0":
                print("-- 未登録のデータ ---------------------------")
                print(entryData['img'])
                print(entryData['text'])
                print(entryData['location'])

                tdatetime = datetime.now()
                updateDatetime = tdatetime.strftime('%Y%m%d%H%M%S.%f')
                commentCode = "Comment_" + updateDatetime

                # ChartDesign_TBL
                trn_sql = "INSERT INTO ChartDesign_TBL (ChartDesignCode, LocationInfo, ImageName, CommentCode) " \
                    " VALUES (" + \
                    "'" + chartDesignCode + "'," + \
                    "'" + entryData['location'] + "'," + \
                    "'" + entryData['img'] + "'," + \
                    "'" + commentCode + "'" + \
                    ") "

                trn_cursor.execute(trn_sql)

                # ChartComment_TBL
                trn_sql = "INSERT INTO ChartComment_TBL (CommentCode, Heading, Efficiency, ChartDesignCode) " \
                    " VALUES (" + \
                    "'" + commentCode + "'," + \
                    "'" + entryData['text'] + "'," + \
                    "'0'," + \
                    "'" + chartDesignCode + "'" + \
                    ") "

                trn_cursor.execute(trn_sql)

                trn_cursor.commit()

        # OK
        status['status'] = "OK"

        trn_cursor.commit()

    except Exception as e:
        trn_cursor.rollback()

        print("saveAllChartDesign save error  " + e.args)
        status['status'] = "NG"
        pass

    # end
    finally:
        print(json.dumps(status, indent=2, ensure_ascii=False))

        return jsonify(status)
