from django.shortcuts import render
from django.http import JsonResponse
from .models import JsonData
from json import load, JSONDecodeError
from datetime import datetime

def upload(request):
    if request.method == 'POST':
        file = request.FILES['file']

        try:
            data = load(file)

            errors = []

            for item in data:
                name = item.get('name')
                date_str = item.get('date')

                if not name:
                    errors.append('Не найдено имя')
                    continue

                if len(name) >= 50:
                    errors.append('Имя больше 50 символов')
                    continue

                if not date_str:
                    errors.append('Не найдена дата')
                    continue

                try:
                    date = datetime.strptime(date_str, '%Y-%m-%d_%H:%M')
                    JsonData.objects.create(name=name, date=date)

                except ValueError:
                    errors.append(f'Неверный формат даты')

        except JSONDecodeError:
            return JsonResponse({'error': 'Ошибка чтения JSON'}, status=400)

        return JsonResponse({'status': 'success'})

    else:
        return render(request, 'uploader/index.html')

def data_list(request):
    data = JsonData.objects.all().order_by('-date')

    return render(request, 'uploader/data_list.html', {'data': data})
