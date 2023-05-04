 //disabled sign up button
  var signUp_btn = document.querySelector(".signup");
  signUp_btn.disabled = true;
  signUp_btn.style.cursor = "not-allowed";
  const email = document.getElementById("email");
   
// function sendOTP(){
  const getOTP =document.getElementById("get-otp")
  getOTP.addEventListener("click",function(event){
    event.preventDefault();
    
  const otpVerify = document.getElementsByClassName("otp-container")[0];
  
   //opt generate
   let otp_val = Math.floor(Math.random()*10000);
   let emailBody = `
       <h1>welcome to EDEZE</h1><br>
       <p>Your OTP is: ${otp_val}</p>
   `;

   //email send code 
   Email.send({
      SecureToken : "1cf75330-7ceb-401e-871a-8f1d50032e31",
      To : email.value,
      From : "bikashkumarnayak807@gmail.com",
      Subject : "otp verification",
      Body : emailBody
    }).then(
      message => {
        if(message === "OK"){
          alert("otp send to email"+ email.value);

          otpVerify.style.display = "flex";
          const otpInput = document.getElementById("otp-field");
          var passwordContainer= document.querySelector(".password-container");
          msg = document.getElementById("message");
          otpInput.addEventListener("input",function(){
            if(otpInput.value.length == 4){
              if(otpInput.value == otp_val){
                msg.innerText = "otp is valid";
                passwordContainer.style.display = "flex";
                signUp_btn.disabled = false;
                signUp_btn.style.cursor = "pointer";
              }
              else{
                msg.innerText = "otp is invalid";
                otpInput.classList.add("shake");
                setTimeout(() => {
                  otpInput.classList.remove("shake");
                }, 500);
              }
            }
            else{
              passwordContainer.style.display = "none";
              signUp_btn.disabled = true;
              signUp_btn.style.cursor = "not-allowed";
            }
            
          });
          
        }
      }
    );
  })
  
// }

// const form  = document.getElementById("registerForm");
signUp_btn.addEventListener('click', function(event){
  event.preventDefault();
  
  const firstName = document.getElementById("firstName");
  const lastName = document.getElementById("lastName");
  const password = document.getElementById("password");

  fetch("http://127.0.0.1:8000/signup",{
    method: 'POST',
        headers: {
        'Content-Type': 'application/json' // Set the content type to JSON
        },
        body: JSON.stringify({
          "First_name": firstName,
          "Second_name": lastName,
          "Email": email,
          "Password": password
        })
  })
  .then(function(response) {
    if (!response.ok) {
    throw new Error('Network response was not ok');
    }
    return response.json(); // Parse the response body as JSON
})
.then(function(data) {
    // Handle the response data
    postdata = data;
    console.log(postdata.status);
    // alert(postdata.Data.status)
    if(postdata.status === "User created"){
        window.location.href = "login.html";
    }
})
.catch(function(error) {
    // Handle any errors that occurred during the request
    console.error('Error:', error);
    alert(error)
});
});














// const form  = document.getElementById("registerForm");
// signUp_btn.addEventListener('click', function(event){
//   event.preventDefault();
//   console.log("clicked");
// });



// function register(event){
//     event.preventDefault();
  
//     const emailInput = document.querySelector('#email');
//     const passwordInput= document.querySelector('#password');

//     const email = emailInput.value;
//     const password = passwordInput.value;
  
//     const data = {
//       email: email,
//       password: password
//     };
  
//     fetch('http://127.0.0.1:8000/signup', {
//       method: 'POST',
//       headers: {
//         'Content-Type': 'application/json'
//       },
//       body: JSON.stringify(data)
//     })
//     .then(response => {
      
//     })
//     .catch(error => {
//       console.log(error);
//     });
//   }