# Kissa frontend (backenddan alohida)

Bu arxiv faqat frontend fayllarini o'z ichiga oladi. Django backend arxiviga qo'shib yuborilmagan.

## Backend loyihasiga joylash

Backend loyiha rootida `frontend/` papkasini shu arxivdagi papka bilan joylashtiring:

```text
backend_project/
├── manage.py
├── app_users/
├── settings/
└── frontend/
    ├── templates/app_users/index.html
    └── static/app_users/
        ├── app.css
        └── app.js
```

## Django sozlamalari

`settings/settings.py` ichida `TEMPLATES` ro'yxatidagi `DIRS`ni quyidagicha o'zgartiring:

```python
'DIRS': [BASE_DIR / 'frontend' / 'templates'],
```

Fayl oxiriga (yoki static sozlamalari yoniga) qo'shing:

```python
STATICFILES_DIRS = [BASE_DIR / 'frontend' / 'static']
```

## Bosh sahifa view va URL

`app_users/views.py` ichiga qo'shing:

```python
from django.shortcuts import render

def frontend_home(request):
    return render(request, 'app_users/index.html')
```

`settings/urls.py` ichida `urlpatterns` boshiga qo'shing:

```python
from app_users.views import frontend_home

urlpatterns = [
    path('', frontend_home, name='frontend-home'),
    # qolgan mavjud URL'lar shu yerda qoladi
]
```

`path` va `urlpatterns` uchun `django.urls` importi mavjudligiga ishonch hosil qiling. `frontend_home` root (`/`) sahifani ko'rsatadi, API endpointlar o'z yo'llarida qoladi.

## Ishga tushirish

```bash
python manage.py runserver
```

Brauzer: http://127.0.0.1:8000/

Frontend API'ni shu origin'dagi mavjud backend endpointlariga yuboradi. Agar backend URL'lari yuqoridagi Kissa API yo'llaridan farq qilsa, `frontend/static/app_users/app.js` ichidagi endpointlarni moslashtirish kerak.
