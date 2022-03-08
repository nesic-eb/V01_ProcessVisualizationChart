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

// ##################################################################################################
// ##################################################################################################

// ==================================================
// ログインした情報を保持する
// 
// ==================================================
function SaveEmailSessionAndNextWindow() {
  var email = $("#email").val();
  console.log("email = "+email)
  var pass = $("#password").val();
  console.log("password = "+pass);
  var url = "";

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

      location.href = url + "./gotoProcessMain?email=" + email + "&orgCode=" + response[1] + "&roll=" + response[2] + "&principalbusiness_code=" + response[3];

      sessionStorage.setItem("email", email);
      sessionStorage.setItem("password", pass);
      
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
  } else {
    a.href = "/gotoPasswordSetting"

  }
  sessionStorage.setItem("email", email);
  sessionStorage.setItem("password", pass);
}

