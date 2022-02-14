# -*- coding: utf-8 -*-
'''
// =============================================================================
// 機能名：共通処理：画面表示において共通的な関数を定義する
//
// =============================================================================
// （ファイル整形）Visual Studio Code : Shift + Alt + f
// =============================================================================
'''
from collections import Counter
import sys
import json
import datetime
import calendar
import pyodbc
from typing import Container, Tuple
from configparser import ConfigParser
from datetime import datetime

# Path: config - log
PATH_CONFIG_APPLICATION = 'application.ini'
SECTION_CONFIG_APPLICATION = 'default'

app_config = ConfigParser()
app_config.read(PATH_CONFIG_APPLICATION)
app_section = app_config[SECTION_CONFIG_APPLICATION]

# ========================================================================
# 組織情報を取得する
# （複数の抽出がある）
#
# ------------------------------------------------------


def getOrgName(code1, code2, code3, code4):
    try:
        print("Start the function getOrgName.....")

        org_conn = pyodbc.connect('DRIVER={SQL Server};'
                                  'Server='+app_section.get('IP')+';'
                                  'Database='+app_section.get('DATABASE')+';'
                                  'uid=' +
                                  app_section.get('DB_USER_ID')+';'
                                  'pwd='+app_section.get('DB_PASSWORD')+';')

        org_cursor = org_conn.cursor()

        org_cursor.execute(
            " SELECT "
            "   ISNULL(Organization_Name_abbr, '') as Organization_Name_abbr "
            " FROM "
            "  Organization_Master_TBL "
            " WHERE Organization_Code_1 = '" + code1 + "' "
            "   AND Organization_Code_2 = '" + code2 + "' "
            "   AND Organization_Code_3 = '" + code3 + "' "
            "   AND Organization_Code_4 = '" + code4 + "' "
            "   AND Delete_flag = '0';")

        for x in org_cursor:
            return x[0]

    except Exception as e:
        print("ERROR : in the function getOrgName.....")
        raise e

# ========================================================================
# 組織情報を取得する
# （複数の抽出がある）
#
# ------------------------------------------------------
# getting Name and Organization Name for Login User Data by parsing email
# created by ETW
# Modified Date 2020-06-08


def getCmnNameAndOrgNameWithOrgCode(email, org1, org2, org3, org4, position_code, loginData):

    try:
        user_conn = pyodbc.connect('DRIVER={SQL Server};'
                                   'Server='+app_section.get('IP')+';'
                                   'Database=' +
                                   app_section.get('DATABASE')+';'
                                   'uid=' +
                                   app_section.get('DB_USER_ID')+';'
                                   'pwd='+app_section.get('DB_PASSWORD')+';')

        ##
        user_cursor = user_conn.cursor()
        sql = \
            " SELECT " \
            "  ISNULL(Surname, '') as surname, " \
            "  ISNULL(Name, '') as name, " \
            "  Organization_Code_1, " \
            "  Organization_Code_2, " \
            "  Organization_Code_3, " \
            "  Organization_Code_4 " \
            " FROM Person_Master_TBL " \
            " WHERE Mail_address = '" + email + "' " \
            " AND Organization_Code_1 = '" + org1 + "' " \
            " AND Organization_Code_2 = '" + org2 + "' " \
            " AND Organization_Code_3 = '" + org3 + "' " \
            " AND Organization_Code_4 = '" + org4 + "' " \
            " AND Position_classification_code = '" + position_code + "' " \
            " AND ISNULL(Delete_flag, '0') <> '1' "

        user_cursor.execute(sql)

        flag = False
        for row in user_cursor:
            flag = True
            loginData.append(row[0]+" "+row[1])
            code1 = row[2]
            code2 = row[3]
            code3 = row[4]
            code4 = row[5]

        if flag == True:
            org_name = getOrgName(code1, code2, code3, code4)
            # org_code_name = code1 + "-" + code2 + "-" + code3 + "-" + code4 + "/" + org_name
            loginData.append(org_name)
            # login_data.append(org_code_name)
            loginData.append(code1)
            loginData.append(code2)
            loginData.append(code3)
            loginData.append(code4)

        else:
            loginData.append("")

    except:
        print("Error: in the function getCmnNameAndOrgNameWithOrgCode..... ")
        return "null"


def getCmnNameAndOrgName(email, loginData):

    try:
        user_conn = pyodbc.connect('DRIVER={SQL Server};'
                                   'Server='+app_section.get('IP')+';'
                                   'Database=' +
                                   app_section.get('DATABASE')+';'
                                   'uid=' +
                                   app_section.get('DB_USER_ID')+';'
                                   'pwd='+app_section.get('DB_PASSWORD')+';')

        ##
        user_cursor = user_conn.cursor()
        user_cursor.execute(
            " SELECT "
            "  ISNULL(Surname, '') as surname, "
            "  ISNULL(Name, '') as name, "
            "  Organization_Code_1, "
            "  Organization_Code_2, "
            "  Organization_Code_3, "
            "  Organization_Code_4 "
            " FROM Person_Master_TBL "
            " WHERE Mail_address = '" + email + "' "
            "  AND Principal_business_concurrent_service_code = '0' "
            "  AND ISNULL(Delete_flag, '0') <> '1' ")

        flag = False
        for row in user_cursor:
            flag = True
            loginData.append(row[0]+" "+row[1])
            code1 = row[2]
            code2 = row[3]
            code3 = row[4]
            code4 = row[5]

        if flag == True:
            org_name = getOrgName(code1, code2, code3, code4)
            # org_code_name = code1 + "-" + code2 + "-" + code3 + "-" + code4 + "/" + org_name
            loginData.append(org_name)
            # login_data.append(org_code_name)
            loginData.append(code1)
            loginData.append(code2)
            loginData.append(code3)
            loginData.append(code4)

        else:
            loginData.append("")

    except:
        print("Error: in the function getCmnNameAndOrgName..... ")
        return "null"


# ========================================================================
# メールアドレスから管理者情報を返す
#
#
# ------------------------------------------------------


def checkRole(email):
    print("checkRole ...")

    try:
        menu_conn = pyodbc.connect('DRIVER={SQL Server};'
                                   'Server='+app_section.get('IP')+';'
                                   'Database='+app_section.get('DATABASE')+';'
                                   'uid='+app_section.get('DB_USER_ID')+';'
                                   'pwd='+app_section.get('DB_PASSWORD')+';')

        menu_cursor = menu_conn.cursor()
        menu_cursor.execute("select Administrator_classification "
                            " from Person_Master_TBL where Mail_address = '" + email + "' AND Delete_flag = '0';")

        for x in menu_cursor:
            if (x[0] == "0"):
                return "user"
            else:
                return "admin"
    except:
        print("checkRole Error ....")
        return "user"

# ========================================================================
# メールアドレスから氏名と組織情報を返す
#
#
# ------------------------------------------------------


def getOrganizationNameAndNamebyEmail(email, wkSessionData):

    try:
        user_conn = pyodbc.connect('DRIVER={SQL Server};'
                                   'Server='+app_section.get('IP')+';'
                                   'Database='+app_section.get('DATABASE')+';'
                                   'uid=' +
                                   app_section.get('DB_USER_ID')+';'
                                   'pwd='+app_section.get('DB_PASSWORD')+';')

        print("getOrganizationNameAndNamebyEmail -- :" + email)
        print(" org1 : " + wkSessionData["SS_OrganizationCode1"])
        print(" org2 : " + wkSessionData["SS_OrganizationCode2"])
        print(" org3 : " + wkSessionData["SS_OrganizationCode3"])
        print(" org4 : " + wkSessionData["SS_OrganizationCode4"])
        print(" PositionClassificationCode : " +
              wkSessionData["SS_PositionClassificationCode"])

        if wkSessionData["SS_OrganizationCode1"] == "":
            # 指定が無い場合は「本務」を取得する
            user_query = "SELECT " \
                " p.password, " \
                " p.Surname, " \
                " p.name, " \
                " org.Organization_Name_abbr, "\
                " p.Organization_Code_1, " \
                " p.Organization_Code_2, " \
                " p.Organization_Code_3, " \
                " p.Organization_Code_4,  " \
                " p.Position_classification_code,  " \
                " p.Administrator_classification,  " \
                " p.Principal_business_concurrent_service_code  " \
                " from Person_Master_TBL as p, " \
                "  Organization_Master_TBL as org " \
                " WHERE p.Mail_address = '" + email + "'" \
                " and p.Organization_Code_1 = org.Organization_Code_1 "\
                " and p.Organization_Code_2 = org.Organization_Code_2 "\
                " and p.Organization_Code_3 = org.Organization_Code_3 "\
                " and p.Organization_Code_4 = org.Organization_Code_4 "\
                " and p.Principal_business_concurrent_service_code = '0' "\
                " and p.Delete_flag = '0' "
        else:
            org1 = wkSessionData["SS_OrganizationCode1"]
            org2 = wkSessionData["SS_OrganizationCode2"]
            org3 = wkSessionData["SS_OrganizationCode3"]
            org4 = wkSessionData["SS_OrganizationCode4"]
            psCode = wkSessionData["SS_PositionClassificationCode"]

            user_query = ""

            if psCode != "":
                # 役職コードを指定して取得する
                user_query = "SELECT " \
                    " p.password, " \
                    " p.Surname, " \
                    " p.name, " \
                    " org.Organization_Name_abbr, "\
                    " p.Organization_Code_1, " \
                    " p.Organization_Code_2, " \
                    " p.Organization_Code_3, " \
                    " p.Organization_Code_4,  " \
                    " p.Position_classification_code,  " \
                    " p.Administrator_classification,  " \
                    " p.Principal_business_concurrent_service_code  " \
                    " from Person_Master_TBL as p, " \
                    "  Organization_Master_TBL as org " \
                    " WHERE p.Mail_address = '" + email + "'" \
                    " and p.Organization_Code_1 = '" + org1 + "' "\
                    " and p.Organization_Code_2 = '" + org2 + "' "\
                    " and p.Organization_Code_3 = '" + org3 + "' "\
                    " and p.Organization_Code_4 = '" + org4 + "' "\
                    " and p.Organization_Code_1 = org.Organization_Code_1 "\
                    " and p.Organization_Code_2 = org.Organization_Code_2 "\
                    " and p.Organization_Code_3 = org.Organization_Code_3 "\
                    " and p.Organization_Code_4 = org.Organization_Code_4 "\
                    " and p.Position_classification_code = '" + psCode + "'"\
                    " and p.Delete_flag = '0' "
            else:
                print(
                    "getOrganizationNameAndNamebyEmail !! ★★★★ Position_classification_code の指定がない！！！！ ★★★★")

                # 役職コードを指定しない
                user_query = "SELECT " \
                    " p.password, " \
                    " p.Surname, " \
                    " p.name, " \
                    " org.Organization_Name_abbr, "\
                    " p.Organization_Code_1, " \
                    " p.Organization_Code_2, " \
                    " p.Organization_Code_3, " \
                    " p.Organization_Code_4,  " \
                    " p.Position_classification_code,  " \
                    " p.Administrator_classification,  " \
                    " p.Principal_business_concurrent_service_code  " \
                    " from Person_Master_TBL as p, " \
                    "  Organization_Master_TBL as org " \
                    " WHERE p.Mail_address = '" + email + "'" \
                    " and p.Organization_Code_1 = '" + org1 + "' "\
                    " and p.Organization_Code_2 = '" + org2 + "' "\
                    " and p.Organization_Code_3 = '" + org3 + "' "\
                    " and p.Organization_Code_4 = '" + org4 + "' "\
                    " and p.Organization_Code_1 = org.Organization_Code_1 "\
                    " and p.Organization_Code_2 = org.Organization_Code_2 "\
                    " and p.Organization_Code_3 = org.Organization_Code_3 "\
                    " and p.Organization_Code_4 = org.Organization_Code_4 "\
                    " and p.Delete_flag = '0' "

        user_cursor = user_conn.cursor()

        user_cursor.execute(user_query)

        for x in user_cursor:
            name = x[1]+" "+x[2]
            org_name = x[3]
            org1 = x[4]
            org2 = x[5]
            org3 = x[6]
            org4 = x[7]
            position_classification_code = x[8]
            roll = x[9]
            Principal_business_concurrent_service_code = x[10]
            value = name + "/"+org_name+"/"+org1+"/"+org2+"/" + \
                org3+"/"+org4+"/"+position_classification_code+"/" + \
                roll+"/"+Principal_business_concurrent_service_code

            print("name = ", name)
            print("org name = ", org_name)
            print("org1 = ", org1)
            print("org2 = ", org2)

            return value

    except:
        print("getOrganizationNameAndNamebyEmail Error ....")
        return ""


# ========================================================================
# 階層を表示するデバック用
#
#
# ------------------------------------------------------


def menudisp(nestidx, menustr):
    return

    try:
        if nestidx == 0:
            print("+" + menustr + "+")
        if nestidx == 1:
            print(" 1 --> " + menustr)
        if nestidx == 2:
            print("    2 -->" + menustr)
        if nestidx == 3:
            print("       3 -->" + menustr)
        if nestidx == 4:
            print("          4 -->" + menustr)
        if nestidx == 5:
            print("             5 -->" + menustr)
        if nestidx == 6:
            print("                6 -->" + menustr)

        return

    except Exception as e:
        print(e)


# ========================================================================
# コントロールマスタから情報を取得する
#
#
# ------------------------------------------------------


def DataGet_ControlMasterTBL(code):
    level_limit = 3

    # SQL
    current_month_conn = pyodbc.connect('DRIVER={SQL Server};'
                                        'Server='+app_section.get('IP')+';'
                                        'Database=' +
                                        app_section.get('DATABASE')+';'
                                        'uid=' +
                                        app_section.get('DB_USER_ID')+';'
                                        'pwd='+app_section.get('DB_PASSWORD')+';')

    current_month_cursor = current_month_conn.cursor()

    level_select_query = \
        " SELECT " \
        "   con.Analysis_Hierachy_Limit " \
        " FROM " \
        "   control_master_tbl AS con " \
        " WHERE " \
        "   con.code = '" + code + "' "

    current_month_cursor.execute(level_select_query)

    for x in current_month_cursor:
        level_limit = int(x[0])

    return level_limit


# ========================================================================
# 休日情報を取得する
#
# （工数詳細チェック承認）
# ------------------------------------------------------
def getHolidayList(year, month, holiday_list):
    try:
        holiday_conn = pyodbc.connect('DRIVER={SQL Server};'
                                      'Server='+app_section.get('IP')+';'
                                      'Database=' +
                                      app_section.get('DATABASE')+';'
                                      'uid='+app_section.get('DB_USER_ID')+';'
                                      'pwd='+app_section.get('DB_PASSWORD')+';')

        holiday_cursor = holiday_conn.cursor()

        holiday_query = \
            "select * " \
            " HolidayCalendar_Master_TBL " \
            " where HolidayMonth = '" + month + "' and Year = '"+str(year)+"';"

        holiday_cursor.execute(holiday_query)
        for x in holiday_cursor:
            holiday_list.append(x[2])

        # print("holiday list = ", holiday_list)

    except:
        print("Error: in get_holiday function... ")
        return "NULL"

# ========================================================================
# 休日情報を取得する
#
# （入力状況レポート）
# ------------------------------------------------------
# getting Holiday Info
# created by MMNE
# created Date 2021-06-30


def getHolidayOfDay(year, month, holiday_data):
    print("year in getHolidayofDay = ", year)
    print("month in getHolidayofDay = ", month)
    try:
        holiday_data = []

        months = ""

        if int(month) < 10:
            months = "0" + str(month)
        else:
            months = str(month)

        holiday_conn = pyodbc.connect('DRIVER={SQL Server};'
                                      'Server=' +
                                      app_section.get('IP')+';'
                                      'Database=' +
                                      app_section.get('DATABASE')+';'
                                      'uid=' +
                                      app_section.get('DB_USER_ID')+';'
                                      'pwd='+app_section.get('DB_PASSWORD')+';')

        holiday_cursor = holiday_conn.cursor()

        holiday_query = \
            "Select " \
            " HolidayDate " \
            " From HolidayCalendar_Master_TBL "\
            " Where Year = '" + str(year) + "' " \
            " and HolidayMonth = '" + months + "'"
        print("holiday_query = ", holiday_query)
        holiday_cursor.execute(holiday_query)
        for row in holiday_cursor:
            if int(row[0]) < 10:
                holiday_row = row[0].split("0")
                holiday_data.append(holiday_row[1])
            else:
                holiday_row = row[0]
                holiday_data.append(holiday_row)

        return holiday_data
    except Exception:
        print("Error: in getHolidayOfDay function... ")
        return "null"


# ========================================================================
# typeに指定した形式で組織情報を取得する
#   type=1  組織に属するユーザーを求める
#               必須データ    org1, org2, org3, org4, position_code,
#   type=2  〇〇を求める
#               必須データ    org1, org2, org3, org4, position_code,
#
# ------------------------------------------------------
def JsonCmn_GetOrganizationGeneral(mytype, email, org1, org2, org3, org4, position_code, concurrent_code, resultList):

    print("JsonCmn_GetOrganizationGeneral ....")

    try:

        resultList.clear()

        # SQL
        select_conn = pyodbc.connect('DRIVER={SQL Server};'
                                     'Server='+app_section.get('IP')+';'
                                     'Database=' +
                                     app_section.get('DATABASE')+';'
                                     'uid='+app_section.get('DB_USER_ID')+';'
                                     'pwd='+app_section.get('DB_PASSWORD')+';')

        select_conn_cursor = select_conn.cursor()

        select_query = \
            " SELECT " \
            "  Organization_Code_1, " \
            "  Organization_Code_2, " \
            "  Organization_Code_3, " \
            "  Organization_Code_4, " \
            "  Organization_Name_abbr " \
            " FROM " \
            "  Organization_Master_TBL " \
            " WHERE "

        if position_code == '10':
            # 担当/派遣社員等
            select_query = select_query + \
                "     Organization_Code_1 = '" + org1 + "' " \
                " AND Organization_Code_2 = '" + org2 + "' " \
                " AND Organization_Code_3 = '" + org3 + "' " \
                " AND Organization_Code_4 = '" + org4 + "'" \
                " AND ISNULL(Delete_flag, '0') <> '1' " \
                " ORDER BY Organization_Code_1, Organization_Code_2, Organization_Code_3, Organization_Code_4 "

        elif position_code == '20':
            # 主任
            select_query = select_query + \
                "     Organization_Code_1 = '" + org1 + "' " \
                " AND Organization_Code_2 = '" + org2 + "' " \
                " AND Organization_Code_3 = '" + org3 + "' " \
                " AND Organization_Code_4 = '" + org4 + "'" \
                " AND ISNULL(Delete_flag, '0') <> '1' " \
                " ORDER BY Organization_Code_1, Organization_Code_2, Organization_Code_3, Organization_Code_4"

        elif position_code == '30':
            # 課長
            select_query = select_query + \
                "     Organization_Code_1 = '" + org1 + "' " \
                " AND Organization_Code_2 = '" + org2 + "' " \
                " AND Organization_Code_3 = '" + org3 + "' " \
                " AND Organization_Code_4 = '" + org4 + "'" \
                " AND ISNULL(Delete_flag, '0') <> '1' " \
                " ORDER BY Organization_Code_1, Organization_Code_2, Organization_Code_3, Organization_Code_4"

        elif position_code == '40':
            # 部長
            select_query = select_query + \
                "     Organization_Code_1 = '" + org1 + "' " \
                " AND Organization_Code_2 = '" + org2 + "' " \
                " AND Organization_Code_3 = '" + org3 + "' " \
                " AND ISNULL(Delete_flag, '0') <> '1' " \
                " ORDER BY Organization_Code_1, Organization_Code_2, Organization_Code_3, Organization_Code_4"

        elif position_code == '50':
            # 事業部長
            select_query = select_query + \
                "     Organization_Code_1 = '" + org1 + "' " \
                " AND Organization_Code_2 = '" + org2 + "' " \
                " AND ISNULL(Delete_flag, '0') <> '1' " \
                " ORDER BY Organization_Code_1, Organization_Code_2, Organization_Code_3, Organization_Code_4"

        else:
            # 本部長
            select_query = select_query + \
                "     Organization_Code_1 = '" + org1 + "' " \
                " AND ISNULL(Delete_flag, '0') <> '1' " \
                " ORDER BY Organization_Code_1, Organization_Code_2, Organization_Code_3, Organization_Code_4"

        print(select_query)

        select_conn_cursor.execute(select_query)

        for x in select_conn_cursor:
            if x[0] is not None:
                resultList.append(
                    x[0] + "-" + x[1] + "-" + x[2] + "-" + x[3] + "/" + x[4])

        select_conn_cursor.close()

    except Exception as e:
        print("JsonCmn_GetOrganizationGeneral error  " + e.args)
        pass

    # end
    finally:
        select_conn.close()


# ========================================================================
# typeに指定した形式で、ユーザー情報を取得する
#   type=1  組織に属するユーザーを求める
#               必須データ    org1, org2, org3, org4, position_code,
#   type=2  〇〇を求める
#               必須データ    org1, org2, org3, org4, position_code,
#
# ------------------------------------------------------
def JsonCmn_GetOrganizationUserGeneral(mytype, email, org1, org2, org3, org4, position_code, concurrent_code, resultList):

    print("JsonCmn_GetOrganizationUserGeneral ....")

    try:

        resultList.clear()

        select_conn = pyodbc.connect('DRIVER={SQL Server};'
                                     'Server='+app_section.get('IP')+';'
                                     'Database=' +
                                     app_section.get('DATABASE')+';'
                                     'uid=' +
                                     app_section.get('DB_USER_ID')+';'
                                     'pwd='+app_section.get('DB_PASSWORD')+';')

        select_conn_cursor = select_conn.cursor()

        if position_code == '10':
            # 担当/派遣社員等
            select_query = "SELECT "\
                "   P.Mail_address AS Mail_address,"\
                "   P.Surname AS Surname, "\
                "   P.Name AS Name, "\
                "   O.Organization_Name_abbr AS Organization_Name_abbr"\
                " FROM Person_Master_TBL AS P, Organization_Master_TBL AS O "\
                " WHERE P.Delete_flag = '0' "\
                " AND P.Mail_address='" + email + "' "\
                " AND P.Organization_Code_1='" + org1 + "' "\
                " AND P.Organization_Code_2='" + org2 + "' "\
                " AND P.Organization_Code_3='" + org3 + "' "\
                " AND P.Organization_Code_4='" + org4 + "' "\
                " AND O.Organization_Code_1=P.Organization_Code_1 "\
                " AND O.Organization_Code_2=P.Organization_Code_2 "\
                " AND O.Organization_Code_3=P.Organization_Code_3 "\
                " AND O.Organization_Code_4=P.Organization_Code_4 "\
                " ORDER BY P.Organization_Code_1, P.Organization_Code_2, P.Organization_Code_3, P.Organization_Code_4"

        elif position_code == '20':
            # 主任
            select_query = "SELECT "\
                "   P.Mail_address AS Mail_address,"\
                "   P.Surname AS Surname, "\
                "   P.Name AS Name, "\
                "   O.Organization_Name_abbr AS Organization_Name_abbr"\
                " FROM Person_Master_TBL AS P, Organization_Master_TBL AS O "\
                " WHERE P.Delete_flag = '0' "\
                " AND P.Mail_address='" + email + "' "\
                " AND P.Organization_Code_1='" + org1 + "' "\
                " AND P.Organization_Code_2='" + org2 + "' "\
                " AND P.Organization_Code_3='" + org3 + "' "\
                " AND P.Organization_Code_4='" + org4 + "' "\
                " AND O.Organization_Code_1=P.Organization_Code_1 "\
                " AND O.Organization_Code_2=P.Organization_Code_2 "\
                " AND O.Organization_Code_3=P.Organization_Code_3 "\
                " AND O.Organization_Code_4=P.Organization_Code_4 "\
                " ORDER BY P.Organization_Code_1, P.Organization_Code_2, P.Organization_Code_3, P.Organization_Code_4"

        elif position_code == '30':
            # 課長
            select_query = "SELECT "\
                "   P.Mail_address AS Mail_address,"\
                "   P.Surname AS Surname, "\
                "   P.Name AS Name, "\
                "   O.Organization_Name_abbr AS Organization_Name_abbr"\
                " FROM Person_Master_TBL AS P, Organization_Master_TBL AS O "\
                " WHERE P.Delete_flag = '0' "\
                " AND P.Organization_Code_1='" + org1 + "' "\
                " AND P.Organization_Code_2='" + org2 + "' "\
                " AND P.Organization_Code_3='" + org3 + "' "\
                " AND P.Organization_Code_4='" + org4 + "' "\
                " AND O.Organization_Code_1=P.Organization_Code_1 "\
                " AND O.Organization_Code_2=P.Organization_Code_2 "\
                " AND O.Organization_Code_3=P.Organization_Code_3 "\
                " AND O.Organization_Code_4=P.Organization_Code_4 "\
                " ORDER BY P.Organization_Code_1, P.Organization_Code_2, P.Organization_Code_3, P.Organization_Code_4"

        elif position_code == '40':
            # 部長
            select_query = "SELECT "\
                "   P.Mail_address AS Mail_address,"\
                "   P.Surname AS Surname, "\
                "   P.Name AS Name, "\
                "   O.Organization_Name_abbr AS Organization_Name_abbr"\
                " FROM Person_Master_TBL AS P, Organization_Master_TBL AS O "\
                " WHERE P.Delete_flag = '0' "\
                " AND P.Organization_Code_1='" + org1 + "' "\
                " AND P.Organization_Code_2='" + org2 + "' "\
                " AND P.Organization_Code_3='" + org3 + "' "\
                " AND O.Organization_Code_1=P.Organization_Code_1 "\
                " AND O.Organization_Code_2=P.Organization_Code_2 "\
                " AND O.Organization_Code_3=P.Organization_Code_3 "\
                " AND O.Organization_Code_4=P.Organization_Code_4 "\
                " ORDER BY P.Organization_Code_1, P.Organization_Code_2, P.Organization_Code_3, P.Organization_Code_4"

        elif position_code == '50':
            # 事業部長
            select_query = "SELECT "\
                "   P.Mail_address AS Mail_address,"\
                "   P.Surname AS Surname, "\
                "   P.Name AS Name, "\
                "   O.Organization_Name_abbr AS Organization_Name_abbr"\
                " FROM Person_Master_TBL AS P, Organization_Master_TBL AS O "\
                " WHERE P.Delete_flag = '0' "\
                " AND P.Organization_Code_1='" + org1 + "' "\
                " AND P.Organization_Code_2='" + org2 + "' "\
                " AND O.Organization_Code_1=P.Organization_Code_1 "\
                " AND O.Organization_Code_2=P.Organization_Code_2 "\
                " AND O.Organization_Code_3=P.Organization_Code_3 "\
                " AND O.Organization_Code_4=P.Organization_Code_4 "\
                " ORDER BY P.Organization_Code_1, P.Organization_Code_2, P.Organization_Code_3, P.Organization_Code_4"

        else:
            # 本部長
            select_query = "SELECT "\
                "   P.Mail_address AS Mail_address,"\
                "   P.Surname AS Surname, "\
                "   P.Name AS Name, "\
                "   O.Organization_Name_abbr AS Organization_Name_abbr"\
                " FROM Person_Master_TBL AS P, Organization_Master_TBL AS O "\
                " WHERE P.Delete_flag = '0' "\
                " AND P.Organization_Code_1='" + org1 + "' "\
                " AND O.Organization_Code_1=P.Organization_Code_1 "\
                " AND O.Organization_Code_2=P.Organization_Code_2 "\
                " AND O.Organization_Code_3=P.Organization_Code_3 "\
                " AND O.Organization_Code_4=P.Organization_Code_4 "\
                " ORDER BY P.Organization_Code_1, P.Organization_Code_2, P.Organization_Code_3, P.Organization_Code_4"

        print(select_query)

        select_conn_cursor.execute(select_query)
        for row in select_conn_cursor:
            resultList.append(org1 + "-" + org2 + "-" + org3 + "-" +
                              org4 + "/" + row[1] + " " + row[2] + "/" + row[0] + "/" + row[3])

    except Exception as e:
        print("JsonCmn_GetOrganizationUserGeneral error  " + e.args)
        pass

    # end
    finally:
        select_conn.close()
