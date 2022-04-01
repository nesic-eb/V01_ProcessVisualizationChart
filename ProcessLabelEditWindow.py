# -*- coding: utf-8 -*-
'''
// =============================================================================
// 機能名：プロセス可視化チャート：カラム・行ラベル位置画面
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
ProcessLabelEditWindow_api = Blueprint('ProcessLabelEditWindow', __name__)


# ========================================================================
# プロセス可視化チャート情報を取得する
#　カラム、行に表示するプロセス欄、業務区分等の情報
#
# ------------------------------------------------------


@ProcessLabelEditWindow_api.route("/getProcessChartBusinessLabelData/", methods=['POST', 'GET'])
def getProcessChartBusinessLabelData():

    try:
        processProcedureID = flask.request.form['processProcedureID']

        print("processProcedureID = [" + processProcedureID + "]")

        # SQL
        select_conn = pyodbc.connect('DRIVER={SQL Server};'
                                     'Server='+app_section.get('IP')+';'
                                     'Database=' +
                                     app_section.get('DATABASE')+';'
                                     'uid='+app_section.get('DB_USER_ID')+';'
                                     'pwd='+app_section.get('DB_PASSWORD')+';')

        select_conn_cursor = select_conn.cursor()

        # ---------------------------------------
        # プロセス可視化チャート情報（一覧情報）を取得する
        # ---------------------------------------
        select_query = \
            " SELECT " \
            "  StartIdx, " \
            "  EndIdx, " \
            "  LabelType, " \
            "  ISNULL(LabelText,'') as LabelText " \
            " FROM " \
            "   ChartBusinessLabel_TBL " \
            " WHERE " \
            "   ProcessProcedureID = '" + processProcedureID + "' " \
            " order by EndIdx"

        select_conn_cursor.execute(select_query)

        topJson = []
        dataList = Counter()
        designList = []

        # チャート情報
        for x in select_conn_cursor:
            design = Counter()
            design['StartIdx'] = x[0]
            design['EndIdx'] = x[1]
            design['LabelType'] = x[2]
            design['LabelText'] = x[3]

            designList.append(design)

        # 取り込み
        dataList['BusinessLabel'] = designList

        select_conn_cursor.close()

        topJson.append(dataList)

    except Exception as e:
        print("getProcessChartBusinessLabelData select error  " + e.args)
        pass

    # end
    finally:
        select_conn.close()

        print(json.dumps(topJson, indent=2, ensure_ascii=False))

        return jsonify(topJson)

# ========================================================================
# プロセス可視化チャート情報を取得する
#　カラム、行に表示するプロセス欄、業務区分等の情報
#
# ------------------------------------------------------


@ProcessLabelEditWindow_api.route("/getChartLabelText/", methods=['POST', 'GET'])
def getChartLabelText():

    try:
        processProcedureID = flask.request.form['processProcedureID']
        labelComment = flask.request.form['labelComment']
        dataStartIdx = flask.request.form['dataStartIdx']
        labelType = flask.request.form['labelType']

        print("processProcedureID = [" + processProcedureID + "]")
        print("labelComment = [" + labelComment + "]")
        print("dataStartIdx = [" + dataStartIdx + "]")
        print("labelType = [" + labelType + "]")

        # SQL
        select_conn = pyodbc.connect('DRIVER={SQL Server};'
                                     'Server='+app_section.get('IP')+';'
                                     'Database=' +
                                     app_section.get('DATABASE')+';'
                                     'uid='+app_section.get('DB_USER_ID')+';'
                                     'pwd='+app_section.get('DB_PASSWORD')+';')

        select_conn_cursor = select_conn.cursor()

        # ---------------------------------------
        # プロセス可視化チャート情報（一覧情報）を取得する
        # ---------------------------------------
        select_query = \
            " SELECT " \
            "  StartIdx, " \
            "  EndIdx, " \
            "  LabelType, " \
            "  ISNULL(LabelText,'') as LabelText " \
            " FROM " \
            "   ChartBusinessLabel_TBL " \
            " WHERE " \
            "  StartIdx = '" + dataStartIdx + "' " \
            "  AND LabelType = '" + labelType + "' " \
            "  AND ProcessProcedureID = '" + processProcedureID + "' " \
            " order by EndIdx"

        select_conn_cursor.execute(select_query)

        topJson = []
        dataList = Counter()
        designList = []

        # チャート情報
        for x in select_conn_cursor:
            design = Counter()
            design['StartIdx'] = x[0]
            design['EndIdx'] = x[1]
            design['LabelType'] = x[2]
            design['LabelText'] = x[3]

            designList.append(design)

        select_conn_cursor.close()

        # 新規の場合
        if len(designList) == 0:
            design = Counter()
            design['StartIdx'] = dataStartIdx
            design['EndIdx'] = dataStartIdx
            design['LabelType'] = labelType
            design['LabelText'] = ""

            designList.append(design)

        # 取り込み
        dataList['BusinessLabel'] = designList

        topJson.append(dataList)

    except Exception as e:
        print("getChartLabelText select error  " + e.args)
        pass

    # end
    finally:
        select_conn.close()

        print(json.dumps(topJson, indent=2, ensure_ascii=False))

        return jsonify(topJson)


# ========================================================================
# プロセス可視化チャート情報を取得する
#　カラム、行に表示するプロセス欄、業務区分等の情報
#
# ------------------------------------------------------


@ProcessLabelEditWindow_api.route("/updateChartLabelText/", methods=['POST', 'GET'])
def updateChartLabelText():

    try:
        processProcedureID = flask.request.form['processProcedureID']
        beforeDataStartIdx = flask.request.form['beforeDataStartIdx']
        labelText = flask.request.form['labelText']
        dataStartIdx = flask.request.form['dataStartIdx']
        dataEndIdx = flask.request.form['dataEndIdx']
        labelType = flask.request.form['labelType']

        print("processProcedureID = [" + processProcedureID + "]")
        print("beforeDataStartIdx = [" + beforeDataStartIdx + "]")
        print("labelText = [" + labelText + "]")
        print("dataStartIdx = [" + dataStartIdx + "]")
        print("dataEndIdx = [" + dataEndIdx + "]")
        print("labelType = [" + labelType + "]")

        status = {}

        # 数値へ
        if (labelType == "Process"):
            dataStartIdx = ord(dataStartIdx) - 64
            dataEndIdx = ord(dataEndIdx) - 64

        if (labelType == "Department"):
            dataStartIdx = dataStartIdx
            dataEndIdx = dataEndIdx

        # -----------------------------------
        # 重なりをチェックする
        # -----------------------------------
        # SQL
        select_conn = pyodbc.connect('DRIVER={SQL Server};'
                                     'Server='+app_section.get('IP')+';'
                                     'Database=' +
                                     app_section.get('DATABASE')+';'
                                     'uid='+app_section.get('DB_USER_ID')+';'
                                     'pwd='+app_section.get('DB_PASSWORD')+';')

        select_conn_cursor = select_conn.cursor()

        # ---------------------------------------
        # 終了位置を含む定義が存在する
        # ---------------------------------------
        designList = []

        select_query = \
            " SELECT " \
            "  StartIdx, " \
            "  EndIdx, " \
            "  LabelType, " \
            "  ISNULL(LabelText,'') as LabelText " \
            " FROM " \
            "   ChartBusinessLabel_TBL " \
            " WHERE " \
            "   ProcessProcedureID = '" + processProcedureID + "' " \
            " AND LabelType = '" + labelType + "' " \
            " AND (StartIdx >= '" + str(dataEndIdx) + "'" \
            + " AND EndIdx <= '" + str(dataEndIdx) + "') "

        select_conn_cursor.execute(select_query)

        for x in select_conn_cursor:
            design = Counter()
            design['StartIdx'] = x[0]
            design['EndIdx'] = x[1]
            design['LabelType'] = x[2]
            design['LabelText'] = x[3]

            designList.append(design)

        # 存在チェック
        selectList = []

        select_query = \
            " SELECT " \
            "  StartIdx, " \
            "  EndIdx, " \
            "  LabelType, " \
            "  ISNULL(LabelText,'') as LabelText " \
            " FROM " \
            "   ChartBusinessLabel_TBL " \
            " WHERE " \
            "   ProcessProcedureID = '" + processProcedureID + "' " \
            " AND LabelType = '" + labelType + "' " \
            " AND StartIdx = '" + str(dataStartIdx) + "'" \
            " AND EndIdx = '" + str(dataEndIdx) + "'"

        select_conn_cursor.execute(select_query)

        for x in select_conn_cursor:
            design = Counter()
            design['StartIdx'] = x[0]
            design['EndIdx'] = x[1]
            design['LabelType'] = x[2]
            design['LabelText'] = x[3]

            selectList.append(design)

        select_conn_cursor.close()

        # 重なりがない
        if len(designList) == 0:
            trn_conn = pyodbc.connect('DRIVER={SQL Server};'
                                      'Server='+app_section.get('IP')+';'
                                      'Database=' +
                                      app_section.get('DATABASE')+';'
                                      'uid='+app_section.get('DB_USER_ID')+';'
                                      'pwd='+app_section.get('DB_PASSWORD')+';')

            trn_cursor = trn_conn.cursor()

            if len(selectList) == 0:
                trn_sql = "INSERT INTO " \
                    " ChartBusinessLabel_TBL (ProcessProcedureID, StartIdx, EndIdx, LabelType, LabelText ) " \
                    " VALUES ( " + \
                    " '" + processProcedureID + "', " \
                    " '" + str(dataStartIdx) + "', " \
                    " '" + str(dataEndIdx) + "', " \
                    " '" + labelType + "', " \
                    " '" + labelText + "' " \
                    " ); "

                trn_cursor.execute(trn_sql)

                trn_cursor.commit()

            else:
                # 更新 ---------------------------
                # SQL

                trn_sql = "UPDATE " \
                    " ChartBusinessLabel_TBL " \
                    " SET " + \
                    "   StartIdx = '" + str(dataStartIdx) + "', " \
                    "   EndIdx = '" + str(dataEndIdx) + "', " \
                    "   LabelText = '" + labelText + "' " \
                    " where " \
                    "   ProcessProcedureID = '" + processProcedureID + "' " \
                    " AND StartIdx = '" + beforeDataStartIdx + "' " \
                    " AND LabelType = '" + labelType + "' "

                trn_cursor.execute(trn_sql)

                trn_cursor.commit()

            status['status'] = "OK"

        else:
            # 重複エラー
            status['status'] = "NG"
            status['message'] = "隣接するラベルが存在します。\r\n隣接する部分を削除するか、位置を変更してください。"

    except Exception as e:
        status['status'] = "NG"

        print("updateChartLabelText select error  " + e.args)
        pass

    # end
    finally:
        select_conn.close()
        trn_conn.close()

        print(json.dumps(status, indent=2, ensure_ascii=False))

        return jsonify(status)

# ========================================================================
# プロセス可視化チャート情報を削除する
#　カラム、行に表示するプロセス欄、業務区分等の情報
#
# ------------------------------------------------------


@ProcessLabelEditWindow_api.route("/deleteChartLabelText/", methods=['POST', 'GET'])
def deleteChartLabelText():

    try:
        processProcedureID = flask.request.form['processProcedureID']
        beforeDataStartIdx = flask.request.form['beforeDataStartIdx']
        labelType = flask.request.form['labelType']

        print("processProcedureID = [" + processProcedureID + "]")
        print("beforeDataStartIdx = [" + beforeDataStartIdx + "]")
        print("labelType = [" + labelType + "]")

        status = {}

        # SQL
        select_conn = pyodbc.connect('DRIVER={SQL Server};'
                                     'Server='+app_section.get('IP')+';'
                                     'Database=' +
                                     app_section.get('DATABASE')+';'
                                     'uid='+app_section.get('DB_USER_ID')+';'
                                     'pwd='+app_section.get('DB_PASSWORD')+';')

        select_conn_cursor = select_conn.cursor()

        # 存在チェック
        selectList = []

        select_query = \
            " SELECT " \
            "  StartIdx, " \
            "  EndIdx, " \
            "  LabelType, " \
            "  ISNULL(LabelText,'') as LabelText " \
            " FROM " \
            "   ChartBusinessLabel_TBL " \
            " WHERE " \
            "   ProcessProcedureID = '" + processProcedureID + "' " \
            " AND LabelType = '" + labelType + "' " \
            " AND StartIdx = '" + beforeDataStartIdx + "'" \

        select_conn_cursor.execute(select_query)

        for x in select_conn_cursor:
            design = Counter()
            design['StartIdx'] = x[0]
            design['EndIdx'] = x[1]
            design['LabelType'] = x[2]
            design['LabelText'] = x[3]

            selectList.append(design)

        select_conn_cursor.close()

        if len(selectList) != 0:
            trn_conn = pyodbc.connect('DRIVER={SQL Server};'
                                      'Server='+app_section.get('IP')+';'
                                      'Database=' +
                                      app_section.get('DATABASE')+';'
                                      'uid='+app_section.get('DB_USER_ID')+';'
                                      'pwd='+app_section.get('DB_PASSWORD')+';')

            trn_cursor = trn_conn.cursor()

            trn_sql = "DELETE " \
                " ChartBusinessLabel_TBL " \
                " WHERE " \
                "   ProcessProcedureID = '" + processProcedureID + "' " \
                " AND LabelType = '" + labelType + "' " \
                " AND StartIdx = '" + str(beforeDataStartIdx) + "'" \

            trn_cursor.execute(trn_sql)

            trn_cursor.commit()

        # OKを返す
        status['status'] = "OK"

    except Exception as e:
        status['status'] = "NG"

        print("deleteChartLabelText select error  " + e.args)
        pass

    # end
    finally:
        select_conn.close()
        trn_conn.close()

        print(json.dumps(status, indent=2, ensure_ascii=False))

        return jsonify(status)
