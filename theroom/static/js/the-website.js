
var randint = function(min,max) {
    return Math.floor(Math.random()*(max-min+1)+min);
};

var offers = function(){
  var milliseconds = randint(5, 25) * 1000;
  var rand_offer = randint(0, $('.offer-img').length-1);

  setTimeout(function(){
    console.log('setTimeout');
    $($('.offer-img')[rand_offer])
        .css('opacity', '1')
        .css('visibility', 'visible');
    $('.overlay').css('visibility', 'visible');
  }, milliseconds);
};

var submitFeedback = function() {
  window.alert("Submitting feedback only works on Fridays from 2:30pm to 3:00pm Eastern.\nPlease come back later.");
};


var populateVerts = function() {
  var src = $('.verts-img').attr('src');
  var vertLength = $('.verts-img').length;
  for (var i = 0; i < vertLength; i++) {
    var r = randint(0, verts.length-1);
    var img = verts[r];
    $($('.verts-img')[i]).attr('src', src + '/' + img);
  }
};

var timeleft = 30;
var setTimeLeft = setInterval(function() {
  $('span.time-left').text(timeleft.toString());
  timeleft -= 1;
  if (timeleft < 0) {
    clearInterval(setTimeLeft);
    var session_key = location.search.split('?session_key=')[1];
    $.ajax({
      url: '/exit',
      data: {session_key: session_key}
    }).then(function(){
      location.href='http://localhost:8000/goodbye'});
  }
}, 1000);

var getWeather = function(){
  var weather = Math.ceil((Math.random() * 100) + 1);
  $('.weather-value').text(weather);
};

var getHoroscope = function () {
  $.ajax("https://horoscopes-and-astrology.com/json")
      .then(function(results) {
        var horoscopes = Object.keys(results.dailyhoroscope);
        var rand = randint(0, horoscopes.length - 1);
        var horoscope = results.dailyhoroscope[horoscopes[rand]].split('\<a')[0]
        $('.horoscope').html(horoscope);
      });
};

$(function() {
  getWeather();
  offers();
  getHoroscope();
  $('img.offer-img').click(function() {
    var to_error = to_error_or_not[randint(0, to_error_or_not.length-1)];
    $('.loader').css('visibility', 'visible');
    setTimeout(function(){
      $('.loader').css('visibility', 'hidden');
      if (to_error) {
        var rand_error = randint(0, errors.length-1);
        window.alert(errors[rand_error]);
      }
      $('.loader').css('visibility', 'hidden');
      $('.overlay').css('visibility', 'hidden');
      $('img.offer-img').css('visibility', 'hidden');
    }, 1000);

  });

  $('a.upgrade').click(function () {
    window.alert("Sorry. The Website has reached the upgrade limit this week.");
  });

  $('img.verts-img').click(function(){
        var rand_error = randint(0, errors.length-1);
        window.alert(errors[rand_error]);
  });
  populateVerts();
});
