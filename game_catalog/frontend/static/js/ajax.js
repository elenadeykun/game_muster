var SUCCESS_STATUS_CODE = 200;
var READY_STATE_STATUS = 4;

function createQuery(method, url, handler, data){
    var xhr = new XMLHttpRequest();
    xhr.open(method, url, true);
    xhr.send(data);

    xhr.onreadystatechange = function() {
        if (xhr.readyState !== READY_STATE_STATUS) {return;}

        if (xhr.status === SUCCESS_STATUS_CODE) {
            var response =  JSON.parse(xhr.responseText);
            handler(response);
        }
    };
}