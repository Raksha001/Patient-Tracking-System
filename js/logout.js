function logout() {
  
    $.ajax({
      url: serverUrl+"logout",
      method: "POST",
      timeout: 0,
      headers: {
        "Content-Type": "application/x-www-form-urlencoded",
      },
      data: {
        token: localStorage.token,

      },
    }).done(function (response) {
      console.log(response);
  
      if (response.status == "true") {
        localStorage.uid = "";
        localStorage.token = "";
  
        window.location.replace("index.html");
      } else {
        window.location.reload();
      }
    });
  }
  