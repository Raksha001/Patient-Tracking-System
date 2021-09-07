function login() {
  var username = document.getElementById("username").value;
  var password = document.getElementById("password").value;

  $.ajax({
    url: serverUrl+"login",
    method: "POST",
    timeout: 0,
    headers: {
      "Content-Type": "application/x-www-form-urlencoded",
    },
    data: {
      username: username,
      password: password,
    },
  }).done(function (response) {
    console.log(response);

    if (response.status == "patient") {
      localStorage.uid = response.uid;
      localStorage.token = response.token;

      window.location.replace("viewprofile.html");
    } else if (response.status == "admin") {
      localStorage.uid = response.uid;
      localStorage.token = response.token;

      window.location.replace("dashboard.html");
    } else {
      window.location.reload();
    }
  });
}
