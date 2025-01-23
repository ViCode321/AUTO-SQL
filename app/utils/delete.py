import openpyxl
import re

wb_principal = None
sheet_principal = None
sql_file_path = None


def Sql_convert(sql_file):
    global sql_file_path
    try:
        # Guardar directamente el contenido del archivo SQL en sql_file_path
        sql_file_path = sql_file.read().decode('utf-8')
        return 'Archivo SQL y '
    except Exception as e:
        raise ValueError(f'Error al procesar el archivo SQL: {str(e)}')


def Excel_convert_delete(file):
    global sheet_principal
    try:
        # Cargar la hoja activa del archivo Excel
        workbook = openpyxl.load_workbook(file)
        sheet_principal = workbook.active
        return f'{file.name} procesados con éxito.'
    except Exception as e:
        raise ValueError(f'Error al procesar el archivo: {str(e)}')


def delete_sql(column):
    global sheet_principal, sql_file_path

    if not sql_file_path or not sheet_principal:
        return 1, "Cargue primero el archivo SQL y el archivo Excel.", ""

    try:
        # Usar directamente el contenido del archivo SQL
        sql_content = sql_file_path

        # Buscar el tipo de dato declarado para @ident
        declare_match = re.search(r"(?i)declare\s+@ident\s+(\w+);", sql_content)
        if not declare_match:
            return 1, "No se encontró la declaración de '@ident' en el archivo SQL.", ""

        ident_type = declare_match.group(1).lower()

        # Leer valores de la columna indicada en el archivo Excel
        ident_values = []
        for row in sheet_principal.iter_rows(min_row=2, values_only=True):  # Saltar encabezado
            if row[column - 1]:  # Comprobar que la celda no esté vacía
                ident_values.append(row[column - 1])

        # Construir la sección DECLARE
        declare_section = f"DECLARE @ident {ident_type};\n\n"
        dynamic_scripts = []

        # Generar scripts dinámicos para cada valor en ident_values
        for ident in ident_values:
            if ident_type == 'int':
                ident_value = f"{int(ident)}"
            elif ident_type in ['varchar', 'nvarchar']:
                ident_value = f"'{ident}'"
            else:
                return 1, f"Tipo de dato no soportado: {ident_type}", ""

            # Reemplazar SET @ident con el nuevo valor
            updated_script = re.sub(
                r"(?i)set\s+@ident\s*=\s*.*?;",
                f"SET @ident = {ident_value};",
                sql_content
            )

            # Eliminar declaraciones redundantes de @ident
            updated_script = re.sub(r"(?i)declare\s+@ident\s+\w+;", "", updated_script)

            dynamic_scripts.append(updated_script.strip())

        # Combinar todo el script
        full_script = declare_section + "\nGO\n\n".join(dynamic_scripts)
        full_script = full_script.replace("\r\n", "\n")  # Normalizar saltos de línea

        return 0, "Script SQL generado correctamente.", full_script

    except Exception as e:
        return 1, f"Ocurrió un error al generar el script SQL: {e}", ""
