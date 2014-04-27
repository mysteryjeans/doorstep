jQuery.easing.easeOutQuart = function(x, t, b, c, d) {
	return -c * (( t = t / d - 1) * t * t * t - 1) + b;
};

$('#pics-slideshow').serialScroll({
	items : 'li',
	prev : '#product-show a.prev',
	next : '#product-show a.next',
	offset : -30, //when scrolling to photo, stop 230 before reaching it (from the left)
	start : 1, //as we are centering it, start at the 2nd
	duration : 1200,
	force : true,
	stop : true,
	lock : false,
	cycle : false, //don't pull back once you reach the end
	easing : 'easeOutQuart', //use this easing equation for a funny effect
	jump : false //click on the images to scroll to them
});


$('#pics-slideshow img').click(function(){
	var img_url = $(this).attr('src');
	var $zoomImage = $('#preview-zoom');
	
	$zoomImage.attr('src', img_url);
	
	// Reinitialize EZ
	$('.zoomContainer').remove();
	$zoomImage.removeData('elevateZoom');
	$zoomImage.data('zoom-image', img_url);
	$zoomImage.elevateZoom();
});

$('#preview-zoom').elevateZoom();