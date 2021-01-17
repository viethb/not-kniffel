{
    "use strict";

    var message_ele = document.getElementsByClassName("alert alert-success alert-dismissible fade show");

    setTimeout(function(){
        console.log("Hello");
        message_ele.style.display = "none";
    }, 1000);
}