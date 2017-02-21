(function($){
  $(function(){

    $('.button-collapse').sideNav();
    $('.parallax').parallax();
  }); // end of document ready
})(jQuery); // end of jQuery name space

$(document).ready(function(){
    $('.collapse').sideNav();
    $('.parallax').parallax();
  });

$(document).ready(function() {
    window.setTimeout("fadeMyDiv();", 3000); //call fade in 3 seconds
  });

function fadeMyDiv() {
    $("#myDiv").fadeOut('slow');
    $("#myDiv").fadeOut('slow');
};

$(function() {
    $('a#like').bind('click', function() {
      $.getJSON($SCRIPT_ROOT + '/ideas/likes', {
        likez: "like",
        idea_id: $('input[name="idea_id"]').val()
      }, function(data) {
        $("#result").text(data.result);
      });
      return false;
    });
  });

$(function() {
    $('a#dislike').bind('click', function() {
      $.getJSON($SCRIPT_ROOT + '/ideas/likes', {
        likez: "dislike",
        idea_id: $('input[name="idea_id"]').val()
      }, function(data) {
        $("#dresult").text(data.result);
      });
      return false;
    });
  });

$(function() {
    $('a#watchIt').bind('click', function() {
      $.getJSON($SCRIPT_ROOT + '/ideas/watchlist', {
        watchIt: "watchit",
        idea_id: $('input[name="idea_id"]').val()
      }, function(data) {
        $("#watchIt").text(data.watch);
      });
      return false;
    });
  });
