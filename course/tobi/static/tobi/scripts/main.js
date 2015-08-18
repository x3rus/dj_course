$(function() {

    // nothing
    console.log("nothing")

$('#static_map').hide();
$('#form-info').hide();

// Submit post on submit
$('#post-activity').on('submit', function(event){
    event.preventDefault();
    console.log("form submitted gpx file!")  // sanity check
    get_file_as_base64_and_upload('id_gpxfile');
});

//display file contents
function get_file_as_base64_and_upload(id_element) {
    //get file object
    var file = document.getElementById(id_element).files[0];
    var file_data;
    if (file) {
        // create reader
        var reader = new FileReader();
        reader.readAsText(file);
        // TODO : avoir de l'explication je comprend que onload est un event 
        // http://www.w3.org/TR/FileAPI/#dfn-loadstart-event , est-ce qu'il y a une
        // autre methode que l'appel de la functione ?!?!
        reader.onload = function(e) {
            // browser completed reading file - display it
            //alert(e.target.result);
            $.base64.utf8encode = true;
            file_data = $.base64.btoa(e.target.result);
            upload_gpx_datafile(file_data,id_element)
        };


    }
}

function upload_gpx_datafile(gpsfile_data,id_fileType) {
// AJAX for sending gpxfile
    console.log("sending file to backend!") // sanity check
//##    var data = new FormData($('form').get(0));
    $.ajax({
        // TODO voir pour avoir une plus belle URL lors de l'appel de la cmd json
       url : "../json_upload_gpsfile/", // the endpoint
       type : "POST", // http method
       data : { the_gpxfile: $('#'+id_fileType).val() ,
                the_gpxfile_data: gpsfile_data  }, // data sent with the post request

       // handle a successful response
       success : function(json) {
               $('#id_datePerformed').val(json.start_time);// remove the value from the input
               $('#id_distance').val(json.length);// remove the value from the input
               $('#id_description').val(json.description);// remove the value from the input
               $('#id_title').val(json.title);// remove the value from the input
               $('#static_map').show();
               $('#form-info').show();
               $("#url_static_map").attr("src",json.url_map);
               console.log(json); // log the returned json to the console
       },

       // handle a non-successful response
       error : function(xhr,errmsg,err) {
           console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
           console.log(errmsg); // provide a bit more info about the error to the console
       }
    });



} //FIN upload_gpx_datafile 


function upload_gpx_file() {
}




 
// #################################
// Create cookie for CSRF  token 
// #################################

// This function gets cookie with a given name
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
var csrftoken = getCookie('csrftoken');

/*
The functions below will create a header with csrftoken
*/

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
function sameOrigin(url) {
    // test that a given url is a same-origin URL
    // url could be relative or scheme relative or absolute
    var host = document.location.host; // host + port
    var protocol = document.location.protocol;
    var sr_origin = '//' + host;
    var origin = protocol + sr_origin;
    // Allow absolute or scheme relative URLs to same origin
    return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
        (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
        // or any other URL that isn't scheme relative or absolute i.e relative.
        !(/^(\/\/|http:|https:).*/.test(url));
}

$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && sameOrigin(settings.url)) {
            // Send the token to same-origin, relative URLs only.
            // Send the token only if the method warrants CSRF protection
            // Using the CSRFToken value acquired earlier
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});

});


