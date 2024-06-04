# views.py or any other script
import os
import django
import json
from django.core.management import call_command
from io import StringIO

# Django 설정 로드
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

# StringIO 객체를 사용하여 dumpdata의 출력을 문자열로 받기
output = StringIO()
call_command('dumpdata', 'movies', stdout=output, indent=4)

# JSON 문자열을 파싱하고 ensure_ascii=False로 다시 저장
data = json.loads(output.getvalue())

with open("data.json", "w", encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)
