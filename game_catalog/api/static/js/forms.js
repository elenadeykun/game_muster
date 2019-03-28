"use strict";

document.addEventListener("DOMContentLoaded", function(){

    document.querySelector("a[name=logout]").addEventListener("click", function(event){

        createQuery("GET", "/logout", function(response){
            showMessage(response.Status);
            document.querySelector(".username").innerText = "";
            changeMenuVisibility();
        });
    });

    document.querySelector("form[name=filter-form").addEventListener("submit", function(event){
        event.preventDefault();
        createQuery("POST", "/filter/", function(response){
            var games = response.games;
            var gamesContainer = document.getElementById("games");
            gamesContainer.innerHTML= "";
            var fragment = document.createDocumentFragment();
            for(var i = 0; i < games.length; i++){
                var game = createGameElement(games[i]);
                fragment.appendChild(game);
            }
            gamesContainer.appendChild(fragment);
            document.querySelector("a[name=close]").click();
        }, new FormData(this));
    });
});

function changeMenuVisibility(){
    if (document.querySelector("a[name=logout]").classList.contains("hidden")){
         document.querySelector("a[name=login-link]").classList.add("hidden");
         document.querySelector("a[name=register-link]").classList.add("hidden");
         document.querySelector("a[name=profile-link]").classList.remove("hidden");
         document.querySelector("a[name=logout]").classList.remove("hidden");
    } else {
        document.querySelector("a[name=login-link]").classList.remove("hidden");
        document.querySelector("a[name=register-link]").classList.remove("hidden");
        document.querySelector("a[name=profile-link]").classList.add("hidden");
        document.querySelector("a[name=logout]").classList.add("hidden");
    }
}