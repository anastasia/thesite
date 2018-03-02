var getlinenumber = function () {
  $.ajax({
    url: '/getsession',
    success: function(results) {
      // console.log("results are!", results);
    }
  })
};
var welcome = function () {
  // setTimeout(getlinenumber, 1000);
  console.log("welcome!");
};
$(function () {
  // getlinenumber();

  welcome();
});
