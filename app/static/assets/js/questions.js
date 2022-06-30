window.addEventListener('load', function (e) {
  var url_endpoint = e.target.location.href.split('/')[3];
  progressBar(url_endpoint);
})

var interval = 100;
var elem = document.getElementById("myBar");
var beginningDate = new Date().getTime(); // Time in miliseconds

function progressBar(url_endpoint) {

    if (url_endpoint == 'free-trivia'){
      var animationTimeInMiliseconds = 30000; //30s
    }else{
      var animationTimeInMiliseconds = 10000; //10s
    }

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
