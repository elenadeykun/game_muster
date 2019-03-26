window.onscroll = function() {
    if(window.pageYOffset + window.innerHeight >= document.body.clientHeight){
        var gamesContainer = document.getElementById("games");
        var page = parseInt(gamesContainer.dataset.page);

         $.ajax({
            url: "/get-particle-games/" + page,
            method: "GET",
            dataType: "json",
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