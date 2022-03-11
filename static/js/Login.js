// =============================================================================
// 画面名：ログイン画面
// 
// -----------------------------------------------------------------------------
// （ファイル整形）Visual Studio Code : Shift + Alt + f 
// =============================================================================

// ##################################################################################################
// ##################################################################################################
/* セッション情報取得 */
sessionStorage.setItem("org_check", "");

// セッション情報作成
sessionStorage.setItem("email", "");
sessionStorage.setItem("org1", "");
sessionStorage.setItem("org2", "");
sessionStorage.setItem("ProcessProcedureID", "");
sessionStorage.setItem("ProcessProcedureName", "");
sessionStorage.setItem("ChartDesignCode", "");
sessionStorage.setItem("ChangeProhibitionflag", "");
// 自動保存（１：保存する）
sessionStorage.setItem("AutoSaveControl", "1");
sessionStorage.setItem("AutoColumnNum", "");
sessionStorage.setItem("AutoRowsNum", "");

// ##################################################################################################
// ##################################################################################################

// ==================================================
// ログインした情報を保持する
// 
// ==================================================
function SaveEmailSessionAndNextWindow() {
  var email = $("#email").val();
  var pass = $("#password").val();

  console.log("email = " + email)
  console.log("password = " + pass);

  // ログインの処理
  $.ajax({
    url: '/checkEmailAndPassword/',
    type: 'POST',
    data: {
      email: email,
      pass: pass
    },
    dataType: 'json',
    success: function (response) {
      if (response.status == "OK") {
        var orgcode = response.orgcode.split("-");

        sessionStorage.setItem("email", email);
        //sessionStorage.setItem("password", pass);
        sessionStorage.setItem("org1", orgcode[0]);
        sessionStorage.setItem("org2", orgcode[1]);

        location.href = "./gotoProcessMain";
      }
      else {
        alert("パスワードが違います。");
      }
    }
  });


}

// ==================================================
// 入力状態を確認する
// 
// ==================================================
function myFunction() {
  var email = $("#email").val();
  var pass = $("#password").val();
  var a = document.getElementById('password_setting_id');
  if (email == "" || pass == "") {
    alert("メールアドレスを入力してください。")
    return;
  }
}

