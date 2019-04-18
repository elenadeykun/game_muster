document.addEventListener("DOMContentLoaded", function(){

    var images = document.querySelectorAll(".screen-img");
    var links = [];

    if (images.length > 0){
        links = Array.prototype.slice.call(images).map((image) => image.src);
    }

    var galleryImage = document.querySelector(".gallery__image");

    for (var i = 0; i < images.length; i++){
        images[i].addEventListener("click", function(event){
        document.querySelector(".gallery__background").style.display = "flex";
        galleryImage.src = this.src;
      });
    }

    var prevBtn = document.querySelector('div[name=prev]');

    prevBtn.addEventListener("click", function(event){
    event.stopPropagation();
        var index = links.indexOf(galleryImage.src);
      if(index > 0){
        galleryImage.src = links[index - 1];
      } else {
        galleryImage.src = links[links.length- 1];
      }
    });

    var nextBtn = document.querySelector('div[name=next]');

    nextBtn.addEventListener("click", function(event){
        event.stopPropagation();
        var index = links.indexOf(galleryImage.src);
      if(index === links.length - 1){
        galleryImage.src = links[0];
      } else {
        galleryImage.src = links[index + 1];
      }
    });

    var galleryBackground = document.querySelector(".gallery__background");
    galleryBackground.addEventListener("click", function(event){
        this.style.display = "none";
    });

});


