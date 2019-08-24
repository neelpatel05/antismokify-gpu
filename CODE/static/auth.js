$(document).ready(function() {
  $("body").on("contextmenu",function(e){
    e.preventDefault
    return false;
  });
  $("header").on("contextmenu",function(){
    e.preventDefault
    return false;
  });
});

function login() {

Swal.fire({
  title: 'Login',
  text: '',
  html: '<form id = "loginForm" method = "POST" action="/welcome"><input id="user_email" class="swal2-input" name="user_email" type ="email" placeholder="Enter Your Email Id" />' +
    '<input id="user_password" class="swal2-input" name="user_password" type ="password" placeholder="Enter Your Password" /></form',
  showCancelButton: true,
  showConfirmButton: true,
  focusConfirm: true,
  confirmButtonText: 'Login',
  cancelButtonText: 'Forgot Password?',
  showLoaderOnConfirm: true,
  preConfirm: (login) => {

    if(document.getElementById('user_email').value == '' || document.getElementById('user_password').value == ''){
      Swal.showValidationMessage(
        "Invalid email or password"
      )
    }else{
      var formData = new FormData();
      formData.append('user_email', document.getElementById('user_email').value);
      formData.append('user_password', document.getElementById('user_password').value);
      return fetch('/login', {
          method: 'POST',
          body: formData
        })
        .then(function (response) {
          return response.json();

        }).then(function (data) {
          console.log(data);
          if (data.status == false) {
            error=data.error
            Swal.showValidationMessage(
              error
            )
          } else {
            hostname = window.location.hostname
            url = "http://"+hostname+"/welcome"
            window.location.replace(url)
          }
        })
      }
  },
  allowOutsideClick: () => !Swal.isLoading()
}).then(function(result){
  if(result.dismiss=="cancel"){
    forgotpassword()
  }
})

}

function forgotpassword() {

var x;

Swal.fire({
  title: 'Forgot Password?',
  html: '<p>No worries! Enter email id and we will send you the pin to change password</p><form id = "loginForm" method = "POST" action="/welcome"><input id="user_email" class="swal2-input" name="user_email" type ="email" placeholder="Enter Your Email Id" /></form',
  focusConfirm: true,
  confirmButtonText: 'Send Pin',
  showLoaderOnConfirm: true,
  preConfirm: function() {

    if(document.getElementById('user_email').value == ''){
      Swal.showValidationMessage(
        "Invalid email or email field cannot be empty"
      )
    }else{
      var formData = new FormData();
      formData.append('user_email', document.getElementById('user_email').value);
      return fetch('/forgotpasswordkey', {
          method: 'POST',
          body: formData
        })
        .then(function (response) {
          return response.json();
        }).then(function (data) {
          console.log(data);
          if (data.status == false) {
            error=data.error
            Swal.showValidationMessage(
              error
            )
          } else if (data.status == true) {
            console.log("in true")
            x=true
          }
        })
      }
  },
}).then(function(){
  if (x==true){
    Swal.fire({
      type:'success',
      title:'Success',
      text:'Pin sent to your email id',
    }).then(function(){
      updatepassword()
    })
  }
})

}

function updatepassword(){

console.log("in updatepassword");
Swal.fire({
  title: 'Updating Password',
  html: '<form id = "loginForm" method = "POST" action="/welcome"><input id="user_email" class="swal2-input" name="user_email" type ="email" placeholder="Enter Your Email Id" />'+
  '<input id="user_password" class="swal2-input" name="user_password" type ="password" placeholder="Enter Your Password" />'+
  '<input id="user_pin" class="swal2-input" name="user_pin" type ="text" placeholder="Enter Your Pin" /></form>',
  focusConfirm: true,
  confirmButtonText: 'Update Password',
  showLoaderOnConfirm: true,
  preConfirm: (updatepassword) => {

    if(document.getElementById('user_password').value == '' || document.getElementById('user_pin').value == ''){
      Swal.showValidationMessage(
        "Invalid email or password"
      )
    }else{
      var formData = new FormData();
      formData.append('user_email', document.getElementById('user_email').value);
      formData.append('user_pin', document.getElementById('user_pin').value);
      formData.append('user_password', document.getElementById('user_password').value);
      return fetch('/forgotpassword', {
          method: 'POST',
          body: formData
        })
        .then(function (response) {
          return response.json();

        }).then(function (data) {
          console.log(data);
          if (data.status == false) {
            error=data.error
            Swal.showValidationMessage(
              error
            )
          } else {
            Swal.fire({
              type:"success",
              title:"Success",
              text:"Your password is updated"
            })
          }
        })
      }
  },
  allowOutsideClick: () => !Swal.isLoading()
})
}

function validateEmail(mail) {
if (/^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/.test(mail))
  return (true)
return (false)
}

function validatePassword(pass) {
if (pass.length > 2)
  return (true)
return (false)
}

function registration() {

var x;
Swal.fire({
  title: 'Register',
  text: '',
  html: '<form id = "registerForm" method = "POST" action="/welcome"><input id="user_email" class="swal2-input" name="user_email" type ="email" placeholder="Enter Your Email Id" />' +
    '<input id="user_password" class="swal2-input" name="user_password" type ="password" placeholder="Enter Your Password (Atleast 3 Characters)" /></form',
  focusConfirm: true,
  showConfirmButton: true,
  showCancelButton: true,
  confirmButtonText: 'Register',
  showLoaderOnConfirm: true,
  preConfirm: (login) => {

    if (!validateEmail(document.getElementById('user_email').value)) {
      Swal.showValidationMessage(
        "Enter a Valid Email Id"
      )
    } else if (!validatePassword(document.getElementById('user_password').value)) {
      Swal.showValidationMessage(
        "Enter a Password Of Atleast 3 Characters"
      )
    } else {
      var formData = new FormData();
      formData.append('user_email', document.getElementById('user_email').value);
      formData.append('user_password', document.getElementById('user_password').value);
      return fetch('/registration', {
          method: 'POST',
          body: formData
        })
        .then(function (response) {
          return response.json();

        }).then(function (data) {
          console.log(data);
          if (data.status == false) {
            error=data.error
            Swal.showValidationMessage(
              error
            )
          } else {
            x=true
          }
        })

    }
  },
  allowOutsideClick: () => !Swal.isLoading()
}).then(function(){
  if (x==true){
    Swal.fire({
      type:'info',
      title:'Verification Required!',
      text:'A link is sent to your email id. Please verify your account'
    })
  }
})

}
