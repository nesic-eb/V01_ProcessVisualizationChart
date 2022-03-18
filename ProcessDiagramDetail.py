# -*- coding: utf-8 -*-
'''
// =============================================================================
// 機能名：プロセス可視化チャート：詳細画面
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
ProcessDiagramDetail_api = Blueprint('ProcessDiagramDetail', __name__)

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

@ProcessDiagramDetail_api.route("/setProcessChartTblData/", methods=['POST', 'GET'])
def setProcessChartTblData():

    try:
        email = flask.request.form['email']
        org1 = flask.request.form['org1']
        org2 = flask.request.form['org2']
        processProcedureID = flask.request.form['processProcedureID']
        processProcedureName = flask.request.form['processProcedureName']
        chartDesignCode = flask.request.form['chartDesignCode']

        permissionFlag = flask.request.form['permissionFlag']
        changeProhibitionFlag = flask.request.form['changeProhibitionFlag']

        totalWorkingTime = flask.request.form['totalWorkingTime']
        workFrequency = flask.request.form['workFrequency']
        numberOfWorkers = flask.request.form['numberOfWorkers']

        print(email)
        print(org1)
        print(org2)
        print(processProcedureID)
        print(processProcedureName)
        print(chartDesignCode)

        print(permissionFlag)
        print(changeProhibitionFlag)
        print(totalWorkingTime)
        print(workFrequency)
        print(numberOfWorkers)

        statusJson = {}

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

        # ---------------------------------------
        # プロセス可視化チャート情報（一覧情報）を更新する
        # ---------------------------------------
        update_query = \
            " UPDATE  ProcessChartData_TBL " \
            "  SET PermissionFlag = '" + pFlag + "' " \
            "  , ChangeProhibitionFlag = '" + cFlag + "' " \
            "  , WorkFrequency = '" + workFrequency + "' " \
            "  , NumberOfWorkers = '" + numberOfWorkers + "' " \
            "  , TotalWorkingTime = '" + totalWorkingTime + "' " \
            " WHERE " \
            "  ProcessProcedureID = '" + processProcedureID + "'"

        conn_cursor.execute(update_query)
        conn_cursor.commit()

        statusJson['status'] = "OK"

    except Exception as e:
        conn_cursor.rollback()
        statusJson['status'] = "NG"
        print("setProcessChartTblData update error  " + e.args)
        pass

    # end
    finally:
        update_conn.close()

        print(json.dumps(statusJson, indent=2, ensure_ascii=False))

        return jsonify(statusJson)
