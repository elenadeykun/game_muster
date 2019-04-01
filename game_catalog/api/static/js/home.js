"use strict";

window.onscroll = function() {
    if(window.pageYOffset + window.innerHeight >= document.body.clientHeight){
        var gamesContainer = document.getElementById("games");

        if (gamesContainer.dataset.filter === "true"){
            sendFilterQuery();
        } else {
            var page = parseInt(gamesContainer.dataset.page);


            createQuery("GET","/get-particle-games/" + page, function(response){
                var games = response.games;
                if(games){
                    var fragment = document.createDocumentFragment();
                    games.forEach(function(elem, i){
                        var game = createGameElement(elem);
                        fragment.appendChild(game);
                    })
                    gamesContainer.appendChild(fragment);
                }
            });
        }

        gamesContainer.dataset.page = page + 1;
    }
}

document.addEventListener("DOMContentLoaded", function(){

     document.getElementById("search-field").addEventListener("keydown", function(event){
        var ENTER_KEY_CODE = 13;

        if (event.keyCode === ENTER_KEY_CODE) {
            getGamesBySearch();
         }
     });

     var search = document.querySelector("button[name=search]");
     search.addEventListener('click', function(event){
        getGamesBySearch();
    });

    var elem = document.querySelector('input[type="range"]');

    var rangeValue = function(){
      var newValue = elem.value;
      var target = document.querySelector('.value');
      target.innerHTML = newValue;
    }

    elem.addEventListener("input", rangeValue);
});

function getGamesBySearch(){
     if(!document.getElementById("search-field").value){
            showMessage("Search string is empty.");
     } else {
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
     }
}