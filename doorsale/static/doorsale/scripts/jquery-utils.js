/*
 * Generic utility functions based on jquery
 * This script should be please after all html tags
 */

function contextMenu() {
	$(document).click(function(e) {
		$('[context-menu]').each(function() {
			if (!$(e.target).parent('[context-menu]').andSelf().is(this) && !$(e.target).parents().andSelf().is($(this).attr('context-menu')))
				$(this).fadeOut('fast');
		});
	});

	$('[context-menu]').each(function() {
		var $contextMenu = $(this);
		$($contextMenu.attr('context-menu')).click(function() {
			$contextMenu.fadeIn('fast');
		});
	});
}


$(function(){
	contextMenu();
});
