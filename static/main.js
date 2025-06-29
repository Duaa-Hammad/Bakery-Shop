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
  $(document).ready(function () {
    $(".cart-icon").on("click", function () {
      $("#cartDrawer").addClass("open");
    });
  });
  // Close the drawer when clicking the close button
  window.closeCart = function () {
    $("#cartDrawer").removeClass("open");
  };
});
// ----------------------------------------------------------------------------------------------
// Add to cart functionality
// This function is called when the "Add to Cart" button is clicked
function addToCart(event, productId) {
  event.preventDefault();
  fetch(`/add_to_cart/${productId}`, {
    method: "POST",
    headers: { "X-Requested-With": "XMLHttpRequest" },
  })
    .then((response) => response.json())
    .then((data) => {
      if (data.cart_html) {
        document.getElementById("cartItems").innerHTML = data.cart_html;
        document.getElementById("cartDrawer").classList.add("open"); // <-- This opens the cart drawer
      } else if (data.error) {
        alert(data.error);
      }
    });
}

function deleteCartItem(cartItemId) {
  fetch(`/delete_cart_item/${cartItemId}`, {
    method: "POST",
    headers: { "X-Requested-With": "XMLHttpRequest" },
  })
    .then((response) => response.json())
    .then((data) => {
      if (data.cart_html) {
        document.getElementById("cartItems").innerHTML = data.cart_html;
      }
    });
}
