// =============================================================================
// 画面名：プロセス可視化チャート：チャート表示画面
// 
// -----------------------------------------------------------------------------
// （ファイル整形）Visual Studio Code : Shift + Alt + f 
// =============================================================================


// ##################################################################################################
// ##################################################################################################3
/* セッション情報取得 */

console.log("■ ---------------------------------------------");
console.log("■ セッション情報 -- ProcessDiagram.js --------");

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

// 画面表示を変更する
$("body").css("zoom", "90%");

// ##################################################################################################
// ##################################################################################################
/* functin以外の処理を記述 */

// チャートデザインコード（hiddin）
$('#chartDesignCode').val(ChartDesignCode);

// 変更禁止なので、更新系のボタンを削除する
if (CHANGEPROHIBITIONFLAG == "1") {
  $("#updateChartName").remove();
  $("#updateWakuSize").remove();
  document.getElementById("DiagramColumns").readOnly = true;
  document.getElementById("DiagramRows").readOnly = true;
  document.getElementById("AutoSaveModeCheck").checked = false;
}

var keepColumnNum = 0;
var keepRowsNum = 0;

// ##################################################################################################
// ##################################################################################################
/* function の処理を記述 */

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
// 自動保存の設定に合わせて＋ーを制御する
// （画像名）
// ----------------------------------------------
function AutoSaveControl() {
  if (CHANGEPROHIBITIONFLAG == "1") {
    return;
  }
  var autoSave = document.getElementById("AutoSaveModeCheck");
  var saveButton = document.getElementById("SaveButton");
  var wakuButton = document.getElementById("updateWakuSize");
  if (autoSave.checked == false) {
    AutoSaveControlflag = "0";
    sessionStorage.setItem("AutoSaveControl", "0");
    saveButton.style.visibility = "visible";
    wakuButton.style.visibility = "hidden";
    PlusMinusImgControl("hidden");
  }
  else {
    AutoSaveControlflag = "1";
    sessionStorage.setItem("AutoSaveControl", "1");
    saveButton.style.visibility = "hidden";
    wakuButton.style.visibility = "visible";
    PlusMinusImgControl("visible");
  }
}

// + - 記号アイコン, 編集アイコン
function PlusMinusImgControl(control) {
  var columsNum = sessionStorage.getItem("AutoColumnNum");
  var rowsNum = sessionStorage.getItem("AutoRowsNum");

  for (colum = 1; colum <= columsNum; colum++) {
    var chr = String.fromCharCode(64 + colum)
    if (control == "hidden") {
      var aplus = document.getElementById(chr + "_colPlus");
      var aMinus = document.getElementById(chr + "_colMinus");
      if (aplus != null) {
        aplus.style.visibility = "hidden";
        aMinus.style.visibility = "hidden";
      }
      var aEdit = document.getElementById(chr + "_process");
      if (aEdit != null) {
        aEdit.style.visibility = "hidden";
      }
    }
    else {
      var aplus = document.getElementById(chr + "_colPlus");
      var aMinus = document.getElementById(chr + "_colMinus");
      if (aplus != null) {
        aplus.style.visibility = "visible";
        aMinus.style.visibility = "visible";
      }
      var aEdit = document.getElementById(chr + "_process");
      if (aEdit != null) {
        aEdit.style.visibility = "visible";
      }
    }
  }

  for (row = 1; row <= rowsNum; row++) {
    if (control == "hidden") {
      var aplus = document.getElementById(row + "_rowPlus");
      var aMinus = document.getElementById(row + "_rowMinus");
      if (aplus != null) {
        aplus.style.visibility = "hidden";
        aMinus.style.visibility = "hidden";
      }
      var aEdit = document.getElementById(row + "_process");
      if (aEdit != null) {
        aEdit.style.visibility = "hidden";
      }
    }
    else {
      var aplus = document.getElementById(row + "_rowPlus");
      var aMinus = document.getElementById(row + "_rowMinus");
      if (aplus != null) {
        aplus.style.visibility = "visible";
        aMinus.style.visibility = "visible";
      }
      var aEdit = document.getElementById(row + "_process");
      if (aEdit != null) {
        aEdit.style.visibility = "visible";
      }
    }
  }
}

// ----------------------------------------------
// 画面で画像が設定されている情報を集めて保存する
// 
// ----------------------------------------------
function SaveToProcessChartDiagram() {
  var columsNum = document.getElementById("DiagramColumns").value;
  var rowsNum = document.getElementById("DiagramRows").value;

  var sendList = {};
  var sendObj = [];

  for (colum = 1; colum <= columsNum; colum++) {
    var chr = String.fromCharCode(64 + colum)
    for (row = 1; row <= rowsNum; row++) {
      var columRowsName = chr + "_" + row + "_select";
      var columRowsMidashi = chr + "_" + row + "_midashi";
      var selImg = document.getElementById(columRowsName).value;
      if (selImg != "") {
        if (selImg != "Space_001") {
          var textMidashi = document.getElementById(columRowsMidashi).value;
          console.log("columRowsName = " + columRowsName + " / IMG = " + selImg + " / midashi = " + textMidashi);

          var dataDic = { "img": selImg, "text": textMidashi, "location": chr + "_" + row };
          sendObj.push(dataDic);
        }
      }
    }
  }

  // デザインコード
  var chartDesignCode = $('#chartDesignCode').val();

  sendList["chartDesignCode"] = chartDesignCode;
  sendList["userInfoList"] = sendObj;

  $.ajax({
    url: '/saveAllChartDesign/',
    type: 'POST',
    data: JSON.stringify(sendList),
    dataType: 'json',
    contentType: "application / json",
    async: false,
    success: function (response) {
      if (response.status == "OK") {
        location.reload();
      }
    }
  });

}

// ----------------------------------------------
// 画面：指定カラムの画像あり／無しを求める
// （画像名）
// ----------------------------------------------
function checkImgName(checkColumn, design) {
  var checkName = "";

  for (var a = 0; a < design.length; a++) {
    var Block = design[a].Block;
    var wkColumn = Block.LocationInfo;

    if (checkColumn == wkColumn) {
      // あった
      checkName = Block.ImageName;
      var WorkingHourInfo = Block.WorkingHour;

      // 合計時間
      if (isNumber(WorkingHourInfo) == true) {
        G_WORKTIME_TOTAL = G_WORKTIME_TOTAL + Number(WorkingHourInfo);
      }
      break;
    }
  }

  return checkName;
};

// ----------------------------------------------
// 画面：指定カラムの画像あり／無しを求める
// （見出し）
// ----------------------------------------------
function checkMidashiText(checkColumn, design) {
  var checkText = "";

  for (var a = 0; a < design.length; a++) {
    var Block = design[a].Block;
    var wkColumn = Block.LocationInfo;

    if (checkColumn == wkColumn) {
      // あった
      checkText = Block.Heading;
      break;
    }
  }

  return checkText;
};

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

// ----------------------------------------------
// 画面表示時に枠情報などを作成する
// (MAIN)
// ----------------------------------------------
function onLoadProcessChartData() {

  var processProcedureID = sessionStorage.getItem("ProcessProcedureID");
  var chartDesignCode = sessionStorage.getItem("ChartDesignCode");

  // イメージ画像情報
  var ImgDataList;
  // チャートヘッダラベル情報
  var ChartBusinessLabelData;

  // 画像情報を取得する
  $.ajax({
    url: '/getProcessChartImagesData/',
    type: 'POST',
    data: {
      ChartType: "FlowChart"
    },
    dataType: 'json',
    async: false,
    success: function (response) {
      //alert(response);
      ImgDataList = response[0].Data;
    }
  });

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
      console.log("Response!!" + response[0].Data.length);

      var colNum = response[0].Data[0].ColumnNumber;
      var rowNum = response[0].Data[0].RowsNumber;
      var blockData = response[0].Data[0];
      var design = response[0].design;

      // console.log("Design = " + design);

      // 画面上部へデータを設定する
      {
        sessionStorage.setItem("AutoColumnNum", colNum);
        sessionStorage.setItem("AutoRowsNum", rowNum);

        // 名称 
        document.getElementById("process_ProcedureName").value = blockData.ProcessProcedureName;
        if (CHANGEPROHIBITIONFLAG == "0") {
          document.getElementById("process_ProcedureName").readOnly = false;
        }
        else {
          document.getElementById("process_ProcedureName").readOnly = true;
        }

        // 作業頻度
        document.getElementById("SelectWorkFrequency").value = blockData.WorkFrequency;

        // 作業人数
        document.getElementById("SelectWorkNumberOfWorkers").value = blockData.NumberOfWorkers;

        // 外部閲覧を禁止する
        if (blockData.PermissionFlag == "0") {
          document.getElementById("PermissionFlag").checked = false;
        }
        else {
          document.getElementById("PermissionFlag").checked = true;
        }

        // 変更を禁止する（作成者のみ可）
        if (blockData.ChangeProhibitionFlag == "0") {
          document.getElementById("ChangeProhibitionFlag").checked = false;
        }
        else {
          document.getElementById("ChangeProhibitionFlag").checked = true;
        }

        keepColumnNum = blockData.ColumnNumber;
        keepRowsNum = blockData.RowsNumber;

        // カラム数
        document.getElementById("DiagramColumns").value = blockData.ColumnNumber;

        // 行数
        document.getElementById("DiagramRows").value = blockData.RowsNumber;
      }

      // 枠（親DIV）
      var div = document.getElementById("processChart_container");

      var br = document.createElement("br");

      // 枠（テーブル）
      var table = document.createElement('table');
      table.setAttribute("style", "border: 1px; background-color: #ffffff");
      table.setAttribute('id', 'data_table');
      div.appendChild(table);

      var trheader = document.createElement('tr');
      trheader.classList.add("t-border");

      // ------------------------------
      // ------------------------------
      // 枠（カラム）
      // ------------------------------
      for (var j = 0; j <= Number(colNum); j++) {
        var chr = String.fromCharCode(64 + j)

        if (j == 0) {
          // No.
          var th = document.createElement('th');
          th.setAttribute("style", "text-align: center; width: 50px; height: 60px; background-color: #98fb98");
          th.setAttribute("id", "full_name");
          th.setAttribute("rowspan", "2");
          th.setAttribute("colspan", "2");
          th.classList.add("t-border");

          var span = document.createElement('span');
          span.setAttribute("style", "text-align: center; width: 25px;");
          span.innerHTML = "No.";
          th.appendChild(span);

          trheader.append(th);
        }
        else {
          var th = document.createElement('th');
          th.classList.add("t-border");

          var div = document.createElement('div');

          // A ～ Z
          th.setAttribute("style", "text-align: center; width: 190px; background-color: #98fb98");
          th.setAttribute("id", chr + "_columName");
          var span = document.createElement('span');
          span.innerHTML = chr + "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"
          div.appendChild(span);

          // Plus（カラム）
          if (CHANGEPROHIBITIONFLAG == "0") {
            {
              var aplus = document.createElement('a');
              aplus.setAttribute("href", "");
              aplus.setAttribute("id", chr + "_colPlus");
              aplus.setAttribute("name", chr + "_colPlus");
              var img = document.createElement('img');
              img.setAttribute("style", "margin-top: 0px; width: 18px;");
              img.setAttribute("id", chr + "_colPlusImg");

              // Zまである場合は、+ は表示しない
              if (Number(blockData.ColumnNumber) < 26) {
                img.setAttribute("src", "/static/img/flowChartImg/Plus.svg");
                // 要素にクリックイベントを追加する
                aplus.onclick = (function (num) {
                  return function () {
                    PlusMinusColumnAction(this, num, "plus");
                  }
                })(j);
              }
            }
            aplus.appendChild(img);
            div.appendChild(aplus);
          }

          // Minus（カラム）
          if (CHANGEPROHIBITIONFLAG == "0") {
            {
              var aMinus = document.createElement('a');
              aMinus.setAttribute("href", "");
              aMinus.setAttribute("id", chr + "_colMinus");
              aMinus.setAttribute("name", chr + "_colMinus");
              var img = document.createElement('img');
              img.setAttribute("id", chr + "_colMinusImg");
              img.setAttribute("style", "margin-top: 0px; width: 18px;");
              img.setAttribute("src", "/static/img/flowChartImg/Minus.svg");

              if (CHANGEPROHIBITIONFLAG == "0") {
                // 要素にクリックイベントを追加する
                aMinus.onclick = (function (num) {
                  return function () {
                    PlusMinusColumnAction(this, num, "Minus");
                  }
                })(j);
              }
            }
            aMinus.appendChild(img);
            div.appendChild(aMinus);
          }

          th.appendChild(div);

          trheader.append(th);
        }
      }

      // テーブルへ
      table.append(trheader);

      // （横）プロセス欄
      {
        var trp = document.createElement('tr');
        trp.classList.add("t-border");
        trp.setAttribute("style", "background-color: #FFFFCC");
        trp.setAttribute("id", "process");

        var columNumMax = 1;
        for (var j = 1; j <= Number(colNum); j++) {
          var chrP = String.fromCharCode(64 + j);

          var LabelData = getProcessLabelData_EndColum(j, "column", ChartBusinessLabelData);
          var colspanNum = 1;
          var labelColor = "#FFFFCC";
          if (LabelData != null) {
            colspanNum = Number(LabelData.EndIdx) - Number(LabelData.StartIdx) + 1;
            labelColor = LabelData.LabelColor;
          }

          if (columNumMax <= Number(colNum)) {
            if (columNumMax <= j) {

              var td = document.createElement('td');
              td.classList.add("t-border");
              td.setAttribute("style", "text-align: center; height: 30px; background-color: " + labelColor + ";");
              td.setAttribute("colspan", String(colspanNum));
              {
                var processLabel = "";
                processLabel = checkProcessLabelData(j, "column", ChartBusinessLabelData);

                var div = document.createElement('div');
                {
                  var span = document.createElement('span');
                  if (processLabel != "") {
                    span.innerHTML = "【" + processLabel + "】" + "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;";
                  }
                  if (CHANGEPROHIBITIONFLAG == "0") {
                    var aEdit = document.createElement('a');
                    aEdit.setAttribute("href", "JavaScript:showModal('EdithWindow', '" + String(j) + "','" + processLabel + "','" + "Process" + "','" + "')");
                    aEdit.setAttribute("id", chrP + "_process");
                    aEdit.setAttribute("name", chrP + "_process");
                    var img = document.createElement('img');
                    img.setAttribute("id", chrP + "_processImg");
                    img.setAttribute("style", "margin-top: -2px; width: 20px;");
                    img.setAttribute("src", "/static/img/flowChartImg/EditData.svg");

                    aEdit.appendChild(img)
                    div.appendChild(aEdit)
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

        table.append(trp);
      }

      // ------------------------------
      // ------------------------------
      // 行
      // ------------------------------
      var rowsNumMax = 1;
      for (var k = 1; k <= rowNum; k++) {
        var tr = document.createElement('tr');
        tr.setAttribute("style", "height: 60px;");
        tr.classList.add("l-border");

        var td = document.createElement('td');
        // 行
        {
          td.setAttribute("style", "text-align: center; width: 25px; background-color: #f08080");
          td.setAttribute("id", k + "_RowPlusNum");
          var p = document.createElement('p');
          p.setAttribute("style", "margin-top: 5px;");
          p.innerHTML = k;
          td.appendChild(p);
        }

        // Plus（行）
        var p = document.createElement('p');
        if (CHANGEPROHIBITIONFLAG == "0") {
          {
            var aplus = document.createElement('a');
            aplus.setAttribute("href", "");
            aplus.setAttribute("id", k + "_rowPlus");
            aplus.setAttribute("name", k + "_rowPlus");
            var img = document.createElement('img');
            img.setAttribute("id", k + "_rowPlusImg");
            img.setAttribute("style", "margin-top: 0px; width: 18px;");
            img.setAttribute("src", "/static/img/flowChartImg/Plus.svg");
            // 要素にクリックイベントを追加する
            aplus.onclick = (function (num) {
              return function () {
                PlusMinusRowsAction(this, num, "plus");
              }
            })(k);
          }
          aplus.appendChild(img);
          td.appendChild(aplus);
        }
        td.append(p);

        // Minus（行）
        if (CHANGEPROHIBITIONFLAG == "0") {
          {
            var aMinus = document.createElement('a');
            aMinus.setAttribute("href", "");
            aMinus.setAttribute("id", k + "_rowMinus");
            aMinus.setAttribute("name", k + "_rowMinus");
            var img = document.createElement('img');
            img.setAttribute("id", k + "_rowMinusImg");
            img.setAttribute("style", "margin-top: -12px; width: 18px; margin-bottom: 3px");
            img.setAttribute("src", "/static/img/flowChartImg/Minus.svg");
            // 要素にクリックイベントを追加する
            aMinus.onclick = (function (num) {
              return function () {
                PlusMinusRowsAction(this, num, "Minus");
              }
            })(k);
          }
          aMinus.appendChild(img);
          td.appendChild(aMinus);
        }
        tr.appendChild(td);

        // --------------------------------
        // （縦）役割区分 
        // --------------------------------
        {
          var LabelData = getProcessLabelData_EndColum(k, "rows", ChartBusinessLabelData);
          var rowspanNum = 1;
          var departmentLabel = "";
          var labelColor = "#FFFFCC";
          if (LabelData != null) {
            rowspanNum = Number(LabelData.EndIdx) - Number(LabelData.StartIdx) + 1;
            departmentLabel = LabelData.LabelText;
            labelColor = LabelData.LabelColor;
          }

          if (rowsNumMax <= Number(rowNum)) {
            if (rowsNumMax <= k) {

              var td = document.createElement('td');
              td.classList.add("t-border");
              td.setAttribute("rowspan", String(rowspanNum));
              td.setAttribute("style", "text-align: center; width: 25px; background-color: " + labelColor + ";");
              {

                var div = document.createElement('div');
                {
                  var span = document.createElement('span');
                  span.setAttribute("style", "margin-top: 0px; writing-mode: vertical-rl; text-orientation: upright; margin-left: 0px;");
                  if (departmentLabel != "") {
                    span.innerHTML = "【" + departmentLabel + "】";
                  }
                  if (CHANGEPROHIBITIONFLAG == "0") {
                    var aEdit = document.createElement('a');
                    aEdit.setAttribute("style", "margin-top: 0px; width: 18px; margin-left: 0px;");
                    aEdit.setAttribute("href", "JavaScript:showModal('EdithWindow', '" + String(k) + "','" + departmentLabel + "','" + "Department" + "','" + "')");
                    aEdit.setAttribute("id", k + "_process");
                    aEdit.setAttribute("name", k + "_process");
                    var img = document.createElement('img');
                    img.setAttribute("id", chr + "_processImg");
                    img.setAttribute("style", "margin-top: 20px; margin-left: -8px; width: 20px; ");
                    img.setAttribute("src", "/static/img/flowChartImg/EditData.svg");

                    aEdit.appendChild(img)
                    span.appendChild(aEdit)
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

        // 枠の中のデータ
        for (var innerloop = 1; innerloop <= colNum; innerloop++) {
          var tdi = document.createElement('td');
          tdi.classList.add("l-border");

          {
            var select = document.createElement('select');
            if (CHANGEPROHIBITIONFLAG == "0") {
              {
                // 要素にクリックイベントを追加する
                select.onchange = (function (location) {
                  return function () {
                    saveChartImg(this, location);
                  }
                })(String.fromCharCode(64 + innerloop) + "_" + k);
              }
            }

            select.setAttribute("id", String.fromCharCode(64 + innerloop) + "_" + k + "_select");
            select.setAttribute("name", String.fromCharCode(64 + innerloop) + "_" + k + "_name");
            select.setAttribute("data-minimum-results-for-search", "Infinity");
            select.setAttribute('style', "margin-top: -60px;");
            select.setAttribute('size', 5);

            var checkName = checkImgName(String.fromCharCode(64 + innerloop) + "_" + k, design);
            if (checkName != "") {
              imgSelectName = checkName;
            }

            for (var a = 0; a < ImgDataList.length; a++) {
              //console.log("name = " + ImgDataList[a].name);
              //console.log("file = " + ImgDataList[a].file);

              var option = document.createElement("option");
              option.value = ImgDataList[a].name;
              if (checkName == ImgDataList[a].name) {
                option.setAttribute('data-img_src', "/static/img/" + ImgDataList[a].file);
                option.setAttribute('selected', true);
              }
              else {
                option.setAttribute('data-img_src', "/static/img/" + ImgDataList[a].file);
              }
              select.appendChild(option);
            }

            // 変更禁止
            if (CHANGEPROHIBITIONFLAG == "1") {
              select.disabled = true;
            }

            tdi.appendChild(select);

            // 見出し
            var checkText = checkMidashiText(String.fromCharCode(64 + innerloop) + "_" + k, design);
            // コメントコードを記憶する
            //var checkCommentCode = checkCommnetCode(String.fromCharCode(64 + innerloop) + "_" + k, design);
            var input = document.createElement('input');
            input.setAttribute('id', String.fromCharCode(64 + innerloop) + "_" + k + "_midashi");
            input.setAttribute('type', "text");
            input.setAttribute('style', "text-align:center; height: 25px;");
            input.setAttribute('value', checkText);
            if (CHANGEPROHIBITIONFLAG == "1") {
              input.readOnly = true;
            }

            if (CHANGEPROHIBITIONFLAG == "0") {
              {
                input.onchange = (function (location) {
                  return function () {
                    saveChartComment(this, location);
                  }
                })(String.fromCharCode(64 + innerloop) + "_" + k);
              }
            }

            tdi.appendChild(input);
            tr.append(tdi);
          }
          // テーブルへ
          table.append(tr);
        }

      }

      // 画面上部へデータを設定する
      {
        var wknum = G_WORKTIME_TOTAL / 60.0;
        document.getElementById("TotalWorkingTime").value = wknum.toFixed(2);
      }

      //自動保存制御
      if (CHANGEPROHIBITIONFLAG == "0") {
        if (AutoSaveControlflag == "0") {
          document.getElementById("AutoSaveModeCheck").checked = false;
          AutoSaveControl();
        }
        else {
          document.getElementById("AutoSaveModeCheck").checked = true;
          AutoSaveControl();
        }
      }
      else {
        document.getElementById("AutoSaveModeCheck").disabled = true;
      }

      // -------------------------------------------
      // 画像選択に必要！！
      // -------------------------------------------
      function custom_template(obj) {
        var data = $(obj.element).data();
        var text = $(obj.element).val();

        if (text == "") {
          template = $("<div style='margin-top:3px;'></div>");
          return template;
        }
        else {
          if (data && data['img_src']) {
            img_src = data['img_src'];
            template = $("<div><img src=\"" + img_src + "\" style=\"width:85%; margin-top:3px;\"/></div>");
            return template;
          }
        }
      }

      var options = {
        'templateSelection': custom_template,
        'templateResult': custom_template,
      }

      for (var r = 1; r <= rowNum; r++) {
        for (var c = 1; c <= colNum; c++) {
          var char_val = String.fromCharCode(64 + c) + '_' + r + "_select";
          $('#' + char_val).select2(options);
        }
      }

      // $('.select2-container--default .select2-selection--single').css({ 'height': '145px' });
      // $('.select2-container--default .select2-selection--single').css({ 'width': '220px' });
      // $('.select2-container--default .select2-selection--single').css({ 'margin-top': '10px' });

    }

  });

}

// ----------------------------------------------
// 名称を保存する
// ----------------------------------------------
function SaveToProcessChartDataTBL() {

  // 名称
  {
    var processProcedureName = document.getElementById("process_ProcedureName").value
    if (processProcedureName == "") {
      alert("資料名が空白です。入力してください。");
      return;
    }
  }

  console.log(processProcedureName);

  var resultStatus = "";

  // 名称を保存する
  $.ajax({
    url: '/saveProcessChartImagesData/',
    type: 'POST',
    data: {
      updateUser: email,
      processProcedureID: ProcessProcedureID,
      processProcedureName: processProcedureName,
      chartDesignCode: ChartDesignCode,
    },
    async: false,
    dataType: 'json',
    success: function (response) {
      resultStatus = response.status;
      if (response.status == "OK") {
      }
    }
  });
}

// ----------------------------------------------
// 画面枠数を保存する
// ----------------------------------------------
function ChangeToProcessChartColumnRow() {

  // 画面枠
  {
    // カラム数
    var columnNumber = document.getElementById("DiagramColumns").value;
    if (Number(columnNumber) < 5 || Number(columnNumber) > 26) {
      alert("カラム数は、5～26 の範囲で指定してください");
      // 元にもどす
      document.getElementById("DiagramColumns").value = keepColumnNum;
      return;
    }

    // 行数
    var rowsNumber = document.getElementById("DiagramRows").value;
    if (Number(rowsNumber) < 5 || Number(rowsNumber) > 99) {
      alert("行数は、5～99 の範囲で指定してください");
      // 元にもどす
      var rowsNumber = document.getElementById("DiagramRows").value = keepRowsNum;
      return;
    }
  }

  console.log(columnNumber);
  console.log(rowsNumber);

  var resultStatus = "";

  // 画面枠を保存する
  $.ajax({
    url: '/changeToProcessChartColumnRow/',
    type: 'POST',
    data: {
      processProcedureID: ProcessProcedureID,
      chartDesignCode: ChartDesignCode,
      columnNumber: columnNumber,
      rowsNumber: rowsNumber
    },
    async: false,
    dataType: 'json',
    success: function (response) {
      //alert(response);
      resultStatus = response.status;
      if (response.status == "OK") {
        // 自画面を再表示する
        window.location.reload();
      }
    }
  })
}


// ----------------------------------------------
// カラムを指定位置に追加／削除する
// ----------------------------------------------
function PlusMinusColumnAction(el, num, updateType) {

  var ids = el.getAttribute("id");
  console.log(ids);
  console.log(num);

  // 位置
  var wkData = ids.split("_");
  var locationInfo = wkData[0] + "_1";

  // パラメータ
  var chartDesignCode = $('#chartDesignCode').val();

  $.ajax({
    url: '/updateProcessChartColumn/',
    type: 'POST',
    data: {
      chartDesignCode: chartDesignCode,
      locationInfo: locationInfo,
      updateType: updateType
    },
    async: false,
    dataType: 'json',
    success: function (response) {
      if (response[0].status == "OK") {
        //alert("Response Status !!" + response[0].status);
        window.location.reload();
      }
    }
  });
}

// ----------------------------------------------
// 行を指定位置に追加する
// ----------------------------------------------
function PlusMinusRowsAction(el, num, updateType) {

  var ids = el.getAttribute("id");
  console.log(ids);
  console.log(num);

  // 位置
  var locationInfo = "A_" + num;

  // パラメータ
  var chartDesignCode = $('#chartDesignCode').val();

  $.ajax({
    url: '/updateProcessChartRow/',
    type: 'POST',
    data: {
      chartDesignCode: chartDesignCode,
      locationInfo: locationInfo,
      updateType: updateType
    },
    async: false,
    dataType: 'json',
    success: function (response) {
      if (response[0].status == "OK") {
        //alert("Response Status !!" + response[0].status);
        window.location.reload();
      }
    }
  });
}

// ----------------------------------------------
// 画像を変更した場合に選択画像を保存する
// ----------------------------------------------
function saveChartImg(el, location) {
  if (AutoSaveControlflag == "0") {
    // 自動更新停止
    return;
  }
  var ids = el.getAttribute("id");
  console.log(ids);
  console.log(location);

  // デザインコード
  var chartDesignCode = $('#chartDesignCode').val();

  // 画像名
  var imgFileName = document.getElementById(ids).value;

  // 見出し
  var midashi = document.getElementById(location + "_midashi");
  midashiText = midashi.value;
  if (imgFileName == "Space_001") {
    midashi.value = "";
    midashiText = "";
  }

  $.ajax({
    url: '/updateChartImg/',
    type: 'POST',
    data: {
      chartDesignCode: chartDesignCode,
      imgFileName: imgFileName,
      locationInfo: location,
      midashi: midashiText
    },
    async: false,
    dataType: 'json',
    success: function (response) {
      if (response.status == "OK") {
      }
    }
  });
}

// ----------------------------------------------
// テキストを変更した時に保存する
// ----------------------------------------------
function saveChartComment(el, location) {
  if (AutoSaveControlflag == "0") {
    // 自動更新停止
    return;
  }

  var ids = el.getAttribute("id");
  console.log(ids);
  console.log(location);

  // デザインコード
  var chartDesignCode = $('#chartDesignCode').val();

  // 見出し
  var midashi = document.getElementById(location + "_midashi");
  var midashiText = midashi.value;

  // 画像名
  var imgFileName = document.getElementById(location + "_select").value;
  if (imgFileName == "Space_001") {
    alert("空白画像を選択時は、見出しを入力できません。他の画像を選択してください。")
    midashi.value = "";
    midashiText = "";
  }

  $.ajax({
    url: '/updateChartComment/',
    type: 'POST',
    data: {
      chartDesignCode: chartDesignCode,
      locationInfo: location,
      midashi: midashiText
    },
    dataType: 'json',
    async: false,
    success: function (response) {
      if (response.status == "OK") {
      }
    }
  });
}

// ----------------------------------------------
// 印刷
// ----------------------------------------------
function chartPrint() {
  // 名称変更
  var updateChartName = document.getElementById('updateChartName');
  updateChartName.style.visibility = "hidden";
  // 詳細画面表示
  var dispProcessDiagramDetail = document.getElementById('dispProcessDiagramDetail');
  dispProcessDiagramDetail.style.visibility = "hidden";
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

  // 枠変更
  updateWakuSize
  var updateWakuSize = document.getElementById('updateWakuSize');
  updateWakuSize.style.visibility = "hidden";

  // 自動保存
  var autoSaveModeCheck = document.getElementById('AutoSaveModeCheck');
  var autoSaveModeCheckText = document.getElementById('AutoSaveModeCheckText');
  autoSaveModeCheck.style.visibility = "hidden";
  autoSaveModeCheckText.style.visibility = "hidden";

  // 手動保存
  var saveButton = document.getElementById('SaveButton');
  saveButton.style.visibility = "hidden";

  // 印刷
  window.print();

  // 名称変更
  updateChartName.style.visibility = "visible";
  dispProcessDiagramDetail.style.visibility = "visible";
  btn_print.style.visibility = "visible";
  btn_Back.style.visibility = "visible";

  permissionFlag.style.visibility = "visible";
  permissionFlagText.style.visibility = "visible";

  changeProhibitionFlag.style.visibility = "visible";
  changeProhibitionFlagText.style.visibility = "visible";

  updateWakuSize.style.visibility = "visible";

  autoSaveModeCheck.style.visibility = "visible";
  autoSaveModeCheckText.style.visibility = "visible";

  saveButton.style.visibility = "visible";

}