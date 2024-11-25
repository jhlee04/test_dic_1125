from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, get_object_or_404
from .models import Term

from collections import defaultdict
from django.contrib.auth.decorators import user_passes_test

from django.shortcuts import render, get_object_or_404, redirect
from .models import Term
from .forms import TermForm, UploadCSVForm
from django.utils.safestring import mark_safe
import csv
import re

from django.shortcuts import render, get_object_or_404
from django.db.models import F
from .models import Term

# 1. Index: 용어 목록 페이지
def index(request):
    query = request.GET.get('q', '')  # 검색어 가져오기
    if query:
        # 검색: 용어 이름과 정의에서 검색
        terms = Term.objects.filter(terms__icontains=query) | Term.objects.filter(definition__icontains=query)

    else:
        terms = Term.objects.all().order_by('type', 'terms')  # 전체 데이터 정렬

    # Type별로 그룹화
    terms_by_type = {}
    for term in terms:
        terms_by_type.setdefault(term.type, []).append(term)

    return render(request, 'glossary/index.html', {'terms_by_type': terms_by_type, 'query': query})


# 2. Term Detail: 용어 상세 페이지
from collections import defaultdict

def term_detail(request, pk):
    # 현재 선택된 용어
    term = get_object_or_404(Term, pk=pk)  # 특정 용어 가져오기
    term.view_count = F('view_count') + 1  # 조회수 증가
    term.save(update_fields=['view_count'])  # 데이터베이스에 저장
    # 모든 용어 가져오기 및 그룹화
    terms = Term.objects.all().order_by('type', 'terms')
    terms_by_type = defaultdict(list)
    for t in terms:
        terms_by_type[t.type].append(t)

    # 다른 용어로 정의 내 링크 추가
    def add_links(definition):
        all_terms = Term.objects.values_list('terms', 'id')
        for other_term, other_id in all_terms:
            pattern = rf'\b{re.escape(other_term)}\b'
            link = f'<a href="/{other_id}/">{other_term}</a>'
            definition = re.sub(pattern, link, definition)
        return definition
    # 링크 추가 확인 
    term.definition = add_links(term.definition)




    # Definition에 링크 추가
    term.definition = mark_safe(add_links(term.definition))

    # 템플릿으로 데이터 전달
    return render(request, 'glossary/term_detail.html', {
        'term': term,
        'terms_by_type': dict(terms_by_type)  # full_term 데이터도 템플릿에서 활용 가능
    })

 

# 관리자 권한 체크 함수
def is_admin(user):
    return user.is_superuser  # 관리자 권한 확인

# CSV 업로드 뷰: 관리자만 접근 가능
@user_passes_test(is_admin, login_url='/login/', redirect_field_name=None)
def upload_csv(request):
    if request.method == 'POST':
        form = UploadCSVForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES['csv_file']
            decoded_file = csv_file.read().decode('utf-8').splitlines()
            reader = csv.DictReader(decoded_file)

            # 기존 데이터 삭제
            Term.objects.all().delete()

            # 새 데이터 저장
            for row in reader:
                Term.objects.create(
                    type=row['type'],
                    terms=row['terms'],
                    definition=row['definition']
                )
            return render(request, 'glossary/upload_success.html')

    else:
        form = UploadCSVForm()
    return render(request, 'glossary/upload_csv.html', {'form': form})


# 용어 수정 뷰: 관리자만 접근 가능
@user_passes_test(is_admin)
def edit_term(request, pk):
    term = get_object_or_404(Term, pk=pk)
    if request.method == 'POST':
        form = TermForm(request.POST, instance=term)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = TermForm(instance=term)
    return render(request, 'glossary/edit_term.html', {'form': form, 'term': term})


from django.db.models import F

def index(request):
    query = request.GET.get('q', '')  # 검색어 가져오기
    if query:
        terms = Term.objects.filter(terms__icontains=query) | Term.objects.filter(definition__icontains=query)
    else:
        terms = Term.objects.all().order_by('type', 'terms')

    # 자주 조회된 용어 가져오기
    popular_terms = Term.objects.order_by('-view_count')[:10]  # 조회수 기준 상위 5개

    # Type별로 그룹화
    terms_by_type = {}
    for term in terms:
        terms_by_type.setdefault(term.type, []).append(term)

    return render(request, 'glossary/index.html', {
        'terms_by_type': terms_by_type,
        'popular_terms': popular_terms,
        'query': query
    })
