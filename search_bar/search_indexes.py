from haystack import indexes
# from hitmeup.models import Something
from django.contrib.auth.models import User

# Create search_bar index for user search_bar, can add additional filters later
class UserIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True, template_name="search/indexes/search_bar/user_text.txt")
    content_auto = indexes.EdgeNgramField(model_attr='username') # for autocomplete

    def get_model(self):
        return User
