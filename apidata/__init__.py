default_app_config='apidata.apps.ApidataConfig'
from elasticsearch import Elasticsearch
from django.conf import settings

es_index = settings.HAYSTACK_CONNECTIONS['default']['INDEX_NAME']
es_url = settings.HAYSTACK_CONNECTIONS['default']['URL']
es = Elasticsearch(es_url)