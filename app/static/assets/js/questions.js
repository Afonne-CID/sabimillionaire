window.addEventListener('load', function () {
  move()
});

var i = 0;
function move() {
  if (i == 0) {
    i = 1;
    var elem = document.getElementById("myBar");
    var width = 1;
    var id = setInterval(frame, 60);
    function frame() {
      if (width >= 100) {

        document.getElementById("next").click();

        clearInterval(id);
        i = 0;

      } else {
        width++;
        elem.style.width = width + "%";
      }
    }
  }
}


$('button#next').click(function (){
  console.log($('form#questions-form').serialize())
})

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