"use strict";

document.addEventListener("DOMContentLoaded", function(){

   var logout = document.querySelector("a[name=logout]");

   if (logout){
        logout.addEventListener("click", function(event){

        createQuery("GET", "/logout", function(response){
            document.location.reload(true);
        });
    });
  }

    document.querySelector("form[name=filter-form]").addEventListener("submit", function(event){
        event.preventDefault();
        document.querySelector('input[name=filter-page]').value = 0;
        document.getElementById("games").dataset.filter = true;
        sendFilterQuery();
    });
});

function sendFilterQuery(){

    createQuery("POST", "/filter/", function(response){
            var games = response.games;
            var gamesContainer = document.getElementById("games");
            document.querySelector("input[name=filter-search-string]").value = document.getElementById("search-field").value;

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
