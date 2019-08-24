ajax = new XMLHttpRequest();

function tryNow() {


  console.log(user_email_id);

  var riddles = [{
      "question": "You find me in December, but not in any other month. What am I?",
      "answer": "The letter D!"
    },
    {
      "question": "A girl fell off of a 30-foot ladder, but she didn’t get hurt at all. How is this possible?",
      "answer": "She fell off the bottom step!"
    },
    {
      "question": "What are two things you wouldn’t eat after waking up?",
      "answer": "Lunch and dinner!"
    },
    {
      "question": "What do snowmen do when they're not feeling well?",
      "answer": "They take a chill pill!"
    }
  ]
  var riddlenumber = Math.floor(Math.random() * (riddles.length))

  Swal.mixin({

    
    progressSteps: ['1', '2', '3']
  }).queue([{
      title: 'Email',
      text: 'Results will be sent to the entered email id. You can change the email id below if you want.',
      type: 'info',
      input: "email",
      inputValue: user_email_id,
      inputPlaceholder: 'Enter your email id here',
      confirmButtonText: 'Next',
      showCancelButton: true,
    },
    {
      title: 'Description',
      text: 'Enter Video Description',
      input: "text",
      inputPlaceholder: 'Enter video description here',
      confirmButtonText: 'Next',
      showCancelButton: true,
    },
    {
      title: 'Upload Video',
      text: "We only support .mp4 files",
      input: "file",
      confirmButtonText: 'Process',
      showCancelButton: true,
    }
  ]).then((result) => {

    flag = 0;

    function getExtension(filename) {
      var parts = filename.split('.');
      return parts[parts.length - 1];
    }

    function isVideo(filename) {
      var ext = getExtension(filename);
      switch (ext.toLowerCase()) {
        case 'mp4':
          return true;
      }
      return false;
    }

    var file = result.value[2];
    if (file == null) {
      flag = 0;
    } else {
      if (isVideo(file.name)) {
        flag = 1;

      }
    }


    if (flag == 1) {
      if (result.value) {
        console.log(result.value)
        Swal.fire({
          title: 'Uploading...',
          text: '',
          allowOutsideClick: false,
          showConfirmButton: false,
          showCancelButton: true,
          html: '<img src="static/assets/cloud-1.gif"><center><div id="progress_bar1" style="font-size:30px">0%</div></center>'
        }).then(function (value) {
          console.log(value);
          if (value.dismiss == "cancel") {
            ajax.abort()
            Swal.fire({
              type: 'error',
              title: 'Canceled',
              text: 'Your uploading and processing is canceled!'
            })
          }
        })


        var formData = new FormData();
        formData.append('email', result.value[0]);
        formData.append('description', result.value[1]);
        formData.append('user_file', result.value[2]);

        ajax.onreadystatechange = function () {
          if (ajax.status) {
            if (ajax.status == 200 && (ajax.readyState == 4)) {
              response1 = JSON.parse(ajax.responseText);
              if (response1) {
                console.log(response1)
                if (response1.status==true){
                  x1 = '<center style="color:#35A0EF; font-weight: 900;"><h2>Results</h2></center><table class="table">'

                  for (var x = 0; x < response1.data.length; x++) {
                    if (response1.data[x].filepath.length > 3) {
                      x1 += '<div id="target"><div class="albums"><div class="albums-inner"><div class="albums-tab"><div class="albums-tab-thumb sim-anim-9">';
                    } else {
                      x1 += '<div id="target"><div class="albums"><div class="albums-inner"><div class="albums-tab"><div class="albums-tab-thumb sim-anim-3">';
                    }
                    for (var y = 0; y < response1.data[x].filepath.length; y++) {
                      x1 += '<img src="' + response1.data[x].filepath[y] + '" class="all studio" />'
                    }
                    z=x+1
                    x1+='</div></div></div></div><div class="albums-tab-text" style="text-decoration: underline;text-decoration-style:dotted;">Scene: '+z+' | Timespan: '+response1.timestampfinal[x][0]+'<span>&nbsp;-&nbsp;</span>'+response1.timestampfinal[x][1]+'</div></div>'

                  }
                  document.getElementById("container").innerHTML = x1
                } else {
                  x1 = '<center style="color:#35A0EF; font-weight: 900;"><h2>Results</h2></center><table class="table">'
                  x1 += '<center style="color:#36A0F0; font-weight: 700;"><h4>There are no smoking scenes in video</h4></center>'
                  document.getElementById("container").innerHTML = x1
                }
              }
              
              Swal.fire({
                title: 'Completed!',
                text: 'Click OK to get results',
                type: 'success',
                html: '<center><p>Question: ' + riddles[riddlenumber].question + '</p><p>Answer: ' + riddles[riddlenumber].answer + '</p><p>Results down below <span class="fas fa-arrow-circle-down"></span></p></center>'
              })
            }
          }
        }


        var percent1 = $("#progress_bar1");

        ajax.upload.addEventListener("progress", function (event) {
          var percent = (event.loaded / event.total) * 100;
          percent1.html(Math.floor(percent) + "%");

          if (percent == 100) {
            if (result.value[2].size > 52428800) {

              Swal.fire({
                title: 'Sit back and relax',
                text: 'You can close the website, we will mail you the results',
                allowOutsideClick: false,
                showConfirmButton: false,
                showCancelButton: true
              })
            } else {
              Swal.fire({
                title: 'Processing',
                text: 'Video is uploaded and is being processed',
                allowOutsideClick: false,
                showCancelButton: false,
                showConfirmButton: false,
                html: '<img src="static/assets/infinity.gif"><br/><center><p>Till then try to solve this riddle!</p><p style="font-weight:800">' + riddles[riddlenumber].question + '</p></center>',
              })
            }
          }
        });
        ajax.open("POST", '/upload', true);
        ajax.send(formData)

      }
    } else {
      Swal.fire({
        title: 'Invalid File!',
        text: 'Please select a valid file',
        type: 'error',
      })
    }

  })
}

function readMore() {
  Swal.fire({
    title: 'What you need to do?',
    text: '',
    html: '<br/><div style="text-align: justify">' +
      '<ul style="list-style-position: inside;padding-inline-start: 0px;">' +
      '<li>Enter your email id.</li>' +
      '<li>Upload your video.</li>' +
      '<li>Sit back and relax. We will email you the results.</li>' +
      '<ul></div><br>',
    type: 'info',
  })
}

function deleteUser() {
  Swal.fire({
    type: 'warning',
    title: 'Are you sure?',
    text: 'Your account will be deleted',
    showConfirmButton: true,
    confirmButtonText: 'Ok',
    showCancelButton: true,
    allowOutsideClick: false,
  }).then(function (data) {
    if (data.value == true) {
      console.log(data.value);
      ajax1 = new XMLHttpRequest();
      ajax1.onreadystatechange = function () {
        if ((ajax1.readyState == 4) && (ajax1.status == 200)) {
          data = JSON.parse(ajax1.responseText)
          if (data.status == true) {
            Swal.fire({
              type: 'success',
              title: 'Successful',
              text: 'Your Account Has Been Deleted!',
              showConfirmButton: true,
              focusConfirm: true,
              confirmButtonText: 'Ok',
              allowOutsideClick: false
            }).then(function (data) {
              if (data.value == true) {
                hostname = window.location.hostname
                url = "http://"+hostname+"/welcome/logout"
                window.location.replace(url)
              }
            })
          } else {
            Swal.fire({
              type: 'error',
              title: 'Error',
              text: 'Server error, try again some time later',
              showConfirmButton: true,
              confirmButtonText: 'Ok'
            })
          }
        }
      }
      ajax1.open("POST", '/deleteuser', true)
      ajax1.send()
    }
  })
}
