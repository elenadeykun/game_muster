"use strict";

document.addEventListener("DOMContentLoaded", function(){

   var logout = document.querySelector("a[name=logout]");

   if (logout){
        logout.addEventListener("click", function(event){

        createQuery("GET", "/logout", function(response){
            showMessage(response.Status);
            document.querySelector(".username").innerText = "";
            changeMenuVisibility();

            if(window.location.href.indexOf("must") > -1) {
                window.location = "/";
            }
        });
    });
  }

    document.querySelector("form[name=filter-form").addEventListener("submit", function(event){
        event.preventDefault();
        document.getElementById("games").dataset.filter = true;
        sendFilterQuery();
    });
});

function sendFilterQuery(){

    createQuery("POST", "/filter/", function(response){
            var games = response.games;
            var gamesContainer = document.getElementById("games");
            console.log(parseInt(document.querySelector('input[name=filter-page]').value));
            if (parseInt(document.querySelector('input[name=filter-page]').value) === 0 ){
                gamesContainer.innerHTML= "";
            }
            var fragment = document.createDocumentFragment();
            if(games){
                for(var i = 0; i < games.length; i++){
                    var game = createGameElement(games[i]);
                    fragment.appendChild(game);
                }
            }
            gamesContainer.appendChild(fragment);
            document.querySelector("a[name=close]").click();
            var filterPage = document.querySelector('input[name=filter-page]');
            filterPage.value = parseInt(filterPage.value) + 1;
        }, new FormData(document.querySelector("form[name=filter-form")));
}


function changeMenuVisibility(){

   document.querySelector('a[name=logout]').remove();
   document.querySelector('a[name=profile-link').remove();
   document.querySelector('.bookmarks').remove();

   var menu = document.querySelector('.dropdown-menu__container');

   var loginLink = document.createElement("a");
   loginLink.classList.add("dropdown-menu__item");
   loginLink.name = "login-link";
   loginLink.href = "/login";
   loginLink.innerText = "Log in";

   var registerLink = loginLink.cloneNode();
   registerLink.href = "/registration";
   registerLink.innerText = "Sign up";

   menu.appendChild(loginLink);
   menu.appendChild(registerLink);
}