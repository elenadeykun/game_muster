$(document).ready(function(){

    $('a[name=remove]').click(function(event){
        event.preventDefault();
        var link = $(this);
        var href = $(this).attr('href');
        $.ajax({
          url: $(this).attr('href'),
          dataType: 'json',
          success: function (data) {

               if (href.match('remove-must')){
                    href =href.replace('remove-must', 'create-must');
                    link.addClass('remust-link');
                    link.text('ReMUST');
                    link.attr('href', href);
               } else {
                    href =href.replace('create-must', 'remove-must');
                    link.removeClass('remust-link');
                    link.text('UnMUST');
                    link.attr('href', href);
               }
               showMessage(data.Status);
            }
         });
    });

});
