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

// var classification = getUrlParameter("classification");
// console.log("classification = " + classification)
// var workitem = getUrlParameter("workitem");
// console.log("workitem = " + workitem)
// var workitem_id = workitem.split("/")
// workitem_id = workitem_id[0]
// var procedure_name = getUrlParameter("procedure_name");
// console.log("workitem_name = " + procedure_name)
// $("#process_ProcedureName").html(procedure_name)


$(document).ready(function () {
  function custom_template(obj) {
    var data = $(obj.element).data();
    var text = $(obj.element).val();

    if (text == "") {
      template = $("<div style='width:100px;height:30px;'></div>");
      return template;
    }
    if (text == "start") {
      if (data && data['img_src']) {
        img_src = data['img_src'];
        template = $("<div><img src=\"" + img_src + "\" style=\"width:100px;height:40px;margin-left:33px;\"/></div>");
        return template;
      }
    }
    if (text == "arrow") {
      if (data && data['img_src']) {
        img_src = data['img_src'];
        template = $("<div><img src=\"" + img_src + "\" style=\"width:100px;height:40px;margin-left:45px;\"/></div>");
        return template;
      }
    }
    if (text == "c8") {
      if (data && data['img_src']) {
        img_src = data['img_src'];
        template = $("<div><img src=\"" + img_src + "\" style=\"width:100px;height:40px;margin-left:40px;\"/></div>");
        return template;
      }
    }
    if (text == "downtoright") {
      if (data && data['img_src']) {
        img_src = data['img_src'];
        template = $("<div><img src=\"" + img_src + "\" style=\"width:100px;height:40px;margin-left:49px;\"/></div>");
        return template;
      }
    }
    if (text == "down_arrow") {
      if (data && data['img_src']) {
        img_src = data['img_src'];
        template = $("<div><img src=\"" + img_src + "\" style=\"width:100px;height:40px;margin-left:7px;\"/></div>");
        return template;
      }
    }
    if (text == "c7") {
      if (data && data['img_src']) {
        img_src = data['img_src'];
        template = $("<div><img src=\"" + img_src + "\" style=\"width:100px;height:40px;margin-left:49px;\"/></div>");
        return template;
      }
    }
    if (text == "uptoleft") {
      if (data && data['img_src']) {
        img_src = data['img_src'];
        template = $("<div><img src=\"" + img_src + "\" style=\"width:100px;height:40px;margin-left:10px;\"/></div>");
        return template;
      }
    }
    if (text == "stop") {
      if (data && data['img_src']) {
        img_src = data['img_src'];
        template = $("<div><img src=\"" + img_src + "\" style=\"width:100px;height:40px;margin-left:40px;\"/></div>");
        return template;
      }
    }
    else {
      if (data && data['img_src']) {
        img_src = data['img_src'];
        template = $("<div><img src=\"" + img_src + "\" style=\"width:100px;height:40px;margin-left:36px;\"/></div>");
        return template;
      }
    }

  }
  var options = {
    'templateSelection': custom_template,
    'templateResult': custom_template,
  }

  for (var i = 1; i <= 9; i++) {

    $('#id_select_A' + i).select2(options);
    $('#id_select_B' + i).select2(options);
    $('#id_select_C' + i).select2(options);
    $('#id_select_D' + i).select2(options);
    $('#id_select_E' + i).select2(options);
    $('#id_select_F' + i).select2(options);
    $('#id_select_G' + i).select2(options);
  }

  $('.select2-container--default .select2-selection--single').css({ 'height': '45px' });
  $('.select2-container--default .select2-selection--single').css({ 'width': '220px' });
});

