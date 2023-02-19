const form = document.getElementById('form');
const email = document.getElementById('email');
const password = document.getElementById('password');
const repassword = document.getElementById('repassword');
const strength = document.getElementById('strength');
const err_email = document.getElementById('err_email');
const err_password = document.getElementById('err_password');
const err_repassword = document.getElementById('err_repassword');

// form valdition
form.addEventListener('submit', function(e){

	if(!password_strength()){
		e.preventDefault();
	}
	if(password.value != repassword.value){
		err_repassword.style.color = "red";
		err_repassword.innerHTML = "كلمات المرور لا تتطابق الرجاء اعادة المحاولة";
		repassword.style.borderColor = "red";
		e.preventDefault();		
	}

    else
    {
		err_repassword.style.color = "";
		err_repassword.innerHTML = "";
		repassword.style.borderColor = "";
	}


    if (password.value == '')
    {
		err_password.style.color = "red";
		err_password.innerHTML = "يجب عليك ادخال كلمة مرور";
		password.style.borderColor = "red";
		e.preventDefault();

    }
    else
    {
		err_password.style.color = "";
		err_password.innerHTML = "";
		password.style.borderColor = "";
	}

    if (email.value == '')
    {
		err_email.style.color = "red";
		err_email.innerHTML = "يجب عليك ادخال بريد إلكتروني";
		email.style.borderColor = "red";
		e.preventDefault();

    }
    else
    {
		err_email.style.color = "";
		err_email.innerHTML = "";
		email.style.borderColor = "";
	}

    if (repassword.value == '')
    {
		err_repassword.style.color = "red";
		err_repassword.innerHTML = "يجب عليك ادخال كلمة مرور(مرة أخرى)";
		repassword.style.borderColor = "red";
		e.preventDefault();

    }

    else
    {
		err_repassword.style.color = "";
		err_repassword.innerHTML = "";
		repassword.style.borderColor = "";
	}

});

// password strength func
function password_strength()
{
	if (password.value.length <= 1)
	{
		strength.innerHTML = "";
		password.style.borderColor = "";

	}
	if (password.value.length < 6)
	{
		strength.innerHTML = "ضعيفة";
		strength.style.color = "red";
		password.style.borderColor = "red";
		return false
	}
	if (password.value.length >= 6 )
	{
		strength.innerHTML = "جيدة";
		strength.style.color = "gold";
		password.style.borderColor = "gold";
		return true
	}
	if (password.value.length > 8 && password.value.match(/[A-Z]/i) && password.value.match(/\d/))
	{
		strength.innerHTML = "قوية";
		strength.style.color = "green";
		password.style.borderColor = "green";
		return true

	}

}