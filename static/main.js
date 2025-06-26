$(function () {
  "use strict";
  function setSliderHeight() {
    var winH = window.innerHeight, // More accurate than $(window).height()
      navH = $("nav").innerHeight();
    $(".slider, .carousel-item").height(winH + navH);
  }
  setSliderHeight();
  $(window).resize(setSliderHeight);
  // -----------------------------------------------------------------------------------------

  // To show the cart drawer when the cart icon is clicked
  $(document).ready(
    function(){
    $(".cart-icon").on("click", function () {
    $("#cartDrawer").addClass("open");
  })
});
  // Close the drawer when clicking the close button
  window.closeCart = function () {
    $("#cartDrawer").removeClass("open");
  };
});

