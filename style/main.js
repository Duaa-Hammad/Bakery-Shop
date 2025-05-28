$(function(){
    'use strict';
    function setSliderHeight() {
        var winH = window.innerHeight, // More accurate than $(window).height()
            navH = $('nav').innerHeight();
        $('.slider, .carousel-item').height(winH - navH);
    }
    setSliderHeight();
    $(window).resize(setSliderHeight);
});