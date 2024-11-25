from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Term

# admin.site.register(Term)
@admin.register(Term)
class TermAdmin(admin.ModelAdmin):
    list_display = ('type', 'terms', 'definition')  # 목록에 표시할 필드
    search_fields = ('type', 'terms', 'definition')  # 검색 가능 필드
### Username (leave blank to use 'ygha'): admin
### Email address: admin@gmail.com
### Password: 1234