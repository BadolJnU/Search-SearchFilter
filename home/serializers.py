from rest_framework import serializers
from .models import SearchHistory

class SearchSerializers(serializers.ModelSerializer):
	class Meta:
	    model = SearchHistory
	    fields = ('loginuser', 'keyword', 'searchdate', 'searchresult')
