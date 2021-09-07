// A $( document ).ready() block.
$(document).ready(function () {
  $.ajax({
    url:
      serverUrl +
      "patientprofile?uid=" +
      localStorage.uid +
      "&token=" +
      localStorage.token,
    method: "GET",
    timeout: 0,
    headers: {
      "Content-Type": "application/x-www-form-urlencoded",
    },
  }).done(function (response) {
    response.patientDetails.forEach((patient)=>{
        document.getElementById("doctorName").innerHTML = patient.doctorInCharge;
        document.getElementById("phone").innerHTML = patient.phone;
        document.getElementById("address").innerHTML = patient.address;
        document.getElementById("concern").innerHTML = patient.concern;
        document.getElementById("xray").innerHTML = patient.xray;
        document.getElementById("design").innerHTML = patient.designFile;
        document.getElementById("previousupload").innerHTML =
          patient.previousupload;
    })
  });
});
