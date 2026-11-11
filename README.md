SISTEMA WEB EN MEMORIA – REGISTRO DE NOTAS Y MATRÍCULAS

1. Requisitos: Python 3.10 o superior.
2. Abra una terminal dentro de esta carpeta.
3. (Opcional) Cree un entorno virtual:
   python -m venv venv
   Windows: venv\Scripts\activate
4. Instale Flask:
   pip install -r requirements.txt
5. Ejecute:
   python app.py
6. Abra en el navegador:
   http://127.0.0.1:5000

RUTAS:
  /                  Inicio
  /alumnos           Listado de alumnos
  /alumnos/nuevo     Formulario GET/POST de alumno
  /matriculas        Listado de matrículas y notas
  /matriculas/nueva  Formulario GET/POST de matrícula
  /api/consolidado   API REST JSON
  /cualquier-ruta    Página personalizada 404

DATOS DE PRUEBA INICIALES:
  Alumna: YIYE AARON CURI ALCANTARA
  DNI: 70856890
  Curso: Python con Flask
  Notas: 17, 18 y 16

NOTA:
Los datos se guardan en listas y diccionarios de Python. No se utiliza base de datos.
Al detener el servidor, los registros añadidos durante la ejecución se pierden.
