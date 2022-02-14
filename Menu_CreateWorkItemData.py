# -*- coding: utf-8 -*-
'''
// =============================================================================
// 機能名：作業項目メニューを作成する
// 
// =============================================================================
// （ファイル整形）Visual Studio Code : Shift + Alt + f                         
// =============================================================================
'''
from collections import Counter
import sys
import json
import pyodbc
from configparser import ConfigParser
import CmnFunction

# Path: config - log
PATH_CONFIG_APPLICATION = 'application.ini'
SECTION_CONFIG_APPLICATION = 'default'

app_config = ConfigParser()
app_config.read(PATH_CONFIG_APPLICATION)
app_section = app_config[SECTION_CONFIG_APPLICATION]

CST_SEPA = "|"

# ========================================================================
# 作業項目IDを取得する
#
#
# ------------------------------------------------------


def DataGet_WorkItemIDMasterTBL(Classification, org1, org2, WorkItem_by_Counter, WorkItemName_Counter):
    WkData_Counter = Counter()

    # SQL
    current_month_conn = pyodbc.connect('DRIVER={SQL Server};'
                                        'Server='+app_section.get('IP')+';'
                                        'Database=' +
                                        app_section.get('DATABASE')+';'
                                        'uid=' +
                                        app_section.get('DB_USER_ID')+';'
                                        'pwd='+app_section.get('DB_PASSWORD')+';')

    current_month_cursor = current_month_conn.cursor()

    # ---------------------------------------
    # 作業項目IDマスタの取得
    # ---------------------------------------
    WorkItem_select_query = \
        " SELECT " \
        "   wt.work_item_id , " \
        "   wt.work_item_name , " \
        "   ct.classification_code ," \
        "   ct.classification_name " \
        " FROM " \
        "   Classification_Master_TBL AS ct , " \
        "   Workitem_Master_TBL AS wt " \
        " WHERE " \
        "   ct.classification_code = '" + Classification + "' " \
        "   AND ct.Organization_Code_1 = '" + org1 + "' " \
        "   AND ct.Organization_Code_2 = '" + org2 + "' " \
        "   AND ct.classification_code = wt.classification_code " \
        "   AND ct.Organization_Code_1 = wt.Organization_Code_1 " \
        "   AND ct.Organization_Code_2 = wt.Organization_Code_2 " \
        " ORDER by work_item_id "

    current_month_cursor.execute(WorkItem_select_query)

    # 全ての情報を一時保存する
    for x in current_month_cursor:
        # Key=work_item_id, Value=work_item_id,work_item_name,classification_code,classification_name
        WkData_Counter[x[0]] = x[0]+"|"+x[1]+"|"+x[2]+"|"+x[3]
        # Key=work_item_id, Value=work_item_name
        WorkItemName_Counter[x[0]] = x[1]

    # print(WkData_Counter)

# ========================================================================
# 展開マスタの取得
#
#
# ------------------------------------------------------


def DataGet_DeploymentMasterTBL(org1, org2, workItemName_Counter, parent_Counter, deployment_Counter):

    item_by_All_Counter = Counter()
    item_by_parent_list = list()
    idx = 0

    # SQL
    current_month_conn = pyodbc.connect('DRIVER={SQL Server};'
                                        'Server='+app_section.get('IP')+';'
                                        'Database=' +
                                        app_section.get('DATABASE')+';'
                                        'uid=' +
                                        app_section.get('DB_USER_ID')+';'
                                        'pwd='+app_section.get('DB_PASSWORD')+';')

    current_month_cursor = current_month_conn.cursor()

    idlist = []
    for item in workItemName_Counter:
        idlist.append("'" + str(item) + "'")

    idlistStr = ','.join(idlist)

    if idlistStr == "":
        return ""

    # ---------------------------------------
    # 展開マスタの取得
    # ---------------------------------------
    deployment_select_query = " SELECT " \
        "   work_item_id , " \
        "   Parent_WorkItem_ID " \
        " FROM " \
        "   deployment_master_tbl " \
        " WHERE work_item_id IN (" + idlistStr + ") " \
        "   AND Organization_Code_1 = '" + org1 + "' " \
        "   AND Organization_Code_2 = '" + org2 + "' " \
        " Order by work_item_id "

    current_month_cursor.execute(deployment_select_query)

    # 全ての情報を一時保存する。
    for x in current_month_cursor:
        if x[1] is not None or x[1] == "":
            item_by_All_Counter[x[0]] = x[0]+"|"+x[1]
        else:
            item_by_All_Counter[x[0]] = x[0]+"|"+"0"
            item_by_parent_list.append(x[0])

    # 親をSort
    item_by_parent_list.sort()
    # print(item_by_parent_list)

    # 親を先に登録する
    idx = 0
    for item in item_by_parent_list:
        idx = idx + 1
        parent_Counter[idx] = item_by_All_Counter[item]
        item_by_All_Counter[item] = ""

    # print(parent_Counter)

    # 残りを追加する
    idx = 0
    for item in item_by_All_Counter:
        if item_by_All_Counter[item] != "":
            if item_by_parent_list.count(item) == 0:
                idx = idx + 1
                deployment_Counter[idx] = item_by_All_Counter[item]

    # print(deployment_Counter)

# ========================================================================
# 作業項目IDが親かどうかをチェックする
# 　（辿る関数）
#
#
# ------------------------------------------------------


def checkParent(parentCounter, workitemid, startidx):
    result = False

    loop = startidx
    while loop < len(parentCounter):
        loop = loop + 1

        topParent = parentCounter[loop]
        if topParent == "" or topParent == 0:
            # 処理済みの作業項目はスキップする
            continue

        topParentArray = [x.strip() for x in topParent.split(CST_SEPA)]
        if topParentArray[0] == workitemid:
            # 存在した
            result = True

    return result

# ========================================================================
# 作業項目メニューの作成
# 　（辿る関数）
#
#
# ------------------------------------------------------


def FollowParent(parent, parentAll, workIDDic, subsJsonList, workitemNameTable, ParentCounter, level_limit, nestidx):

    lp = 0

    while lp <= len(workIDDic):
        lp = lp + 1

        parentstr = workIDDic[lp]
        if parentstr == "" or parentstr == 0:
            continue

        wkParent = [x.strip() for x in parentstr.split(CST_SEPA)]
        # print(wkParent)

        if len(wkParent) > 1:
            if wkParent[1] == "":
                # 親は捨てる
                continue

            # 親が親情報に存在したら、終了（別の親へ）
            elif ParentCounter[wkParent[1]] > 0:
                break

            elif (wkParent[1] == parent):

                idname = workitemNameTable[wkParent[0]]
                if idname == 0:
                    break

                CmnFunction.menudisp(nestidx + 1, idname)

                # 作成してきた辞書を追加する
                magoJsonList = []
                wkParentAll = parentAll + CST_SEPA + wkParent[0]
                FollowParent(wkParent[0], wkParentAll, workIDDic, magoJsonList,
                             workitemNameTable, ParentCounter, level_limit, nestidx + 1)

                # 階層数を超えたら終了する
                if level_limit > nestidx:
                    # 次を辿る（自分を親に持つデータ）
                    if len(magoJsonList) > 0:
                        # 孫がいないので
                        wkDic = {"id": wkParent[0], "title": wkParent[0] + " / " +
                                 idname + " . " + str(nestidx+1), "subs": magoJsonList}
                    else:
                        # 孫がいないので
                        wkDic = {
                            "id": wkParent[0], "title": wkParent[0] + " / " + idname + " . " + str(nestidx+1)}

                    subsJsonList.append(wkDic)

                # 削除（使用済み）
                workIDDic[lp] = ""

# ========================================================================
# 作業項目メニューの作成
#    （呼び出し関数）
#
#
# ------------------------------------------------------


def CreateWorkItemList(code, classification, org1, org2, topWorkItemList):
    # print("hello create work ite list ");
    # print(code)
    # print(classification)
    # print(topWorkItemList)
    Parent_by_Counter = Counter()
    Deployment_by_Counter = Counter()
    WorkItem_by_Counter = Counter()
    WorkItemName_Counter = Counter()

    # コントールマスタから展開数を取得する
    level_limit = 5
    level_limit = CmnFunction.DataGet_ControlMasterTBL(code)

    # 作業項目IDの取得
    DataGet_WorkItemIDMasterTBL(
        classification, org1, org2, WorkItem_by_Counter, WorkItemName_Counter)

    # 展開マスタの取得
    DataGet_DeploymentMasterTBL(
        org1, org2, WorkItemName_Counter, Parent_by_Counter, Deployment_by_Counter)

    # JSON を作る
    nestidx = 1

    loop = 0
    # 親のループ
    while loop < len(Parent_by_Counter):
        loop = loop + 1

        topParent = Parent_by_Counter[loop]
        if topParent == "" or topParent == 0:
            # 処理済みの作業項目はスキップする
            continue

        topParentArray = [x.strip() for x in topParent.split(CST_SEPA)]

        # 親を見つけた
        if topParentArray[1] == "0" or topParentArray[1] == "0":
            topWorkItemDic = {}

            # -----------------------------
            # 親情報を作成する
            # -----------------------------
            idname = WorkItemName_Counter[topParentArray[0]]
            if idname == 0:
                break

            # debug
            nestidx = 1
            CmnFunction.menudisp(nestidx, topParentArray[0] + " / " + idname)

            # 削除（使用済み）
            Parent_by_Counter[loop] = ""

            # -----------------------------
            # 子を辿る
            # -----------------------------
            lp = 0

            subsJsonList = []  # n層目

            while lp < len(Deployment_by_Counter):
                lp = lp + 1

                parentstr = Deployment_by_Counter[lp]
                if parentstr == "" or parentstr == 0:
                    # 処理済みの作業項目はスキップする
                    continue

                # 親情報に存在したら、終了（別の親へ）
                wkParent = [x.strip() for x in parentstr.split(CST_SEPA)]
                if checkParent(Parent_by_Counter, wkParent[1], loop) == True:
                    break

                if len(wkParent) > 1:
                    idname = WorkItemName_Counter[wkParent[0]]
                    CmnFunction.menudisp(nestidx + 1, idname)

                    # 次を辿る（自分を親に持つデータ）
                    magoJsonList = []
                    parentAll = "" + CST_SEPA + wkParent[0]
                    FollowParent(wkParent[0], parentAll, Deployment_by_Counter, magoJsonList,
                                 WorkItemName_Counter, Parent_by_Counter, level_limit, nestidx + 1)

                    # 階層数を超えたら終了する
                    if level_limit > nestidx:
                        if len(magoJsonList) > 0:
                            wkDic = {"id": wkParent[0], "title": wkParent[0] + " / " +
                                     idname + " . " + str(nestidx+1), "subs": magoJsonList}
                            subsJsonList.append(wkDic)
                        else:
                            wkDic = {
                                "id": wkParent[0], "title": wkParent[0] + " / " + idname + " . " + str(nestidx+1)}
                            subsJsonList.append(wkDic)

                    # 削除（使用済み）
                    Deployment_by_Counter[lp] = ""

            # JSON
            idname = WorkItemName_Counter[topParentArray[0]]
            topWorkItemDic = {
                "id": topParentArray[0], "title": topParentArray[0] + " / " + idname + " . 1",  "subs": subsJsonList}
            topWorkItemList.append(topWorkItemDic)

    # print(topWorkItemList)
    # debug
    #print(json.dumps(topWorkItemList, ensure_ascii=False, indent=4))
