

$('[parent-category]').each(function() {
	var $sub_categories = $(this);
	$($sub_categories.attr('parent-category')).click(function() {
		if ($sub_categories.is(':visible')) {
			$sub_categories.hide(100);
			$(this).removeClass('arrow-down');
		} else {
			$sub_categories.show(100);
			$(this).addClass('arrow-down');
		}
	});
});


function expandCategories(categoryID) {
	var categoryID = '#category-id-' + categoryID;
	$(categoryID).parents('.sub-categories').show();
	$(categoryID).parents('.parent-category-container').each(function(){
		$('.parent-category', this).first().addClass('arrow-down');
	});
}
