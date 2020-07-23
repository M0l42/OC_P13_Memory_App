from django.urls import path
from .views.home import home_view, legal_mentions
from .views.forms import UploadCSVFormView, contact_view
from .views.cards import QuickModeView, MemoryView, deck_menu_view, deck_update, deck_search_view
from .views.user import LogInFormView, SignUpFormView, LogOutView, EditAccountFormView

urlpatterns = [
    path('', home_view, name='home'),
    path('contact-us/', contact_view, name='contact'),
    path('legal-mention/', legal_mentions, name='legal-mention'),
    path('deck/', deck_menu_view, name='deck_menu'),
    path('deck/create/', UploadCSVFormView.as_view(), name='update'),
    path('deck/update/<int:deck>/', deck_update, name='deck_update'),
    path('deck/quick-memory/<int:deck>/', QuickModeView.as_view(), name='quickmode'),
    path('deck/memory/<int:deck>/', MemoryView.as_view(), name='memory'),
    path('deck/search/', deck_search_view, name='deck_search'),
    path('deck/search/category/<slug>', deck_search_view, name='deck_search_category'),

    path('login/', LogInFormView.as_view(), name='login'),
    path('sign-up/', SignUpFormView.as_view(), name='sign-up'),
    path('log-off/', LogOutView.as_view(), name='log-off'),
    path('edit-account/', EditAccountFormView.as_view(), name='edit-account'),
]
