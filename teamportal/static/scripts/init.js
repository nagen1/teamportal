
$(document).ready(function() {
    $('.collapse').sideNav();
    $('.parallax').parallax();
    $('.collapsible').collapsible();
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

$(function(){
    $("#autocomplete").autocomplete({
      source: function( request, response ) {
        $.getJSON($SCRIPT_ROOT + "/autcomplete", {
            search: request.term
        }, function( data ) {
            response( $.map( data.results, function( item ) {
                return {
                    label: item.label,
                    value: item.value
                }
            }));
        });
},
       select: function (event, ui) {
             $("#name").val(ui.item.label);
             $("#value").val(ui.item.value);
             return false;
       },
       focus: function(event, ui) {
        $("#autocomplete").val(ui.item.label);
        return false; // Prevent the widget from inserting the value.
       }
       //minLength: 3
   });
});
