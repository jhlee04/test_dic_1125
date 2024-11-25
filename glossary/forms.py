from django import forms
from .models import Term  # 'Term' 모델을 가져오기

class UploadCSVForm(forms.Form):
    csv_file = forms.FileField()
    
from django import forms
from .models import Term  # Term 모델 가져오기
    
class TermForm(forms.ModelForm):
    class Meta:
        model = Term  # 모델 지정
        fields = ['type', 'terms', 'definition']  # 폼에서 사용할 필드
