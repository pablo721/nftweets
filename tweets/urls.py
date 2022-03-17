from django.urls import path, include
from .views import *

app_name = 'mood'

urlpatterns = [
    path('popular/', PopularView.as_view(), name='popular'),
    path('mentions/', MentionsView.as_view(), name='mentions'),
    path('specific/', SpecificView.as_view(), name='specific'),
    path('spaces/', SpacesView.as_view(), name='spaces'),
    path('influencers/', InfluencersView.as_view(), name='influencers'),
]

