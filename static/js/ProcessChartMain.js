// =============================================================================
// 画面名：プロセス可視化チャート：メイン画面
// 
// -----------------------------------------------------------------------------
// （ファイル整形）Visual Studio Code : Shift + Alt + f 
// =============================================================================


// ##################################################################################################
// ##################################################################################################
/* セッション情報取得 */
console.log("■ ---------------------------------------------");
console.log("■ セッション情報 -- ProcessCheck.js --------");

var user_emal = sessionStorage.getItem("email");
var org1 = sessionStorage.getItem("org1");
var org2 = sessionStorage.getItem("org2");

$('#org1').val(org1);
$('#org2').val(org2);

// ##################################################################################################
// ##################################################################################################
/* function の処理を記述 */

var comboTree1 = null;
$(document).ready(function () {
  comboTree1 = $('#workitemID').comboTree({
    isMultiple: false
  });
});

var comboTree2 = null;
$(document).ready(function () {
  comboTree2 = $('#workitemID1').comboTree({
    isMultiple: false
  });
});

// ==================================================
// 分類情報取得
// 
// ==================================================
function getProcessCheckInfo() {
  $('#work_name1').val("");

  $.ajax({
    url: '/getClassification/',
    async: false,
    type: 'POST',
    data: {
      org1: org1,
      org2: org2
    },
    dataType: 'json',
    success: function (response) {
      for (var i = 0; i < response.length; i++) {
        $("#classification_code").append("<option value='" + response[i] + "'>" + response[i] + "</option>");
        $("#classification_code1").append("<option value='" + response[i] + "'>" + response[i] + "</option>");

      }

    }
  });
  getAllProcessProcedureName();
  CreateProcessdataTable();
}

//Get all processProcedureName
function getAllProcessProcedureName() {

  $.ajax({
    url: '/getAllProcessProcedureName/',
    async: false,
    type: 'POST',
    data: {
      org1: org1,
      org2: org2
    },
    dataType: 'json',
    success: function (response) {
      for (var i = 0; i < response.length; i++) {
        $("#work_name1").append("<option value='" + response[i] + "'>" + response[i] + "</option>");

      }

    }
  });
}



//Create Datatable
function CreateProcessdataTable() {

  $.ajax({
    url: '/getAllProcessCheckData/',
    async: false,
    type: 'POST',
    data: {
      org1: org1,
      org2: org2
    },
    dataType: 'json',
    success: function (response) {
      // JSONのキーからの取得
      var jsonObj = JSON.stringify(response);
      var jsonData = JSON.parse(jsonObj)

      // Debug ---------------------------
      console.log(jsonData); // 確認用

      var jsonStatus = jsonData[0].status
      console.log("jsonStatus=" + jsonStatus);

      for (var i = 0; i < jsonData[0].data.length; i++) {
        var wkData = jsonData[0].data[i]
        // console.log("Classification=" + wkData.Classification);
        // console.log("WorkItem=" + wkData.WorkItem);
        // console.log("procedure_name=" + wkData.procedure_name);
        // console.log("CreateMailAddress=" + wkData.CreateMailAddress);
        // console.log("CreateMailAddressName=" + wkData.CreateMailAddressName);
        // console.log("ChangeProhibitionflag=" + wkData.ChangeProhibitionflag);
        // console.log("CreateDateTime=" + wkData.CreateDateTime);
        // console.log("ProcessProcedureID=" + wkData.ProcessProcedureID);
        // console.log("ChartDesignCode=" + wkData.ChartDesignCode);
        // console.log("Chart_Kind=" + wkData.Chart_Kind);
      }
      // Debug ---------------------------

      var dataSet = [];

      // add response data in array
      for (var i = 0; i < jsonData[0].data.length; i++) {
        const row_array = [];
        var wkData = jsonData[0].data[i];

        row_array[0] = parseInt(i) + 1;
        row_array[1] = wkData.Classification;
        row_array[2] = wkData.WorkItem;
        row_array[3] = wkData.procedure_name;
        row_array[4] = wkData.CreateMailAddressName;
        row_array[5] = wkData.CreateDateTime;
        row_array[6] = wkData.ProcessProcedureID;
        row_array[7] = wkData.ChartDesignCode;
        row_array[8] = wkData.ChangeProhibitionflag;
        row_array[9] = wkData.CreateMailAddress;

        dataSet.push(row_array);
      };

      //Create datatable
      $('#processCheckdata').DataTable({
        data: dataSet,
        columns: [
          { title: "番号", "width": "5%" },
          { title: "分類" },
          { title: "作業項目" },
          { title: "作業名" },
          { title: "作成者" },
          { title: "作成日" },
           /* DELETE */ {
            mRender: function (data, type, row) {
              return '<a href="javascript:DispChartAction(\'' + row[3] + '\',\'' + row[6] + '\',\'' + row[7] + '\',\'' + row[9] + '\',\'' + row[8] + '\');"' +
                '" class="btn btn-primary">&nbsp;&nbsp;チャート表示&nbsp;&nbsp;</a>' +
                '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<button class="btn btn-danger" data-id="' + row[0] +
                '" onclick="DeleteAction(\'' + row[3] + '\',\'' + row[2] + '\',\'' + row[6] + '\',\'' + row[9] + '\',\'' + row[8] + '\')">削除</button>'
            }, "width": "20%"
          },
        ],
        "displayLength": 25,
        "pageLength": 25,
        "dom": 'lp<t>frti',
        "ordering": false,
        "bSortable": false,
        "bDestroy": true,
        "language": {
          "sProcessing": "処理中...",
          "sLengthMenu": "_MENU_ 件表示",
          "sZeroRecords": "データはありません。",
          "sInfo": " _TOTAL_ 件中 _START_ から _END_ まで表示",
          "sInfoEmpty": " 0 件中 0 から 0 まで表示",
          "sInfoFiltered": "（全 _MAX_ 件より抽出）",
          "sInfoPostFix": "",
          "sSearch": "検索：",
          "sUrl": "",
          "oPaginate": {
            "sFirst": "先頭",
            "sPrevious": "前",
            "sNext": "次",
            "sLast": "最終"
          }
        }
      });

    },
    error: function (response) {
    }
  });

}


// ==================================================
// 分類情報選択時に該当する情報を取得する
// 
// ==================================================

$('#classification_code').on('change', function () {

  var code = this.value;
  code = code.split("/");
  $('#work_name').val("");
  $('#work_name1').empty().append('<option>Select</option>');

  var org_code1 = $('#org1').val();
  var org_code2 = $('#org2').val();

  if (code[0] == "Select") {
    getAllProcessProcedureName();
    CreateProcessdataTable();
  }
  else {

    $.ajax({
      url: '/getProcessCheckDataByClassification/',
      async: false,
      type: 'POST',
      data: {
        classification_code: code[0],
        org1: org1,
        org2: org2
      },
      dataType: 'json',
      success: function (response) {
        // JSONのキーからの取得
        var jsonObj = JSON.stringify(response);
        var jsonData = JSON.parse(jsonObj)

        // Debug ---------------------------
        console.log(jsonData); // 確認用

        var jsonStatus = jsonData[0].status
        console.log("jsonStatus=" + jsonStatus);

        for (var i = 0; i < jsonData[0].data.length; i++) {
          var wkData = jsonData[0].data[i]
          // console.log("Classification=" + wkData.Classification);
          // console.log("WorkItem=" + wkData.WorkItem);
          // console.log("procedure_name=" + wkData.procedure_name);
          // console.log("CreateMailAddress=" + wkData.CreateMailAddress);
          // console.log("CreateMailAddressName=" + wkData.CreateMailAddressName);
          // console.log("ChangeProhibitionflag=" + wkData.ChangeProhibitionflag);
          // console.log("CreateDateTime=" + wkData.CreateDateTime);
          // console.log("ProcessProcedureID=" + wkData.ProcessProcedureID);
          // console.log("ChartDesignCode=" + wkData.ChartDesignCode);
          // console.log("Chart_Kind=" + wkData.Chart_Kind);
        }
        // Debug ---------------------------

        var dataSet = [];

        // add response data in array
        for (var i = 0; i < jsonData[0].data.length; i++) {
          const row_array = [];
          var wkData = jsonData[0].data[i];

          row_array[0] = parseInt(i) + 1;
          row_array[1] = wkData.Classification;
          row_array[2] = wkData.WorkItem;
          row_array[3] = wkData.procedure_name;
          row_array[4] = wkData.CreateMailAddressName;
          row_array[5] = wkData.CreateDateTime;
          row_array[6] = wkData.ProcessProcedureID;
          row_array[7] = wkData.ChartDesignCode;
          row_array[8] = wkData.ChangeProhibitionflag;
          row_array[9] = wkData.CreateMailAddress;

          dataSet.push(row_array);
        };

        bTable = $('#processCheckdata').dataTable();
        bTable.fnClearTable();
        if (dataSet.length != 0) {
          bTable.fnAddData(dataSet);
        };

      },
      error: function (response) {
      }
    });
  }

  $.ajax({
    url: '/getWorkItemIDInfo/',
    async: false,
    type: 'POST',
    data: {
      classification_code1: code[0],
      org1: org1,
      org2: org2
    },
    dataType: 'json',
    success: function (response) {
      console.log("Response data workitem = " + response);
      var data = response;
      var text = '{"id":"1", "subs":"", "title":"Select"}';
      var obj = JSON.parse(text);
      data.splice(0, 0, obj);
      comboTree1.setSource(data);
    },
    error: function (response) {
      comboTree1.setSource("");
    }
  });

  $.ajax({
    url: '/getProcessProcedureNameByClassification/',
    async: false,
    type: 'POST',
    data: {
      classification_code: code[0],
      org1: org1,
      org2: org2
    },
    dataType: 'json',
    success: function (response) {
      console.log("Response getProcessProcedureNameByClassification>>>" + response)
      for (var i = 0; i < response.length; i++) {
        console.log(response[i])
        $("#work_name1").append("<option value='" + response[i] + "'>" + response[i] + "</option>");

      }

    }
  });

});


// ==================================================
// 作業項目情報選択時に該当する情報を取得する
// 
// ==================================================
$('#workitemID').on('change', function () {
  var workid_code = this.value;
  workid_code = workid_code.split("/");

  var classification_code = $('#classification_code').val();
  classification_code = classification_code.split("/");

  if (this.value == "Select" || this.value == "") {
    $('#work_name').val("");

    // 分類コードが選択されている場合のみ
    if (classification_code != "Select" && classification_code != "") {
      console.log("Work item name onchange if>" + workid_code[0].trim());

      $.ajax({
        url: '/getProcessCheckDataByClassification/',
        async: false,
        type: 'POST',
        data: {
          classification_code: classification_code[0],
          org1: org1,
          org2: org2
        },
        dataType: 'json',
        success: function (response) {
          // JSONのキーからの取得
          var jsonObj = JSON.stringify(response);
          var jsonData = JSON.parse(jsonObj)

          // Debug ---------------------------
          console.log(jsonData); // 確認用

          var jsonStatus = jsonData[0].status
          console.log("jsonStatus=" + jsonStatus);

          for (var i = 0; i < jsonData[0].data.length; i++) {
            var wkData = jsonData[0].data[i]
            // console.log("Classification=" + wkData.Classification);
            // console.log("WorkItem=" + wkData.WorkItem);
            // console.log("procedure_name=" + wkData.procedure_name);
            // console.log("CreateMailAddress=" + wkData.CreateMailAddress);
            // console.log("CreateMailAddressName=" + wkData.CreateMailAddressName);
            // console.log("ChangeProhibitionflag=" + wkData.ChangeProhibitionflag);
            // console.log("CreateDateTime=" + wkData.CreateDateTime);
            // console.log("ProcessProcedureID=" + wkData.ProcessProcedureID);
            // console.log("ChartDesignCode=" + wkData.ChartDesignCode);
            // console.log("Chart_Kind=" + wkData.Chart_Kind);
          }
          // Debug ---------------------------

          var dataSet = [];

          // add response data in array
          for (var i = 0; i < jsonData[0].data.length; i++) {
            const row_array = [];
            var wkData = jsonData[0].data[i];

            row_array[0] = parseInt(i) + 1;
            row_array[1] = wkData.Classification;
            row_array[2] = wkData.WorkItem;
            row_array[3] = wkData.procedure_name;
            row_array[4] = wkData.CreateMailAddressName;
            row_array[5] = wkData.CreateDateTime;
            row_array[6] = wkData.ProcessProcedureID;
            row_array[7] = wkData.ChartDesignCode;
            row_array[8] = wkData.ChangeProhibitionflag;
            row_array[9] = wkData.CreateMailAddress;

            dataSet.push(row_array);
          };

          bTable = $('#processCheckdata').dataTable();
          bTable.fnClearTable();
          if (dataSet.length != 0) {
            bTable.fnAddData(dataSet);
          };

        },
        error: function (response) {
        }
      });
    }

  } else {
    $('#work_name').val("");
    console.log("Work item name onchange else>" + workid_code[0].trim());
    var workid = workid_code[0].trim();

    $.ajax({
      url: '/getProcessCheckDataByWorkItemID/',
      async: false,
      type: 'POST',
      data: {
        workitem_id: workid,
        classification_code: classification_code[0],
        org1: org1,
        org2: org2
      },
      dataType: 'json',
      success: function (response) {
        // JSONのキーからの取得
        var jsonObj = JSON.stringify(response);
        var jsonData = JSON.parse(jsonObj)

        // Debug ---------------------------
        console.log(jsonData); // 確認用

        var jsonStatus = jsonData[0].status
        console.log("jsonStatus=" + jsonStatus);

        for (var i = 0; i < jsonData[0].data.length; i++) {
          var wkData = jsonData[0].data[i]
          // console.log("Classification=" + wkData.Classification);
          // console.log("WorkItem=" + wkData.WorkItem);
          // console.log("procedure_name=" + wkData.procedure_name);
          // console.log("CreateMailAddress=" + wkData.CreateMailAddress);
          // console.log("CreateMailAddressname=" + wkData.CreateMailAddressName);
          // console.log("CreateDateTime=" + wkData.CreateDateTime);
          // console.log("ProcessProcedureID=" + wkData.ProcessProcedureID);
          // console.log("Chart_Kind=" + wkData.Chart_Kind);
        }
        // Debug ---------------------------

        var dataSet1 = [];

        // add response data in array
        for (var i = 0; i < jsonData[0].data.length; i++) {
          const row_array = [];
          var wkData = jsonData[0].data[i];

          row_array[0] = parseInt(i) + 1;
          row_array[1] = wkData.Classification;
          row_array[2] = wkData.WorkItem;
          row_array[3] = wkData.procedure_name;
          row_array[4] = wkData.CreateMailAddressName;
          row_array[5] = wkData.CreateDateTime;
          row_array[6] = wkData.ProcessProcedureID;
          row_array[7] = wkData.ChartDesignCode;
          row_array[8] = wkData.ChangeProhibitionflag;
          row_array[9] = wkData.CreateMailAddress;

          dataSet1.push(row_array);
        };

        //console.log("Data Set = " + dataSet1)
        oTable = $('#processCheckdata').dataTable();
        oTable.fnClearTable();
        if (dataSet1.length != 0) {
          oTable.fnAddData(dataSet1);
        };
      },
      error: function (response) {
      }
    });

    $.ajax({
      url: '/getWorkNameInfo/',
      async: false,
      type: 'POST',
      data: {
        workitem_id: workid,
        org_code1: org1,
        org_code2: org2
      },
      dataType: 'json',
      success: function (response) {
        if (response != "" && response != " " && response != "null") {
          var code_value = response[0];
          // $('#work_name').val(code_value);
        }
      }
    });
  }
});


// ==================================================
// コピー先　作業名情報選択時に該当する情報を取得する
// 
// ==================================================

$('#work_name1').on('change', function () {

  var code = this.value;

  if (code != "Select") {
    $.ajax({
      url: '/getChartDesignCode/',
      async: false,
      type: 'POST',
      data: {
        workName: code,
        org1: org1,
        org2: org2
      },
      dataType: 'json',
      success: function (response) {
        $('#chartDesigncode').val(response);
      },
      error: function (response) {
      }
    });
  }
});


// ==================================================
// コピー先　分類情報選択時に該当する情報を取得する
// 
// ==================================================

$('#classification_code1').on('change', function () {

  var code = this.value;
  code = code.split("/");
  $('#work_name2').val("");

  $.ajax({
    url: '/getWorkItemIDInfo/',
    async: false,
    type: 'POST',
    data: {
      classification_code1: code[0],
      org1: org1,
      org2: org2
    },
    dataType: 'json',
    success: function (response) {
      var data = response;
      var text = '{"id":"1", "subs":"", "title":"Select"}';
      var obj = JSON.parse(text);
      data.splice(0, 0, obj);
      comboTree2.setSource(data);
    },
    error: function (response) {
      comboTree2.setSource("");
    }
  });
});


// ==================================================
// 登録を行う
//
//
// ==================================================

$('#btn_register').click(function (e) {
  e.preventDefault();
  var classification_code = $('#classification_code').val();
  classification_code = classification_code.split("/");

  var workitem_id = $('#workitemID').val();
  workitem_id = workitem_id.split("/");

  var workName = $('#work_name').val();
  var chartkind = $('#chart_kind').val();

  $.ajax({
    url: '/registerProcessCheckData/',
    type: 'POST',
    data: {
      classification_code: classification_code[0].trim(),
      workitem_id: workitem_id[0].trim(),
      workName: workName,
      org1: org1,
      org2: org2,
      user_emal: user_emal,
      chartkind: chartkind
    },
    dataType: 'json',
    success: function (response) {
      if (response[0] == "Normal") {
        alert("登録しました。");
        window.location.reload();
      } else {
        //alert(response[0] + " : " + response[1]);
        window.location.reload();
      }
    }
  });
});

// ==================================================
// 表示を行う
//
// ==================================================

function DispChartAction(processProcedureName, processProcedureID, chartDesignCode, createUser, changeProhibitionflag) {
  // 選択した情報をセッション情報へ
  sessionStorage.setItem("email", user_emal);
  sessionStorage.setItem("org1", org1);
  sessionStorage.setItem("org2", org2);
  sessionStorage.setItem("ProcessProcedureID", processProcedureID);
  sessionStorage.setItem("ProcessProcedureName", processProcedureName);
  sessionStorage.setItem("ChartDesignCode", chartDesignCode);

  // 変更可能？
  sessionStorage.setItem("ChangeProhibitionflag", "0");
  if (changeProhibitionflag == "1") {
    if (createUser != user_emal) {
      // 作成者でないので、編集禁止
      sessionStorage.setItem("ChangeProhibitionflag", "1");
    }
  }

  // 画面に遷移する
  location.href = "../gotoProcessDiagram"
};

// ==================================================
// 削除を行う
// 
// ==================================================

function DeleteAction(work_name, workitem, processProcedureID, createUser, changeProhibitionflag) {

  // 削除可能？
  if (changeProhibitionflag == "1") {
    if (createUser != user_emal) {
      // 作成者でないので、編集禁止
      alert("削除は、作成者が可能です。");
      location.href = "../gotoProcessMain"
      return;
    }
  }

  var workName = work_name.trim();
  var result = window.confirm(workName + 'を削除します。よろしいでしょうか？');

  var workitem_id = workitem.split("/");

  if (result == true) {
    $.ajax({
      url: '/deleteProcessCheckData/',
      type: 'POST',
      data: {
        workName: workName,
        workitem_id: workitem_id[0].trim(),
        org1: org1,
        org2: org2,
        processProcedureID: processProcedureID
      },
      success: function (response) {
        location.href = "../gotoProcessMain"
      }//end of success

    });//end of ajax
  }

};



// ==================================================
// コピーするを行う
//
//
// ==================================================

$('#btn_copy').click(function (e) {
  e.preventDefault();
  var work_name1 = $('#work_name1').val();

  var classification_code1 = $('#classification_code1').val();
  classification_code1 = classification_code1.split("/");

  var workitemID1 = $('#workitemID1').val();
  workitemID1 = workitemID1.split("/");

  var work_name2 = $('#work_name2').val();

  var chartkind = $('#chart_kind').val();

  var chartDesigncode = $('#chartDesigncode').val();

  $.ajax({
    url: '/copyProcessCheckData/',
    type: 'POST',
    data: {
      classification_code: classification_code1[0].trim(),
      workitem_id: workitemID1[0].trim(),
      chartDesigncode: chartDesigncode,
      workName2: work_name2,
      org1: org1,
      org2: org2,
      user_emal: user_emal,
      chartkind: chartkind
    },
    dataType: 'json',
    success: function (response) {
      if (response[0] == "Normal") {
        alert("登録しました。");
        window.location.reload();
      } else {
        alert(response[0] + " : " + response[1]);
        window.location.reload();
      }
    }
  });
});