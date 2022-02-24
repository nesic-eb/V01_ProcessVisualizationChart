// =============================================================================
// 画面名：プロセス可視化チャートの詳細画面
// 
// -----------------------------------------------------------------------------
// （ファイル整形）Visual Studio Code : Shift + Alt + f 
// =============================================================================


// ##################################################################################################
// ##################################################################################################
/* セッション情報取得 */
console.log("■ ---------------------------------------------");
console.log("■ セッション情報 -- ProcessDiagramDetail.js --------");

// ##################################################################################################
// ##################################################################################################
/* functin以外の処理を記述 */

// A $( document ).ready() block.
$(document).ready(function () {

    console.log("ready!");
    var chartDesignCode = "DesignCode_20220214135920";

    $.ajax({
        url: '/getProcessChartDrawingData/',
        type: 'POST',
        data: {
            chartDesignCode: chartDesignCode
        },
        dataType: 'json',
        success: function (response) {
            // 図面データ取得
            console.log("REACh")

            var result = JSON.stringify(response)
            var data = response[0].Data
            console.log("data = " + JSON.stringify(data))

            var Num = response[0].Num
            console.log("Num = " + JSON.stringify(Num))

            var design = response[0].design
            console.log("design = " + JSON.stringify(design))

            var RowsNumber = data[0].RowsNumber
            console.log("rows = " + RowsNumber)

            var ColumnNumber = data[0].ColumnNumber
            console.log("column = " + ColumnNumber);

            // ---------------------------
            // 画面上部の値
            // ---------------------------
            // 合計時間
            document.getElementById("sumHounr").value = data[0].TotalWorkingTime;
            // 作業頻度
            document.getElementById("WorkFrequency").value = data[0].WorkFrequency;
            // 作業人数
            document.getElementById("NumberOfWorkers").value = data[0].WorkFrequency;
            // 外部閲覧を禁止する
            if (data[0].WorkFrequency == "0") {
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

            // ---------------------------
            // 画面：左側 
            // ---------------------------
            // 図面データに合わせて枠を表示する
            createLeftTable(RowsNumber, ColumnNumber, design);

            // ---------------------------
            // 画面：右側
            // ---------------------------
            // 図面データに合わせてコメントを表示する
            rightTableCreate(design)

        }
    });
});


// ##################################################################################################
// ##################################################################################################
/* function の処理を記述 */

// ----------------------------------------------
// 画面：チャート図形枠の最大幅を取得する
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
// 画面：左側を作図する
// ----------------------------------------------
function createLeftTable(rows, column, design) {

    // 枠（幅）の最大値を求める
    var widthMax = imgTableWidth(design);

    // 画面左側ブロックの親
    var left_table = document.getElementById("left_table_Div");
    left_table.setAttribute("style", "width: " + String(widthMax) + "px;")
    //left_table.setAttribute("style", "width: 1000px;")

    var mainTable = document.createElement("table");
    mainTable.setAttribute("style", "border: 1px; background-color: #cdefff; ");

    // 行
    for (var j = 0; j <= rows; j++) {
        var tr = document.createElement("tr");
        tr.classList.add("l-border");

        // カラムループ
        for (var i = 0; i <= column; i++) {
            var chr = "";
            if (j == 0) {
                var th = document.createElement("th");
                th.classList.add("l-border");
                th.setAttribute("style", "text-align:center; width: 20px; height: 30px;");
                th.style.backgroundColor = "#98fb98";
                if (i == 0) {
                    var node = document.createTextNode("No.");
                    th.appendChild(node)
                } else {
                    chr = String.fromCharCode(64 + i);
                    var node = document.createTextNode(chr);
                    th.appendChild(node)
                }
                tr.appendChild(th);

            } else {
                chr = String.fromCharCode(64 + i);
                var td = document.createElement("td");
                td.classList.add("l-border");
                if (i == 0) {
                    td.setAttribute("style", "text-align:center; vertical-align:middle; width: 20px; height: 30px;");
                    td.style.backgroundColor = "#f08080";
                }
                else {
                    // 枠
                    td.setAttribute("style", "text-align:center; vertical-align:middle; width: 20px; height: 30px;");
                    td.style.backgroundColor = "#ffffff";
                }
                td.setAttribute("id", chr + "_" + j)
                if (i == 0) {
                    var node = document.createTextNode(j);
                    td.appendChild(node);
                }

                tr.appendChild(td);
            }
        }

        // テーブルに行を追加
        mainTable.appendChild(tr)
    }

    // 親DIVにtableを追加
    left_table.append(mainTable)

    console.log("design in function = " + design);

    for (var a = 0; a < design.length; a++) {
        var Block = design[a].Block;
        var LocationInfo = Block.LocationInfo;
        console.log("LocationInfo = " + LocationInfo);
        var location_id = document.getElementById(LocationInfo);

        var ImageName = Block.ImageName;
        console.log("ImageName = " + ImageName);
        var CommentCode = Block.CommentCode;
        console.log("CommentCode=" + CommentCode);
        var Heading = Block.Heading;
        console.log("Heading = " + Heading);
        var Explanation = Block.Explanation;
        console.log("Explanation=" + Explanation);

        var br = document.createElement("br");

        // 選択画像
        var image = document.createElement("img");
        image.setAttribute("src", "static/img/flowChartImg/" + ImageName + ".png");
        image.setAttribute("title", "images");
        image.setAttribute("style", "width: 60%; margin-left: -20px; margin-top: 2px;");
        location_id.appendChild(image);
        location_id.appendChild(br);

        // 説明
        var text_box = document.createElement("input");
        text_box.setAttribute("type", "text");
        text_box.setAttribute("style", "background-color: wheat; width: 160px; height: 30px; margin-top: 5px; text-align:center; color: brown;");
        text_box.setAttribute("readonly", "true");
        text_box.setAttribute("value", Heading);
        location_id.appendChild(text_box);

        // 編集アイコン
        var a_link = document.createElement("a")
        a_link.setAttribute("href", "JavaScript:showModal('EdithWindow', '" + LocationInfo + "')");
        a_link.setAttribute("title", "editLink");
        a_link.setAttribute("id", LocationInfo);
        a_link.setAttribute("name", LocationInfo);

        var img_edit = document.createElement("img");
        img_edit.setAttribute("src", "static/img/flowChartImg/editData.png");
        img_edit.setAttribute("title", "edit");
        img_edit.setAttribute("style", "width: 20px;");
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
        container_id.setAttribute("style", "border: 1px solid #e3e3e3;");

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
        tbl.setAttribute("style", "border: 1px #e3e3e3; width=1100px;");

        // 空行
        {
            // 展開の状態
            var trWk = document.createElement("tr");
            var tdwk = document.createElement("td");
            var text_box = document.createElement("input")
            text_box.setAttribute("type", "hidden");
            text_box.setAttribute("value", "1");
            text_box.setAttribute("id", "OpenStatus_" + String(i));
            text_box.setAttribute("name", "OpenStatus_" + String(i));

            var p1 = document.createElement("p");
            var node = document.createTextNode("　");
            p1.appendChild(node);
            tdwk.appendChild(p1);

            tdwk.appendChild(text_box);
            trWk.appendChild(tdwk);
            tbl.appendChild(trWk)

        }

        // １行目
        var tr1 = document.createElement("tr");
        {
            var td1 = document.createElement("td");
            td1.setAttribute("style", "width: 200px;");

            // 位置
            var p1 = document.createElement("p");
            var node = document.createTextNode("位置")
            p1.appendChild(node);;
            td1.appendChild(p1);

            var text_box = document.createElement("input");
            text_box.setAttribute("type", "text");
            text_box.setAttribute("style", "background-color: yellow; width: 180px; height: 30px; margin-top: 5px; text-align:left;");
            text_box.setAttribute("readonly", "true");
            text_box.setAttribute("value", LocationInfo);
            td1.appendChild(text_box);

            // 見出し
            var td2 = document.createElement("td");
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

            // 予備
            var td3 = document.createElement("td");
            td3.setAttribute("style", "width: 10px;");
            var p3 = document.createElement("p")
            var node3 = document.createTextNode("");
            p3.appendChild(node3);
            td3.appendChild(p3);
        }

        tr1.appendChild(td1);
        tr1.appendChild(td2);
        tr1.appendChild(td3);

        tbl.appendChild(tr1)

        // ２行目（説明）
        var tr2 = document.createElement("tr");
        {
            var td1 = document.createElement("td");
            td1.setAttribute("colspan", "3");
            var p = document.createElement("p")
            var node4 = document.createTextNode("説明")
            p.appendChild(node4);
            td1.appendChild(p)

            var textarea = document.createElement("textarea");
            textarea.setAttribute("style", "width:763px; height: 100px;");
            textarea.setAttribute("readonly", "true");
            textarea.value = CommentInfo

            td1.appendChild(textarea)
            tr2.appendChild(td1);
            tbl.appendChild(tr2)
        }

        // 空行
        {
            var trWk = document.createElement("tr");
            var tdwk = document.createElement("td");
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
            text_box.setAttribute("style", "width: 563px; height:35px;");
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
            textarea.setAttribute("style", "width:563px; height: 120px;");
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
            var node4 = document.createTextNode("作業時間")
            p.appendChild(node4);
            td1.appendChild(p);

            var text_box = document.createElement("input");
            text_box.setAttribute("type", "text");
            text_box.setAttribute("style", "width: 180px; height:35px;");
            text_box.setAttribute("class", "form-control");
            text_box.setAttribute("readonly", "true");
            text_box.setAttribute("value", WorkingHourInfo);
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
    } // end loop

};


