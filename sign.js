function seterror(id,error)
{
  element = document.getElementById(id)
  element.getElementsByClassName('error')[0].innerHTML = '* '+error
}

function clearerror(){
  errors = document.getElementsByClassName('error')
  for(var error in errors)
  {
    error.innerHTML = "";
  }
}

function validate()
{
    var val = true
    clearerror()

    // Validating Name
    var name = document.forms['sign-form']['name'].value
    if(name.length < 5){
      seterror("name","Please Provide Your Full Name")
      val = false
    }
    if(!/^[a-zA-Z ]+$/.test(name)){
      seterror("name","Use Alphabets Only")
      val = false
    } 

    // Validating Username
    var username = document.forms['sign-form']['username'].value
    if(!/^[a-zA-Z]+[a-zA-Z0-9_]*$/.test(username)){
      seterror("username","Username not available ")
    }

    // Validating Email
    var email = document.forms['sign-form']['email'].value
    if(!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)){
      seterror("email","Invalid Email Format")
      val = false
    }
    else if(email.length > 30){
      seterror("email","Invalid Email (Too long email address)")
      val = false
    }

    // Validating Password
    var pass1 = document.forms['sign-form']['pass1'].value
    if (pass1.length < 8) {
      seterror("password","Password must contain atleast 8 characters")
      val = false;
    }
    else if (!/[A-Z]/.test(pass1)) {
      seterror("password","Password must contain at least one uppercase letter")
      val = false;
    }
    else if (!/[a-z]/.test(pass1)) {
      seterror("password","Password must contain atleast one lowercase letter")
      val = false;
    }
    else if (!/\d/.test(pass1)) {
      seterror("password","Password must contain atleast one digit")
      val = false;
    }
    else if (!/[^a-zA-Z0-9]/.test(pass1)) {
      seterror("password","Password must contain atleast one special character(i.e #,&,etc.)")
      val = false;
    }

    // Validating Confirm Password
    var pass2 = document.forms['sign-form']['pass2'].value
    if (pass1 !== pass2) {
      seterror("password1","Passwords do not match")
      val = false;
    }

    return val
}