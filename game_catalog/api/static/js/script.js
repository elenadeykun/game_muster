document.addEventListener("DOMContentLoaded", function(){

    var gameImages = document.getElementsByClassName("game__img");

    for (var i = 0; i < gameImages.length; i++) {
        if(gameImages[i].dataset.url){
            gameImages[i].src = gameImages[i].dataset.url;
        }
    }

    var createLinks = document.querySelectorAll("a[name=create]");

    for (var i = 0; i < createLinks.length; i++) {
        createLinks[i].addEventListener("click", function(event){
             event.preventDefault();

             var xhr = new XMLHttpRequest();
             xhr.open("GET", this.href, true);
             xhr.send();

             xhr.onreadystatechange = function() {
                 if (xhr.readyState != 4) return;

                 if (xhr.status == 200) {
                      showMessage(JSON.parse(xhr.responseText).Status);
                 }
             }
        });
    }

    var search = document.querySelector("a[name=search]");
    search.addEventListener('click', function(){
        event.preventDefault();

       /* var xhr = new XMLHttpRequest();
        xhr.open('GET', this.href, true);
        var data = {'search_string' : document.getElementById('search-field').value};
        xhr.send(data);

        xhr.onreadystatechange = function() {
             if (xhr.readyState != 4) return;

             if (xhr.status == 200) {
               games = JSON.parse(xhr.responseText).games;
               games_container = document.getElementById("games");
               games_container.innerHTML= "";
              
               fragment = document.createDocumentFragment();
               games.forEach(function(elem, i){
                    game = createGameElement(elem);
                    fragment.appendChild(game);
               })
               games_container.appendChild(fragment);
             /*
               gamesContainer = document.getElementById("games");
               gamesContainer.innerHTML= "";
               fragment = document.createDocumentFragment();
               gamesContainer.appendChild(fragment);
               games = JSON.parse(xhr.responseText).games;

               for (var i = 0; i < games.length; i++){
                    game = createGameElement(games[i]);
                    fragment.appendChild(game);
               }

               gamesContainer.appendChild(fragment);
             }
        }*/

        $.ajax({
          url: $(this).attr("href"),
          method: "GET",
          dataType: "json",
          data: {"search_string" : document.getElementById("search-field").value},
          success: function (data) {
               games = data.games;
               games_container = document.getElementById("games");
               games_container.innerHTML= "";
               fragment = document.createDocumentFragment();
               games.forEach(function(elem, i){
                    game = createGameElement(elem);
                    fragment.appendChild(game);
               })
               games_container.appendChild(fragment);
          }
         });
    });
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
    title.classList.add("game__title")
    title.textContent = gameData.name;

    var linkContainer = document.createElement("p");
    var link = document.createElement("a");
    link.classList.add("game__link");
    link.href = "game/" + gameData.id;
    link.textContent = "Open";
    linkContainer.appendChild(link);
    var mustLink = link.cloneNode();
    mustLink.href = "#" ;
    mustLink.textContent = "Must";
    linkContainer.appendChild(mustLink);

    description.appendChild(title);
    description.appendChild(linkContainer);
    game.appendChild(description);
    var img = document.createElement("img");
    img.classList.add("game__img");

    if(!!gameData.screenshots){
       img.src = gameData.screenshots[0].url;
    } else {
       img.src = "/static/media/no-image.png";
    }

    game.appendChild(img);
    return game;
}
