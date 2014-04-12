(function($) {
	"use strict";

	var classes = 'entrycontrol fa fa-fw fa-arrow-circle-right',
		clicker = $('<i>').addClass(classes).on('click',
			function(ev) {
				$(this).parent().find('.content').toggle(200);
				$(this).toggleClass('fa-arrow-circle-down');
				$(this).toggleClass('fa-arrow-circle-right');
			}
		);

	$('.entry').prepend(clicker);
})(jQuery);
