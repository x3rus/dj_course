
$(function() {

    $(document).ready(function() {
        var table = $('#myTable').DataTable();
        // Event click image 
        $('#myTable tbody').on( 'click', 'img.icon-delete', function () {
            if (confirm('are you sure you want to delete this activity ?')==true){
                table
                    .row( $(this).parents('tr') )
                    .remove()
                    .draw();

                // TODO avant le refresh valider la suppression
                del_activity( $(this).closest("tr").attr("id")  );
            }
        } ); // FIN $('#myTable tbody').on( 'click', 'img.icon-delete' ....

/* Inutile d'utiliser jquery pour ca car de doute manière je refresh l'ensemble 
 * de la page !!! je le met donc dans le template !
 * $('#myTable tbody').on( 'click', 'td.title', function () {
            if (confirm('visualise ceci ')==true){

                console.log( $(this).closest("tr").attr("id")  );
                console.log( $(this).parents('tr').attr("id") );
                // TODO avant le refresh valider la suppression
                del_activity( $(this).closest("tr").attr("id")  );
            }
        } ); // FIn $('#myTable tbody').on( 'click', 'td.title'...

*/

    } );



    function del_activity(activity_id) {
        console.log("delete post " )// sanity check
            // TODO mettre 
            $.ajax({
                url : "../json_del_activity/", // the endpoint
                type : "POST", // http method
                data : { del_activity_id: activity_id }, // data sent with the post ID

                // handle a successful response
                success : function(json) {
                    console.log(json); // log the returned json to the console
                    console.log("success delete tr id : " + json.activity_2_del); // another sanity check
                    return true;
                },

                // handle a non-successful response
                error : function(xhr,errmsg,err) {
                    $('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: "+errmsg+
                            " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
                    console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
                    return false;
                }
            });
    } // FIN func del_activity

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
    }); // fin $.ajaxSetup



}); // fin $(function() {




