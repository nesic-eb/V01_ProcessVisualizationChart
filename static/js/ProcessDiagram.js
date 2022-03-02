// =============================================================================
// 画面名：プロセスチャート画面
// 
// -----------------------------------------------------------------------------
// （ファイル整形）Visual Studio Code : Shift + Alt + f 
// =============================================================================


// ##################################################################################################
// ##################################################################################################
/* セッション情報取得 */

console.log("■ ---------------------------------------------");
console.log("■ セッション情報 -- ProcessDiagram.js --------");


var email = sessionStorage.getItem("email")
var org1 = sessionStorage.getItem("org1")
var org2 = sessionStorage.getItem("org2")
var ProcessProcedureID = sessionStorage.getItem("ProcessProcedureID")
var ProcessProcedureName = sessionStorage.getItem("ProcessProcedureName")
var ChartDesignCode = sessionStorage.getItem("ChartDesignCode")


console.log("Email = " + email);
console.log("Org1 = " + org1);
console.log("Org2 = " + org2);
console.log("Process Procedure ID = " + ProcessProcedureID);
console.log("Process Procedure Name = " + ProcessProcedureName);
console.log("Chart Design Code = " + ChartDesignCode);

// ##################################################################################################
// ##################################################################################################
/* functin以外の処理を記述 */

// 手順書名 
$("#process_ProcedureName").html(ProcessProcedureName)

// チャートデザインコード
$('#chartDesignCode').val(ChartDesignCode);




// ##################################################################################################
// ##################################################################################################
/* function の処理を記述 */

// ----------------------------------------------
// 画面表示時に枠情報などを作成する
// (MAIN)
// ----------------------------------------------
function onLoadProcessChartData() {

  var processProcedureID = sessionStorage.getItem("ProcessProcedureID");
  var chartDesignCode = sessionStorage.getItem("ChartDesignCode");

  // イメージ画像を取得する
  var ImgDataList;

  // 画像情報を取得する
  $.ajax({
    url: '/getProcessChartImagesData/',
    type: 'POST',
    data: {
      ChartType: "FlowChart"
    },
    dataType: 'json',
    success: function (response) {
      //alert(response);
      ImgDataList = response[0].Data;
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
    success: function (response) {
      console.log("Response!!" + response[0].Data.length);

      //if (response[0].Data.length > 0) {
      var colNum = response[0].Data[0].ColumnNumber;
      var rowNum = response[0].Data[0].RowsNumber;
      var design = response[0].design;

      console.log("Design = " + design);

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

      // 枠（カラム）
      for (var j = 0; j <= colNum; j++) {
        var chr = String.fromCharCode(64 + j)

        var th = document.createElement('th');
        th.classList.add("t-border");

        if (j == 0) {
          var div = document.createElement('div');
          // No.
          th.setAttribute("style", "text-align: center; width: 35px; height: 35px;");
          th.setAttribute("id", "full_name");
          var span = document.createElement('span');
          span.innerHTML = "No.";
          div.appendChild(span)
          th.appendChild(div);
        }
        else {
          var div = document.createElement('div');

          // A ～ Z
          th.setAttribute("style", "text-align: center; width: 200px;");
          th.setAttribute("id", chr + "_colPlus");
          var span = document.createElement('span');
          span.innerHTML = chr + "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"
          div.appendChild(span);

          // Plus
          {
            var aplus = document.createElement('a');
            aplus.setAttribute("href", "");
            aplus.setAttribute("id", chr + "_rowPlus");
            aplus.setAttribute("name", chr + "_rowPlus");
            aplus.setAttribute("onclick", "PlusColumnAction(this)'>");
            var img = document.createElement('img');
            img.setAttribute("style", "margin-top: 0px; width: 18px;");
            img.setAttribute("src", "/static/img/flowChartImg/Plus.svg");
          }
          aplus.appendChild(img);
          div.appendChild(aplus);

          // Minus
          {
            var aMinus = document.createElement('a');
            aMinus.setAttribute("href", "");
            aMinus.setAttribute("id", chr + "_rowMinus");
            aMinus.setAttribute("name", chr + "_rowMinus");
            aMinus.setAttribute("onclick", "MinusColumnAction(this)'>");
            var img = document.createElement('img');
            img.setAttribute("style", "margin-top: 0px; width: 18px;");
            img.setAttribute("src", "/static/img/flowChartImg/Minus.svg");
          }
          aMinus.appendChild(img);
          div.appendChild(aMinus);

          th.appendChild(div);
        }

        trheader.append(th);
      }
      // テーブルへ
      table.append(trheader);

      // 行
      for (var k = 1; k <= rowNum; k++) {
        var tr = document.createElement('tr');
        tr.setAttribute("style", "height: 60px;");
        tr.classList.add("l-border");

        var td = document.createElement('td');

        {
          td.setAttribute("style", "text-align: center;");
          td.setAttribute("id", chr + "_RowPlus");
          var p = document.createElement('p');
          p.setAttribute("style", "margin-top: 5px;");
          p.innerHTML = k;
          td.appendChild(p);
        }

        var p = document.createElement('p');

        // Plus
        {
          var aplus = document.createElement('a');
          aplus.setAttribute("href", "");
          aplus.setAttribute("id", chr + "_rowPlus");
          aplus.setAttribute("name", chr + "_rowPlus");
          aplus.setAttribute("onclick", "PlusRowAction(this)'>");
          var img = document.createElement('img');
          img.setAttribute("style", "margin-top: 0px; width: 18px;");
          img.setAttribute("src", "/static/img/flowChartImg/Plus.svg");
        }
        aplus.appendChild(img);
        td.appendChild(aplus);
        td.append(p);

        // Minus
        {
          var aMinus = document.createElement('a');
          aMinus.setAttribute("href", "");
          aMinus.setAttribute("id", chr + "_rowMinus");
          aMinus.setAttribute("name", chr + "_rowMinus");
          aMinus.setAttribute("onclick", "PlusRowAction(this)'>");
          var img = document.createElement('img');
          img.setAttribute("style", "margin-top: -12px; width: 18px; margin-bottom: 3px");
          img.setAttribute("src", "/static/img/flowChartImg/Minus.svg");
        }
        aMinus.appendChild(img);
        td.appendChild(aMinus);

        tr.append(td);

        // 枠の中のデータ
        for (var innerloop = 1; innerloop <= colNum; innerloop++) {
          var tdi = document.createElement('td');
          tdi.classList.add("l-border");

          {
            var select = document.createElement('select');

            select.setAttribute("id", String.fromCharCode(64 + innerloop) + "_" + k);
            select.setAttribute("data-minimum-results-for-search", "Infinity");
            select.setAttribute('style', "margin-top: -60px;");

            for (var a = 0; a < ImgDataList.length; a++) {
              console.log("name = " + ImgDataList[a].name);
              console.log("file = " + ImgDataList[a].file);

              var option = document.createElement("option");
              option.value = ImgDataList[a].name;
              option.setAttribute('data-img_src', "/static/img/" + ImgDataList[a].file);
              select.appendChild(option);
            }
          }
          tdi.appendChild(select);


          //tdi.appendChild(p);

          var input = document.createElement('input');
          input.setAttribute('type', "text");
          tdi.appendChild(input);

          tr.append(tdi);
          // row += "<td><select id='" + String.fromCharCode(64 + innerloop) + "_" + k + "' =''>" +
          //   "</select><input type='text' name=''></td>"
        }

        // 画像情報を取得する
        //  getProcessChartImageData(rowNum, colNum, design);

        // テーブルへ
        table.append(tr);
      }

      //select.appendChild(input);
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
          var char_val = String.fromCharCode(64 + c) + '_' + r;
          $('#' + char_val).select2(options);
        }
      }

      // $('.select2-container--default .select2-selection--single').css({ 'height': '45px' });
      // $('.select2-container--default .select2-selection--single').css({ 'width': '220px' });
      // $('.select2-container--default .select2-selection--single').css({ 'margin-top': '10px' });


      // else {
      //   //chart Designcode is null
      //   $.ajax({
      //     url: '/getchartDesignCode/',
      //     async: false,
      //     type: 'POST',
      //     data: {
      //       process_procedureID: ProcessProcedureID,
      //       process_ProcedureName: process_ProcedureName
      //     },
      //     dataType: 'json',
      //     success: function (response) {

      //       //if chartDesignCode is null
      //       var colNum = response[0][1];
      //       var rowNum = response[0][2];

      //       console.log("col num = " + colNum);
      //       console.log("row num = " + rowNum);

      //       var div = document.getElementById("processChart_container");
      //       var table = document.createElement('table');
      //       table.setAttribute('id', 'data_table');
      //       table.setAttribute("border", "1")
      //       div.appendChild(table);
      //       var header = "<tr>";

      //       for (var j = 0; j < colNum; j++) {
      //         var chr = String.fromCharCode(64 + j)
      //         console.log("Char = " + chr)
      //         if (j == 0) {
      //           header += "<th class='text-center' id='full_name'>No.</th>";
      //         }
      //         else {

      //           header += "<th style='text-align: center;'>" +
      //             "<div><span style='margin-left: 70px;'>" + String.fromCharCode(64 + j) + "</span>" +
      //             "<a href='' id='" + chr + "_colPlus' name='" + chr + "_colPlus' onclick='PlusColumnAction(this)'><img style='margin-left: 60px;' src='/static/img/png/Plus.png' width='18px' alt='' name='A'></a>" +
      //             "<a href='' id='" + chr + "_colMinus' name='" + chr + "_colMinus' onclick='MinusColumnAction(this)'><img src='/static/img/png/Minus.png' width='18px' alt='' name='A'></a>" +
      //             "</div></th>"

      //         }
      //       }
      //       header += "</tr>";
      //       $('#data_table').append(header);

      //       for (var k = 1; k <= rowNum; k++) {
      //         var row = "<tr><td style='text-align: center;'><span>" + k + "</span>" +
      //           "<a href='' id='" + chr + "_rowPlus' name='" + chr + "_rowPlus' onclick='PlusRowAction(this)'><img style='margin-top: 10px;' src='/static/img/png/Plus.png' width='18px' alt='' name='Colum1'></a>" +
      //           "<a href='' id='" + chr + "_rowMinus' name='" + chr + "_rowMinus' onclick='MinusRowAction(this)'><img src='/static/img/png/Minus.png' width='18px' alt='' name='Colum1'></a>" +
      //           "</td>"
      //         for (var innerloop = 1; innerloop <= colNum - 1; innerloop++) {
      //           row += "<td><select id='" + String.fromCharCode(64 + innerloop) + "_" + k + "' data-minimum-results-for-search='Infinity'>" +
      //             "</select><input type='text' name=''></td>"
      //         }
      //         row += "</tr>"
      //         $('#data_table').append(row)
      //       }

      //       var design = 0;

      //       getProcessChartImageData(rowNum, colNum, design);

      //     }

      //  });
      //}
    }

  });

}


//getProcessChartImagesData
function getProcessChartImageData(rowNum, colNum, design) {

  console.log("in get process chart image data = " + design);

  // getProcessChartImagesData
  $.ajax({
    url: '/getProcessChartImagesData/',
    type: 'POST',
    data: {
      ChartType: "FlowChart"
    },
    dataType: 'json',
    success: function (response) {
      //alert(response);
      var data_array = Object.values(response[0].Data)
      console.log("Data array = " + data_array);
      var data_array_key = Object.keys(response[0].Data)

      for (var r = 1; r <= rowNum; r++) {
        for (var c = 1; c <= colNum - 1; c++) {

          var char_val = String.fromCharCode(64 + c) + '_' + r;
          $("#" + char_val).append("<option value=''></option>");

          if (design.length > 0) {
            for (var a = 0; a < design.length; a++) {

              var Block = design[a].Block;
              var LocationInfo = Block.LocationInfo;
              var location_id = document.getElementById(LocationInfo);
              var ImageName = Block.ImageName;

              if (char_val == LocationInfo) {
                console.log("char val = " + char_val);
                console.log("Location info = " + LocationInfo);
                $("#" + char_val).append("<option value='" + char_val + "' data-img_src='/static/img/flowChartImg/" + ImageName + ".png' selected></option>");
              }
              else {
                for (var i = 0; i < data_array.length; i++) {
                  $("#" + char_val).append("<option value='" + char_val + "' data-img_src='/static/img/" + data_array[i] + "'></option>");

                }
              }
            }
          }
          else {
            for (var i = 0; i < data_array.length; i++) {
              $("#" + char_val).append("<option value='" + char_val + "' data-img_src='/static/img/" + data_array[i] + "'></option>");

            }
          }
        }
      }





      function custom_template(obj) {
        var data = $(obj.element).data();
        var text = $(obj.element).val();

        if (text == "") {
          template = $("<div style='width:100px;height:30px;margin-top:3px;'></div>");
          return template;
        }
        else {
          if (data && data['img_src']) {
            img_src = data['img_src'];
            template = $("<div><img src=\"" + img_src + "\" style=\"width:100px;height:40px;margin-left:36px;margin-top:3px;\"/></div>");
            return template;
          }

        }

      }

      var options = {
        'templateSelection': custom_template,
        'templateResult': custom_template,
      }

      for (var r = 1; r <= rowNum; r++) {
        for (var c = 1; c <= colNum - 1; c++) {
          var char_val = String.fromCharCode(64 + c) + '_' + r;
          $('#' + char_val).select2(options);

        }
      }

      $('.select2-container--default .select2-selection--single').css({ 'height': '45px' });
      $('.select2-container--default .select2-selection--single').css({ 'width': '220px' });
      $('.select2-container--default .select2-selection--single').css({ 'margin-top': '10px' });

    }

  });

}























function PlusColumnAction(el) {

  var ids = el.getAttribute("id");
  alert(ids);
  console.log(ids);

  var chartDesignCode = $('#chartDesignCode').val();
  var updateType = "plus";
  var LocationInfo = "D_1"

  $.ajax({
    url: '/getProcessChartColumnUpdate/',
    type: 'POST',
    data: {
      chartDesignCode: chartDesignCode,
      LocationInfo: LocationInfo,
      updateType: updateType
    },
    dataType: 'json',
    success: function (response) {
      if (response[0].statsu == "OK") {
        alert("Response Status !!" + response[0].statsu);
        window.location.reload();
      }

      // const json_string = JSON.stringify(response, null, 2);

      // console.log(json_string); // 確認用

      // document.getElementById("textarea").value = json_string;
    }

  });

}


function MinusColumnAction(el) {

  var ids = el.getAttribute("id");
  alert(ids);
  console.log(ids);

  var chartDesignCode = $('#chartDesignCode').val();
  var updateType = "minus";
  var LocationInfo = "D_1"

  $.ajax({
    url: '/getProcessChartColumnUpdate/',
    type: 'POST',
    data: {
      chartDesignCode: chartDesignCode,
      LocationInfo: LocationInfo,
      updateType: updateType
    },
    dataType: 'json',
    success: function (response) {
      if (response[0].statsu == "OK") {
        alert("Response Status !!" + response[0].statsu);
        window.location.reload();
      }

      // const json_string = JSON.stringify(response, null, 2);

      // console.log(json_string); // 確認用

      // document.getElementById("textarea").value = json_string;
    }

  });

}





