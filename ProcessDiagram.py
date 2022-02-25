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
# 画像情報の取得
#
#
# ------------------------------------------------------


# ========================================================================
# プロセス可視化チャート図情報を取得する
#
#
# ------------------------------------------------------

@ProcessDiagram_api.route("/getchartDesignCode/", methods=['POST', 'GET'])
def getchartDesignCode():

    try:
        process_procedureID = flask.request.form['process_procedureID']
        process_ProcedureName = flask.request.form['process_ProcedureName']

        print(process_ProcedureName)
        print(process_procedureID)

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
            "   ProcessProcedureName = '" + process_ProcedureName + "'"\
            "   AND ProcessProcedureID = '" + process_procedureID + "'"

        select_conn_cursor.execute(select_query)
        ChartDesignCodeList = []
        topJson = []

        # チャート情報
        for x in select_conn_cursor:
            ChartDesignCodeList.append(x[13])
            ChartDesignCodeList.append(x[11])
            ChartDesignCodeList.append(x[12])

        select_conn_cursor.close()

        topJson.append(ChartDesignCodeList)

    except Exception as e:
        print("getchartDesignCode select error  " + e.args)
        pass

    # end
    finally:
        select_conn.close()

        print(json.dumps(topJson, indent=2, ensure_ascii=False))

        return jsonify(topJson)
