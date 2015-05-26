from haystack import indexes
from django.contrib.auth.models import User

# Create search_bar index for user search_bar, can add additional filters later
class UserIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True, template_name="search/indexes/search_bar/user_text.txt")
    user_auto = indexes.EdgeNgramField(model_attr='username') # for autocomplete username
    first_name_auto = indexes.EdgeNgramField(model_attr='first_name') # for autocomplete first name
    last_name_auto = indexes.EdgeNgramField(model_attr='last_name') # for autocomplete last name

    def get_model(self):
        return User
