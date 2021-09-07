// A $( document ).ready() block.
$( document ).ready(function() {

    $.ajax({
        "url": serverUrl+"dashboard",
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

        if(response.status == "admin"){
            document.getElementById("casesCompleted").innerHTML = response.casesCompleted;
            document.getElementById("doctorCount").innerHTML = response.doctorCount;
            document.getElementById("liveCount").innerHTML = response.liveCount;
            document.getElementById("patientCount").innerHTML = response.patientCount;
            document.getElementById("duration").innerHTML = response.duration;
            document.getElementById("patientName").innerHTML = response.patientName;
            document.getElementById("doctorName").innerHTML = response.doctorName;

        } else {
            window.location.replace("error.html");
        }

    });
});