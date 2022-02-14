# -*- coding: utf-8 -*-
'''
// =============================================================================
// 機能名：レポート／プロセス可視化チャート
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
        logging.info(
            "Database connection successfully in getAllProcessCheckData function.....")

        processCheck_allselect_query = \
            " SELECT " \
            "   ct.Classification_Code , " \
            "   ct.Classification_Name , " \
            "   pt.Work_Item_ID , " \
            "   wt.Work_Item_Name , " \
            "   pt.Work_Name, " \
            "   ISNULL(pt.Created_By, '-') as Create_user , " \
            "   ISNULL(pt.Create_Date, '-') as Create_Date " \
            " FROM " \
            "   ProcessCheckIndex_TBL AS pt , " \
            "   Workitem_Master_TBL AS wt , " \
            "   Classification_Master_TBL AS ct  " \
            " WHERE " \
            "   pt.Organization_Code_1 = '" + org1 + "' " \
            "   AND pt.Organization_Code_2 = '" + org2 + "' " \
            "   AND pt.Work_Item_ID = wt.Work_Item_ID " \
            "   AND pt.Organization_Code_1 = wt.Organization_Code_1 " \
            "   AND pt.Organization_Code_2 = wt.Organization_Code_2 " \
            "   AND wt.Classification_Code = ct.Classification_Code " \
            "   AND pt.Organization_Code_1 = ct.Organization_Code_1 " \
            "   AND pt.Organization_Code_2 = ct.Organization_Code_2 " \
            " ORDER by pt.work_item_id "

        processCheck_cursor = processCheck_conn.cursor()
        processCheck_cursor.execute(processCheck_allselect_query)

        for x in processCheck_cursor:
            processCheck_data.append(
                x[0] + "/" + x[1] + " | " + x[2] + "/" + x[3] + " | "+x[4] + " | "+x[5] + " | " + x[6])
        return jsonify(processCheck_data)

    except:
        return "NULL"


# ========================================================================
# プロセス確認に登録しているデータを取得する。
#
#
# ------------------------------------------------------

@ProcessChartMain_api.route("/getProcessCheckDataByClassification/", methods=['POST'])
def getProcessCheckDataByClassification():
    logger.info(
        "Getting process check List in getProcessCheckDataByClassification... ")

    try:
        classification_code = flask.request.form['classification_code']
        print("classification_code = ", classification_code)
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
        logging.info(
            "Database connection successfully in getProcessCheckDataByClassification function.....")

        processCheck_select_query = \
            " SELECT " \
            "   ct.Classification_Code , " \
            "   ct.Classification_Name , " \
            "   pt.Work_Item_ID , " \
            "   wt.Work_Item_Name , " \
            "   pt.Work_Name , " \
            "   ISNULL(pt.Created_By, '-') as Create_user , " \
            "   ISNULL(pt.Create_Date, '-') as Create_Date " \
            " FROM " \
            "   ProcessCheckIndex_TBL AS pt , " \
            "   Workitem_Master_TBL AS wt , " \
            "   Classification_Master_TBL AS ct  " \
            " WHERE " \
            "   pt.Organization_Code_1 = '" + org1 + "' " \
            "   AND pt.Organization_Code_2 = '" + org2 + "' " \
            "   AND pt.Work_Item_ID = wt.Work_Item_ID " \
            "   AND pt.Organization_Code_1 = wt.Organization_Code_1 " \
            "   AND pt.Organization_Code_2 = wt.Organization_Code_2 " \
            "   AND wt.Classification_Code = '" + classification_code + "' " \
            "   AND wt.Classification_Code = ct.Classification_Code " \
            "   AND pt.Organization_Code_1 = ct.Organization_Code_1 " \
            "   AND pt.Organization_Code_2 = ct.Organization_Code_2 " \
            " ORDER by work_item_id "
        processCheck_cursor = processCheck_conn.cursor()
        processCheck_cursor.execute(processCheck_select_query)

        for x in processCheck_cursor:
            processCheck_data.append(
                x[0] + "/" + x[1] + " | " + x[2] + "/" + x[3] + " | "+x[4] + " | "+x[5] + " | " + x[6])
        return jsonify(processCheck_data)

    except:
        return "NULL"


# ========================================================================
# プロセス確認に登録しているデータを取得する。
#
#
# ------------------------------------------------------

@ProcessChartMain_api.route("/getProcessCheckDataByWorkItemID/", methods=['POST'])
def getProcessCheckDataByWorkItemID():
    logger.info(
        "Getting process check List in getProcessCheckDataByWorkItemID... ")

    try:
        workitem_id = flask.request.form['workitem_id']
        print("WorkItem ID = ", workitem_id)
        classification_code = flask.request.form['classification_code']
        print("classification_code = ", classification_code)
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
        logging.info(
            "Database connection successfully in getProcessCheckDataByWorkItemID function.....")

        processCheck_select_query = \
            " SELECT " \
            "   ct.Classification_Code , " \
            "   ct.Classification_Name , " \
            "   pt.Work_Item_ID , " \
            "   wt.Work_Item_Name , " \
            "   pt.Work_Name , " \
            "   ISNULL(pt.Created_By, '-') as Create_user , " \
            "   ISNULL(pt.Create_Date, '-') as Create_Date " \
            " FROM " \
            "   ProcessCheckIndex_TBL AS pt , " \
            "   Workitem_Master_TBL AS wt , " \
            "   Classification_Master_TBL AS ct  " \
            " WHERE " \
            "   pt.Organization_Code_1 = '" + org1 + "' " \
            "   AND pt.Organization_Code_2 = '" + org2 + "' " \
            "   AND pt.Work_Item_ID = '" + workitem_id + "' " \
            "   AND pt.Work_Item_ID = wt.Work_Item_ID " \
            "   AND pt.Organization_Code_1 = wt.Organization_Code_1 " \
            "   AND pt.Organization_Code_2 = wt.Organization_Code_2 " \
            "   AND wt.Classification_Code = '" + classification_code + "' " \
            "   AND wt.Classification_Code = ct.Classification_Code " \
            "   AND pt.Organization_Code_1 = ct.Organization_Code_1 " \
            "   AND pt.Organization_Code_2 = ct.Organization_Code_2 " \
            " ORDER by work_item_id "

        processCheck_cursor = processCheck_conn.cursor()
        processCheck_cursor.execute(processCheck_select_query)

        for x in processCheck_cursor:
            processCheck_data.append(
                x[0] + "/" + x[1] + " | " + x[2] + "/" + x[3] + " | "+x[4] + " | "+x[5] + " | " + x[6])
        return jsonify(processCheck_data)

    except:
        return "NULL"


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
    user_name = flask.request.form['user_name']

    now = datetime.now()
    # dd/mm/YY H:M:S
    dt_string = now.strftime("%Y/%m/%d %H:%M:%S")

    try:
        insertconn = pyodbc.connect('DRIVER={SQL Server};'
                                    'Server='+app_section.get('IP')+';'
                                    'Database='+app_section.get('DATABASE')+';'
                                    'uid='+app_section.get('DB_USER_ID')+';'
                                    'pwd='+app_section.get('DB_PASSWORD')+';')
        selectconn = pyodbc.connect('DRIVER={SQL Server};'
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
                "   COUNT(Work_Name) " \
                " FROM " \
                "   ProcessCheckIndex_TBL " \
                " WHERE Work_Name = '" + workName + "'" \
                " AND Organization_Code_1 = '" + org1 + "'" \
                " AND Organization_Code_2 = '" + org2 + "'"
            select_conn_process_cursor.execute(select_query)

            same_flag = True
            for x in select_conn_process_cursor:
                if x[0] == 1:
                    same_flag = False

            if same_flag == False:
                messageList.append("Error")
                messageList.append("同じプロセス手順名が登録されています。")
                return jsonify(messageList)

            if same_flag == True:

                # Insert
                insert_query = \
                    " INSERT INTO " \
                    "  ProcessCheckIndex_TBL " \
                    "  ( Work_Name, Organization_Code_1, Organization_Code_2, Work_Item_ID, Total_Time, " \
                    "      Working_Frequency, Worker_Count, Create_Date, Created_By, Modify_date, Modified_By) " \
                    "  VALUES ( " \
                    "'" + workName + "', " \
                    "'" + org1 + "', " \
                    "'" + org2 + "', " \
                    "'" + workitem_id + "', " \
                    "'0.0' , " \
                    " NULL , " \
                    " NULL , " \
                    "'" + dt_string + "' , " \
                    "'" + user_name + "' , " \
                    " NULL , " \
                    " NULL ) "

                try:
                    insert_processdata_cursor = insertconn.cursor()
                    insert_processdata_cursor.execute(insert_query)
                    insertconn.commit()
                except Exception as e:
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

    delete_processCheck_conn = pyodbc.connect('DRIVER={SQL Server};'
                                              'Server=' +
                                              app_section.get('IP')+';'
                                              'Database=' +
                                              app_section.get('DATABASE')+';'
                                              'uid=' +
                                              app_section.get('DB_USER_ID')+';'
                                              'pwd='+app_section.get('DB_PASSWORD')+';')

    try:
        workName = flask.request.form['workName']
        print("Procedure delete = ", workName)
        workitem_id = flask.request.form['workitem_id']
        print("workitem_id delete = ", workitem_id)
        org1 = flask.request.form['org1']
        org2 = flask.request.form['org2']

        delete_cursor = delete_processCheck_conn.cursor()

        delete_processCheck_query = \
            "Delete from " \
            " ProcessCheckIndex_TBL " \
            " WHERE " \
            " Work_Name = '"+workName+"' " \
            " And Work_Item_ID = '" + workitem_id + "' " \
            " And Organization_Code_1 = '" + org1 + "' " \
            " And Organization_Code_2 = '" + org2 + "' "

        delete_cursor.execute(delete_processCheck_query)
        delete_processCheck_conn.commit()

        return "success delete"

    except:
        return "fail to delete.."
