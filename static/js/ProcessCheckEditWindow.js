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
console.log("■ セッション情報 -- ProcessCheckEditWindow.js --------");


function clearData(){
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



function buttonClick() {
    //alert('Click');
    window.close();
    var comment_code = $("#comment_code").val();
    console.log("comment code = "+comment_code);
    var new_comment_code = $("#new_comment_code").val();
    if(comment_code == "0000"){
        comment_code = new_comment_code;
    }
    var heading = $("#heading").val();
    console.log("heading = "+heading);
    var explaination = $("#explaination").val();
    console.log("explaination = "+explaination);
    var efficiency = $("#efficiency").val();
    console.log("efficiency = "+efficiency);
    var ExceptionWork = $("#ExceptionWork").val();
    console.log("ExceptionWork= "+ExceptionWork);
    var OperationTarget = $("#OperationTarget").val();
    console.log("OperationTarget = "+OperationTarget);
    var working_hour = $("#working_hour").val();
    console.log("working_hour = "+working_hour);
    var SupplementComment = $("#SupplementComment").val();
    console.log("SupplementComment = "+SupplementComment);
    $.ajax({
        url: '/updateChartCommentInfo/',
        type: 'POST',
        data: {
            comment_code : comment_code,
            heading : heading,
            explaination : explaination,
            efficiency : efficiency,
            ExceptionWork : ExceptionWork,
            OperationTarget :  OperationTarget,
            working_hour :  working_hour,
            SupplementComment :  SupplementComment
        },
        success: function (response) {
        }
    });

}


function commentCode_onchange(){
    var comment_code = $("#comment_code").val();
    if(comment_code == "0000"){
        $("#new_comment_code").attr("readonly",false);
    }
}


      

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

$.ajax({
    url: '/getCommentList/',
    type: 'GET',
    dataType: 'json',
    success: function (response) {
        console.log("response in get comment list "+response)
        for(var i=0;i<response.length;i++){
            var CommentCode = getUrlParameter("CommentCode");
            if(CommentCode == response[i]){
                $("#comment_code").append("<option value='"+response[i]+"' selected>"+response[i]+"</option>");
            }else{
                $("#comment_code").append("<option value='"+response[i]+"'>"+response[i]+"</option>");
            }
            
        }
        
    }
});

$( document ).ready(function() {


var dataID = getUrlParameter("dataId");
console.log("dataID = " + dataID)
$("#location_id").text(dataID)

// var CommentCode = getUrlParameter("CommentCode");
// console.log("CommentCode = " + CommentCode)
// var cmm_code = $("#comment_code").val();
// console.log("cmm_code = "+cmm_code)
    

var Heading = getUrlParameter("Heading");
console.log("Heading = " + Heading)
$("#heading").val(Heading)


var Explanation = getUrlParameter("Explanation");
console.log("Explanation = " + Explanation)
$("#explaination").val(Explanation)


var Efficiency = getUrlParameter("Efficiency");
console.log("Efficiency = " + Efficiency);
$('#efficiency').val(String(Efficiency));



var OperationTarget = getUrlParameter("OperationTarget");
console.log("OperationTarget = " + OperationTarget);
$("#OperationTarget").val(String(OperationTarget));


var WorkingHour = getUrlParameter("WorkingHour");
console.log("WorkingHour = " + WorkingHour)
$("#working_hour").val(String(WorkingHour));


var ExceptionWork = getUrlParameter("ExceptionWork");
console.log("ExceptionWork = " + ExceptionWork)
$("#ExceptionWork").val(ExceptionWork)


var SupplementComment = getUrlParameter("SupplementComment");
console.log("SupplementComment = " + SupplementComment)
$("#SupplementComment").val(SupplementComment);

});