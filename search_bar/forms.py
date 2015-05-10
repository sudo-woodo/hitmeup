__author__ = 'goodoldbob'
# forms.py
from haystack.forms import SearchForm

class UserSearchForm(SearchForm):

    def no_query_found(self):
        return self.searchqueryset.all()