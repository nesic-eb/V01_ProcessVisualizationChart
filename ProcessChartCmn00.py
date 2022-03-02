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

        wkList = []
        dataCnt = 1

        # 全ての情報を一時保存する
        for x in select_conn_cursor:
            wkData = Counter()
            wkData['name'] = x[0]
            wkData['file'] = x[1]

            wkList.append(wkData)

        ChartType['ChartType'] = FlowChart
        ChartType['Data'] = wkList

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
#　画像に紐づくコメント情報
#
# ------------------------------------------------------


@ProcessChartCmn00_api.route("/getProcessChartDrawingData/", methods=['POST', 'GET'])
def getProcessChartDrawingData():

    try:
        processProcedureID = flask.request.form['processProcedureID']
        chartDesignCode = flask.request.form['chartDesignCode']

        print("processProcedureID = " + processProcedureID + "]")
        print("chartDesignCode = [" + chartDesignCode + "]")

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
            "  ISNULL(ClassificationCode,'') as ClassificationCode," \
            "  ISNULL(WorkItemID,'') as WorkItemID," \
            "  ISNULL(OrganizationCode1,'') as OrganizationCode1," \
            "  ISNULL(OrganizationCode2,'') as OrganizationCode2," \
            "  ISNULL(PermissionFlag,'') as PermissionFlag," \
            "  ISNULL(ChangeProhibitionFlag,'') as ChangeProhibitionFlag," \
            "  ISNULL(WorkFrequency,'') as WorkFrequency," \
            "  ISNULL(NumberOfWorkers,'') as NumberOfWorkers," \
            "  ISNULL(TotalWorkingTime,'') as TotalWorkingTime," \
            "  ISNULL(ColumnNumber,'6') as ColumnNumber," \
            "  ISNULL(RowsNumber,'6') as RowsNumber," \
            "  ISNULL(ChartDesignCode,'') as ChartDesignCode " \
            " FROM " \
            "   ProcessChartData_TBL "

        select_conn_cursor.execute(select_query)

        topJson = []
        dataList = Counter()
        dataListData = []
        dataCnt = 0

        chartType = ""

        # チャート情報
        for x in select_conn_cursor:
            if x[0] == processProcedureID:
                if x[13] == chartDesignCode:
                    wkChartType = x[0].split('_')
                    chartType = wkChartType[0]

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

        print("chartType = " + chartType)

        # ---------------------------------------
        # プロセス可視化チャート図情報を取得する
        # ---------------------------------------
        select_query = \
            "SELECT " \
            "  de.ChartDesignCode, " \
            "  de.LocationInfo, " \
            "  de.ImageName, " \
            "  de.CommentCode, " \
            "  ISNULL(co.Heading, '') as Heading, " \
            "  ISNULL(co.Explanation, '') as Explanation, " \
            "  ISNULL(co.Efficiency, '') as Efficiency, " \
            "  ISNULL(co.OperationTarget,'') as OperationTarget, " \
            "  ISNULL(co.WorkingHour, '') as WorkingHour, " \
            "  ISNULL(co.ExceptionWork,'') as ExceptionWork, " \
            "  ISNULL(co.SupplementComment, '') as SupplementComment, " \
            "  (select ImageFileName from ChartImage_Master_TBL where ChartKind = '" + chartType + "' and ImageName = de.ImageName) as ImageFileName, " \
            "  SUBSTRING(de.LocationInfo, 1, 1) as ColumnName, " \
            "  SUBSTRING(de.LocationInfo, 3, 7) as RowsNo " \
            "FROM " \
            "    ChartDesign_TBL as de, " \
            "    ChartComment_TBL as co " \
            "WHERE " \
            "   de.ChartDesignCode = '" + chartDesignCode + "'" \
            "   AND co.CommentCode = de.CommentCode " \
            "Order by RowsNo, ColumnName "

        select_conn_cursor.execute(select_query)

        designList = []

        # チャート情報
        for x in select_conn_cursor:
            designPointBlock = Counter()

            design = Counter()
            design['ChartDesignCode'] = x[0]
            design['LocationInfo'] = x[1]
            design['ImageName'] = x[2]
            design['ImageFileName'] = x[11]
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
# プロセス可視化チャート図情報を取得する
#　親情報に紐づく情報（全部）
#
# ------------------------------------------------------


@ProcessChartCmn00_api.route("/getProcessChartCommentDataAll/", methods=['POST', 'GET'])
def getProcessChartCommentDataAll():

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

        topJson = []

        # ---------------------------------------
        # コメント内容情報を取得する
        # ---------------------------------------
        select_query = \
            "SELECT " \
            "  co.CommentCode, " \
            "  ISNULL(co.Heading, '') as Heading, " \
            "  ISNULL(co.Explanation, '') as Explanation, " \
            "  ISNULL(co.Efficiency, '') as Efficiency, " \
            "  ISNULL(co.OperationTarget,'') as OperationTarget, " \
            "  ISNULL(co.WorkingHour, '') as WorkingHour, " \
            "  ISNULL(co.ExceptionWork,'') as ExceptionWork, " \
            "  ISNULL(co.SupplementComment, '') as SupplementComment " \
            "  ISNULL(co.ChartDesignCode, '') as ChartDesignCode " \
            "FROM " \
            "  ChartComment_TBL as co " \
            "WHERE " \
            "  co.ChartDesignCode = '" + chartDesignCode + "'" \
            "Order by co.CommentCode "

        select_conn_cursor.execute(select_query)

        commentList = []
        dataList = Counter()
        dataCnt = 0

        # チャート情報
        for x in select_conn_cursor:
            dataCnt = dataCnt + 1

            commentData = Counter()
            # Comment
            commentData['CommentCode'] = x[0]
            commentData['Heading'] = x[1]
            commentData['Explanation'] = x[2]
            commentData['Efficiency'] = x[3]
            commentData['OperationTarget'] = x[4]
            commentData['WorkingHour'] = x[5]
            commentData['ExceptionWork'] = x[6]
            commentData['SupplementComment'] = x[7]
            commentData['ChartDesignCode'] = x[8]

            commentList.append(commentData)

        # 取り込み
        dataList['Num'] = format(dataCnt, '05')
        dataList['Comment'] = commentList

        select_conn_cursor.close()

        topJson.append(dataList)

    except Exception as e:
        print("getProcessChartDrawingDataAll select error  " + e.args)
        pass

    # end
    finally:
        select_conn.close()

        print(json.dumps(topJson, indent=2, ensure_ascii=False))

        return jsonify(topJson)


# ========================================================================
# プロセス可視化チャート図：コメント内容情報を取得する
# 位置指定
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
            "  ISNULL(co.Heading, '') as Heading, " \
            "  ISNULL(co.Explanation, '') as Explanation, " \
            "  ISNULL(co.Efficiency, '') as Efficiency, " \
            "  ISNULL(co.OperationTarget,'') as OperationTarget, " \
            "  ISNULL(co.WorkingHour, '') as WorkingHour, " \
            "  ISNULL(co.ExceptionWork,'') as ExceptionWork, " \
            "  ISNULL(co.SupplementComment, '') as SupplementComment " \
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


# ========================================================================
# プロセス可視化チャート図：カラムを増減する
#　例）D列にデータあって、D列を削除すると、D列のデータは消える
#
# ------------------------------------------------------

@ProcessChartCmn00_api.route("/getProcessChartColumnUpdate/", methods=['POST', 'GET'])
def getProcessChartColumnUpdate():

    try:
        chartDesignCode = flask.request.form['chartDesignCode']
        LocationInfo = flask.request.form['LocationInfo']
        updateType = flask.request.form['updateType']

        print(chartDesignCode)
        print(LocationInfo)
        print(updateType)

        topJson = []
        resultStatus = {}

        getColumnRows = {}
        getProcessChartDataColumnAndRows(chartDesignCode, getColumnRows)

        # SQL
        select_conn = pyodbc.connect('DRIVER={SQL Server};'
                                     'Server='+app_section.get('IP')+';'
                                     'Database=' +
                                     app_section.get('DATABASE')+';'
                                     'uid='+app_section.get('DB_USER_ID')+';'
                                     'pwd='+app_section.get('DB_PASSWORD')+';')

        select_conn_cursor = select_conn.cursor()

        select_query = "SELECT " \
            "  de.ChartDesignCode, " \
            "  de.LocationInfo, " \
            "  de.ImageName, " \
            "  de.CommentCode " \
            "FROM " \
            "    ChartDesign_TBL as de " \
            "WHERE " \
            "  de.ChartDesignCode = '" + chartDesignCode + "'" \
            "  AND SUBSTRING(de.LocationInfo,1,1) >= " + \
            " SUBSTRING('" + LocationInfo + "',1,1)"

        select_conn_cursor.execute(select_query)

        dataList = []

        # 位置情報を作成する
        for x in select_conn_cursor:
            design = Counter()
            design['ChartDesignCode'] = x[0]
            design['LocationInfo'] = x[1]
            design['ImageName'] = x[2]
            design['CommentCode'] = x[3]
            design['updateLocationInfo'] = columnNameChange(x[1], updateType)

            dataList.append(design)

        # Close
        select_conn.close()

        # Debug
        for colum in dataList:
            print('LocationInfo = ' + colum['LocationInfo'])
            print('    --> ' + colum['updateLocationInfo'])

        # 全削除、全追加
        trn_conn = pyodbc.connect('DRIVER={SQL Server};'
                                  'Server='+app_section.get('IP')+';'
                                  'Database=' +
                                  app_section.get('DATABASE')+';'
                                  'uid='+app_section.get('DB_USER_ID')+';'
                                  'pwd='+app_section.get('DB_PASSWORD')+';')
        try:
            trn_cursor = trn_conn.cursor()

            trn_sql = "DELETE " \
                " FROM ChartDesign_TBL " \
                " WHERE " \
                "  ChartDesignCode = '" + chartDesignCode + "'" \
                "  AND SUBSTRING(LocationInfo,1,1) >= " + \
                " SUBSTRING('" + LocationInfo + "',1,1)"

            trn_cursor.execute(trn_sql)

            # 登録
            for colum in dataList:
                if ord(colum['updateLocationInfo'][0]) > ord(LocationInfo[0]):
                    # 指定カラムは操作しない
                    trn_sql = "INSERT INTO ChartDesign_TBL (ChartDesignCode, LocationInfo, ImageName, CommentCode) " \
                        " VALUES (" + \
                        "'" + colum['ChartDesignCode'] + "'," + \
                        "'" + colum['updateLocationInfo'] + "'," + \
                        "'" + colum['ImageName'] + "'," + \
                        "'" + colum['CommentCode'] + "'" + \
                        ") "

                    trn_cursor.execute(trn_sql)

            # 親データのカラム数を更新する
            updateColumn = getColumnRows['Column']
            if updateType == "plus":
                updateColumn = updateColumn + 1
            else:
                updateColumn = updateColumn - 1

            trn_sql = "UPDATE " \
                " ProcessChartData_TBL " \
                " SET ColumnNumber = '" + str(updateColumn) + "'" \
                " WHERE " \
                "  ChartDesignCode = '" + chartDesignCode + "'"

            # 結果
            trn_conn.commit()
            resultStatus['statsu'] = "OK"

        except Exception as e:
            trn_conn.rollback()
            resultStatus['statsu'] = "NG"

        # 処理結果
        topJson.append(resultStatus)

    except Exception as e:
        resultStatus['statsu'] = "NG"
        print("getProcessChartCommentData select error  " + e.args)
        pass

    # end
    finally:

        print(json.dumps(topJson, indent=2, ensure_ascii=False))

        return jsonify(topJson)


# カラム文字を加算／減算する
def columnNameChange(columnName, updateType):
    wkColumnArray = columnName.split('_')
    resultstr = columnName

    if updateType == "plus":
        if (wkColumnArray[0] != 'Z'):
            # 加算 C -> D
            code = ord(wkColumnArray[0])
            code += 1
            resultstr = chr(code)
    else:
        if (wkColumnArray[0] != 'A'):
            # 減算 D -> C
            code = ord(wkColumnArray[0])
            code -= 1
            resultstr = chr(code)

    return resultstr + "_" + wkColumnArray[1]


# ========================================================================
# プロセス可視化チャート図：行を増減する
#　例）3行にデータあって、３行を削除すると、３行のデータは消える
#
# ------------------------------------------------------

@ProcessChartCmn00_api.route("/getProcessChartRowsUpdate/", methods=['POST', 'GET'])
def getProcessChartRowsUpdate():

    try:
        chartDesignCode = flask.request.form['chartDesignCode']
        LocationInfo = flask.request.form['LocationInfo']
        updateType = flask.request.form['updateType']

        print(chartDesignCode)
        print(LocationInfo)
        print(updateType)

        topJson = []
        resultStatus = {}

        getColumnRows = {}
        getProcessChartDataColumnAndRows(chartDesignCode, getColumnRows)

        # SQL
        select_conn = pyodbc.connect('DRIVER={SQL Server};'
                                     'Server='+app_section.get('IP')+';'
                                     'Database=' +
                                     app_section.get('DATABASE')+';'
                                     'uid='+app_section.get('DB_USER_ID')+';'
                                     'pwd='+app_section.get('DB_PASSWORD')+';')

        select_conn_cursor = select_conn.cursor()

        # 行番号の文字数を取得する
        # D_11 など、３カラム以降を取得する
        targetRow = LocationInfo[2:]
        targetRowLen = len(targetRow)

        select_query = "SELECT " \
            "  de.ChartDesignCode, " \
            "  de.LocationInfo, " \
            "  de.ImageName, " \
            "  de.CommentCode " \
            "FROM " \
            "    ChartDesign_TBL as de " \
            "WHERE " \
            "  de.ChartDesignCode = '" + chartDesignCode + "'" \
            "  AND SUBSTRING(de.LocationInfo,3," + str(targetRowLen) + ") >= " \
            " SUBSTRING('" + LocationInfo + "',3," + str(targetRowLen) + ")"

        select_conn_cursor.execute(select_query)

        dataList = []

        # 位置情報を作成する
        for x in select_conn_cursor:
            design = Counter()
            design['ChartDesignCode'] = x[0]
            design['LocationInfo'] = x[1]
            design['ImageName'] = x[2]
            design['CommentCode'] = x[3]
            design['updateLocationInfo'] = rowsNameChange(x[1], updateType)

            dataList.append(design)

        # Debug
        for colum in dataList:
            print('LocationInfo = ' + colum['LocationInfo'])
            print('    --> ' + colum['updateLocationInfo'])

        # 全削除、全追加
        trn_conn = pyodbc.connect('DRIVER={SQL Server};'
                                  'Server='+app_section.get('IP')+';'
                                  'Database=' +
                                  app_section.get('DATABASE')+';'
                                  'uid='+app_section.get('DB_USER_ID')+';'
                                  'pwd='+app_section.get('DB_PASSWORD')+';')
        try:
            trn_cursor = trn_conn.cursor()

            trn_sql = "DELETE " \
                " FROM ChartDesign_TBL " \
                " WHERE " \
                "  ChartDesignCode = '" + chartDesignCode + "'" \
                "  AND SUBSTRING(LocationInfo,3," + str(targetRowLen) + ") >= " \
                " SUBSTRING('" + LocationInfo + "',3," + \
                str(targetRowLen) + ")"

            trn_cursor.execute(trn_sql)

            # 登録
            for colum in dataList:
                trn_sql = "INSERT INTO ChartDesign_TBL (ChartDesignCode, LocationInfo, ImageName, CommentCode) " \
                    " VALUES (" + \
                    "'" + colum['ChartDesignCode'] + "'," + \
                    "'" + colum['updateLocationInfo'] + "'," + \
                    "'" + colum['ImageName'] + "'," + \
                    "'" + colum['CommentCode'] + "'" + \
                    ") "

                trn_cursor.execute(trn_sql)

            # 親データの行数を更新する
            updateRows = getColumnRows['Rows']
            if updateType == "plus":
                updateRows = updateRows + 1
            else:
                updateRows = updateRows - 1

            trn_sql = "UPDATE " \
                " ProcessChartData_TBL " \
                " SET RowsNumber = '" + str(updateRows) + "'" \
                " WHERE " \
                "  ChartDesignCode = '" + chartDesignCode + "'"

            trn_cursor.execute(trn_sql)

            # 結果
            trn_conn.commit()
            resultStatus['statsu'] = "OK"

        except Exception as e:
            trn_conn.rollback()
            resultStatus['statsu'] = "NG"

        # 処理結果
        topJson.append(resultStatus)

    except Exception as e:
        resultStatus['statsu'] = "NG"
        print("getProcessChartRowsUpdate select error  " + e.args)
        pass

    # end
    finally:

        print(json.dumps(topJson, indent=2, ensure_ascii=False))

        return jsonify(topJson)


# 行番号を加算／減算する
def rowsNameChange(rowsName, updateType):
    wkRowsArray = rowsName.split('_')
    resultstr = rowsName

    # 行番号
    targetRowNo = int(rowsName[2:])

    if updateType == "plus":
        # 加算 C_1 -> C_2
        targetRowNo = targetRowNo + 1
        resultstr = wkRowsArray[0] + "_" + str(targetRowNo)
    else:
        # 減算 C_2 -> C_1
        targetRowNo = targetRowNo - 1
        resultstr = wkRowsArray[0] + "_" + str(targetRowNo)

    return resultstr

# 親テーブルのカラム数、行数を取得する


def getProcessChartDataColumnAndRows(chartDesignCode, getDataList):

    try:
        # SQL
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
            "  ColumnNumber ," \
            "  RowsNumber " \
            " FROM " \
            "   ProcessChartData_TBL " \
            " WHERE " \
            "   chartDesignCode = '" + chartDesignCode + "'"

        select_conn_cursor.execute(select_query)

        for x in select_conn_cursor:
            getDataList['Column'] = int(x[0])
            getDataList['Rows'] = int(x[1])

        select_conn_cursor.close()

    except Exception as e:
        print("getProcessChartDataColumnAndRows select error  " + e.args)
        pass

    # end
    finally:
        select_conn.close()
