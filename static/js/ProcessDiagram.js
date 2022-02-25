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

// ##################################################################################################
// ##################################################################################################
/* functin以外の処理を記述 */

// var sessionOrg1 = sessionStorage.getItem("org1");
// var sessionOrg2 = sessionStorage.getItem("org2");

var sessionOrg1 = '50';
var sessionOrg2 = '05';
var sessionEmail = "fujii.kyoichi.za@nesic.com";


var getUrlParameter = function getUrlParameter(sParam) {
  var sPageURL = window.location.search.substring(1),
    sURLVariables = sPageURL.split('&'),
    sParameterName,
    i;

  for (i = 0; i < sURLVariables.length; i++) {
    sParameterName = sURLVariables[i].split('=');

    if (sParameterName[0] === sParam) {
      return typeof sParameterName[1] === undefined ? true : decodeURIComponent(sParameterName[1]);
    }
  }
  return false;
};

var classification = getUrlParameter("classification");
console.log("classification = " + classification)
var workitem = getUrlParameter("workitem");
console.log("workitem = " + workitem)
var workitem_id = workitem.split("/")
workitem_id = workitem_id[0]
var procedure_name = getUrlParameter("procedure_name");
console.log("workitem_name = " + procedure_name)
$("#process_ProcedureName").html(procedure_name)

var process_procedureID = getUrlParameter("ProcessProcedureID");
console.log("process_procedureID = " + process_procedureID);



function getProcessChartData() {
  var process_ProcedureName = document.getElementById('process_ProcedureName').innerText;
  console.log("process_ProcedureName = " + process_ProcedureName);

  //getChartDesignCode
  $.ajax({
    url: '/getchartDesignCode/',
    async: false,
    type: 'POST',
    data: {
      process_procedureID: process_procedureID,
      process_ProcedureName: process_ProcedureName
    },
    dataType: 'json',
    success: function (response) {

      if (response[0][0] == null) {

        //if chartDesignCode is null
        var colNum = response[0][1];
        var rowNum = response[0][2];

        console.log("col num = " + colNum);
        console.log("row num = " + rowNum);

        var div = document.getElementById("processChart_container");
        var table = document.createElement('table');
        table.setAttribute('id', 'data_table');
        table.setAttribute("border", "1")
        div.appendChild(table);
        var header = "<tr>";

        for (var j = 0; j < colNum; j++) {
          var chr = String.fromCharCode(64 + j)
          console.log("Char = " + chr)
          if (j == 0) {
            header += "<th class='text-center' id='full_name'>No.</th>";
          }
          else {
            header += "<th style='text-align: center;'>" +
              "<div><span style='margin-left: 70px;'>" + String.fromCharCode(64 + j) + "</span>" +
              "<a href='' id='A_Plus' name='A_Plus'><img style='margin-left: 60px;' src='/static/img/png/Plus.png' width='18px' alt='' name='A'></a>" +
              "<a href='' id='A_Minus' name='A_Minus'><img src='/static/img/png/Minus.png' width='18px' alt='' name='A'></a>" +
              "</div></th>"

          }
        }
        header += "</tr>";
        $('#data_table').append(header);

        for (var k = 1; k <= rowNum; k++) {
          var row = "<tr><td style='text-align: center;'><span>" + k + "</span>" +
            "<a href='' id='1_Plus' name='1_Plus'><img style='margin-top: 10px;' src='/static/img/png/Plus.png' width='18px' alt='' name='Colum1'></a>" +
            "<a href='' id='1_Minus' name='1_Minus'><img src='/static/img/png/Minus.png' width='18px' alt='' name='Colum1'></a>" +
            "</td>"
          for (var innerloop = 1; innerloop <= colNum - 1; innerloop++) {
            row += "<td><select id='" + String.fromCharCode(64 + innerloop) + "_" + k + "' data-minimum-results-for-search='Infinity'>" +
              "</select><input type='text' name=''></td>"
          }
          row += "</tr>"
          $('#data_table').append(row)
        }
        var design = 0;
        getProcessChartImageData(rowNum, colNum, design);
      }

      else {
        $('#chartDesignCode').val(response[0][0]);
        // getProcessChartDrawingData
        var chartDesignCode = $('#chartDesignCode').val();
        console.log("chart Design code = " + chartDesignCode);
        getProcessChartDrawingData(chartDesignCode);

      }

    }
  });
}


// getProcessChartDrawingData
function getProcessChartDrawingData(chartDesignCode) {
  $.ajax({
    url: '/getProcessChartDrawingData/',
    type: 'POST',
    data: {
      chartDesignCode: chartDesignCode
    },
    dataType: 'json',
    success: function (response) {
      console.log("Response!!" + response[0].Data.length);
      console.log("Response Column!!" + response[0].Data[0].ColumnNumber);

      for (var i = 0; i < response[0].Data.length; i++) {
        if (response[0].Data[i].ProcessProcedureID == process_procedureID) {
          var colNum = response[0].Data[0].ColumnNumber;
          var rowNum = response[0].Data[0].RowsNumber;
          var design = response[0].design;
          console.log("Design = " + design);

          var div = document.getElementById("processChart_container");
          var table = document.createElement('table');
          table.setAttribute('id', 'data_table');
          table.setAttribute("border", "1")
          div.appendChild(table);
          var header = "<tr>";

          for (var j = 0; j < colNum; j++) {
            var chr = String.fromCharCode(64 + j)
            console.log("Char = " + chr)
            if (j == 0) {
              header += "<th class='text-center' id='full_name'>No.</th>";
            }
            else {
              header += "<th style='text-align: center;'>" +
                "<div><span style='margin-left: 70px;'>" + String.fromCharCode(64 + j) + "</span>" +
                "<a href='' id='A_Plus' name='A_Plus'><img style='margin-left: 60px;' src='/static/img/png/Plus.png' width='18px' alt='' name='A'></a>" +
                "<a href='' id='A_Minus' name='A_Minus'><img src='/static/img/png/Minus.png' width='18px' alt='' name='A'></a>" +
                "</div></th>"

            }
          }
          header += "</tr>";
          $('#data_table').append(header);

          for (var k = 1; k <= rowNum; k++) {
            var row = "<tr><td style='text-align: center;'><span>" + k + "</span>" +
              "<a href='' id='1_Plus' name='1_Plus'><img style='margin-top: 10px;' src='/static/img/png/Plus.png' width='18px' alt='' name='Colum1'></a>" +
              "<a href='' id='1_Minus' name='1_Minus'><img src='/static/img/png/Minus.png' width='18px' alt='' name='Colum1'></a>" +
              "</td>"
            for (var innerloop = 1; innerloop <= colNum - 1; innerloop++) {
              row += "<td><select id='" + String.fromCharCode(64 + innerloop) + "_" + k + "' data-minimum-results-for-search='Infinity'>" +
                "</select><input type='text' name=''></td>"
            }
            row += "</tr>"
            $('#data_table').append(row)
          }

        }
      }

      getProcessChartImageData(rowNum, colNum, design);

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
      console.log("image list length = " + data_array)
      var data_array_key = Object.keys(response[0].Data)
      console.log("image list key = " + data_array_key)

      for (var r = 1; r <= rowNum; r++) {
        for (var c = 1; c <= colNum - 1; c++) {
          var char_val = String.fromCharCode(64 + c) + '_' + r;
          $("#" + char_val).append("<option value=''></option>");

          if (design.length > 0) {
            console.log("Design if");
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
            console.log("Design else");
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


