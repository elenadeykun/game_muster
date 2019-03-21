$(document).ready(function(){
    console.log($('.screen-img'));
    $('.screen-img').each(function(i,elem){
        elem.src = $(this).data("url");
    });
});