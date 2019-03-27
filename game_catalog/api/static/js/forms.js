"use strict";

document.addEventListener("DOMContentLoaded", function(){

    document.querySelector("form[name=login-form]").addEventListener("submit", function(event){
        event.preventDefault();
        createQuery("POST", "/login", function(response){
            if(response.Errors){
               var errors = document.getElementById("login-errors");
               errors.innerHTML = response.Errors;
            } else {
               document.querySelector("a[name=close").click();
               updateProfile(response.user);
               showMessage(response.Status);
            }
         }, new FormData(this));

    });

    document.querySelector("form[name=register-form").addEventListener("submit", function(event){
        event.preventDefault();
        createQuery("POST", "/registration", function(response){
            if(response.Errors){
                   var errors = document.getElementById("register-errors");
                   errors.innerHTML = response.Errors;
            } else {
                   document.querySelector("a[name=close]").click();
                   updateProfile(response.user);
                   showMessage(response.Status);
            }
        }, new FormData(this));
    });

    document.querySelector("a[name=logout]").addEventListener("click", function(event){

        createQuery("GET", "/logout", function(response){
            showMessage(response.Status);
            document.querySelector(".username").innerText = "";
            changeMenuVisibility(false);
        });
    });

    document.querySelector("form[name=filter-form").addEventListener("submit", function(event){
        event.preventDefault();
        createQuery("POST", "/filter/", function(response){
            var games = response.games;
            var gamesContainer = document.getElementById("games");
            gamesContainer.innerHTML= "";
            var fragment = document.createDocumentFragment();
            for(var i = 0; i < games.length; i++){
                var game = createGameElement(games[i]);
                fragment.appendChild(game);
            }
            gamesContainer.appendChild(fragment);
            document.querySelector("a[name=close]").click();
        }, new FormData(this));
    });
});


function updateProfile(user){
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