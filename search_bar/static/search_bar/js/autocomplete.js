(function ($HMU, $, Handlebars, Bloodhound) { $(function() {
    'use strict';

    var userSuggestions = new Bloodhound({
        queryTokenizer: Bloodhound.tokenizers.whitespace,
        datumTokenizer: Bloodhound.tokenizers.whitespace,
        remote: {
            url: $HMU._USER_AUTOCOMPLETE_URL + '?q=%QUERY',
            wildcard: '%QUERY',
            transform: function (response) {
                return response.suggestions;
            }
        }
    });

    var $form = $('#user-search-form');
    var $tt = $('#user-search-form-input');

    $tt.typeahead(null, {
        name: 'user-suggestions',
        source: userSuggestions,
        display: 'username',
        limit: 10, // Doesn't work if it's 5 for SOME reason...
        templates: {
            suggestion: Handlebars.compile([
                '<div>',
                '    <img src="{{ gravatar_url }}" class="img-thumbnail search-result-image">',
                '    <div class="search-result-text">',
                '        <strong class="search-result-text-username">{{ username }}</strong> <br />',
                '        <span class="search-result-text-fullname">{{ first_name }} {{ last_name }}</span>',
                '    </div>',
                '</div>'
            ].join('\n'))
        }
    });

    // Submit on selection
    $tt.on('typeahead:selected', $form.submit);
})})(window.$HMU, window.jQuery, window.Handlebars, window.Bloodhound);
