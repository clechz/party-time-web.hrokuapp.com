const content = document.querySelector(".content")
const loader = document.querySelector(".loader")

content.style.display = "none !important"
document.addEventListener("load", function () {
	loader.style.display = "none !important"
	content.style.display = "block !important"

});