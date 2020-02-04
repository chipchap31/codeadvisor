
var dialog = (function(){
  "use strict";

  function open(id){
    var target = document.getElementById(id);
    target.classList.add('open')
  }
  function close(id){
    var target = document.getElementById(id);
    target.classList.remove('open')
  }
  return { open, close }

})()
