document.addEventListener("DOMContentLoaded", function(){

    document.querySelector("form[name=login-form").addEventListener("submit", function(event){
        event.preventDefault();

         var xhr = new XMLHttpRequest();
         xhr.open("POST", "/login", true);
         var data = new FormData(this);
         xhr.send(data);

         xhr.onreadystatechange = function() {
             if (xhr.readyState != 4) {return;}

             if (xhr.status == 200) {
                var response =  JSON.parse(xhr.responseText);

                if(response.Errors){
                    var errors = document.getElementById("login-errors");
                    errors.innerHTML = response.Errors;
                } else {
                    document.querySelector("a[name=close").click();
                    updateProfile(response.user);
                    showMessage(response.Status);
                }
             }
         };
    });

    document.querySelector("form[name=register-form").addEventListener("submit", function(event){
        event.preventDefault();

        var xhr = new XMLHttpRequest();
        xhr.open("POST", "/registration", true);
        var data = new FormData(this);
        xhr.send(data);

        xhr.onreadystatechange = function() {
            if (xhr.readyState != 4) {return;}

            if (xhr.status == 200) {
               var response =  JSON.parse(xhr.responseText);

               if(response.Errors){
                   var errors = document.getElementById("register-errors");
                   errors.innerHTML = response.Errors;
               } else {
                   document.querySelector("a[name=close]").click();
                   updateProfile(response.user);
                   showMessage(response.Status);
               }
            }
        };
    });


    document.querySelector("a[name=logout]").addEventListener("click", function(event){

        var xhr = new XMLHttpRequest();
        xhr.open("GET", "/logout", true);
        var data = new FormData(this);
        xhr.send(data);

        xhr.onreadystatechange = function() {
            if (xhr.readyState != 4) {return;}

            if (xhr.status == 200) {
               var response =  JSON.parse(xhr.responseText);
               showMessage(response.Status);
               document.querySelector(".username").innerText = "";
               changeMenuVisibility(false);
            }
        };
    });

    document.querySelector("form[name=filter-form").addEventListener("submit", function(event){
        event.preventDefault();

        /*var xhr = new XMLHttpRequest();
        xhr.open('GET', '/filter', true);
        var data = new FormData(this);
        xhr.send(data);

        xhr.onreadystatechange = function() {
            if (xhr.readyState != 4) return;

            if (xhr.status == 200) {
               var response =  JSON.parse(xhr.responseText);

               if(response.Errors){
                   var errors = document.getElementById("register-errors");
                   errors.innerHTML = response.Errors;
               } else {
                   games = JSON.parse(xhr.responseText).games;
                   games_container = document.getElementById("games");
                   games_container.innerHTML= "";
                   fragment = document.createDocumentFragment();
                   games.forEach(function(elem, i){
                        game = createGameElement(elem);
                        fragment.appendChild(game);
                    })
                   games_container.appendChild(fragment);
                   document.querySelector('a[name=close').click();
               }
            }
        }*/

        $.ajax({
            url: "/filter",
            method: "GET",
            data: $("form[name=filter-form]").serialize(),
            dataType: "json",
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
               document.querySelector("a[name=close]").click();
            }
         });
    });

});


function updateProfile(user){
    "use strict";
    document.getElementById("profile-username").value = user.username;
    document.getElementById("profile-email").value = user.email;
    document.getElementById("profile-last-name").value = user.last-name;
    document.getElementById("profile-first-name").value = user.first-name;
    document.querySelector(".username").innerText = user.username;

    changeMenuVisibility(true);

}

function changeMenuVisibility(isAuth){
    if (isAuth){
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