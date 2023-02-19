const form = document.getElementById('form');
const phone = document.getElementById('phone');
const name = document.getElementById('name');
const err_phone = document.getElementById('err_phone');
const err_name = document.getElementById('err_name');

// form valdition
form.addEventListener('submit', function (e) {

	// validate stage one check if fileds are empty
    if (validate_number()){

		e.preventDefault(); 
	    if (phone.value == '')
	    {
			err_phone.style.color = "red";
			err_phone.innerHTML = "يجب عليك ادخال رقمك";
			phone.style.borderColor = "red";
			e.preventDefault();

	    }

	    else
	    {
			err_phone.style.color = "";
			err_phone.innerHTML = "";
			phone.style.borderColor = "";
	    }

	    if (name.value == '')
	    {
			err_name.style.color = "red";
			err_name.innerHTML = "يجب عليك ادخال اسمك";
			name.style.borderColor = "red";
			e.preventDefault();

	    }

	    else
	    {
			err_name.style.color = "";
			err_name.innerHTML = "";
			name.style.borderColor = "";
	    }

    }

    else{
		e.preventDefault();
    }

});
function validate_number(){

	if (phone.value.length == 10 && phone.value[0] == 0  && !phone.value.match(/[A-Z]/i) || phone.value.length == 9 && phone.value[0] == 5 && !phone.value.match(/[A-Z]/i))
	{
		err_phone.style.color = "";
		err_phone.innerHTML = "";
		phone.style.borderColor = "";
		return true
	}

	else 
	{
		err_phone.style.color = "red";
		err_phone.innerHTML = "رقم الهاتف غير صحيح";
		phone.style.borderColor = "red";
		return false
	}

}