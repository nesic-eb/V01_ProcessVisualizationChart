# -*- coding: utf-8 -*-
'''
// =============================================================================
// 機能名：プロセス可視化チャートサービス／メイン
//
// =============================================================================
// （ファイル整形）Visual Studio Code : Shift + Alt + f
// =============================================================================
'''
from typing import Container
import requests
from configparser import ConfigParser
import flask
from flask import Flask, jsonify, render_template, request, abort, session, redirect, url_for
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
from datetime import timedelta
import pandas as pd
import calendar
from collections import Counter

# -------------------------------------
# 画面関連
# -------------------------------------
import CmnFunction

from ProcessChartCmn00 import ProcessChartCmn00_api
from ProcessChartMain import ProcessChartMain_api  # プロセス可視化チャートサービス
from ProcessDiagram import ProcessDiagram_api
from ProcessDiagramDetail import ProcessDiagramDetail_api
from ProcessEditWindow import ProcessEditWindow_api
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
app = Flask(__name__)
app.secret_key = "ZWl0aGFudGFyLndpbkBuZXNpYy5jb206MTIzNDU2"
app.permanent_session_lifetime = timedelta(minutes=60)
app.config['DEBUG'] = True
app.config['JSON_AS_ASCII'] = False

# ========================================================

app.register_blueprint(ProcessChartCmn00_api)
app.register_blueprint(ProcessChartMain_api)
app.register_blueprint(ProcessDiagram_api)
app.register_blueprint(ProcessDiagramDetail_api)
app.register_blueprint(ProcessEditWindow_api)

# ========================================================

is_closing = False


def try_exit():
    if is_closing:
        # clean up here
        tornado.ioloop.IOLoop.instance().stop()
        logging.info('exit success')


def start_tornado(app, port=app_section.get('HTTP_LISTEN_PORT')):
    try:
        http_server = tornado.httpserver.HTTPServer(
            tornado.wsgi.WSGIContainer(app)
        )

        # http_server = tornado.httpserver.HTTPServer(
        # tornado.wsgi.WSGIContainer(app),
        # ssl_options={
        #	"certfile": app_section.get('CERTIFICATE_FOLDER') + "//nsps-0229-202007.crt",
        #	"keyfile":  app_section.get('CERTIFICATE_FOLDER') + "//nsps-0229-202007.key",
        # }
        # )

        http_server.listen(port)
        logger.info(
            "Tornado server starting on port {port}".format(port=str(port)))
        tornado.ioloop.PeriodicCallback(try_exit, 100).start()
        tornado.ioloop.IOLoop.instance().start()
    except Exception as e:
        raise e


# ========================================================================
# プロセス可視化チャートメイン画面を表示する
#
# ------------------------------------------------------
@app.route("/")
def index():
    return render_template("Login.html")



@app.route("/gotoProcessMain",methods=['POST', 'GET'])
def gotoProcessMain():
    logger.info("gotoProcess Main  .....")
    email = flask.request.form["email"]
    print("email = ",email)
    password = flask.request.form["password"]
    print("password = ",password)
    try:
        user_conn = pyodbc.connect('DRIVER={SQL Server};'
                                   'Server='+app_section.get('IP')+';'
                                   'Database=' +
                                   app_section.get('DATABASE')+';'
                                   'uid='+app_section.get('DB_USER_ID')+';'
                                   'pwd='+app_section.get('DB_PASSWORD')+';')

        user_cursor = user_conn.cursor()
        user_cursor.execute(
            " SELECT "
            "  mail_address, "
            "  password "            
            " FROM Person_Master_TBL "
            " WHERE Mail_address = '" + email + "'"
            "   AND ISNULL(Delete_flag, '0') <> '1' "
            "   AND Principal_business_concurrent_service_code = '0' "
        )

        for x in user_cursor:
            db_password = x[1]
            # OrgCode（組織コード）           

        if (password == db_password):
            return render_template("ProcessChartMain.html")
        else:
            return render_template("Login.html",errorMsg = "メールとパスワードが間違っています。")
    except Exception as inst:
        print(inst)
        logger.info("Error: in the function checkMatchEmailPassword ......")
        return False


    


# ========================================================================
# プロセスチャート画面を表示する
#
# ------------------------------------------------------

@app.route("/gotoProcessDiagram")
def gotoProcessDiagram():
    logger.info("gotoProcessDiagram .....")
    return render_template("ProcessDiagram.html")


# ========================================================================
# プロセスチャートの詳細画面を表示する
#
# ------------------------------------------------------
@app.route("/goToProcessDiagramDetail")
def goToProcessDiagramDetail():
    logger.info("goToProcessDiagramDetail .....")
    return render_template("ProcessDiagramDetail.html")

# ========================================================================
# プロセスチャートの詳細画面を表示する
#
# ------------------------------------------------------


@app.route("/gotoProcessEditWindow")
def gotoProcessEditWindow():
    logger.info("gotoProcessEditWindow .....")
    return render_template("ProcessEditWindow.html")

# ========================================================================
# プロセスチャートの詳細画面を表示する
#
# ------------------------------------------------------


@app.route("/gotoProcessUsageGuide")
def gotoProcessUsageGuide():
    logger.info("gotoProcessUsageGuide .....")
    return render_template("ProcessChartUsageGuide.html")


# ############################################################################################################
# ############################################################################################################
# ############################################################################################################
# ######################################################
# メイン
# ######################################################
if __name__ == "__main__":
    # app.run(debug=True)
    start_tornado(app)
