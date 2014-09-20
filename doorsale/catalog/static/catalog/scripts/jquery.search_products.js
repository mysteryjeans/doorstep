$('#advance-search-filter').click(function() {
	var $advanceSearchOptions = $('.advance-search-option');
	if ($advanceSearchOptions.is(':visible')) {
		$advanceSearchOptions.fadeOut(200);
		$('input[type="text"]', $advanceSearchOptions).val('');
		$('select', $advanceSearchOptions).val('');
		$('.fa-search-minus').removeClass('fa-search-minus').addClass('fa-search-plus');
	} else {
		$advanceSearchOptions.fadeIn(200);
		$('.fa-search-plus').removeClass('fa-search-plus').addClass('fa-search-minus');
	}
});

$('.advance-search-option input[type="text"], .advance-search-option select').each(function(){
	if($(this).val() != '')
		$('.advance-search-option').show();	
});