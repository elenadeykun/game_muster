$(document).ready(function(){

    $('form[name=login-form]').submit(function(event){
        event.preventDefault();
        console.log($('form[name=login-form]'));


        $.ajax({
            url: '/login',
            method: 'POST',
            data: $('form[name=login-form]').serialize(),
            dataType: 'json',
            success: function (data) {
                if(data.Errors){
                    var errors = document.getElementById("login-errors");
                    errors.innerHTML = data.Errors;
                } else {
                    $('a[name=close]')[0].click();
                    updateProfile(data.user);
                    showMessage(data.Status);
                }
            }
         });
    });

    $('form[name=register-form]').submit(function(event){
        event.preventDefault();

        $.ajax({
            url: '/registration',
            method: 'POST',
            data: $('form[name=register-form]').serialize(),
            dataType: 'json',
            success: function (data) {

                if(data.Errors){
                    var errors = document.getElementById("register-errors");
                    errors.innerHTML = data.Errors;
                } else {
                    $('a[name=close]')[0].click();
                    updateProfile(data.user);
                    showMessage(data.Status);
                }
            }
         });
    });

    $('a[name=logout').click( function(){

        $.ajax({
          url: '/logout',
          dataType: 'json',
          success: function (data) {
              $('form[name=profile-form]')[0].reset();
              showMessage(data.Status);
            }
         });
    });

    $('form[name=filter-form]').submit(function(event){
        event.preventDefault();

        $.ajax({
            url: '/filter',
            method: "GET",
            data: $('form[name=filter-form]').serialize(),
            dataType: 'json',
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

function updateProfile(user){
    document.getElementById('profile-username').value = user.username;
    document.getElementById('profile-email').value = user.email;
    document.getElementById('profile-last-name').value = user.last-name;
    document.getElementById('profile-first-name').value = user.first-name;
}