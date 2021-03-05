from haystack import indexes
from .models import NewCompany

class NewCompanyIndex(indexes.SearchIndex,indexes.Indexable):
    text = indexes.CharField(document=True,use_template=True)
    companyName = indexes.CharField(model_attr='companyName')
    location = indexes.CharField(model_attr='location')
    makesOffer = indexes.CharField(model_attr='makesOffer')

    def get_model(self):
        return NewCompany

    def index_queryset(self, using=None):
        return self.get_model().objects.all()
