
var goBack = function () {
  location.href="/"
};


var updateWaitingLinePosition = function(place_in_line) {
  if (place_in_line > 1) {
    $('.line-number-text').html("There are <span class='line-number'> " + place_in_line + "</span>" + " people ahead of you.");
  } else {
    $('.line-number-text').html("There is <span class='line-number'> " + place_in_line + "</span>" + " person ahead of you.");
  }
};



$(function() {
  offers();

});
