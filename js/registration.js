// A $( document ).ready() block.
$( document ).ready(function() {
    var formdata = new FormData();
    if (!!$('.uploadProfileInput').get(0).files[0])
    formdata.append("xray", $('.uploadProfileInput').get(0).files[0], "ProfileImage." + $('.uploadProfileInput').get(0).files[0].name.split('.').pop());
    formdata.append("firstName", document.getElementById('firstName').value);
    formdata.append("lastName", document.getElementById('lastName').value);
    formdata.append("address", document.getElementById('address').value);
    formdata.append("phoneNumber", document.getElementById('phone').value);
    formdata.append("concern", document.getElementById('concern').value);
    formdata.append("durationOfTreatment", document.getElementById('duration').value);
    formdata.append("startDateOfTreatment", document.getElementById('startdate').value);

    $.ajax({
        "url": serverUrl+"register",
        "method": "POST",
        "timeout": 0,
        "headers": {
            "Content-Type": "application/x-www-form-urlencoded"
        },
        "data": formdata
    }).done(function (response) {

        if(response.status == "admin"){
            window.location.replace("dashboard.html");

        } else {
            window.location.replace("error-404.html");
        }

    });
});