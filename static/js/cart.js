// Utility function to get CSRF token from cookies (Not used here since no authenticated users)
function getToken(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Initialize cart if not already set for guest users
var cart = getCookie('cart') ? JSON.parse(getCookie('cart')) : {};
if (cart == undefined) {
    cart = {};
    console.log('Cart Created!', cart);
    document.cookie = 'cart=' + JSON.stringify(cart) + ";domain=;path=/";
}
console.log('Cart:', cart);

// Get all elements with the 'update-cart' class
var updateBtns = document.getElementsByClassName('update-cart');

// Add event listeners to 'Add to Cart' and 'Remove from Cart' buttons for guest users
for (var i = 0; i < updateBtns.length; i++) {
    updateBtns[i].addEventListener('click', function () {
        var productId = this.dataset.product;
        var action = this.dataset.action;
        console.log('Clicked productId:', productId, 'Action:', action);

        // Handle guest users (add items to cart via cookies)
        addCookieItem(productId, action);
    });
}

// Function to handle adding/removing items for guest users using cookies
function addCookieItem(productId, action) {
    console.log('User is not authenticated, updating cart via cookies.');

    if (action == 'add') {
        if (cart[productId] == undefined) {
            cart[productId] = { 'quantity': 1 };  // Add new item to the cart
        } else {
            cart[productId]['quantity'] += 1;  // Increment the quantity
        }
    }

    if (action == 'remove') {
        if (cart[productId] != undefined) {
            cart[productId]['quantity'] -= 1;  // Decrease quantity
            if (cart[productId]['quantity'] <= 0) {
                delete cart[productId];  // Remove item if quantity is 0 or less
            }
        }
    }

    console.log('Updated Cart:', cart);
    document.cookie = 'cart=' + JSON.stringify(cart) + ";domain=;path=/";  // Update the cart cookie
    location.reload();  // Reload the page to reflect changes
}

// Utility function to get a cookie by name
function getCookie(name) {
    var cookieArr = document.cookie.split(";");
    for (var i = 0; i < cookieArr.length; i++) {
        var cookiePair = cookieArr[i].split("=");
        if (name == cookiePair[0].trim()) {
            return decodeURIComponent(cookiePair[1]);
        }
    }
    return null;
}
