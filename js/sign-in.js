function login(){
    var username = document.getElementById("email").value;
    var password = document.getElementById("password").value;


    $.ajax({
        "url": "http://127.0.0.1:5000/login",
        "method": "POST",
        "timeout": 0,
        "headers": {
            "Content-Type": "application/x-www-form-urlencoded"
        },
        "data": {
            "username": username,
            "password": password
        }
    }).done(function (response) {
        console.log(response);

        if(response.status == "success"){
            localStorage.fullName = response.fullName;
            localStorage.profilePic = response.profilePic;
            localStorage.profilePic = response.profilePic;
            localStorage.profilePic = response.profilePic;
            localStorage.profilePic = response.profilePic;
            localStorage.profilePic = response.profilePic;

            window.location.replace("dashboard.html");

        } else {
            localStorage.fullName = "";
            localStorage.fullName = "";
            localStorage.fullName = "";
            localStorage.fullName = "";
            localStorage.fullName = "";

            window.location.reload();
        }

    });
      
}