
function basketChanged() {
	$('#basket-dropdown-button').dropdown();
	$('#basket-dropdown').appendTo($('main#content'));
	// Initializing new forms in basket-container
	bootstrapAjax($, '#basket-dropdown');
}
$(document).ready(function() {
	$('#basket-dropdown').appendTo($('main#content'));
});
