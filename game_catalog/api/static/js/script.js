$(document).ready(function(){
    $('.game__img').each(function(i,elem){
        if($(this).data("url")){
            elem.src = $(this).data("url");
        }
    });

    $('form[name=login-form]').submit(function(event){
        event.preventDefault();

        $.ajax({
            url: '/login',
            method: 'POST',
            data: $('form[name=login-form]').serialize(),
            dataType: 'json',
            success: function (data) {
               $('a[name=close]')[0].click();
            }
         });
    });

    $('a[name=logout').click( function(){

        $.ajax({
          url: '/logout',
          dataType: 'json',
          success: function (data) {
              alert(data.stat);
            }
         });
    });

    $('form[name=filter-form]').submit(function(event){
        event.preventDefault();

        $.ajax({
            url: '/ajax/filter',
            method: "GET",
            data: $('form[name=filter-form]').serialize(),
            dataType: 'json',
            success: function (data) {
               games = data.games;
               games_container = document.getElementById("games");
               // ???
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

    console.log(gameData.id);
    game.appendChild(img);
    return game;
}
