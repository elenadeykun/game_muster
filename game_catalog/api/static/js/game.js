$(document).ready(function(){
    $('.screen-img').each(function(i,elem){
        elem.src = $(this).data("url");
    });
});