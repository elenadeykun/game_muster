$(document).ready(function(){
    $('.game__img').each(function(i,elem){

        if($(this).data("url")){
            elem.src = $(this).data("url");
        }
    });
});