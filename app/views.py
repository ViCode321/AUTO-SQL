#app/views.py
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from .utils.insert import Excel_convert_insert, insert_sql
from .utils.delete import Excel_convert_delete, Sql_convert, delete_sql

def index(request):
    return render(request, 'index.html')

def submit_excel(request):
    file = None
    if request.method == 'POST':
        if 'file' not in request.FILES:
            return JsonResponse({'error': 'Porfavor suba el archivo Excel'}, status=400)
        file = request.FILES['file']
        if not file.name.endswith(('.xls', '.xlsx')):
            return JsonResponse({'error': 'El archivo debe ser un documento Excel (xls o xlsx).'}, status=400)
        try:
            message = Excel_convert_insert(file)
            return JsonResponse({'message': message}, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'Método no permitido.'}, status=405)

def insert_view(request):
    if request.method == 'POST':
        base = request.POST.get('base').strip()
        table = request.POST.get('table').strip()
        status, message, result = insert_sql(base, table)
        if status == 1:
            return JsonResponse({'error': message}, status=400)
        else:
            response = HttpResponse(content_type='application/sql')
            filename = f"INSERT_{base}_{table}.sql"
            response['Content-Disposition'] = f'attachment; filename="{filename}"'
            response.write(result)
            return response
    return render(request, 'insert.html')

def submit_excel_sql(request):
    if request.method == 'POST':
        if 'sql' not in request.FILES:
            return JsonResponse({'error': 'Porfavor suba el archivo SQL'}, status=400)
        if 'file' not in request.FILES:
            return JsonResponse({'error': 'Porfavor suba el archivo Excel'}, status=400)
        sql = request.FILES['sql']
        file = request.FILES['file']
        if not sql.name.endswith(('.sql')):
            return JsonResponse({'error': 'El archivo debe ser un Script .sql'}, status=400)
        if not file.name.endswith(('.xls', '.xlsx')):
            return JsonResponse({'error': 'El archivo debe ser un documento Excel (xls o xlsx).'}, status=400)
        message = ''
        try:
            message += Sql_convert(sql)
            print(message)
            message += Excel_convert_delete(file)
            return JsonResponse({'message': message}, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'Método no permitido.'}, status=405)

def delete_view(request):
    if request.method == 'POST':
        column = int(request.POST.get('column'))
        status, message, result = delete_sql(column)
        if status == 1:
            return JsonResponse({'error': message}, status=400)
        else:
            response = HttpResponse(content_type='application/sql')
            filename = f"DELETE.sql"
            response['Content-Disposition'] = f'attachment; filename="{filename}"'
            response.write(result)
            return response
    return render(request, 'delete.html')

