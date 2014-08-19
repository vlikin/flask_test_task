function playSong(song) {
    $('audio').attr('src', '/static/files/music/' + song);
}
jQuery(document).ready(function() {
  $('.bxslider').bxSlider();
});