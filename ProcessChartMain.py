# -*- coding: utf-8 -*-
'''
// =============================================================================
// 機能名：レポート／プロセス可視化チャート
//
// =============================================================================
// （ファイル整形）Visual Studio Code : Shift + Alt + f
// =============================================================================
'''
from asyncio.windows_events import NULL
from turtle import update
from typing import Container
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

import Menu_CreateWorkItemData

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
ProcessChartMain_api = Blueprint('ProcessChartMain', __name__)

# ========================================================================
# 分類情報を取得する
#
#
# ------------------------------------------------------


@ProcessChartMain_api.route("/getClassification/", methods=['POST', 'GET'])
def getClassification():

    logger.info("Start the function getClassification in ProcessCheck......")

    try:
        classificationData = []

        org1 = flask.request.form['org1']
        org2 = flask.request.form['org2']
        print("Org1 in process check = ", org1)
        print("Org2 in process check = ", org2)

        classificationData = []
        classification_conn = pyodbc.connect('DRIVER={SQL Server};'
                                             'Server=' +
                                             app_section.get('IP')+';'
                                             'Database=' +
                                             app_section.get('DATABASE')+';'
                                             'uid=' +
                                             app_section.get('DB_USER_ID')+';'
                                             'pwd='+app_section.get('DB_PASSWORD')+';')

        classification_cursor = classification_conn.cursor()

        classification_cursor.execute(
            " SELECT "
            "   Classification_Code, "
            "	Classification_Name_abbr "
            " FROM Classification_Master_TBL "
            " WHERE Organization_Code_1 = '" + org1 + "' "
            "   AND Organization_Code_2 = '" + org2 + "' ")

        for row in classification_cursor:
            classificationData.append(row[0]+"/"+row[1])

        return jsonify(classificationData)

    except Exception as e:
        logger.Error(
            "ERROR : in the function getClassification in ProcessCheck.....")
        raise e


# ========================================================================
# 作業項目情報を取得する
#
# 戻り値（JSON）
# ------------------------------------------------------

@ProcessChartMain_api.route("/getWorkItemIDInfo/", methods=['POST', 'GET'])
def getWorkItemIDInfo():
    logger.info("Start the function getWorkItemIDInfo.....")

    try:
        workitemIDList = []
        classificationCode = flask.request.form['classification_code1']

        org1 = flask.request.form['org1']
        org2 = flask.request.form['org2']

        workitem_conn = pyodbc.connect('DRIVER={SQL Server};'
                                       'Server='+app_section.get('IP')+';'
                                       'Database=' +
                                       app_section.get('DATABASE')+';'
                                       'uid=' +
                                       app_section.get('DB_USER_ID')+';'
                                       'pwd='+app_section.get('DB_PASSWORD')+';')

        workitem_cursor = workitem_conn.cursor()
        logging.info(
            "Database connection successfully in getWorkItemIDInfo....")

        workitem_query = \
            "SELECT " \
            " wt.work_item_id, " \
            " wt.work_item_name " \
            " FROM Classification_Master_TBL AS ct, " \
            "  Workitem_Master_TBL AS wt " \
            " WHERE ct.classification_code = '" + classificationCode + "' " \
            "  AND ct.classification_code = wt.classification_code " \
            "  AND ct.Organization_Code_1 = wt.Organization_Code_1 " \
            "  AND ct.Organization_Code_2 = wt.Organization_Code_2 " \
            " order by wt.work_item_id "

        workitem_cursor.execute(workitem_query)

        Menu_CreateWorkItemData.CreateWorkItemList(
            "2020_05_31", classificationCode, org1, org2, workitemIDList)
        return jsonify(workitemIDList)

    except Exception as e:
        logger.Error(
            "ERROR : in the function getWorkItemIDInfo in ProcessCheck.....")
        raise e


# ========================================================================
# 作業項目の情報を取得する
#
# ------------------------------------------------------
# getting Work Name

@ProcessChartMain_api.route("/getWorkNameInfo/", methods=['POST', 'GET'])
def getWorkNameInfo():
    logger.info("Start the function getWorkNameInfo......")
    try:
        workitemList = []

        workitem_id = flask.request.form['workitem_id']
        workitem_id = workitem_id.strip()
        org_code1 = flask.request.form['org_code1']
        org_code2 = flask.request.form['org_code2']

        procedurename_conn = pyodbc.connect('DRIVER={SQL Server};'
                                            'Server='+app_section.get('IP')+';'
                                            'Database=' +
                                            app_section.get('DATABASE')+';'
                                            'uid=' +
                                            app_section.get('DB_USER_ID')+';'
                                            'pwd='+app_section.get('DB_PASSWORD')+';')

        procedurename_cursor = procedurename_conn.cursor()

        logging.info(
            "Database connection successfully in getWorkNameInfo...")

        procedurename_cursor.execute(
            "select "
            " Work_Name "
            "from ProcessCheckIndex_TBL where Work_Item_ID = '"+workitem_id+"'"
            " AND Organization_Code_1 = '"+org_code1+"'"
            " AND Organization_Code_2 = '"+org_code2+"';")

        for x in procedurename_cursor:
            workitemList.append(x[0])

        return jsonify(workitemList)

    except Exception as e:
        logger.Error(
            "ERROR : in the function getWorkNameInfo in ProcessCheck.....")
        raise e


# ========================================================================
# プロセス確認に登録しているデータを取得する。
#
#
# ------------------------------------------------------

@ProcessChartMain_api.route("/getAllProcessCheckData/", methods=['POST'])
def getAllProcessCheckData():
    logger.info(
        "Getting process check List in getAllProcessCheckData... ")

    try:
        org1 = flask.request.form['org1']
        org2 = flask.request.form['org2']
        print("org1 = ", org1)
        print("org2 = ", org2)

        #
        processCheck_data = []

        processCheck_conn = pyodbc.connect('DRIVER={SQL Server};'
                                           'Server='+app_section.get('IP')+';'
                                           'Database=' +
                                           app_section.get('DATABASE')+';'
                                           'uid=' +
                                           app_section.get('DB_USER_ID')+';'
                                           'pwd='+app_section.get('DB_PASSWORD')+';')

        processCheck_allselect_query = \
            " SELECT " \
            "   ct.Classification_Code , " \
            "   ct.Classification_Name , " \
            "   pt.WorkItemID , " \
            "   wt.Work_Item_Name , " \
            "   pt.ProcessProcedureName, " \
            "   ISNULL(pt.CreateMailAddress, '-') as Create_user, " \
            "   ISNULL(pt.CreateDateTime, '-') as Create_Date, " \
            "   pt.ProcessProcedureID, " \
            "   pt.ChangeProhibitionflag, " \
            "   ISNULL(pt.ChartDesignCode, '') as ChartDesignCode " \
            "     , ( " \
            " select " \
            " Surname + ' ' + name " \
            " from " \
            "  Person_Master_TBL " \
            " where " \
            "  Mail_address = pt.CreateMailAddress " \
            "  and Delete_flag <> '1' " \
            "  and Principal_business_concurrent_service_code = '0' " \
            " ) as usrname " \
            " FROM " \
            "   ProcessChartData_TBL AS pt , " \
            "   Workitem_Master_TBL AS wt , " \
            "   Classification_Master_TBL AS ct  " \
            " WHERE " \
            "   pt.OrganizationCode1 = '" + org1 + "' " \
            "   AND pt.OrganizationCode2 = '" + org2 + "' " \
            "   AND pt.WorkItemID = wt.Work_Item_ID " \
            "   AND pt.OrganizationCode1 = wt.Organization_Code_1 " \
            "   AND pt.OrganizationCode2 = wt.Organization_Code_2 " \
            "   AND wt.Classification_Code = ct.Classification_Code " \
            "   AND pt.OrganizationCode1 = ct.Organization_Code_1 " \
            "   AND pt.OrganizationCode2 = ct.Organization_Code_2 " \
            " ORDER by pt.WorkItemID "

        processCheck_cursor = processCheck_conn.cursor()
        processCheck_cursor.execute(processCheck_allselect_query)

        topjson = []
        statusJson = Counter()
        processCheck_data = []

        for x in processCheck_cursor:
            wkChartKind = x[7].split('_')
            dataList = {}
            dataList['Classification'] = x[0] + "/" + x[1].strip()
            dataList['WorkItem'] = x[2] + "/" + x[3]
            dataList['procedure_name'] = x[4]
            dataList['CreateMailAddress'] = x[5]
            dataList['CreateDateTime'] = x[6]
            dataList['ProcessProcedureID'] = x[7]
            dataList['ChangeProhibitionflag'] = x[8]
            dataList['ChartDesignCode'] = x[9]
            dataList['CreateMailAddressName'] = x[10]

            dataList['Chart_Kind'] = wkChartKind[0]

            processCheck_data.append(dataList)

        # 持ち帰り
        statusJson['status'] = "OK"
        statusJson['data'] = processCheck_data

    except Exception as e:
        statusJson['status'] = "NG"
        print("getAllProcessCheckData select error  " + e.args)

    # end
    finally:
        topjson.append(statusJson)

        print(json.dumps(topjson, indent=2, ensure_ascii=False))

        return jsonify(topjson)

# ========================================================================
# プロセス確認に登録しているデータを取得する。
#　「分類コードを選択した場合」
#
# ------------------------------------------------------


@ProcessChartMain_api.route("/getProcessCheckDataByClassification/", methods=['POST'])
def getProcessCheckDataByClassification():
    logger.info(
        "Getting process check List in getProcessCheckDataByClassification... ")

    try:
        classification_code = flask.request.form['classification_code']
        org1 = flask.request.form['org1']
        org2 = flask.request.form['org2']

        print("classification_code = ", classification_code)
        print("org1 = ", org1)
        print("org2 = ", org2)

        #
        processCheck_data = []

        processCheck_conn = pyodbc.connect('DRIVER={SQL Server};'
                                           'Server='+app_section.get('IP')+';'
                                           'Database=' +
                                           app_section.get('DATABASE')+';'
                                           'uid=' +
                                           app_section.get('DB_USER_ID')+';'
                                           'pwd='+app_section.get('DB_PASSWORD')+';')

        processCheck_allselect_query = \
            " SELECT " \
            "   ct.Classification_Code , " \
            "   ct.Classification_Name , " \
            "   pt.WorkItemID , " \
            "   wt.Work_Item_Name , " \
            "   pt.ProcessProcedureName, " \
            "   ISNULL(pt.CreateMailAddress, '-') as Create_user, " \
            "   ISNULL(pt.CreateDateTime, '-') as Create_Date, " \
            "   pt.ProcessProcedureID, " \
            "   pt.ChangeProhibitionflag " \
            "     , ( " \
            " select " \
            " Surname + ' ' + name " \
            " from " \
            "  Person_Master_TBL " \
            " where " \
            "  Mail_address = pt.CreateMailAddress " \
            "  and Delete_flag <> '1' " \
            "  and Principal_business_concurrent_service_code = '0' " \
            " ) as usrname " \
            " FROM " \
            "   ProcessChartData_TBL AS pt , " \
            "   Workitem_Master_TBL AS wt , " \
            "   Classification_Master_TBL AS ct  " \
            " WHERE " \
            "   pt.OrganizationCode1 = '" + org1 + "' " \
            "   AND pt.OrganizationCode2 = '" + org2 + "' " \
            "   AND pt.WorkItemID = wt.Work_Item_ID " \
            "   AND pt.OrganizationCode1 = wt.Organization_Code_1 " \
            "   AND pt.OrganizationCode2 = wt.Organization_Code_2 " \
            "   AND wt.Classification_Code = '" + classification_code + "' " \
            "   AND wt.Classification_Code = ct.Classification_Code " \
            "   AND pt.OrganizationCode1 = ct.Organization_Code_1 " \
            "   AND pt.OrganizationCode2 = ct.Organization_Code_2 " \
            " ORDER by pt.WorkItemID "

        processCheck_cursor = processCheck_conn.cursor()
        processCheck_cursor.execute(processCheck_allselect_query)

        topjson = []
        statusJson = Counter()
        processCheck_data = []

        for x in processCheck_cursor:
            wkChartKind = x[7].split('_')
            dataList = {}
            dataList['Classification'] = x[0] + "/" + x[1].strip()
            dataList['WorkItem'] = x[2] + "/" + x[3]
            dataList['procedure_name'] = x[4]
            dataList['CreateMailAddress'] = x[5]
            dataList['CreateDateTime'] = x[6]
            dataList['ProcessProcedureID'] = x[7]
            dataList['Chart_Kind'] = wkChartKind[0]
            dataList['ChangeProhibitionflag'] = x[8]
            dataList['CreateMailAddressName'] = x[9]

            processCheck_data.append(dataList)

        # 持ち帰り
        statusJson['status'] = "OK"
        statusJson['data'] = processCheck_data

    except Exception as e:
        statusJson['status'] = "NG"
        print("getProcessCheckDataByClassification select error  " + e.args)

    # end
    finally:
        topjson.append(statusJson)

        print(json.dumps(topjson, indent=2, ensure_ascii=False))

        return jsonify(topjson)


# ========================================================================
# プロセス確認に登録しているデータを取得する。
#　「分類コード、作業項目を選択した場合」
#
# ------------------------------------------------------

@ProcessChartMain_api.route("/getProcessCheckDataByWorkItemID/", methods=['POST'])
def getProcessCheckDataByWorkItemID():
    logger.info(
        "Getting process check List in getProcessCheckDataByWorkItemID... ")

    try:
        workitem_id = flask.request.form['workitem_id']
        classification_code = flask.request.form['classification_code']

        org1 = flask.request.form['org1']
        org2 = flask.request.form['org2']

        print("WorkItem ID = ", workitem_id)
        print("classification_code = ", classification_code)
        print("org1 = ", org1)
        print("org2 = ", org2)

        #
        processCheck_data = []

        processCheck_conn = pyodbc.connect('DRIVER={SQL Server};'
                                           'Server='+app_section.get('IP')+';'
                                           'Database=' +
                                           app_section.get('DATABASE')+';'
                                           'uid=' +
                                           app_section.get('DB_USER_ID')+';'
                                           'pwd='+app_section.get('DB_PASSWORD')+';')

        processCheck_allselect_query = \
            " SELECT " \
            "   ct.Classification_Code , " \
            "   ct.Classification_Name , " \
            "   pt.WorkItemID , " \
            "   wt.Work_Item_Name , " \
            "   pt.ProcessProcedureName, " \
            "   ISNULL(pt.CreateMailAddress, '-') as Create_user, " \
            "   ISNULL(pt.CreateDateTime, '-') as Create_Date, " \
            "   pt.ProcessProcedureID," \
            "   pt.ChangeProhibitionflag " \
            "     , ( " \
            " select " \
            " Surname + ' ' + name " \
            " from " \
            "  Person_Master_TBL " \
            " where " \
            "  Mail_address = pt.CreateMailAddress " \
            "  and Delete_flag <> '1' " \
            "  and Principal_business_concurrent_service_code = '0' " \
            " ) as usrname " \
            " FROM " \
            "   ProcessChartData_TBL AS pt , " \
            "   Workitem_Master_TBL AS wt , " \
            "   Classification_Master_TBL AS ct  " \
            " WHERE " \
            "   pt.OrganizationCode1 = '" + org1 + "' " \
            "   AND pt.OrganizationCode2 = '" + org2 + "' " \
            "   AND pt.WorkItemID = '" + workitem_id + "' " \
            "   AND pt.WorkItemID = wt.Work_Item_ID " \
            "   AND pt.OrganizationCode1 = wt.Organization_Code_1 " \
            "   AND pt.OrganizationCode2 = wt.Organization_Code_2 " \
            "   AND wt.Classification_Code = '" + classification_code + "' " \
            "   AND wt.Classification_Code = ct.Classification_Code " \
            "   AND pt.OrganizationCode1 = ct.Organization_Code_1 " \
            "   AND pt.OrganizationCode2 = ct.Organization_Code_2 " \
            " ORDER by pt.WorkItemID "

        processCheck_cursor = processCheck_conn.cursor()
        processCheck_cursor.execute(processCheck_allselect_query)

        topjson = []
        statusJson = Counter()
        processCheck_data = []

        for x in processCheck_cursor:
            wkChartKind = x[7].split('_')
            dataList = {}
            dataList['Classification'] = x[0] + "/" + x[1].strip()
            dataList['WorkItem'] = x[2] + "/" + x[3]
            dataList['procedure_name'] = x[4]
            dataList['CreateMailAddress'] = x[5]
            dataList['CreateDateTime'] = x[6]
            dataList['ProcessProcedureID'] = x[7]
            dataList['Chart_Kind'] = wkChartKind[0]
            dataList['ChangeProhibitionflag'] = x[8]
            dataList['CreateMailAddressName'] = x[9]

            processCheck_data.append(dataList)

        # 持ち帰り
        statusJson['status'] = "OK"
        statusJson['data'] = processCheck_data

    except Exception as e:
        statusJson['status'] = "NG"
        print("getProcessCheckDataByWorkItemID select error  " + e.args)

    # end
    finally:
        topjson.append(statusJson)

        print(json.dumps(topjson, indent=2, ensure_ascii=False))

        return jsonify(topjson)


# ========================================================================
# プロセス確認メンテナンス：登録機能
#
#
# ------------------------------------------------------

@ProcessChartMain_api.route('/registerProcessCheckData/', methods=['POST'])
def registerProcessCheckData():

    logger.info("Start the function registerProcessCheckData.....")

    messageList = []

    classification_code = flask.request.form['classification_code']
    workitem_id = flask.request.form['workitem_id']
    workName = flask.request.form['workName']
    org1 = flask.request.form['org1']
    org2 = flask.request.form['org2']
    user_emal = flask.request.form['user_emal']
    chartkind = flask.request.form['chartkind']

    now = datetime.now()
    # dd/mm/YY H:M:S
    dt_string = now.strftime("%Y/%m/%d %H:%M:%S")

    wkProcessProcedureID = chartkind + "_" + now.strftime("%Y%m%d%H%M%S%f")
    wkChartDesignCode = "DesignCode_" + now.strftime("%Y%m%d%H%M%S")

    try:
        selectconn = pyodbc.connect('DRIVER={SQL Server};'
                                    'Server='+app_section.get('IP')+';'
                                    'Database='+app_section.get('DATABASE')+';'
                                    'uid='+app_section.get('DB_USER_ID')+';'
                                    'pwd='+app_section.get('DB_PASSWORD')+';')

        insertconn = pyodbc.connect('DRIVER={SQL Server};'
                                    'Server='+app_section.get('IP')+';'
                                    'Database='+app_section.get('DATABASE')+';'
                                    'uid='+app_section.get('DB_USER_ID')+';'
                                    'pwd='+app_section.get('DB_PASSWORD')+';')

        workitem_id = workitem_id.strip()

        if (workitem_id != ""):
            print("Insert New workitem_id" + workitem_id)

            # 同じプロセス手順名が存在するかを確認する
            select_conn_process_cursor = selectconn.cursor()

            select_query = " SELECT " \
                "   COUNT(ProcessProcedureName) " \
                " FROM " \
                "   ProcessChartData_TBL " \
                " WHERE ProcessProcedureName = '" + workName + "'" \
                " AND WorkItemID = '" + workitem_id + "'" \
                " AND OrganizationCode1 = '" + org1 + "'" \
                " AND OrganizationCode2 = '" + org2 + "'"

            select_conn_process_cursor.execute(select_query)

            same_flag = True
            for x in select_conn_process_cursor:
                if x[0] == 1:
                    same_flag = False

            if same_flag == False:
                messageList.append("Error")
                messageList.append("既に、同じ名称が登録されています。")
                return jsonify(messageList)

            if same_flag == True:

                # Insert
                insert_query = \
                    " INSERT INTO " \
                    "  ProcessChartData_TBL " \
                    "  ( ProcessProcedureID, ProcessProcedureName, ClassificationCode, WorkItemID, " \
                    "    OrganizationCode1, OrganizationCode2, PermissionFlag, ChangeProhibitionflag, " \
                    "    WorkFrequency, NumberOfWorkers, TotalWorkingTime, ColumnNumber, RowsNumber, " \
                    "    CreateMailAddress, CreateDateTime, UpdateMailAddress, UpdateDateTime, ChartDesignCode) " \
                    "  VALUES ( " \
                    "'" + wkProcessProcedureID + "', " \
                    "'" + workName + "', " \
                    "'" + classification_code + "', " \
                    "'" + workitem_id + "', " \
                    "'" + org1 + "', " \
                    "'" + org2 + "', " \
                    "'0', " \
                    "'1', " \
                    "'0', " \
                    "'0', " \
                    "'0.0' , " \
                    "'8' , " \
                    "'8' , " \
                    "'" + user_emal + "' , " \
                    "'" + dt_string + "' , " \
                    " NULL , " \
                    " NULL , " \
                    "'" + wkChartDesignCode + "' ) "

                try:
                    insert_processdata_cursor = insertconn.cursor()
                    insert_processdata_cursor.execute(insert_query)
                    insertconn.commit()

                except Exception as e:
                    insertconn.rollback()
                    messageList.append("Error")
                    messageList.append("Insert Error（内部エラー）")
                    return jsonify(messageList)

        # 正常終了
        messageList.append("Normal")
        return jsonify(messageList)

    except Exception as e:
        logger.Error("Error : in the function registerProcessCheckData.....")
        messageList.append("Error")
        messageList.append("Exception Error（内部エラー）: " + str(type(e)))
        return jsonify(messageList)


# ========================================================================
# 削除する
#
# ------------------------------------------------------

@ProcessChartMain_api.route("/deleteProcessCheckData/", methods=['POST'])
def deleteProcessCheckData():
    logger.info(
        "start the function deleteProcessCheckData ")

    try:
        select_processCheck_conn = pyodbc.connect('DRIVER={SQL Server};'
                                                  'Server=' +
                                                  app_section.get('IP')+';'
                                                  'Database=' +
                                                  app_section.get(
                                                      'DATABASE')+';'
                                                  'uid=' +
                                                  app_section.get(
                                                      'DB_USER_ID')+';'
                                                  'pwd='+app_section.get('DB_PASSWORD')+';')

        delete_processCheck_conn = pyodbc.connect('DRIVER={SQL Server};'
                                                  'Server=' +
                                                  app_section.get('IP')+';'
                                                  'Database=' +
                                                  app_section.get(
                                                      'DATABASE')+';'
                                                  'uid=' +
                                                  app_section.get(
                                                      'DB_USER_ID')+';'
                                                  'pwd='+app_section.get('DB_PASSWORD')+';')

        workName = flask.request.form['workName']
        workitem_id = flask.request.form['workitem_id']
        org1 = flask.request.form['org1']
        org2 = flask.request.form['org2']
        processProcedureID = flask.request.form['processProcedureID']

        print("Procedure delete = ", workName)
        print("workitem_id delete = ", workitem_id)
        print("processProcedureID delete = ", processProcedureID)

        select_cursor = select_processCheck_conn.cursor()

        # 統一キーを取得する
        chartDesignCode = ""
        select_query = \
            "SELECT " \
            "  ISNULL(ChartDesignCode, '') as ChartDesignCode" \
            " FROM " \
            "  ProcessChartData_TBL " \
            " WHERE " \
            "  ProcessProcedureName = '" + workName + "' " \
            " And ProcessProcedureID = '" + processProcedureID + "' " \
            " And OrganizationCode1 = '" + org1 + "' " \
            " And OrganizationCode2 = '" + org2 + "' "

        select_cursor.execute(select_query)

        for x in select_cursor:
            if x[0] != "":
                chartDesignCode = x[0]

        if chartDesignCode != "":
            delete_cursor = delete_processCheck_conn.cursor()

            try:
                # 1. 親データ
                delete_processCheck_query = \
                    "Delete from " \
                    " ProcessChartData_TBL " \
                    " WHERE " \
                    " ProcessProcedureName = '" + workName + "' " \
                    " And ProcessProcedureID = '" + processProcedureID + "' " \
                    " And OrganizationCode1 = '" + org1 + "' " \
                    " And OrganizationCode2 = '" + org2 + "' "

                delete_cursor.execute(delete_processCheck_query)

                # 2. デザインテーブル
                delete_processCheck_query = \
                    "Delete from " \
                    " ChartDesign_TBL " \
                    " WHERE " \
                    " ChartDesignCode = '" + chartDesignCode + "' " \

                delete_cursor.execute(delete_processCheck_query)

                # 3. コメントテーブル
                delete_processCheck_query = \
                    "Delete from " \
                    " ChartComment_TBL " \
                    " WHERE " \
                    " ChartDesignCode = '" + chartDesignCode + "' " \

                delete_cursor.execute(delete_processCheck_query)

                # 削除成功
                delete_processCheck_conn.commit()

            except Exception as e:
                # 削除失敗
                delete_processCheck_conn.rollback()
                return "fail to deleteProcessCheckData delete.."

        return "success delete"

    except:
        return "fail to deleteProcessCheckData delete.."

    # end
    finally:
        delete_processCheck_conn.close()
        select_cursor.close()


# ========================================================================
# コピー先作業名情報を取得する
#
#
# ------------------------------------------------------

@ProcessChartMain_api.route("/getAllProcessProcedureName/", methods=['POST', 'GET'])
def getAllProcessProcedureName():

    logger.info(
        "Start the function getAllProcessProcedureName in ProcessCheck......")

    try:
        processProcedureNameData = []

        org1 = flask.request.form['org1']
        org2 = flask.request.form['org2']

        processProcedure_conn = pyodbc.connect('DRIVER={SQL Server};'
                                               'Server=' +
                                               app_section.get('IP')+';'
                                               'Database=' +
                                               app_section.get('DATABASE')+';'
                                               'uid=' +
                                               app_section.get(
                                                   'DB_USER_ID')+';'
                                               'pwd='+app_section.get('DB_PASSWORD')+';')

        processProcedure_cursor = processProcedure_conn.cursor()

        processProcedure_cursor.execute(
            " SELECT "
            "   ProcessProcedureName "
            " FROM ProcessChartData_TBL "
            " WHERE OrganizationCode1 = '" + org1 + "' "
            "   AND OrganizationCode2 = '" + org2 + "' ")

        for row in processProcedure_cursor:
            processProcedureNameData.append(row[0])

        return jsonify(processProcedureNameData)

    except Exception as e:
        logger.Error(
            "ERROR : in the function getAllProcessProcedureName in ProcessCheck.....")
        raise e


# ========================================================================
# コピー先作業名情報を取得する(By classification)
#
#
# ------------------------------------------------------

@ProcessChartMain_api.route("/getProcessProcedureNameByClassification/", methods=['POST', 'GET'])
def getProcessProcedureNameByClassification():

    logger.info(
        "Start the function getProcessProcedureNameByClassification in ProcessCheck......")

    try:
        processProcedureNameData = []

        classificationCode = flask.request.form['classification_code']
        org1 = flask.request.form['org1']
        org2 = flask.request.form['org2']

        processProcedure_conn = pyodbc.connect('DRIVER={SQL Server};'
                                               'Server=' +
                                               app_section.get('IP')+';'
                                               'Database=' +
                                               app_section.get('DATABASE')+';'
                                               'uid=' +
                                               app_section.get(
                                                   'DB_USER_ID')+';'
                                               'pwd='+app_section.get('DB_PASSWORD')+';')

        processProcedure_cursor = processProcedure_conn.cursor()

        processProcedure_cursor.execute(
            " SELECT "
            "   ProcessProcedureName "
            " FROM ProcessChartData_TBL "
            " WHERE ClassificationCode = '" + classificationCode + "' "
            " AND OrganizationCode1 = '" + org1 + "' "
            "   AND OrganizationCode2 = '" + org2 + "' ")

        for row in processProcedure_cursor:
            processProcedureNameData.append(row[0])

        return jsonify(processProcedureNameData)

    except Exception as e:
        logger.Error(
            "ERROR : in the function getProcessProcedureNameByclassification in ProcessCheck.....")
        raise e


# ========================================================================
# Get ChartDesign code
#
#
# ------------------------------------------------------

@ProcessChartMain_api.route("/getChartDesignCode/", methods=['POST', 'GET'])
def getChartDesignCode():

    logger.info(
        "Start the function getChartDesignCode in ProcessCheck......")

    try:
        chartDesignCodedata = []

        workName = flask.request.form['workName']
        org1 = flask.request.form['org1']
        org2 = flask.request.form['org2']

        processProcedure_conn = pyodbc.connect('DRIVER={SQL Server};'
                                               'Server=' +
                                               app_section.get('IP')+';'
                                               'Database=' +
                                               app_section.get('DATABASE')+';'
                                               'uid=' +
                                               app_section.get(
                                                   'DB_USER_ID')+';'
                                               'pwd='+app_section.get('DB_PASSWORD')+';')

        processProcedure_cursor = processProcedure_conn.cursor()

        processProcedure_cursor.execute(
            " SELECT "
            "   ChartDesignCode "
            " FROM ProcessChartData_TBL "
            " WHERE ProcessProcedureName = '" + workName + "' "
            " AND OrganizationCode1 = '" + org1 + "' "
            "   AND OrganizationCode2 = '" + org2 + "' ")

        for row in processProcedure_cursor:
            chartDesignCodedata.append(row[0])

        return jsonify(chartDesignCodedata)

    except Exception as e:
        logger.Error(
            "ERROR : in the function getChartDesignCode in ProcessCheck.....")
        raise e


# ========================================================================
# プロセス確認メンテナンス：コピー機能
#
#
# ------------------------------------------------------

@ProcessChartMain_api.route('/copyProcessCheckData/', methods=['POST'])
def copyProcessCheckData():

    logger.info("Start the function copyProcessCheckData.....")

    messageList = []
    cmntList = []
    designList = []

    classification_code = flask.request.form['classification_code']
    workitem_id = flask.request.form['workitem_id']
    chartDesigncode = flask.request.form['chartDesigncode']
    workName2 = flask.request.form['workName2']
    org1 = flask.request.form['org1']
    org2 = flask.request.form['org2']
    user_emal = flask.request.form['user_emal']
    chartkind = flask.request.form['chartkind']

    now = datetime.now()
    # dd/mm/YY H:M:S
    dt_string = now.strftime("%Y/%m/%d %H:%M:%S")

    wkProcessProcedureID = chartkind + "_" + now.strftime("%Y%m%d%H%M%S%f")
    wkChartDesignCode = "DesignCode_" + now.strftime("%Y%m%d%H%M%S")

    try:
        selectconn = pyodbc.connect('DRIVER={SQL Server};'
                                    'Server='+app_section.get('IP')+';'
                                    'Database='+app_section.get('DATABASE')+';'
                                    'uid='+app_section.get('DB_USER_ID')+';'
                                    'pwd='+app_section.get('DB_PASSWORD')+';')

        insertconn = pyodbc.connect('DRIVER={SQL Server};'
                                    'Server='+app_section.get('IP')+';'
                                    'Database='+app_section.get('DATABASE')+';'
                                    'uid='+app_section.get('DB_USER_ID')+';'
                                    'pwd='+app_section.get('DB_PASSWORD')+';')

        copyconn = pyodbc.connect('DRIVER={SQL Server};'
                                  'Server='+app_section.get('IP')+';'
                                  'Database='+app_section.get('DATABASE')+';'
                                  'uid='+app_section.get('DB_USER_ID')+';'
                                  'pwd='+app_section.get('DB_PASSWORD')+';')

        insertDesignconn = pyodbc.connect('DRIVER={SQL Server};'
                                          'Server='+app_section.get('IP')+';'
                                          'Database=' +
                                          app_section.get('DATABASE')+';'
                                          'uid=' +
                                          app_section.get('DB_USER_ID')+';'
                                          'pwd='+app_section.get('DB_PASSWORD')+';')

        insertCommentconn = pyodbc.connect('DRIVER={SQL Server};'
                                           'Server='+app_section.get('IP')+';'
                                           'Database=' +
                                           app_section.get('DATABASE')+';'
                                           'uid=' +
                                           app_section.get('DB_USER_ID')+';'
                                           'pwd='+app_section.get('DB_PASSWORD')+';')

        workitem_id = workitem_id.strip()

        if (workitem_id != ""):
            print("Insert New workitem_id" + workitem_id)

            # 同じプロセス手順名が存在するかを確認する
            select_conn_process_cursor = selectconn.cursor()

            select_query = " SELECT " \
                "   COUNT(ProcessProcedureName) " \
                " FROM " \
                "   ProcessChartData_TBL " \
                " WHERE ProcessProcedureName = '" + workName2 + "'" \
                " AND WorkItemID = '" + workitem_id + "'" \
                " AND OrganizationCode1 = '" + org1 + "'" \
                " AND OrganizationCode2 = '" + org2 + "'"

            select_conn_process_cursor.execute(select_query)

            same_flag = True
            for x in select_conn_process_cursor:
                if x[0] == 1:
                    same_flag = False

            if same_flag == False:
                messageList.append("Error")
                messageList.append("既に、同じ名称が登録されています。")
                return jsonify(messageList)

            if same_flag == True:

                # Insert
                insert_query = \
                    " INSERT INTO " \
                    "  ProcessChartData_TBL " \
                    "  ( ProcessProcedureID, ProcessProcedureName, ClassificationCode, WorkItemID, " \
                    "    OrganizationCode1, OrganizationCode2, PermissionFlag, ChangeProhibitionflag, " \
                    "    WorkFrequency, NumberOfWorkers, TotalWorkingTime, ColumnNumber, RowsNumber, " \
                    "    CreateMailAddress, CreateDateTime, UpdateMailAddress, UpdateDateTime, ChartDesignCode) " \
                    "  VALUES ( " \
                    "'" + wkProcessProcedureID + "', " \
                    "'" + workName2 + "', " \
                    "'" + classification_code + "', " \
                    "'" + workitem_id + "', " \
                    "'" + org1 + "', " \
                    "'" + org2 + "', " \
                    "'0', " \
                    "'1', " \
                    "'0', " \
                    "'0', " \
                    "'0.0' , " \
                    "'8' , " \
                    "'8' , " \
                    "'" + user_emal + "' , " \
                    "'" + dt_string + "' , " \
                    " NULL , " \
                    " NULL , " \
                    "'" + wkChartDesignCode + "' ) "

                # ChartComment_TBL Select
                copy_cursor = copyconn.cursor()
                select_comment_query = " SELECT " \
                    "   Heading, " \
                    "   Efficiency " \
                    " FROM " \
                    "   ChartComment_TBL " \
                    " WHERE ChartDesignCode = '" + chartDesigncode + "'"

                copy_cursor.execute(select_comment_query)
                for row in copy_cursor:
                    cmntData = []
                    cmntData.append(row[0])
                    cmntData.append(row[1])
                    cmntList.append(cmntData)

                # ChartDesign_TBL Select
                copy_cursor = copyconn.cursor()
                select_chart_query = " SELECT " \
                    "   LocationInfo, " \
                    "   ImageName " \
                    " FROM " \
                    "   ChartDesign_TBL " \
                    " WHERE ChartDesignCode = '" + chartDesigncode + "'"

                copy_cursor.execute(select_chart_query)

                for c in copy_cursor:
                    designData = []
                    designData.append(c[0])
                    designData.append(c[1])
                    designList.append(designData)

                # Insert ChartDesign_TBL
                trn_sql_varied = "INSERT INTO ChartDesign_TBL (ChartDesignCode, LocationInfo, ImageName, CommentCode) " \
                    " VALUES ( " \
                    " '@CHARTDESIGNCODE@' , " \
                    " '@LOCATIONINFO@' , " \
                    " '@IMAGENAME@' , " \
                    " '@COMMENTCODE@' ) "

                # Insert ChartComment_TBL
                trn_sql1_varied = "INSERT INTO ChartComment_TBL (CommentCode, Heading, Efficiency, ChartDesignCode) " \
                    " VALUES ( " \
                    " '@COMMENTCODE@' , " \
                    " '@HEADING@' , " \
                    " '@EFFICIENCY@' , " \
                    " '@CHARTDESIGNCODE@' ) "

                print("len = ", len(designList))
                for i in range(0, len(designList)):
                    # SQL文
                    trn_sql = trn_sql_varied
                    trn_sql = trn_sql.replace(
                        '@CHARTDESIGNCODE@', wkChartDesignCode)
                    trn_sql = trn_sql.replace(
                        '@LOCATIONINFO@', designList[i][0])
                    trn_sql = trn_sql.replace('@IMAGENAME@', designList[i][1])

                    tdatetime = datetime.now()
                    updateDatetime = tdatetime.strftime('%Y%m%d%H%M%S.%f')
                    commentCode = "Comment_" + updateDatetime
                    trn_sql = trn_sql.replace('@COMMENTCODE@', commentCode)

                    # SQL文
                    trn_sql1 = trn_sql1_varied
                    trn_sql1 = trn_sql1.replace(
                        '@COMMENTCODE@', commentCode)
                    trn_sql1 = trn_sql1.replace('@HEADING@', cmntList[i][0])
                    trn_sql1 = trn_sql1.replace('@EFFICIENCY@', cmntList[i][1])
                    trn_sql1 = trn_sql1.replace(
                        '@CHARTDESIGNCODE@', wkChartDesignCode)

                    #
                    insert_design_cursor = insertDesignconn.cursor()
                    insert_design_cursor.execute(trn_sql)
                    insertDesignconn.commit()

                    insert_comment_cursor = insertCommentconn.cursor()
                    insert_comment_cursor.execute(trn_sql1)
                    insertCommentconn.commit()

                try:
                    insert_processdata_cursor = insertconn.cursor()
                    insert_processdata_cursor.execute(insert_query)
                    insertconn.commit()

                except Exception as e:
                    insertconn.rollback()
                    insertDesignconn.rollback()
                    insertCommentconn.rollback()
                    messageList.append("Error")
                    messageList.append("Insert Error（内部エラー）")
                    return jsonify(messageList)

        # 正常終了
        messageList.append("Normal")
        return jsonify(messageList)

    except Exception as e:
        logger.Error("Error : in the function registerProcessCheckData.....")
        messageList.append("Error")
        messageList.append("Exception Error（内部エラー）: " + str(type(e)))
        return jsonify(messageList)
