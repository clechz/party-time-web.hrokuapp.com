const form = document.getElementById('form');
const email = document.getElementById('email');
const password = document.getElementById('password');
const err_password = document.getElementById('err_password');
const err_email = document.getElementById('err_email');
const strength = document.getElementById('strength');

form.addEventListener('submit', (e) => {

    if (password.value == '')
    {
		err_password.style.color = "red"
		err_password.innerHTML = "يجب عليك إدخال كلمة مرور";
		password.style.borderColor = "red";
		e.preventDefault()

    }
    else
    {
		err_password.style.color = ""
		err_password.innerHTML = "";
		password.style.borderColor = "";
    }
    if (email.value == '')
    {
		err_email.style.color = "red"
		err_email.innerHTML = "يجب عليك إدخال بريد إلكتروني";
		email.style.borderColor = "red";
		e.preventDefault()

    }
    else
    {
		err_email.style.color = "";
		err_email.innerHTML = "";
		email.style.borderColor = "";
    }

})