$(document).ready(function () {
    $(document).on("click", ".add-to-cart", function (e) {
        e.preventDefault();

        var goodsInCartCount = $("#goods-in-cart-count");
        var cartCount = parseInt(goodsInCartCount.text() || 0);

        var product_slug = $(this).data("product-slug");
        var productInCartCount = $(`#${product_slug}`);
        var productCount = parseInt(productInCartCount.text() || 0);
        var totalProductsInCart = $("#total-products-in-cart");
        var productPrice = $(`#price-${product_slug}`);
        intProductPrice = parseInt(productPrice.text() || 0);
        var totalPrice = $("#total-price");
        intTotalPrice = parseInt(totalPrice.text() || 0);
        var productTotalPrice = $(`#total-product-${product_slug}`);
        intProductTotalPrice = parseInt(productTotalPrice.text() || 0);

        var product_id = $(this).data("product-id");
        var add_to_cart_url = $(this).attr("href");

        $.ajax({
            type: "POST",
            url: add_to_cart_url,
            data: {
                product_id: product_id,
                csrfmiddlewaretoken: $("[name=csrfmiddlewaretoken]").val(),
            },
            success: function (data) {
                cartCount++;
                goodsInCartCount.text(cartCount);
                totalProductsInCart.text(cartCount);
                productCount++;
                productInCartCount.text(productCount);

                intProductTotalPrice += intProductPrice;
                intTotalPrice += intProductPrice;
                productTotalPrice.text(intProductTotalPrice);
                totalPrice.text(intTotalPrice);
            },

            error: function (data) {
                console.log("Ошибка при добавлении товара в корзину");
            },
        });
    });

    $(document).on("click", ".remove-from-cart", function (e) {
        e.preventDefault();

        var goodsInCartCount = $("#goods-in-cart-count");
        var cartCount = parseInt(goodsInCartCount.text() || 0);

        var product_slug = $(this).data("product-slug");
        var productInCartCount = $(`#${product_slug}`);
        var productCount = parseInt(productInCartCount.text() || 0);
        var totalProductsInCart = $("#total-products-in-cart");
        var totalProductsInCartCount = parseInt(totalProductsInCart.text() || 0);
        var totalPrice = $("#total-price");
        intTotalPrice = parseInt(totalPrice.text() || 0);
        var total_price_ = $(this).data("product-total-price");
        var productTotalPrice = $(`#total-product-${product_slug}`);
        intProductTotalPrice = parseInt(productTotalPrice.text() || 0);

        var cart_id = $(this).data("cart-id");
        var remove_from_cart_url = $(this).attr("href");

        $.ajax({
            type: "POST",
            url: remove_from_cart_url,
            data: {
                cart_id: cart_id,
                csrfmiddlewaretoken: $("[name=csrfmiddlewaretoken]").val(),
            },
            success: function (data) {
                cartCount -= productCount;
                goodsInCartCount.text(cartCount);

                totalProductsInCartCount -= productCount;
                totalProductsInCart.text(totalProductsInCartCount);
                intTotalPrice -= intProductTotalPrice;
                totalPrice.text(intTotalPrice);

                var newDiv = document.createElement("div");
                newDiv.id = "removed-product";
                newDiv.textContent = "Удалено";
                var oldDiv = document.getElementById("product-exists-row");
                oldDiv.replaceWith(newDiv);
            },
            error: function (data) {
                console.log("Ошибка при добавлении товара в корзину");
            },
        });
    });

    $(document).on("click", ".clear-up", function (e) {
        e.preventDefault();
        var clear_up_url = $(this).attr("href");
        $.ajax({
            type: "POST",
            url: clear_up_url,
            data: {
                csrfmiddlewaretoken: $("[name=csrfmiddlewaretoken]").val(),
            },
            success: function (data) {
                var newDiv = document.createElement("div");
                newDiv.id = "the-cart-is-empty";
                newDiv.innerHTML = "<h1 class=\"text-center\">Ваша корзина пуста</h1>";
                var oldDiv = document.getElementById("cart-is-not-empty");
                oldDiv.replaceWith(newDiv);
            },
            error: function (data) {
                console.log("Ошибка");
            },
        });
    });

    $(document).on("click", ".take-away", function (e) {
        e.preventDefault();

        var goodsInCartCount = $("#goods-in-cart-count");
        var cartCount = parseInt(goodsInCartCount.text() || 0);

        var product_slug = $(this).data("product-slug");
        var productInCartCount = $(`#${product_slug}`);
        var productCount = parseInt(productInCartCount.text() || 0);
        var totalProductsInCart = $("#total-products-in-cart");
        var productPrice = $(`#price-${product_slug}`);
        intProductPrice = parseInt(productPrice.text() || 0);
        var totalPrice = $("#total-price");
        intTotalPrice = parseInt(totalPrice.text() || 0);
        var productTotalPrice = $(`#total-product-${product_slug}`);
        intProductTotalPrice = parseInt(productTotalPrice.text() || 0);

        var product_id = $(this).data("product-id");
        var add_to_cart_url = $(this).attr("href");

        $.ajax({
            type: "POST",
            url: add_to_cart_url,
            data: {
                product_id: product_id,
                csrfmiddlewaretoken: $("[name=csrfmiddlewaretoken]").val(),
            },
            success: function (data) {
                cartCount--;
                goodsInCartCount.text(cartCount);
                totalProductsInCart.text(cartCount);
                intTotalPrice -= intProductPrice;
                totalPrice.text(intTotalPrice);
                if (productCount > 1) {
                    productCount--;
                    productInCartCount.text(productCount);
                    intProductTotalPrice -= intProductPrice;
                    productTotalPrice.text(intProductTotalPrice);
                } else {
                    var newDiv = document.createElement("div");
                    newDiv.id = "removed-product";
                    newDiv.textContent = "Удалено";
                    var oldDiv = document.getElementById("product-exists-row");
                    oldDiv.replaceWith(newDiv);
                }
            },

            error: function (data) {
                console.log("Ошибка");
            },
        });
    });
});