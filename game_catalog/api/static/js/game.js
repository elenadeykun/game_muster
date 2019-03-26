document.addEventListener("DOMContentLoaded", function(){
    var images = document.getElementsByClassName("screen-img");

    for (var i = 0; i < images.length; i++) {
        images[i].src = images[i].dataset.url;
    }
})