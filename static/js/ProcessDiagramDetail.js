// =============================================================================
// 画面名：プロセス可視化チャート：詳細画面
// 
// -----------------------------------------------------------------------------
// （ファイル整形）Visual Studio Code : Shift + Alt + f 
// =============================================================================


// ##################################################################################################
// ##################################################################################################
/* セッション情報取得 */
console.log("■ ---------------------------------------------");
console.log("■ セッション情報 -- ProcessDiagramDetail.js --------");

var email = sessionStorage.getItem("email");
var org1 = sessionStorage.getItem("org1");
var org2 = sessionStorage.getItem("org2");
var ProcessProcedureID = sessionStorage.getItem("ProcessProcedureID");
var ProcessProcedureName = sessionStorage.getItem("ProcessProcedureName");
var ChartDesignCode = sessionStorage.getItem("ChartDesignCode");
var AutoSaveControlflag = sessionStorage.getItem("AutoSaveControl");

// 変更禁止フラグ（１：禁止）
var CHANGEPROHIBITIONFLAG = sessionStorage.getItem("ChangeProhibitionflag");

// 時間合計
var G_WORKTIME_TOTAL = 0

console.log("Email = " + email);
console.log("Org1 = " + org1);
console.log("Org2 = " + org2);
console.log("Process Procedure ID = " + ProcessProcedureID);
console.log("Process Procedure Name = " + ProcessProcedureName);
console.log("Chart Design Code = " + ChartDesignCode);
console.log("AutoSaveControlflag = " + AutoSaveControlflag);
console.log("CHANGEPROHIBITIONFLAG = " + CHANGEPROHIBITIONFLAG);

console.log("■ ---------------------------------------------");

var G_COMMENT_MAX = 0
var G_WORKTIME_TOTAL = 0

// ##################################################################################################
// ##################################################################################################
/* functin以外の処理を記述 */

// A $( document ).ready() block.
$(document).ready(function () {

    console.log("---- ready! -----------------------------------------------");

    var processProcedureID = sessionStorage.getItem("ProcessProcedureID");
    var chartDesignCode = sessionStorage.getItem("ChartDesignCode");

    var ChartBusinessLabelData;

    // チャートヘッダラベル情報を取得する
    $.ajax({
        url: '/getProcessChartBusinessLabelData/',
        type: 'POST',
        data: {
            processProcedureID: processProcedureID
        },
        dataType: 'json',
        async: false,
        success: function (response) {
            //alert(response);
            ChartBusinessLabelData = response[0].BusinessLabel;
        }
    });

    $.ajax({
        url: '/getProcessChartDrawingData/',
        type: 'POST',
        data: {
            processProcedureID: processProcedureID,
            chartDesignCode: chartDesignCode
        },
        dataType: 'json',
        async: false,
        success: function (response) {
            // 図面データ取得
            console.log("REACh")

            var result = JSON.stringify(response)
            var data = response[0].Data
            //console.log("data = " + JSON.stringify(data))

            var Num = response[0].Num
            console.log("Num = " + JSON.stringify(Num))

            var design = response[0].design
            //console.log("design = " + JSON.stringify(design))

            var RowsNumber = data[0].RowsNumber
            console.log("rows = " + RowsNumber)

            var ColumnNumber = data[0].ColumnNumber
            console.log("column = " + ColumnNumber);

            // ---------------------------
            // 画面上部の値
            // ---------------------------
            // 画面上部へデータを設定する
            {
                // チャート
                var label = document.getElementById("chart_titile");
                label.textContent = data[0].ProcessProcedureName;

                // 合計時間
                document.getElementById("TotalWorkingTime").value = data[0].TotalWorkingTime;

                // 作業頻度
                var opname = "WorkFrequency_" + String(('00' + Number(data[0].WorkFrequency)).slice(-2));
                $("#SelectWorkFrequency option[value='" + opname + "']").prop('selected', true);

                // 作業人数
                var opname = "NumberOfWorkers_" + String(('00' + Number(data[0].NumberOfWorkers)).slice(-2));
                $("#SelectWorkNumberOfWorkers option[value='" + opname + "']").prop('selected', true);

                // 外部閲覧を禁止する
                if (data[0].PermissionFlag == "0") {
                    document.getElementById("PermissionFlag").checked = false;
                }
                else {
                    document.getElementById("PermissionFlag").checked = true;
                }

                // 外部閲覧を禁止する
                if (data[0].ChangeProhibitionFlag == "0") {
                    document.getElementById("ChangeProhibitionFlag").checked = false;
                }
                else {
                    document.getElementById("ChangeProhibitionFlag").checked = true;
                }
            }

            // ---------------------------
            // 画面：左側 
            // ---------------------------
            // 図面データに合わせて枠を表示する
            createLeftTable(RowsNumber, ColumnNumber, design, ChartBusinessLabelData);

            // ---------------------------
            // 画面：右側
            // ---------------------------
            // 図面データに合わせてコメントを表示する
            rightTableCreate(design)

        }
    });
});

// 変更禁止なので、更新系のボタンを削除する
if (CHANGEPROHIBITIONFLAG == "1") {
    $("#updateChartData").remove();
    document.getElementById("SelectWorkFrequency").disabled = true;
    document.getElementById("SelectWorkNumberOfWorkers").disabled = true;
    document.getElementById("ChangeProhibitionFlag").disabled = true;
}

// ##################################################################################################
// ##################################################################################################
/* function の処理を記述 */

// ----------------------------------------------
// 画面：プロセス欄／業務欄のテキストを求める
// （開始位置が一致する）
// ----------------------------------------------
function checkProcessLabelData(idx, checkType, businessLabelData) {
    var checkText = "";

    if (checkType = "column") {
        for (var a = 0; a < businessLabelData.length; a++) {
            if ("Process" == businessLabelData[a].LabelType) {
                var StartIdx = businessLabelData[a].StartIdx;

                if (idx == Number(StartIdx)) {
                    // あった
                    checkText = businessLabelData[a].LabelText;
                    break;
                }
            }
        }
    }

    if (checkType == "rows") {
        for (var a = 0; a < businessLabelData.length; a++) {
            if ("Department" == businessLabelData[a].LabelType) {
                var StartIdx = businessLabelData[a].StartIdx;

                if (idx == Number(StartIdx)) {
                    // あった
                    checkText = businessLabelData[a].LabelText;
                    break;
                }
            }
        }
    }

    return checkText;
}

// ----------------------------------------------
// 画面：プロセス欄／業務欄の終了位置を見つける
// （開始位置が一致する）
// ----------------------------------------------
function getProcessLabelData_EndColum(idx, checkType, businessLabelData) {
    var LabelData = null;

    // 横
    if (checkType == "column") {
        for (var a = 0; a < businessLabelData.length; a++) {
            if ("Process" == businessLabelData[a].LabelType) {
                var StartIdx = businessLabelData[a].StartIdx;

                if (idx == Number(StartIdx)) {
                    // あった
                    LabelData = businessLabelData[a];
                    break;
                }
            }
        }
    }

    // 縦
    if (checkType == "rows") {
        for (var a = 0; a < businessLabelData.length; a++) {
            if ("Department" == businessLabelData[a].LabelType) {
                var StartIdx = businessLabelData[a].StartIdx;

                if (idx == Number(StartIdx)) {
                    // あった
                    LabelData = businessLabelData[a];
                    break;
                }
            }
        }
    }

    return LabelData;
}

/**
 * 数値チェック関数
 * 入力値が数値 (符号あり小数 (- のみ許容)) であることをチェックする
 * [引数]   numVal: 入力値
 * [返却値] true:  数値
 *          false: 数値以外
 */
function isNumber(numVal) {
    // チェック条件パターン
    var pattern = /^[-]?([1-9]\d*|0)(\.\d+)?$/;
    // 数値チェック
    return pattern.test(numVal);
}

// ----------------------------------------------
// コメントをすべて閉じる
// ----------------------------------------------
function AllCloseComment() {
    for (i = 0; i < G_COMMENT_MAX; i++) {
        var openStatusName = "OpenStatus_" + String(i);

        // 閉じる
        var tablename = "#table_" + String(i)
        $(tablename).hide();
        document.getElementById(openStatusName).value = "0";
    };
};

// ----------------------------------------------
// コメントをすべて開く
// ----------------------------------------------
function AllOpenComment() {
    for (i = 0; i < G_COMMENT_MAX; i++) {
        var openStatusName = "OpenStatus_" + String(i);

        // 開く
        var tablename = "#table_" + String(i);
        $(tablename).show();
        document.getElementById(openStatusName).value = "1";
    };
};

// ----------------------------------------------
// 選択したコメントを開く
// ----------------------------------------------
function TargetOpenComment(targetComment) {
    for (i = 0; i < G_COMMENT_MAX; i++) {
        var terget = "Comment_" + String(i);
        const getLocationInfo = document.getElementById(terget).value;
        if (getLocationInfo == targetComment) {
            var openStatusName = "OpenStatus_" + String(i);
            // 開く
            var tablename = "#table_" + String(i);
            $(tablename).show();
            document.getElementById(openStatusName).value = "1";
        };
    };
};

// ----------------------------------------------
// 画面：図形の最大幅を取得する
// ----------------------------------------------
function imgTableWidth(design) {

    // A～Z 
    var widthMax = 0;

    for (var i = 1; i < 27; i++) {
        var checkColumn = String.fromCharCode(64 + i);
        var checkflg = false;
        for (var a = 0; a < design.length; a++) {
            var Block = design[a].Block;
            var wkColumn = Block.LocationInfo.split('_')

            if (checkColumn == wkColumn[0]) {
                // あった
                widthMax = widthMax + 140;
                checkflg = true;
                break;
            }
        }

        // なかった
        if (checkflg == false) {
            widthMax = widthMax + 20;
        }
    }

    return widthMax;
};

// ----------------------------------------------
// 画面：指定カラムの画像あり／無しを求める
// ----------------------------------------------
function checkImgTd(column, design) {
    var checkflg = false;

    var checkColumn = String.fromCharCode(64 + column);
    for (var a = 0; a < design.length; a++) {
        var Block = design[a].Block;
        var wkColumn = Block.LocationInfo.split('_')

        if (checkColumn == wkColumn[0]) {
            // あった
            checkflg = true;
            break;
        }
    }

    return checkflg;
};

// ----------------------------------------------
// 画面：左側を作図する
// ----------------------------------------------
function createLeftTable(rows, column, design, chartBusinessLabelData) {

    // 枠（幅）の最大値を求める
    var widthMax = imgTableWidth(design);

    // 画面左側ブロックの親
    var left_table = document.getElementById("left_table_Div");
    left_table.setAttribute("style", "width: " + String(widthMax) + "px;")
    //left_table.setAttribute("style", "width: 1000px;")

    var mainTable = document.createElement("table");
    mainTable.setAttribute("style", "border: 1px; background-color: #cdefff; ");

    // 行
    var rowsNumMax = 1;
    for (var j = 0; j <= rows; j++) {
        var tr = document.createElement("tr");
        tr.classList.add("l-border");

        // カラムループ
        for (var i = 0; i <= column; i++) {
            var chr = "";
            if (j == 0) {
                var th = document.createElement("th");
                th.classList.add("l-border");
                th.setAttribute("style", "text-align:center; width: 20px; height: 28px;");
                th.style.backgroundColor = "#98fb98";
                if (i == 0) {
                    th.setAttribute("rowspan", "2");
                    th.setAttribute("colspan", "2");
                    var node = document.createTextNode("No.");
                    th.appendChild(node)
                } else {
                    chr = String.fromCharCode(64 + i);
                    var node = document.createTextNode(chr);
                    th.appendChild(node)
                }
                tr.appendChild(th);

            } else {
                // 
                chr = String.fromCharCode(64 + i);
                var td = document.createElement("td");
                td.classList.add("l-border");
                if (i == 0) {
                    td.setAttribute("style", "text-align:center; vertical-align:middle; width: 20px; height: 28px;");
                    td.style.backgroundColor = "#f08080";
                }
                else {
                    // 枠
                    var checkflg = checkImgTd(i, design);
                    if (checkflg == true) {
                        td.setAttribute("style", "text-align:center; vertical-align:middle; width: 140px; height: 28px;");
                    }
                    else {
                        td.setAttribute("style", "text-align:center; vertical-align:middle; width: 20px; height: 28px;");
                    }
                    td.style.backgroundColor = "#ffffff";
                }
                td.setAttribute("id", chr + "_" + j)
                if (i == 0) {
                    // 行番号
                    var node = document.createTextNode(j);
                    td.appendChild(node);
                    tr.appendChild(td);

                    // ラベル欄（行）
                    var LabelData = getProcessLabelData_EndColum(j, "rows", chartBusinessLabelData);
                    var rowspanNum = 1;
                    var departmentLabel = "";
                    var labelColor = "#FFFFCC";
                    if (LabelData != null) {
                        rowspanNum = Number(LabelData.EndIdx) - Number(LabelData.StartIdx) + 1;
                        departmentLabel = LabelData.LabelText;
                        labelColor = LabelData.LabelColor;
                    }

                    if (rowsNumMax <= rows) {
                        if (rowsNumMax <= j) {
                            var td = document.createElement('td');
                            td.classList.add("t-border");
                            td.setAttribute("rowspan", String(rowspanNum));
                            td.setAttribute("style", "text-align: center; width: 20px; background-color: " + labelColor + ";");
                            {
                                var div = document.createElement('div');
                                {
                                    var span = document.createElement('span');
                                    span.setAttribute("style", "margin-top: 0px; writing-mode: vertical-rl; text-orientation: upright; margin-left: 0px;");
                                    if (departmentLabel != "") {
                                        span.innerHTML = "【" + departmentLabel + "】";
                                    }
                                    div.appendChild(span)
                                }
                                td.appendChild(div);
                            }

                            tr.appendChild(td);
                            rowsNumMax = rowsNumMax + rowspanNum;
                        }
                    }
                }
                else {
                    // データ行
                    tr.appendChild(td);
                }
            }
        }

        // テーブルに行を追加
        mainTable.appendChild(tr)

        // ラベル欄（プロセス欄）
        if (j == 0) {

            var trp = document.createElement('tr');
            trp.classList.add("l-border");
            trp.setAttribute("style", "background-color: #FFFFCC");

            var columNumMax = 1;
            for (var i = 1; i <= column; i++) {
                var LabelData = getProcessLabelData_EndColum(i, "column", chartBusinessLabelData);
                var colspanNum = 1;
                var labelColor = "#FFFFCC";
                if (LabelData != null) {
                    colspanNum = Number(LabelData.EndIdx) - Number(LabelData.StartIdx) + 1;
                    labelColor = LabelData.LabelColor;
                }

                if (columNumMax <= column) {
                    if (columNumMax <= i) {

                        var td = document.createElement('td');
                        td.classList.add("l-border");
                        td.setAttribute("style", "text-align: center; height: 28px; background-color: " + labelColor + ";");
                        td.setAttribute("colspan", String(colspanNum));
                        {
                            var processLabel = "";
                            processLabel = checkProcessLabelData(i, "column", chartBusinessLabelData);

                            var div = document.createElement('div');
                            {
                                var span = document.createElement('span');
                                if (processLabel != "") {
                                    span.innerHTML = "【" + processLabel + "】";
                                }
                            }
                            div.appendChild(span)
                            td.appendChild(div);
                        }
                        trp.appendChild(td);
                        columNumMax = columNumMax + colspanNum;
                    }
                }

            } // end for

            mainTable.appendChild(trp)
        }

    }

    // 親DIVにtableを追加
    left_table.append(mainTable)

    G_COMMENT_MAX = design.length;

    console.log("design in G_COMMENT_MAX = " + G_COMMENT_MAX);
    for (var a = 0; a < design.length; a++) {
        var Block = design[a].Block;
        var LocationInfo = Block.LocationInfo;
        var location_id = document.getElementById(LocationInfo);

        var ImageName = Block.ImageName;
        var ImageFileName = Block.ImageFileName;
        var CommentCode = Block.CommentCode;
        var Heading = Block.Heading;
        var Explanation = Block.Explanation;
        var Efficiency = Block.Efficiency;
        var OperationTarget = Block.OperationTarget;
        var WorkingHour = Block.WorkingHour;
        var ExceptionWork = Block.ExceptionWork;
        var SupplementComment = Block.SupplementComment;

        var br = document.createElement("br");

        // 選択画像
        var image = document.createElement("img");
        image.setAttribute("src", "static/img/" + ImageFileName);
        image.setAttribute("title", "images");
        image.setAttribute("style", "width: 85%; margin-top: 2px;");
        location_id.appendChild(image);
        location_id.appendChild(br);

        // 説明
        var text_box = document.createElement("input");
        text_box.setAttribute("type", "text");
        text_box.setAttribute("style", "background-color: wheat; width: 180px; height: 30px; margin-top: 5px; text-align:center; color: brown;");
        text_box.setAttribute("readonly", "true");
        text_box.setAttribute("value", Heading);
        location_id.appendChild(text_box);

        // 編集アイコン
        var a_link = document.createElement("a")
        a_link.setAttribute("href", "JavaScript:showModal('EdithWindow', '" + LocationInfo + "','" + CommentCode + "')");
        a_link.setAttribute("title", "editLink");
        a_link.setAttribute("id", LocationInfo);
        a_link.setAttribute("name", LocationInfo);

        var img_edit = document.createElement("img");
        img_edit.setAttribute("src", "static/img/flowChartImg/editData.svg");
        img_edit.setAttribute("title", "edit");
        img_edit.setAttribute("style", "width: 20px; margin-top: -30px; margin-left: -20px;");
        img_edit.setAttribute("name", LocationInfo)
        a_link.appendChild(img_edit);

        location_id.appendChild(a_link);
    }
};

// ----------------------------------------------
// 画面：右側を作図する
// ----------------------------------------------
function rightTableCreate(design) {
    //var tr = document.getElementById("tr");
    var br = document.createElement("br");

    // 左表示エリアの親
    var container_top = document.getElementById("container_top");

    var hr = document.createElement("hr");
    hr.style.border = "2";

    // 要素数のループ
    for (var i = 0; i < design.length; i++) {
        var containerName = "container_" + String(i);
        var container_id = document.createElement("div");
        container_id.setAttribute("id", containerName);
        container_id.setAttribute("class", "container");
        container_id.setAttribute("style", "border: 1px solid #e3e3e3; width: 700px;");

        var hr = document.createElement("hr");
        hr.style.border = "2";

        // JSON - BLock Area
        var Block = design[i].Block;
        // 位置
        var LocationInfo = Block.LocationInfo;
        var Heading = Block.Heading;
        var CommentInfo = Block.Explanation;
        var EfficiencyInfo = "効率可能"
        if (Block.Efficiency == "0") {
            EfficiencyInfo = "効率不可"
        }
        var OperationTarget = Block.OperationTarget;
        var WorkingHourInfo = Block.WorkingHour;
        var ExceptionWorkInfo = Block.ExceptionWork;
        var SupplementCommentIngo = Block.SupplementComment;

        // 枠
        var tbl = document.createElement("table");
        var tablename = "table_" + String(i)
        tbl.setAttribute("id", tablename);
        tbl.setAttribute("style", "border: 1px #e3e3e3; width: 100%;");

        // 空行
        {
            // 展開の状態
            var trWk = document.createElement("tr");
            //trWk.classList.add("l-border");

            {
                var td1 = document.createElement("td");
                td1.setAttribute("style", "width: 10px;");
                //td1.classList.add("l-border");
            }
            trWk.appendChild(td1);

            {
                var td2 = document.createElement("td");
                td2.setAttribute("style", "width: 130px;");
                //td2.classList.add("l-border");

                var text_box = document.createElement("input")
                text_box.setAttribute("type", "hidden");
                text_box.setAttribute("value", "1");
                text_box.setAttribute("id", "OpenStatus_" + String(i));
                text_box.setAttribute("name", "OpenStatus_" + String(i));
                td2.appendChild(text_box);
            }
            trWk.appendChild(td2);

            {
                var td1_5 = document.createElement("td");
                td1_5.setAttribute("style", "width: 10px;");
                //td1_5.classList.add("l-border");

                var p1 = document.createElement("p");
                var node = document.createTextNode("");
                p1.appendChild(node);
                td1_5.appendChild(p1);
            }
            trWk.appendChild(td1_5);

            {
                var td3 = document.createElement("td");
                td3.setAttribute("style", "width: 300px;");
                //td3.classList.add("l-border");

                var p1 = document.createElement("p");
                var node = document.createTextNode("");
                p1.appendChild(node);
                td3.appendChild(p1);
            }
            trWk.appendChild(td3);

            // 予備
            {
                var td4 = document.createElement("td");
                td4.setAttribute("style", "width: 10px;");
                //td4.classList.add("l-border");

                var p3 = document.createElement("p")
                var node3 = document.createTextNode("");
                p3.appendChild(node3);
                td4.appendChild(p3);
            }

            trWk.appendChild(td4);

            tbl.appendChild(trWk)
        }

        // １行目
        var tr1 = document.createElement("tr");
        {
            var td1 = document.createElement("td");
            //td1.classList.add("l-border");

            // 位置
            {
                var p1 = document.createElement("p");
                var node = document.createTextNode("位置")
                p1.appendChild(node);;
                td1.appendChild(p1);

                var text_box = document.createElement("input");
                text_box.setAttribute("type", "text");
                text_box.setAttribute("style", "background-color: yellow; width: 180px; height: 30px; margin-top: 5px; text-align:left;");
                text_box.setAttribute("readonly", "true");
                text_box.setAttribute("id", "Comment_" + String(i));
                text_box.setAttribute("value", LocationInfo);
                td1.appendChild(text_box);
            }

            // 見出し
            {
                var td2 = document.createElement("td");
                //td2.classList.add("l-border");
                td2.setAttribute("colspan", "2");
                td2.setAttribute("style", "width: 400px;");

                var p2 = document.createElement("p");
                var node2 = document.createTextNode("見出し")
                p2.appendChild(node2);;
                td2.appendChild(p2);

                var text_box = document.createElement("input");
                text_box.setAttribute("type", "text");
                text_box.setAttribute("style", "width: 400px; height:35px;");
                text_box.setAttribute("class", "form-control");
                text_box.setAttribute("readonly", "true");
                text_box.setAttribute("value", Heading);
                td2.appendChild(text_box);
            }

            // 予備
            var td3 = document.createElement("td");
            //td3.classList.add("l-border");

            td3.setAttribute("style", "width: 10px;");
            var p3 = document.createElement("p")
            var node3 = document.createTextNode("");
            p3.appendChild(node3);
            td3.appendChild(p3);

            var td4 = document.createElement("td");
            //td4.classList.add("l-border");

            td4.setAttribute("style", "width: 10px;");
            var p4 = document.createElement("p")
            var node4 = document.createTextNode("");
            p3.appendChild(node4);
            td4.appendChild(p4);
        }

        tr1.appendChild(td1);
        tr1.appendChild(td2);
        tr1.appendChild(td3);
        tr1.appendChild(td4);

        tbl.appendChild(tr1)

        // ２行目（説明）
        var tr2 = document.createElement("tr");
        {
            var td1 = document.createElement("td");
            //td1.classList.add("l-border");
            td1.setAttribute("colspan", "3");
            td1.setAttribute("style", "width: 720px;");
            var p = document.createElement("p")
            var node4 = document.createTextNode("説明")
            p.appendChild(node4);
            td1.appendChild(p)

            var textarea = document.createElement("textarea");
            textarea.setAttribute("style", "width: 590px; height: 100px;");
            textarea.setAttribute("readonly", "true");
            textarea.value = CommentInfo
            td1.appendChild(textarea)

            tr2.appendChild(td1);

            // 予備
            var td3 = document.createElement("td");
            //td3.classList.add("l-border");

            td3.setAttribute("style", "width: 10px;");
            var p3 = document.createElement("p")
            var node3 = document.createTextNode("");
            p3.appendChild(node3);
            td3.appendChild(p3);

            tr2.appendChild(td3);

            var td4 = document.createElement("td");
            //td4.classList.add("l-border");

            td4.setAttribute("style", "width: 30px;");
            var p4 = document.createElement("p")
            var node4 = document.createTextNode("");
            p4.appendChild(node4);
            td4.appendChild(p4);

            tr2.appendChild(td4);

            tbl.appendChild(tr2)
        }

        // 空行
        {
            var trWk = document.createElement("tr");
            var tdwk = document.createElement("td");
            //tdwk.classList.add("l-border");

            var p = document.createElement("p")
            var node4 = document.createTextNode("　")
            p.appendChild(node4);
            tdwk.appendChild(p);
            trWk.appendChild(tdwk);
            tbl.appendChild(trWk)
        }

        // ３行目（効率可否／例外時の作業項目）
        var tr3 = document.createElement("tr");
        {
            // 効率可能／不可
            var td1 = document.createElement("td");
            td1.setAttribute("colspan", "1.5");
            var p = document.createElement("p")
            var node4 = document.createTextNode("効率可否")
            p.appendChild(node4);

            var text_box = document.createElement("input");
            text_box.setAttribute("type", "text");
            text_box.setAttribute("style", "width: 180px; height:35px;");
            text_box.setAttribute("class", "form-control");
            text_box.setAttribute("readonly", "true");
            text_box.setAttribute("value", EfficiencyInfo);
            td1.appendChild(p);
            td1.appendChild(text_box);

            // 例外時の作業項目
            var td2 = document.createElement("td");
            td2.setAttribute("colspan", "1.5");
            var p = document.createElement("p")
            var node4 = document.createTextNode("例外時の作業項目")
            p.appendChild(node4);
            var text_box = document.createElement("input");
            text_box.setAttribute("type", "text");
            text_box.setAttribute("style", "width: 403px; height:35px;");
            text_box.setAttribute("class", "form-control");
            text_box.setAttribute("readonly", "true");
            text_box.setAttribute("value", ExceptionWorkInfo);

            td2.appendChild(p);
            td2.appendChild(text_box);

            tr3.appendChild(td1);
            tr3.appendChild(td2);
            tbl.appendChild(tr3)
        }

        // ４行目（操作対象等,補足説明, 参考資料等 ）
        var tr4 = document.createElement("tr");
        {
            // 操作対象等
            var td1 = document.createElement("td");
            td1.setAttribute("colspan", "1.5");
            var p = document.createElement("p")
            var node4 = document.createTextNode("操作対象等")
            p.appendChild(node4);
            td1.appendChild(p);

            var text_box = document.createElement("input");
            text_box.setAttribute("type", "text");
            text_box.setAttribute("style", "width: 180px; height:35px;");
            text_box.setAttribute("class", "form-control");
            text_box.setAttribute("readonly", "true");
            text_box.setAttribute("value", OperationTarget);
            td1.appendChild(text_box);
            tr4.appendChild(td1);

            // 補足説明, 参考資料等
            var td2 = document.createElement("td");
            td2.setAttribute("colspan", "1.5");
            td2.setAttribute("rowspan", "2");
            var p = document.createElement("p")
            var node4 = document.createTextNode("補足説明, 参考資料等")
            p.appendChild(node4);
            td2.appendChild(p);

            var textarea = document.createElement("textarea");
            textarea.setAttribute("style", "width:400px; height: 120px;");
            textarea.setAttribute("readonly", "true");
            textarea.value = SupplementCommentIngo

            td2.appendChild(textarea);
            tr4.appendChild(td2);
            tbl.appendChild(tr4)
        }

        // ５行目（作業時間）
        var tr5 = document.createElement("tr");
        {
            var tr5 = document.createElement("tr");
            var td1 = document.createElement("td");
            td1.setAttribute("colspan", "1.5");
            var p = document.createElement("p")
            var node4 = document.createTextNode("作業時間（分）")
            p.appendChild(node4);
            td1.appendChild(p);

            var text_box = document.createElement("input");
            text_box.setAttribute("type", "text");
            text_box.setAttribute("style", "width: 180px; height:35px;");
            text_box.setAttribute("class", "form-control");
            text_box.setAttribute("readonly", "true");
            text_box.setAttribute("value", WorkingHourInfo);
            // 合計時間
            if (isNumber(WorkingHourInfo) == true) {
                G_WORKTIME_TOTAL = G_WORKTIME_TOTAL + Number(WorkingHourInfo);
            }

            td1.appendChild(text_box);
            tr5.appendChild(td1);

            tbl.appendChild(tr5);
        }

        container_id.appendChild(tbl);

        // 展開ボタン
        var openImg = document.createElement("img");
        openImg.setAttribute("src", "static/img/flowChartImg/OpenClose.svg");
        openImg.setAttribute("title", "edit");
        openImg.setAttribute("style", "width: 20px;");
        openImg.setAttribute("name", "open")

        var openButton = document.createElement("button");
        openButton.setAttribute("id", "show_btn");
        openButton.setAttribute("style", "margin-left: -25px;margin-bottom: -15px;");
        // openButton.addEventListener("click", "show_hide_div()");
        // 要素にクリックイベントを追加する
        openButton.onclick = (function (num) {
            return function () {
                var openStatusName = "OpenStatus_" + String(num);
                const status = document.getElementById(openStatusName).value;

                if (status == "1") {
                    var tablename = "#table_" + String(num)
                    $(tablename).hide();
                    document.getElementById(openStatusName).value = "0";
                } else {
                    var tablename = "#table_" + String(num)
                    $(tablename).show();
                    document.getElementById(openStatusName).value = "1";
                }
            }
        })(i);

        openButton.appendChild(openImg);
        container_id.appendChild(openButton);

        // 親に追加
        container_top.append(container_id);

        // 画面上部へデータを設定する
        // 合計時間
        var wknum = G_WORKTIME_TOTAL / 60.0;
        document.getElementById("TotalWorkingTime").value = wknum.toFixed(2);

    } // end loop

};

// ###################################################################################
// ###################################################################################
// ###################################################################################

// ----------------------------------------------
// 保存（ProcessChartDataTBL）
// ----------------------------------------------
function SaveToProcessChartDataTBL() {
    // 外部閲覧を禁止する
    var wkPermissionFlag = document.getElementById("PermissionFlag").checked;

    // 変更を禁止する
    var wkChangeProhibitionflag = document.getElementById("ChangeProhibitionFlag").checked;

    // 合計時間
    var wkTotalWorkingTime = document.getElementById("TotalWorkingTime").value;

    // 作業頻度
    var wkWorkFrequency = document.getElementById("SelectWorkFrequency").value;
    wkWorkFrequency = wkWorkFrequency.replace("WorkFrequency_", "");
    wkWorkFrequency = wkWorkFrequency.replace("0", "");
    if (isNumber(wkWorkFrequency) == false) {
        alert("作業頻度は、数値で入力してください。");
        return;
    }
    // 作業人数
    var wkNumberOfWorkers = document.getElementById("SelectWorkNumberOfWorkers").value;
    wkNumberOfWorkers = wkNumberOfWorkers.replace("NumberOfWorkers_", "");
    wkNumberOfWorkers = wkNumberOfWorkers.replace("0", "");
    if (isNumber(wkNumberOfWorkers) == false) {
        alert("作業人数は、数値で入力してください。");
        return;
    }

    var email = sessionStorage.getItem("email");
    var org1 = sessionStorage.getItem("org1");
    var org2 = sessionStorage.getItem("org2");
    var processProcedureID = sessionStorage.getItem("ProcessProcedureID");
    var processProcedureName = sessionStorage.getItem("ProcessProcedureName");
    var chartDesignCode = sessionStorage.getItem("ChartDesignCode");

    // 更新
    $.ajax({
        url: '/setProcessChartTblData/',
        type: 'POST',
        data: {
            email: email,
            org1: org1,
            org2: org2,
            processProcedureID: processProcedureID,
            processProcedureName: processProcedureName,
            chartDesignCode: chartDesignCode,
            permissionFlag: wkPermissionFlag,
            changeProhibitionFlag: wkChangeProhibitionflag,
            totalWorkingTime: wkTotalWorkingTime,
            workFrequency: wkWorkFrequency,
            numberOfWorkers: wkNumberOfWorkers
        },
        dataType: 'json',
        success: function (response) {

        }
    });
};


// ----------------------------------------------
// 印刷
// ----------------------------------------------
function chartPrint() {
    // 画面左側を非表示にして、コメント部のみを印刷する
    var l_wrapper = document.getElementById('l_wrapper');
    var r_wrapper = document.getElementById('r_wrapper');

    l_wrapper.setAttribute("style", "width: 0px;");
    l_wrapper.style.visibility = "hidden";

    r_wrapper.setAttribute("style", "margin-left: -450px;");

    // 不要ボタン等の非表示
    // ----------------------------------
    // チャート印刷
    var btn_print = document.getElementById('btn_print');
    btn_print.style.visibility = "hidden";
    // 戻る
    var btn_Back = document.getElementById('btn_Back');
    btn_Back.style.visibility = "hidden";

    // 外部閲覧を禁止する
    var permissionFlag = document.getElementById('PermissionFlag');
    var permissionFlagText = document.getElementById('PermissionFlagText');
    permissionFlag.style.visibility = "hidden";
    permissionFlagText.style.visibility = "hidden";

    // 変更を禁止する
    var changeProhibitionFlag = document.getElementById('ChangeProhibitionFlag');
    var changeProhibitionFlagText = document.getElementById('ChangeProhibitionFlagText');
    changeProhibitionFlag.style.visibility = "hidden";
    changeProhibitionFlagText.style.visibility = "hidden";

    // 保存
    var updateChartData = document.getElementById('updateChartData');
    updateChartData.style.visibility = "hidden";

    // 印刷
    window.print();

    // 元に戻す
    updateChartData.style.visibility = "visible";

    changeProhibitionFlag.style.visibility = "visible";
    changeProhibitionFlagText.style.visibility = "visible";

    permissionFlag.style.visibility = "visible";
    permissionFlagText.style.visibility = "visible";

    btn_print.style.visibility = "visible";
    btn_Back.style.visibility = "visible";

    l_wrapper.style.visibility = "visible";
    l_wrapper.setAttribute("style", "width: 103%;");

    r_wrapper.setAttribute("style", "margin-left: 0x;");
}