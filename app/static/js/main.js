$(window).resize(function () {
   $('body').css('padding-top', parseInt($('nav').css("height")));
});

$(window).load(function () {
   $('body').css('padding-top', parseInt($('nav').css("height")));
});
$(document).ready(function(){
	$("nav li.disabled a").prop("disabled",true)
});
document.body.addEventListener('click', function (event) {
  // filter out clicks on any other elements
  if (event.target.nodeName == 'A' && event.target.getAttribute('aria-disabled') == 'true') {
    event.preventDefault();
  }
});