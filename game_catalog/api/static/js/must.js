"use strict";

document.addEventListener("DOMContentLoaded", function(){

    var removeLinks = document.querySelectorAll("a[name=remove]");

    for (var i = 0; i < removeLinks.length; i++) {
        removeLinks[i].addEventListener("click", function(event){
            event.preventDefault();

            var link = $(this);
            var href = this.href;

            var xhr = new XMLHttpRequest();
            xhr.open("GET", this.href, true);
            xhr.send();

            xhr.onreadystatechange = function() {
            if (xhr.readyState != 4) {return;}

            if (xhr.status == 200) {
               var response =  JSON.parse(xhr.responseText);
                if (href.match("remove-must")){
                    href =href.replace("remove-must", "create-must");
                    link.addClass("remust-link");
                    link.text("ReMUST");
                    link.attr("href", href);
               } else {
                    href =href.replace("create-must", "remove-must");
                    link.removeClass("remust-link");
                    link.text("UnMUST");
                    link.attr("href", href);
               }
               showMessage(response.Status);
            }
        };
    })};
});
