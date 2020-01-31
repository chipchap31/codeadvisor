document.addEventListener("DOMContentLoaded", function () {
    // listen for select_wraps

    var select_wrap = Array.from(document.getElementsByClassName('select_wrap'));

    for (var i = 0; i < select_wrap.length; i++) {

        // get elements 

        var options = select_wrap[i].getElementsByTagName("select")[0]

        console.log(options)

    }


})
