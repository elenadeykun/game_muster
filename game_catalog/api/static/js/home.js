"use strict";

window.onscroll = function() {
    if(window.pageYOffset + window.innerHeight >= document.body.clientHeight){
        var gamesContainer = document.getElementById("games");
        var page = parseInt(gamesContainer.dataset.page);

        createQuery("GET","/get-particle-games/" + page, function(response){
            var games = response.games;
            var fragment = document.createDocumentFragment();
            games.forEach(function(elem, i){
                 var game = createGameElement(elem);
                 fragment.appendChild(game);
            })
            gamesContainer.appendChild(fragment);
        });

        gamesContainer.dataset.page = page + 1;
    }
}

document.addEventListener("DOMContentLoaded", function(){
     var search = document.querySelector("button[name=search]");
     search.addEventListener('click', function(event){
        createQuery("GET", "/search/" + document.getElementById("search-field").value, function(response){
            var games = response.games;
            var gamesContainer = document.getElementById("games");
            gamesContainer.innerHTML= "";
            var fragment = document.createDocumentFragment();
            for (var i = 0; i < games.length; i++){
                 var game = createGameElement(games[i]);
                 fragment.appendChild(game);
            }
            gamesContainer.appendChild(fragment);
        });
    });
});