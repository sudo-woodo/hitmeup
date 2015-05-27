from haystack import indexes
from django.contrib.auth.models import User

# Create search_bar index for user search_bar, can add additional filters later
class UserIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    username_auto = indexes.NgramField(model_attr='username', boost=2)
    full_name_auto = indexes.EdgeNgramField(model_attr='get_full_name')

    def get_model(self):
        return User
