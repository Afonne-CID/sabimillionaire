window.addEventListener('load', function () {
  progressBar()
});

var animationTimeInMiliseconds = 10000; //30s 
var interval = 100;
var elem = document.getElementById("myBar");
var beginningDate = new Date().getTime(); // Time in miliseconds

function progressBar() {
  resetProgressBar();

  id = setInterval(frame, interval);

  function frame() {
  var milisecondsFromBegin = new Date().getTime() - beginningDate;
  var width = Math.floor(milisecondsFromBegin / animationTimeInMiliseconds * 100);
  elem.style.width = width + "%";

    if (width >= 100) {
      document.getElementById("next").click();
      clearInterval(id);
    }
  }
}
function resetProgressBar() {

  elem.style.width = 0;
}

// var i = 0;
// var interval = 60;
// var animationTimeInMiliseconds = 10000;
// var beginningDate = new Date().getTime();

// function progressBar() {
//   if (i == 0) {
//     i = 1;
//     var elem = document.getElementById("myBar");
//     var width = 1;
//     var id = setInterval(frame, interval);
//     function frame() {
//       if (width >= 100) {

//         document.getElementById("next").click();
//         clearInterval(id);
//         i = 0;

//       } else {
//         width++;
//         elem.style.width = width + "%";
//       }
//     }
//   }
// }

// $('button#next').click( function(e) {
//   e.preventDefault();
//     console.log($('form#questions-form').serialize())
//     $.ajax({
//         url: '/free-trivia',
//         type: 'POST',
//         dataType: 'json',
//         data: $('form#questions-form').serialize(),
//         success: function() {
//                   console.log('worked!')
//                 }
//     });
// });