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
ProcessChartCmn00_api = Blueprint('ProcessChartCmn00', __name__)

# ========================================================================
# 画像情報の取得
#
#
# ------------------------------------------------------


@ProcessChartCmn00_api.route("/getProcessChartImagesData/", methods=['POST', 'GET'])
def getProcessChartImagesData():

    try:
        FlowChart = flask.request.form['ChartType']

        print(FlowChart)

        # SQL
        select_conn = pyodbc.connect('DRIVER={SQL Server};'
                                     'Server='+app_section.get('IP')+';'
                                     'Database=' +
                                     app_section.get('DATABASE')+';'
                                     'uid='+app_section.get('DB_USER_ID')+';'
                                     'pwd='+app_section.get('DB_PASSWORD')+';')

        select_conn_cursor = select_conn.cursor()

        # ---------------------------------------
        # 画像情報を取得する
        # ---------------------------------------
        select_query = \
            " SELECT " \
            "  ImageName,  " \
            "  ImageFileName  " \
            " FROM " \
            "   ChartImage_Master_TBL " \
            " WHERE " \
            "   ChartKind = '" + FlowChart + "'" \
            "  AND DeleteFlag = '0' " \
            " ORDER BY OrderNumber "

        select_conn_cursor.execute(select_query)

        topJson = []

        ChartType = Counter()
        ChartType['ChartType'] = FlowChart

        wkData = Counter()
        dataCnt = 1

        # 全ての情報を一時保存する
        for x in select_conn_cursor:
            wkData[x[0]] = x[1]

        ChartType['ChartType'] = FlowChart
        ChartType['Data'] = wkData

        select_conn_cursor.close()

        topJson.append(ChartType)

    except Exception as e:
        print("getProcessChartImagesData select error  " + e.args)
        pass

    # end
    finally:
        select_conn.close()

        print(json.dumps(topJson, indent=2, ensure_ascii=False))

        return jsonify(topJson)


# ========================================================================
# プロセス可視化チャート情報（一覧情報）を取得する
#
#
# ------------------------------------------------------


@ProcessChartCmn00_api.route("/getProcessChartListAll/", methods=['POST', 'GET'])
def getProcessChartListAll():

    try:
        email = flask.request.form['email']
        org1 = flask.request.form['sessionOrg1']
        org2 = flask.request.form['sessionOrg2']

        print(email)
        print(org1)
        print(org2)

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
            "  ProcessProcedureID ," \
            "  ProcessProcedureName ," \
            "  ClassificationCode ," \
            "  WorkItemID ," \
            "  OrganizationCode1 ," \
            "  OrganizationCode2 ," \
            "  PermissionFlag ," \
            "  ChangeProhibitionFlag ," \
            "  WorkFrequency ," \
            "  NumberOfWorkers ," \
            "  TotalWorkingTime ," \
            "  ColumnNumber ," \
            "  RowsNumber " \
            " FROM " \
            "   ProcessChartData_TBL " \
            " WHERE " \
            "   OrganizationCode1 = '" + org1 + "'" \
            " AND OrganizationCode2 = '" + org2 + "'" \
            " ORDER BY ProcessProcedureName "

        select_conn_cursor.execute(select_query)

        topJson = []
        dataList = Counter()
        dataListData = []
        dataCnt = 0

        # 全ての情報を一時保存する
        for x in select_conn_cursor:
            ChartType = Counter()
            ChartType['ProcessProcedureID'] = x[0]
            ChartType['ProcessProcedureName'] = x[1]
            ChartType['ClassificationCode'] = x[2]
            ChartType['WorkItemID'] = x[3]
            ChartType['OrganizationCode1'] = x[4]
            ChartType['OrganizationCode2'] = x[5]
            ChartType['PermissionFlag'] = x[6]
            ChartType['ChangeProhibitionFlag'] = x[7]
            ChartType['WorkFrequency'] = x[8]
            ChartType['NumberOfWorkers'] = x[9]
            ChartType['TotalWorkingTime'] = x[10]
            ChartType['ColumnNumber'] = x[11]
            ChartType['RowsNumber'] = x[12]

            dataListData.append(ChartType)

            dataCnt = dataCnt + 1

        dataList['Num'] = format(dataCnt, '03')
        dataList['Data'] = dataListData

        select_conn_cursor.close()

        topJson.append(dataList)

    except Exception as e:
        print("getProcessChartListAll select error  " + e.args)
        pass

    # end
    finally:
        select_conn.close()

        print(json.dumps(topJson, indent=2, ensure_ascii=False))

        return jsonify(topJson)


# ========================================================================
# プロセス可視化チャート図情報を取得する
#
#
# ------------------------------------------------------


@ProcessChartCmn00_api.route("/getProcessChartDrawingData/", methods=['POST', 'GET'])
def getProcessChartDrawingData():

    try:
        chartDesignCode = flask.request.form['chartDesignCode']

        print(chartDesignCode)

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
            "  ProcessProcedureID ," \
            "  ProcessProcedureName ," \
            "  ClassificationCode ," \
            "  WorkItemID ," \
            "  OrganizationCode1 ," \
            "  OrganizationCode2 ," \
            "  PermissionFlag ," \
            "  ChangeProhibitionFlag ," \
            "  WorkFrequency ," \
            "  NumberOfWorkers ," \
            "  TotalWorkingTime ," \
            "  ColumnNumber ," \
            "  RowsNumber ," \
            "  ChartDesignCode " \
            " FROM " \
            "   ProcessChartData_TBL " \
            " WHERE " \
            "   ChartDesignCode = '" + chartDesignCode + "'"

        select_conn_cursor.execute(select_query)

        topJson = []
        dataList = Counter()
        dataListData = []
        dataCnt = 0

        # チャート情報
        for x in select_conn_cursor:
            ChartType = Counter()
            ChartType['ProcessProcedureID'] = x[0]
            ChartType['ProcessProcedureName'] = x[1]
            ChartType['ClassificationCode'] = x[2]
            ChartType['WorkItemID'] = x[3]
            ChartType['OrganizationCode1'] = x[4]
            ChartType['OrganizationCode2'] = x[5]
            ChartType['PermissionFlag'] = x[6]
            ChartType['ChangeProhibitionFlag'] = x[7]
            ChartType['WorkFrequency'] = x[8]
            ChartType['NumberOfWorkers'] = x[9]
            ChartType['TotalWorkingTime'] = x[10]
            ChartType['ColumnNumber'] = x[11]
            ChartType['RowsNumber'] = x[12]
            ChartType['ChartDesignCode'] = x[13]

            dataListData.append(ChartType)

            dataCnt = dataCnt + 1

        dataList['Num'] = format(dataCnt, '03')
        dataList['Data'] = dataListData

        # ---------------------------------------
        # プロセス可視化チャート図情報を取得する
        # ---------------------------------------
        select_query = \
            "SELECT " \
            "  de.ChartDesignCode, " \
            "  de.LocationInfo, " \
            "  de.ImageName, " \
            "  de.CommentCode, " \
            "  co.Heading, " \
            "  co.Explanation, " \
            "  co.Efficiency, " \
            "  co.OperationTarget, " \
            "  co.WorkingHour, " \
            "  co.ExceptionWork, " \
            "  co.SupplementComment " \
            "FROM " \
            "    ChartDesign_TBL as de, " \
            "    ChartComment_TBL as co " \
            "WHERE " \
            "   de.ChartDesignCode = '" + chartDesignCode + "'" \
            "   AND co.CommentCode = de.CommentCode " \
            "Order by de.LocationInfo "

        select_conn_cursor.execute(select_query)

        designList = []

        # チャート情報
        for x in select_conn_cursor:
            designPointBlock = Counter()

            design = Counter()
            design['ChartDesignCode'] = x[0]
            design['LocationInfo'] = x[1]
            design['ImageName'] = x[2]
            design['CommentCode'] = x[3]
            # Comment
            design['Heading'] = x[4]
            design['Explanation'] = x[5]
            design['Efficiency'] = x[6]
            design['OperationTarget'] = x[7]
            design['WorkingHour'] = x[8]
            design['ExceptionWork'] = x[9]
            design['SupplementComment'] = x[10]

            designPointBlock['Pnt'] = x[1]
            designPointBlock['Block'] = design
            designList.append(designPointBlock)

        # 取り込み
        dataList['design'] = designList

        select_conn_cursor.close()

        topJson.append(dataList)

    except Exception as e:
        print("getProcessChartDrawingData select error  " + e.args)
        pass

    # end
    finally:
        select_conn.close()

        print(json.dumps(topJson, indent=2, ensure_ascii=False))

        return jsonify(topJson)

# ========================================================================
# プロセス可視化チャート図：コメント内容情報を取得する
#
#
# ------------------------------------------------------


@ProcessChartCmn00_api.route("/getProcessChartCommentData/", methods=['POST', 'GET'])
def getProcessChartCommentData():

    try:
        chartDesignCode = flask.request.form['chartDesignCode']
        LocationInfo = flask.request.form['LocationInfo']

        print(chartDesignCode)
        print(LocationInfo)

        # SQL
        select_conn = pyodbc.connect('DRIVER={SQL Server};'
                                     'Server='+app_section.get('IP')+';'
                                     'Database=' +
                                     app_section.get('DATABASE')+';'
                                     'uid='+app_section.get('DB_USER_ID')+';'
                                     'pwd='+app_section.get('DB_PASSWORD')+';')

        select_conn_cursor = select_conn.cursor()

        topJson = []

        # ---------------------------------------
        # プロセス可視化チャート図情報を取得する
        # ---------------------------------------
        select_query = \
            "SELECT " \
            "  de.ChartDesignCode, " \
            "  de.LocationInfo, " \
            "  de.ImageName, " \
            "  de.CommentCode, " \
            "  co.Heading, " \
            "  co.Explanation, " \
            "  co.Efficiency, " \
            "  co.OperationTarget, " \
            "  co.WorkingHour, " \
            "  co.ExceptionWork, " \
            "  co.SupplementComment " \
            "FROM " \
            "    ChartDesign_TBL as de, " \
            "    ChartComment_TBL as co " \
            "WHERE " \
            "   de.ChartDesignCode = '" + chartDesignCode + "'" \
            "   AND de.LocationInfo = '" + LocationInfo + "'" \
            "   AND de.CommentCode = co.CommentCode "

        select_conn_cursor.execute(select_query)

        designList = []
        dataList = Counter()

        # チャート情報
        for x in select_conn_cursor:
            designPointBlock = Counter()

            design = Counter()
            design['ChartDesignCode'] = x[0]
            design['LocationInfo'] = x[1]
            design['ImageName'] = x[2]
            design['CommentCode'] = x[3]
            # Comment
            design['Heading'] = x[4]
            design['Explanation'] = x[5]
            design['Efficiency'] = x[6]
            design['OperationTarget'] = x[7]
            design['WorkingHour'] = x[8]
            design['ExceptionWork'] = x[9]
            design['SupplementComment'] = x[10]

            designPointBlock['Pnt'] = x[1]
            designPointBlock['Block'] = design
            designList.append(designPointBlock)

        # 取り込み
        dataList['design'] = designList

        select_conn_cursor.close()

        topJson.append(dataList)

    except Exception as e:
        print("getProcessChartCommentData select error  " + e.args)
        pass

    # end
    finally:
        select_conn.close()

        print(json.dumps(topJson, indent=2, ensure_ascii=False))

        return jsonify(topJson)
