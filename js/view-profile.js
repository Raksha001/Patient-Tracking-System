// A $( document ).ready() block.
$( document ).ready(function() {

    $.ajax({
        "url": "http://127.0.0.1:5000/patientprofile",
        "method": "POST",
        "timeout": 0,
        "headers": {
            "Content-Type": "application/x-www-form-urlencoded"
        },
        "data": {
            "uid": localStorage.uid,
            "token": localStorage.token
        }
    }).done(function (response) {

        if(response.status == "patient"){
            document.getElementById("doctorName").innerHTML = response.doctorName;
            document.getElementById("phone").innerHTML = response.phone;
            document.getElementById("address").innerHTML = response.address;
            document.getElementById("concern").innerHTML = response.concern;
            document.getElementById("xray").innerHTML = response.xray;
            document.getElementById("design").innerHTML = response.design;
            document.getElementById("previousupload").innerHTML = response.previousupload;

        } else {
            window.location.replace("home.html");
        }

    });
});