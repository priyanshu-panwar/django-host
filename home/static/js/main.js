(function ($) {
	"use strict";

	// NAVIGATION
	var responsiveNav = $("#responsive-nav"),
		catToggle = $("#responsive-nav .category-nav .category-header"),
		catList = $("#responsive-nav .category-nav .category-list"),
		menuToggle = $("#responsive-nav .menu-nav .menu-header"),
		menuList = $("#responsive-nav .menu-nav .menu-list");

	catToggle.on("click", function () {
		menuList.removeClass("open");
		catList.toggleClass("open");
	});

	menuToggle.on("click", function () {
		catList.removeClass("open");
		menuList.toggleClass("open");
	});

	$(document).click(function (event) {
		if (!$(event.target).closest(responsiveNav).length) {
			if (responsiveNav.hasClass("open")) {
				responsiveNav.removeClass("open");
				$("#navigation").removeClass("shadow");
			} else {
				if ($(event.target).closest(".nav-toggle > button").length) {
					if (!menuList.hasClass("open") && !catList.hasClass("open")) {
						menuList.addClass("open");
					}
					$("#navigation").addClass("shadow");
					responsiveNav.addClass("open");
				}
			}
		}
	});

	// HOME SLICK
	// $("#home-slick").slick({
	// 	autoplay: true,
	// 	infinite: true,
	// 	speed: 300,
	// 	arrows: true,
	// });
	// PRODUCT DETAILS SLICK

	setTimeout(function () {
		if ($("html").attr("dir") == "rtl") {
			$("#home-slick").slick({
				autoplay: true,
				infinite: true,
				speed: 300,
				arrows: true,
				rtl: true,
			});
			$("#product-main-view").slick({
				infinite: true,
				speed: 300,
				dots: false,
				arrows: true,
				fade: true,
				asNavFor: "#product-view",
				rtl: true,
			});

			$("#query").css("text-align", "right");
		} else {
			$("#home-slick").slick({
				autoplay: true,
				infinite: true,
				speed: 300,
				arrows: true,
				rtl: false,
			});
			$("#product-main-view").slick({
				infinite: true,
				speed: 300,
				dots: false,
				arrows: true,
				fade: true,
				asNavFor: "#product-view",
			});
		}
	}, 100);

	// PRODUCTS SLICK
	$("#product-slick-1").slick({
		slidesToShow: 3,
		slidesToScroll: 2,
		autoplay: true,
		infinite: true,
		speed: 300,
		dots: true,
		arrows: false,
		appendDots: ".product-slick-dots-1",
		responsive: [
			{
				breakpoint: 991,
				settings: {
					slidesToShow: 1,
					slidesToScroll: 1,
				},
			},
			{
				breakpoint: 480,
				settings: {
					dots: false,
					arrows: true,
					slidesToShow: 1,
					slidesToScroll: 1,
				},
			},
		],
	});

	$("#product-slick-2").slick({
		slidesToShow: 3,
		slidesToScroll: 2,
		autoplay: true,
		infinite: true,
		speed: 300,
		dots: true,
		arrows: false,
		appendDots: ".product-slick-dots-2",
		responsive: [
			{
				breakpoint: 991,
				settings: {
					slidesToShow: 1,
					slidesToScroll: 1,
				},
			},
			{
				breakpoint: 480,
				settings: {
					dots: false,
					arrows: true,
					slidesToShow: 1,
					slidesToScroll: 1,
				},
			},
		],
	});

	$("#product-view").slick({
		slidesToShow: 3,
		slidesToScroll: 1,
		arrows: true,
		centerMode: true,
		focusOnSelect: true,
		asNavFor: "#product-main-view",
	});

	// PRODUCT ZOOM
	$("#product-main-view .product-view").zoom();

	// PRICE SLIDER
	var slider = document.getElementById("price-slider");
	if (slider) {
		noUiSlider.create(slider, {
			start: [1, 999],
			connect: true,
			tooltips: [true, true],
			format: {
				to: function (value) {
					return value.toFixed(2) + "$";
				},
				from: function (value) {
					return value;
				},
			},
			range: {
				min: 1,
				max: 999,
			},
		});
	}
})(jQuery);

function storeItemInCart(id) {
	var quantity = $("#quant_category" + id).val();
	localStorage.setItem("product_id", id);
	localStorage.setItem("quantity", quantity);
	var payload = {
		quantity: quantity,
	};
	$.ajax({
		url: "/order/addtoshopcart/" + id,
		type: "POST",
		dataType: "json",
		data: payload,
		headers: { "X-CSRFToken": $.cookie("csrftoken") },
		success: function () {
			window.location.reload();
		},
		error: function (err) {
			window.location.reload();
		},
	});
}

function storeItemInCartFromProduct(id) {
	var quantity = $("#quant_product" + id).val();
	localStorage.setItem("product_id", id);
	localStorage.setItem("quantity", quantity);
	var payload = {
		quantity: quantity,
	};
	$.ajax({
		url: "/order/addtoshopcart/" + id,
		type: "POST",
		dataType: "json",
		data: payload,
		headers: { "X-CSRFToken": $.cookie("csrftoken") },
		success: function () {
			window.location.reload();
		},
		error: function (err) {
			window.location.reload();
		},
	});
}
