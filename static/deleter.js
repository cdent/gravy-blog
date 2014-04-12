(function($) {
    "use strict";

    /*
     * So little here it's almost not worth the bother.
     */

    $('#delete-form').on('submit', function(ev) {
        return confirm('Are you sure you want to delete this entry?');
    });

})(jQuery)
