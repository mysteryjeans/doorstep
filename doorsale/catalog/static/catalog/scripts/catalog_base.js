$('[parent-category]').each(function() {
	var $sub_categories = $(this);
	$($sub_categories.attr('parent-category')).click(function() {
		if ($sub_categories.is(':visible')) {
			$sub_categories.hide(100);
			$(this).attr('arrow', '\u21E2');
		} else {
			$sub_categories.show(100);
			$(this).attr('arrow', '\u21E3');
		}
	});
}); 