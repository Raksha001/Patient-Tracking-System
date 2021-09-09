$( document ).ready(function() {

    $.ajax({
        "url": serverUrl+"dashboard",
        "method": "POST",
        "timeout": 0,
        "headers": {
            "Content-Type": "application/x-www-form-urlencoded"
        },
        "data": {
            "token": localStorage.token
        }
    }).done(function (response) {

        if(response.status == "admin"){
            document.getElementById("casesCompleted").innerHTML = response.completedCount;
            document.getElementById("doctorCount").innerHTML = response.doctorCount;
            document.getElementById("liveCount").innerHTML = response.liveCount;
            document.getElementById("patientCount").innerHTML = response.patientCount;
            document.getElementById("duration").innerHTML = response.durationOfTreatment;
            document.getElementById("patientName").innerHTML = response.users.patientName;
            document.getElementById("doctorName").innerHTML = response.users.doctorInCharge;

        } else {
            window.location.replace("error-404.html");
        }

    });
});