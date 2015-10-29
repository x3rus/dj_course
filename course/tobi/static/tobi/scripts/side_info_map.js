$(function() {



/* REF : http://stackoverflow.com/questions/253689/switching-a-div-background-image-with-jquery */
$('#left-arrow').click(function(){
    console.log("click left arrow");
    if($('#side_info_map').hasClass('expanded_full_sidebar-info')) {
        $('#side_info_map').addClass('collapsed_full_sidebar-info').removeClass('expanded_full_sidebar-info');
    } else {
        $('#side_info_map').addClass('expanded_full_sidebar-info').removeClass('collapsed_full_sidebar-info');
    } /* fi expanded*/
    console.log("click left arrow done");
});

$('#right-arrow').click(function(){
    console.log("click right arrow");
    if($('#side_info_map').hasClass('')) {
        $('#side_info_map').addClass('expanded_full_sidebar-info').removeClass('collapsed_full_sidebar-info');
    } else {
        $('#side_info_map').addClass('collapsed_full_sidebar-info').removeClass('expanded_full_sidebar-info');
    } /* fi expanded*/
});


}); // Fin  $(funcion() {
