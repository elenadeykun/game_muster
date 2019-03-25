$(document).ready(function(){
    $('.game__img').each(function(i,elem){
        if($(this).data("url")){
            elem.src = $(this).data("url");
        }
    });


    $('a[name=create]').click(function(event){
        event.preventDefault();
        $.ajax({
          url: $(this).attr('href'),
          dataType: 'json',
          success: function (data) {
              showMessage(data.Status);
          }
         });
    });

});

function showMessage(text){
    var message = document.createElement('div');
    message.classList.add("message-box");
    message.classList.add("tooltip");

    var messageText = document.createElement('h4');
    messageText.textContent = text;
    message.appendChild(messageText);

    var main = document.getElementsByTagName('main');
    main[0].appendChild(message);
    setTimeout(function (message){
               message.parentNode.removeChild(message);
               }, 3000, message);
}



function createGameElement(gameData){
    game = document.createElement('div');
    game.classList.add('game__container');
    description = document.createElement('span');
    description.classList.add('game__body');

    title = document.createElement('h4');
    title.classList.add('game__title')
    title.textContent = gameData.name;

    linkContainer = document.createElement('p');
    link = document.createElement('a');
    link.classList.add('game__link');
    link.href = "game/" + gameData.id;
    link.textContent = 'Open';
    linkContainer.appendChild(link);
    mustLink = link.cloneNode();
    mustLink.href = "#" ;
    mustLink.textContent = 'Must';
    linkContainer.appendChild(mustLink);

    description.appendChild(title);
    description.appendChild(linkContainer);
    game.appendChild(description);
    img = document.createElement("img");
    img.classList.add("game__img");

    if(!!gameData.screenshots){
       img.src = gameData.screenshots[0].url;
    } else {
       img.src = "/static/media/pacman.jpg";
    }

    game.appendChild(img);
    return game;
}

window.onscroll = function() {
    if($(window).scrollTop()+$(window).height()>=$(document).height()){
        var gamesContainer = document.getElementById('games');
        var page = parseInt(gamesContainer.dataset.page);

         $.ajax({
            url: '/get-particle-games/' + page,
            method: 'GET',
            dataType: 'json',
            success: function (data) {
               games = data.games;
               fragment = document.createDocumentFragment();
               games.forEach(function(elem, i){
                    game = createGameElement(elem);
                    fragment.appendChild(game);
               })
               gamesContainer.appendChild(fragment);
            }
         });

         gamesContainer.dataset.page = page + 1;
    }
}
