(function ($HMU, $, Bloodhound) { $(function() {
    'use strict';

    var userSuggestions = new Bloodhound({
        datumTokenizer: Bloodhound.tokenizers.obj.whitespace('value'),
        queryTokenizer: Bloodhound.tokenizers.whitespace,
        remote: {
            url: $HMU._USER_AUTOCOMPLETE_URL + '?q=%QUERY',
            wildcard: '%QUERY',
            transform: function (response) {
                return response.suggestions;
            }
        }
    });

    var $tt = $('#user-search-form-input');

    $tt.typeahead(null, {
        name: 'user-suggestions',
        source: userSuggestions,
        limit: 10 // Doesn't work if it's 5 for SOME reason...
    });

    // Submit on selection
    $tt.on('typeahead:selected', function(event, selection) {
        $('#user-search-form').submit();
    });
})})(window.$HMU, window.jQuery, Bloodhound);