// =============================================================================
// 画面名：プロセス可視化チャート：編集画面
// 
// -----------------------------------------------------------------------------
// （ファイル整形）Visual Studio Code : Shift + Alt + f 
// =============================================================================


// ##################################################################################################
// ##################################################################################################
/* セッション情報取得 */

console.log("■ ---------------------------------------------");
console.log("■ セッション情報 -- ProcessCheckEditWindow.js --------");

console.log("edit_dataId=" + sessionStorage.getItem("edit_dataId"));
console.log("ChartDesignCode=" + sessionStorage.getItem("ChartDesignCode"));
console.log("edit_CommentCode=" + sessionStorage.getItem("edit_CommentCode"));

console.log("ChangeProhibitionflag=" + sessionStorage.getItem("ChangeProhibitionflag"));

// 変更禁止フラグ（１：禁止）
var CHANGEPROHIBITIONFLAG = sessionStorage.getItem("ChangeProhibitionflag");

// 初期表示時のコメントコード
var ORG_COMMENT_CODE = sessionStorage.getItem("edit_CommentCode");

// ##################################################################################################
// ##################################################################################################
/* function の処理を記述 */

// 初期化
function clearData() {
    //alert("clear data...")
    $("#comment_code").val("0000");
    $("#heading").val("");
    $("#explaination").val("");
    $("#efficiency").val("");
    $("#ExceptionWork").val("");
    $("#OperationTarget").val("");
    $("#working_hour").val("");
    $("#SupplementComment").val("");
}

// ----------------------------------------------
// コメントコードを変更する
// ----------------------------------------------
function commentCode_onchange() {
    var comment_code = $("#comment_code").val();
    if (comment_code == "0000") {
        const now = new Date(); // 現在の日付からDateオブジェクト作成

        const nowString = now.getFullYear()
            + (now.getMonth() + 1).toString().padStart(2, "0")
            + now.getDate().toString().padStart(2, "0")
            + now.getHours().toString().padStart(2, "0")
            + now.getMinutes().toString().padStart(2, "0")
            + now.getSeconds().toString().padStart(2, "0")
            + ".000000"

        var newCommentCode = "Comment_" + nowString
        $("#new_comment_code").val(newCommentCode);
        $("#new_comment_code").attr("readonly", true);
        clearData();
    }
    else {
        $("#new_comment_code").val("");
        $("#new_comment_code").attr("readonly", true);

        // コメントコードを検索して表示する
        sessionStorage.setItem("edit_CommentCode", comment_code);

        onloadProcessEditWindow()
    }
}

// ----------------------------------------------
// 画面：情報を表示する
// ----------------------------------------------
function onloadProcessEditWindow() {

    // デザインコード
    chartDesignCode = sessionStorage.getItem("ChartDesignCode");

    // 位置情報
    locationInfo = sessionStorage.getItem("edit_dataId");
    $("#location_id").text(sessionStorage.getItem("edit_dataId"))

    // コメントコード
    var commentCode = sessionStorage.getItem("edit_CommentCode")

    /// ------------------------------------
    /// コメントリストを取得して、設定する
    /// ------------------------------------
    $.ajax({
        url: '/getCommentList/',
        type: 'POST',
        data: {
            commentCode: ORG_COMMENT_CODE
        },
        dataType: 'json',
        success: function (response) {
            console.log("response in get comment list " + response)
            $("#comment_code").empty();
            $("#comment_code").append("<option value='0000'>" + "新規作成" + "</option>");
            for (var i = 0; i < response.length; i++) {
                if (commentCode == response[i]) {
                    $("#comment_code").append("<option value='" + response[i] + "' selected>" + response[i] + "</option>");
                } else {
                    $("#comment_code").append("<option value='" + response[i] + "'>" + response[i] + "</option>");
                }
            }
        }
    });


    /// ------------------------------------
    /// コメント情報を取得する
    /// ------------------------------------
    $.ajax({
        url: '/getProcessChartCommentDataFromCode/',
        type: 'POST',
        data: {
            chartDesignCode: chartDesignCode,
            commentCode: commentCode
        },
        success: function (response) {
            var BlockData = response[0].design[0].Block;
            dispEditData(BlockData);
        }
    });

    // 変更禁止なので、更新系のボタンを削除する
    if (CHANGEPROHIBITIONFLAG == "1") {
        $("#updateDataButton").remove();
        $("#cancelDataButton").remove();
        $("#deleteDataButton").remove();
        $("#clearDataButton").remove();

        document.getElementById("comment_code").disabled = true;
    }
}

// ----------------------------------------------
// 画面：各情報を表示する
// ----------------------------------------------
function dispEditData(BlockData) {

    // 見出し
    var Heading = BlockData.Heading;
    $("#heading").val(Heading)

    // 説明
    var Explanation = BlockData.Explanation;
    $("#explaination").val(Explanation)

    // 効率可否
    var Efficiency = BlockData.Efficiency;
    if (Efficiency == 0) {
        $("#efficiency option[value='0']").prop('selected', true);
    }
    else {
        $("#efficiency option[value='1']").prop('selected', true);
    }

    // 操作
    var OperationTarget = BlockData.OperationTarget;
    if (OperationTarget == "") {
        $("#OperationTarget option[value='']").prop('selected', true);
    }
    else {
        $("#OperationTarget option[value='" + OperationTarget + "']").prop('selected', true);
    }

    // 作業時間
    var WorkingHour = BlockData.WorkingHour;
    if (WorkingHour == "0" || WorkingHour == "") {
        $("#working_hour option[value='0']").prop('selected', true);
    }
    else {
        $("#working_hour option[value='" + WorkingHour + "']").prop('selected', true);
    }

    var ExceptionWork = BlockData.ExceptionWork;
    $("#ExceptionWork").val(ExceptionWork)

    var SupplementComment = BlockData.SupplementComment;
    $("#SupplementComment").val(SupplementComment);
}


// ----------------------------------------------
// 画面：各情報を更新する
// ----------------------------------------------
function updateButtonClick() {
    //alert('Click');

    // デザインコード
    chartDesignCode = sessionStorage.getItem("ChartDesignCode");

    // 位置情報
    locationInfo = sessionStorage.getItem("edit_dataId");
    $("#location_id").text(sessionStorage.getItem("edit_dataId"))

    updateType = "update";
    var new_comment_code = $("#new_comment_code").val();

    var comment_code = $("#comment_code").val();
    if (comment_code == "0000") {
        updateType = "insert";
        comment_code = new_comment_code;
    }

    var heading = $("#heading").val();
    var explaination = $("#explaination").val();
    var efficiency = $("#efficiency").val();
    var ExceptionWork = $("#ExceptionWork").val();
    var OperationTarget = $("#OperationTarget").val();
    var working_hour = $("#working_hour").val();
    var SupplementComment = $("#SupplementComment").val();

    console.log("updateType = " + updateType);
    console.log("commentcode = " + comment_code);
    console.log("heading = " + heading);
    console.log("explaination = " + explaination);
    console.log("efficiency = " + efficiency);
    console.log("ExceptionWork= " + ExceptionWork);
    console.log("OperationTarget = " + OperationTarget);
    console.log("working_hour = " + working_hour);
    console.log("SupplementComment = " + SupplementComment);

    $.ajax({
        url: '/updateChartCommentInfo/',
        type: 'POST',
        data: {
            updateType: updateType,
            chartDesignCode: chartDesignCode,
            locationInfo: locationInfo,
            comment_code: comment_code,
            heading: heading,
            explaination: explaination,
            efficiency: efficiency,
            ExceptionWork: ExceptionWork,
            OperationTarget: OperationTarget,
            working_hour: working_hour,
            SupplementComment: SupplementComment
        },
        success: function (response) {
            // コメントコードを入れ替える
            ORG_COMMENT_CODE = comment_code;
            // 閉じる
            window.close()
        }
    });
}

// ----------------------------------------------
// 画面：各情報を削除する
// ----------------------------------------------
function deleteButtonClick() {

    // デザインコード
    chartDesignCode = sessionStorage.getItem("ChartDesignCode");

    // 位置情報
    locationInfo = sessionStorage.getItem("edit_dataId");
    $("#location_id").text(sessionStorage.getItem("edit_dataId"))

    // コメントコード
    var commentCode = $("#comment_code").val();
    if (ORG_COMMENT_CODE == commentCode) {
        alert("設定されているコメントは削除できません");
        return;
    }

    $.ajax({
        url: '/deleteChartCommentData/',
        type: 'POST',
        data: {
            chartDesignCode: chartDesignCode,
            locationInfo: locationInfo,
            commentCode: commentCode,
        },
        success: function (response) {
        }
    });

}

// ----------------------------------------------
// 画面キャンセルする
// ----------------------------------------------
function cancelButtonClick() {
    var result = window.confirm("変更内容を保存しないで、キャンセルしますか？");
    if (result == true) {
        window.close();
    }

}
