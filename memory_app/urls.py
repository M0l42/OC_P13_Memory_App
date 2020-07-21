from django.urls import path
from .views.home import home_view
from .views.forms import UploadCSVFormView
from .views.cards import QuickModeView, MemoryView, deck_menu_view

urlpatterns = [
    path('', home_view, name='home'),
    path('update/', UploadCSVFormView.as_view(), name='update'),
    path('deck/', deck_menu_view, name='deck_menu'),
    path('deck/quick-memory/<int:deck>/', QuickModeView.as_view(), name='quickmode'),
    path('deck/memory/<int:deck>/', MemoryView.as_view(), name='memory')
]
