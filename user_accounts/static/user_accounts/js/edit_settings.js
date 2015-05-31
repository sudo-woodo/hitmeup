(function($) { $(function() {
    'use strict';

    // Close alerts on tab click
    $('.nav-tabs').click(function(e) {
        $('.alert').alert('close');
    })
})})(window.jQuery);
