import csv
from django.core.management.base import BaseCommand
from glossary.models import Term

class Command(BaseCommand):
    help = "Load terms from a CSV file"

    def handle(self, *args, **kwargs):
        # 기존 데이터를 삭제
        Term.objects.all().delete()
        self.stdout.write(self.style.WARNING("기존 데이터를 삭제했습니다."))

        # CSV 파일에서 데이터 로드
        with open('terms.csv', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                Term.objects.create(
                    type=row['type'],
                    terms=row['terms'],
                    definition=row['definition'],
                    full_term=row.get('full term', '')  # 'full term' 열을 추가로 읽음
                )
        self.stdout.write(self.style.SUCCESS("새 데이터를 성공적으로 로드했습니다."))
