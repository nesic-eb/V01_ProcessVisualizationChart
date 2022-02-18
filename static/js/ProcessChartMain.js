// =============================================================================
// 画面名：プロセス可視化チャート画面
// 
// -----------------------------------------------------------------------------
// （ファイル整形）Visual Studio Code : Shift + Alt + f 
// =============================================================================


// ##################################################################################################
// ##################################################################################################
/* セッション情報取得 */
console.log("■ ---------------------------------------------");
console.log("■ セッション情報 -- ProcessCheck.js --------");

var org1 = '50';
var org2 = '05';

$('#org1').val(org1);
$('#org2').val(org2);
console.log("org1 = " + org1);
console.log("org2 = " + org2);

// パラメータから取得すること！！
var user_name = ""
var user_emal = "fujii.kyoichi.za@nesic.com"

// ##################################################################################################
// ##################################################################################################
/* function の処理を記述 */

var comboTree1 = null;
$(document).ready(function () {
  comboTree1 = $('#workitemID').comboTree({
    isMultiple: false
  });
});

// ==================================================
// 分析情報取得
// 
// ==================================================
function getProcessCheckInfo() {

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
      console.log("Response>>>" + response)
      for (var i = 0; i < response.length; i++) {
        console.log(response[i])
        $("#classification_code").append("<option value='" + response[i] + "'>" + response[i] + "</option>");

      }

    }
  });

  CreateProcessdataTable();

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
        console.log("Classification=" + wkData.Classification);
        console.log("WorkItem=" + wkData.WorkItem);
        console.log("procedure_name=" + wkData.procedure_name);
        console.log("CreateMailAddress=" + wkData.CreateMailAddress);
        console.log("CreateDateTime=" + wkData.CreateDateTime);
        console.log("ProcessProcedureID=" + wkData.ProcessProcedureID);
        console.log("Chart_Kind=" + wkData.Chart_Kind);
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
        row_array[4] = wkData.CreateMailAddress;
        row_array[5] = wkData.CreateDateTime;
        row_array[6] = wkData.ProcessProcedureID;

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
              return '<a href="../goToProcessDiagram?classification=' + row[1] + '&workitem=' + row[2] + '&procedure_name=' + row[3] + "&ProcessProcedureID=" + row[6] +
                '" class="btn btn-primary">変更</a>' +
                '&nbsp;<button class="btn btn-primary" data-id="' + row[0] + '" onclick="DeleteAction(\'' + row[3] + '\',\'' + row[2] + '\')">削除</button>'
            }
          },
        ],
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
          "sSearch": "検索:",
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
// 分析情報選択時に該当する情報を取得する
// 
// ==================================================

$('#classification_code').on('change', function () {

  var code = this.value;
  code = code.split("/");
  $('#work_name').val("");
  var org_code1 = $('#org1').val();
  var org_code2 = $('#org2').val();

  if (code[0] == "Select") {
    CreateProcessdataTable();
  }
  else {

    $.ajax({
      url: '/getProcessCheckDataByClassification/',
      async: false,
      type: 'POST',
      data: {
        classification_code: code[0],
        org1: org_code1,
        org2: org_code2
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
          console.log("Classification=" + wkData.Classification);
          console.log("WorkItem=" + wkData.WorkItem);
          console.log("procedure_name=" + wkData.procedure_name);
          console.log("CreateMailAddress=" + wkData.CreateMailAddress);
          console.log("CreateDateTime=" + wkData.CreateDateTime);
          console.log("ProcessProcedureID=" + wkData.ProcessProcedureID);
          console.log("Chart_Kind=" + wkData.Chart_Kind);
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
          row_array[4] = wkData.CreateMailAddress;
          row_array[5] = wkData.CreateDateTime;
          ;
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
      console.log("Hello else data>>" + response)
      comboTree1.setSource("");

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
    console.log("Work item name onchange if>" + workid_code[0].trim());

    $.ajax({
      url: '/getProcessCheckDataByClassification/',
      async: false,
      type: 'POST',
      data: {
        classification_code: classification_code[0],
        org1: org_code1,
        org2: org_code2
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
          console.log("Classification=" + wkData.Classification);
          console.log("WorkItem=" + wkData.WorkItem);
          console.log("procedure_name=" + wkData.procedure_name);
          console.log("CreateMailAddress=" + wkData.CreateMailAddress);
          console.log("CreateDateTime=" + wkData.CreateDateTime);
          console.log("ProcessProcedureID=" + wkData.ProcessProcedureID);
          console.log("Chart_Kind=" + wkData.Chart_Kind);
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
          row_array[4] = wkData.CreateMailAddress;
          row_array[5] = wkData.CreateDateTime;

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

  } else {
    $('#work_name').val("");
    console.log("Work item name onchange else>" + workid_code[0].trim());
    var workid = workid_code[0].trim();
    var org_code1 = $('#org1').val();
    var org_code2 = $('#org2').val();

    $.ajax({
      url: '/getProcessCheckDataByWorkItemID/',
      async: false,
      type: 'POST',
      data: {
        workitem_id: workid,
        classification_code: classification_code[0],
        org1: org_code1,
        org2: org_code2
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
          console.log("Classification=" + wkData.Classification);
          console.log("WorkItem=" + wkData.WorkItem);
          console.log("procedure_name=" + wkData.procedure_name);
          console.log("CreateMailAddress=" + wkData.CreateMailAddress);
          console.log("CreateDateTime=" + wkData.CreateDateTime);
          console.log("ProcessProcedureID=" + wkData.ProcessProcedureID);
          console.log("Chart_Kind=" + wkData.Chart_Kind);
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
          row_array[4] = wkData.CreateMailAddress;
          row_array[5] = wkData.CreateDateTime;

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
        org_code1: org_code1,
        org_code2: org_code2
      },
      dataType: 'json',
      success: function (response) {
        if (response != "" && response != " " && response != "null") {
          var code_value = response[0];
          $('#work_name').val(code_value);
        }
      }
    });
  }
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
        alert(response[0] + " : " + response[1]);
        window.location.reload();
      }
    }
  });
});


// ==================================================
// 削除を行う
// 
// ==================================================

function DeleteAction(work_name, workitem) {
  var workName = work_name.trim();
  var workitem_id = workitem.split("/");
  var result = window.confirm(workName + 'を削除します。よろしいでしょうか？');
  if (result == true) {
    $.ajax({
      url: '/deleteProcessCheckData/',
      type: 'POST',
      data: {
        workName: workName,
        workitem_id: workitem_id[0].trim(),
        org1: org1,
        org2: org2
      },
      success: function (response) {
        window.location.reload();
      }//end of success

    });//end of ajax
  }
}