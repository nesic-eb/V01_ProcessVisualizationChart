// =============================================================================
// 画面名：プロセス可視化チャート：カラム・行ラベル編集画面
// 
// -----------------------------------------------------------------------------
// （ファイル整形）Visual Studio Code : Shift + Alt + f 
// =============================================================================


// ##################################################################################################
// ##################################################################################################
/* セッション情報取得 */

console.log("■ ---------------------------------------------");
console.log("■ セッション情報 -- ProcessLabelEditWindow.js --------");

console.log("dataStartIdx=" + sessionStorage.getItem("dataStartIdx"));
console.log("labelComment=" + sessionStorage.getItem("labelComment"));
console.log("labelType=" + sessionStorage.getItem("labelType"));

// 変更禁止フラグ（１：禁止）
var CHANGEPROHIBITIONFLAG = sessionStorage.getItem("ChangeProhibitionflag");

// 画面のデザインコード
var ORG_PROCESSPROCEDUREID = sessionStorage.getItem("ProcessProcedureID");

console.log("ChangeProhibitionflag=" + CHANGEPROHIBITIONFLAG);

// ##################################################################################################
// ##################################################################################################
/* function の処理を記述 */

// 初期化
function clearData() {
    //alert("clear data...")
    $("#label_dataId").val("");
    $("#label_comment").val("");
}

// ----------------------------------------------
// 画面：情報を表示する
// ----------------------------------------------
function onLoadProcessLableData() {

    // 位置情報
    dataStartIdx = sessionStorage.getItem("dataStartIdx");
    $("#dataStartIdx").text(sessionStorage.getItem("dataStartIdx"));

    // コメント情報
    var labelComment = sessionStorage.getItem("labelComment");
    var labelType = sessionStorage.getItem("labelType");

    // ラベルが未設定の場合は、開始位置の設定を行う
    if (labelComment == "") {
        if (labelType == "Process") {
            var chr = String.fromCharCode(64 + Number(dataStartIdx));
            $("#lableStart").val(chr);
        }
        if (labelType == "Department") {
            var idx = dataStartIdx;
            $("#lableStart").val(idx);
        }
    }

    /// ------------------------------------
    /// コメントリストを取得して、設定する
    /// ------------------------------------
    $.ajax({
        url: '/getChartLabelText/',
        type: 'POST',
        data: {
            processProcedureID: ORG_PROCESSPROCEDUREID,
            dataStartIdx: dataStartIdx,
            labelComment: labelComment,
            labelType: labelType
        },
        dataType: 'json',
        success: function (response) {
            labelData = response[0].BusinessLabel;

            if (labelType == "Process") {
                var startchr = String.fromCharCode(64 + Number(labelData[0].StartIdx));
                var endchr = String.fromCharCode(64 + Number(labelData[0].EndIdx));
                $("#chartLableText").empty();
                $("#chartLableText").val(labelData[0].LabelText);
                $("#lableStart").val(startchr);
                $("#lableEnd").val(endchr);

                $("#selectColor option[value='" + labelData[0].LabelColor + "']").attr("selected", "selected");
                var ObjSelectLabel = document.getElementById("selectColorLabel");
                ObjSelectLabel.style.backgroundColor = labelData[0].LabelColor;

                var ll = document.getElementById("location_id");
                ll.innerHTML = startchr + " ～ " + endchr;
            }

            if (labelType == "Department") {
                var startchr = labelData[0].StartIdx;
                var endchr = labelData[0].EndIdx;
                $("#chartLableText").empty();
                $("#chartLableText").val(labelData[0].LabelText);
                $("#lableStart").val(startchr);
                $("#lableEnd").val(endchr);

                $("#selectColor option[value='" + labelData[0].LabelColor + "']").attr("selected", "selected");
                var ObjSelectLabel = document.getElementById("selectColorLabel");
                ObjSelectLabel.style.backgroundColor = labelData[0].LabelColor;

                var ll = document.getElementById("location_id");
                ll.innerHTML = startchr + " ～ " + endchr;
            }
        }
    });

    // 変更禁止なので、更新系のボタンを削除する
    if (CHANGEPROHIBITIONFLAG == "1") {
        $("#updateDataButton").remove();
        $("#cancelDataButton").remove();
        $("#deleteDataButton").remove();

        document.getElementById("chartLableText").disabled = true;
    }
}

// ----------------------------------------------
// 画面：各情報を更新する
// ----------------------------------------------
function updateButtonClick() {
    // タイプ
    var labelType = sessionStorage.getItem("labelType")

    // 位置情報（元）
    var beforeDataStartIdx = sessionStorage.getItem("dataStartIdx");

    var diagramColumns = sessionStorage.getItem("diagramColumns");
    var diagramColumnsAlpha = String.fromCharCode(64 + Number(diagramColumns));
    var diagramRows = sessionStorage.getItem("diagramRows");

    // コメント情報
    var labelText = $("#chartLableText").val();
    if (labelText.trim() == "") {
        alert("ラベル名を入力してください。");
        return;
    }

    // 開始
    if (labelType == "Process") {
        var startchr = $("#lableStart").val();
        if (startchr.trim() == "") {
            alert("開始位置を入力してください。");
            return;
        }
        if (startchr.trim() != "") {
            if (startchr.length != 1 || (startchr < "A" || startchr > diagramColumnsAlpha)) {
                alert("開始位置は、A ～ " + diagramColumnsAlpha + " で入力してください。");
                return;
            }
        }
    }

    if (labelType == "Department") {
        var startchr = $("#lableStart").val();
        if (startchr.trim() == "") {
            alert("開始位置を入力してください。");
            return;
        }
        if (startchr.trim() != "") {
            if (startchr.length != 1 || (startchr < "0" || startchr > diagramRows)) {
                alert("開始位置は、1 ～ " + diagramRows + " で入力してください。");
                return;
            }
        }
    }

    // 終了
    if (labelType == "Process") {
        var endchr = $("#lableEnd").val();
        if (endchr.trim() == "") {
            alert("終了位置を入力してください。");
            return;
        }
        if (endchr.trim() != "") {
            if (startchr.length != 1 || (endchr < "A" || endchr > diagramColumnsAlpha)) {
                alert("終了位置は、A ～ " + diagramColumnsAlpha + " で入力してください。");
                return;
            }
        }
    }

    if (labelType == "Department") {
        var endchr = $("#lableEnd").val();
        if (endchr.trim() == "") {
            alert("終了位置を入力してください。");
            return;
        }
        if (endchr.trim() != "") {
            if (startchr.length != 1 || (endchr < "0" || endchr > diagramRows)) {
                alert("終了位置は、1 ～ " + diagramRows + " で入力してください。");
                return;
            }
        }
    }

    // 判定
    if (labelType == "Process") {
        if (endchr < startchr) {
            alert("開始位置が小さいカラム名になるように入力してください。");
            return;
        }
    }

    if (labelType == "Department") {
        if (endchr < startchr) {
            alert("開始位置が小さい行番号になるように入力してください。");
            return;
        }
    }

    // カラー
    var ObjSelectColor = document.getElementById("selectColor");
    var colorValue = ObjSelectColor.value;

    $.ajax({
        url: '/updateChartLabelText/',
        type: 'POST',
        data: {
            processProcedureID: ORG_PROCESSPROCEDUREID,
            beforeDataStartIdx: beforeDataStartIdx,
            dataStartIdx: startchr,
            dataEndIdx: endchr,
            labelText: labelText,
            labelType: labelType,
            labelColor: colorValue
        },
        success: function (response) {
            if (response.status == "NG") {
                alert(response.message);
            }
            // 閉じる
            window.close()
        }
    });

}

// ----------------------------------------------
// 画面：各情報を削除する
// ----------------------------------------------
function deleteButtonClick() {
    var result = window.confirm("削除しますか？");
    if (result == false) {
        return;
    }

    // タイプ
    var labelType = sessionStorage.getItem("labelType")

    // 位置情報（元）
    var beforeDataStartIdx = sessionStorage.getItem("dataStartIdx");

    $.ajax({
        url: '/deleteChartLabelText/',
        type: 'POST',
        data: {
            processProcedureID: ORG_PROCESSPROCEDUREID,
            beforeDataStartIdx: beforeDataStartIdx,
            labelType: labelType
        },
        success: function (response) {
            if (response.status == "NG") {
                alert(response.message);
            }
            // 閉じる
            window.close()
        }
    });
}

// ----------------------------------------------
// 画面キャンセルする
// ----------------------------------------------
function cancelButtonClick() {
    var result = true;
    //result = window.confirm("変更内容を保存しないで、キャンセルしますか？");
    if (result == true) {
        window.close();
    }
}

// ----------------------------------------------
// ラベルカラーを選択した
// ----------------------------------------------
function onSelectColorChange() {
    var ObjSelectColor = document.getElementById("selectColor");
    var ObjSelectLabel = document.getElementById("selectColorLabel");
    var selectColor = ObjSelectColor.value;
    ObjSelectLabel.style.backgroundColor = selectColor;
}