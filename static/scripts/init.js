(function($){
  $(function(){

    $('.button-collapse').sideNav();
    $('.parallax').parallax();
  }); // end of document ready
})(jQuery); // end of jQuery name space

$(document).ready(function(){
    // the "href" attribute of .modal-trigger must specify the modal ID that wants to be triggered
    $('.modal-trigger').leanModal();
  });

$(document).ready(function() {
    window.setTimeout("fadeMyDiv();", 3000); //call fade in 3 seconds
  });

function fadeMyDiv() {
    $("#myDiv").fadeOut('slow');
    $("#myDiv").fadeOut('slow');
};