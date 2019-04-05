"use strict";

document.addEventListener("DOMContentLoaded", function(){

    var gameImages = document.getElementsByClassName("game__img");

    for (var i = 0; i < gameImages.length; i++) {
        if(gameImages[i].dataset.url){
            gameImages[i].src = gameImages[i].dataset.url;
        }
    }
});

function showMessage(text){
    var message = document.createElement("div");
    message.classList.add("message-box");
    message.classList.add("tooltip");

    var messageText = document.createElement("h4");
    messageText.textContent = text;
    message.appendChild(messageText);

    var main = document.getElementsByTagName("main");
    main[0].appendChild(message);
    setTimeout(function (message){
               message.parentNode.removeChild(message);
               }, 3000, message);
}

function createGameElement(gameData){
    var game = document.createElement("div");
    game.classList.add("game__container");
    var description = document.createElement("span");
    description.classList.add("game__body");

    var title = document.createElement("h4");
    title.classList.add("game__header")
    title.textContent = gameData.name;

    var linkContainer = document.createElement("p");
    var link = document.createElement("a");
    link.classList.add("game__link");
    link.href = "game/" + gameData.id;
    link.textContent = "Open";
    var mustLink = document.createElement("button");
    mustLink.classList.add("game__must");
    mustLink.dataset.action = "/create-must/" + gameData.id ;
    mustLink.textContent = "Must";
    mustLink.name = "create";
    mustLink.addEventListener("click", function(event){
        createMust(this);
    });
    linkContainer.appendChild(mustLink);

    description.appendChild(title);
    description.appendChild(linkContainer);
    description.appendChild(link);
    game.appendChild(description);
    var img = document.createElement("img");
    img.classList.add("game__img");

    if(!!gameData.image__url){
       img.src = gameData.image__url;
    } else {
       img.src = "/static/media/no-image.png";
    }

    game.appendChild(img);
    return game;
}

function createMust(must){
    if (must.dataset.action.localeCompare("/login") === 0){
        window.location = must.dataset.action;
    } else {
        createQuery("GET", must.dataset.action, function(response){
            showMessage(response.Status);
        });
    }
}
