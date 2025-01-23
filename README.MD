# Guía de Inicio Rápido para AUTO-SQL

Aplicación web desarrollada en Django para la generación de queries en sql por medio de un archivo excel.

Hasta el momento puedo crear grandes cantidades de código SQL, "INSERT" y "DELETE", solo se debe proporcionar un archivo excel de los registros a insertar, o un archivo excel con los registros a eliminar y proporcionar la columna que contiene los Ids para crear las queries "DELETE".

## Configuración Inicial
Para comenzar, sigue estos pasos:
1. Primero hay que crear una carpeta em tu pc y accede a ella
```bash
mkdir project
cd project
```
2. Clonar el repositorio:
```bash
git clone https://github.com/ViCode321/AUTO-SQL.git
cd AUTO-SQL
```
3. Crear el entorno virtual y activarlo
```bash
python -m venv myvenv
source myvenv/Scripts/activate
```
4. Instalar requerimientos
```bash
pip install -r requirements.txt
```
5. Ejecutar la app
```bash
python manage.py runserver
```

## Librerías y Frameworks
```bash
asgiref==3.8.1
Django==5.1.2
et-xmlfile==1.1.0
openpyxl==3.1.5
pillow==10.4.0
sqlparse==0.5.1
tzdata==2024.2
```
