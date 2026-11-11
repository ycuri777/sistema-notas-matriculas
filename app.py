from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, abort
from datetime import datetime

app = Flask(__name__)
app.secret_key = "clave-desarrollo-cambiar-en-produccion"

# Almacenamiento temporal en memoria: los datos se reinician al detener el servidor.
alumnos = [
    {"id": 1, "nombres": "Ana María", "apellidos": "Torres Rojas", "dni": "74125896", "correo": "ana.torres@email.com"}
]
matriculas = [
    {"id": 1, "alumno_id": 1, "curso": "Python con Flask", "nota1": 17.0, "nota2": 18.0, "nota3": 16.0,
     "fecha": datetime.now().strftime("%d/%m/%Y")}
]
siguiente_alumno_id = 2
siguiente_matricula_id = 2


def buscar_alumno(alumno_id):
    return next((a for a in alumnos if a["id"] == alumno_id), None)


def nota_valida(valor):
    try:
        nota = float(valor)
        return 0 <= nota <= 20, nota
    except (TypeError, ValueError):
        return False, None


@app.route("/")
def inicio():
    return render_template("index.html", total_alumnos=len(alumnos),
                           total_matriculas=len(matriculas),
                           promedio_general=round(
                               sum((m["nota1"] + m["nota2"] + m["nota3"]) / 3 for m in matriculas) / len(matriculas), 2
                           ) if matriculas else 0)


@app.route("/alumnos")
def listar_alumnos():
    return render_template("alumnos.html", alumnos=alumnos)


@app.route("/alumnos/nuevo", methods=["GET", "POST"])
def nuevo_alumno():
    global siguiente_alumno_id
    if request.method == "POST":
        nombres = request.form.get("nombres", "").strip()
        apellidos = request.form.get("apellidos", "").strip()
        dni = request.form.get("dni", "").strip()
        correo = request.form.get("correo", "").strip()

        if not nombres or not apellidos or not correo or not dni:
            return render_template("nuevo_alumno.html", valores=request.form,
                                   error="Todos los campos son obligatorios."), 400
        if not dni.isdigit() or len(dni) != 8:
            return render_template("nuevo_alumno.html", valores=request.form,
                                   error="El DNI debe contener exactamente 8 dígitos."), 400
        if any(a["dni"] == dni for a in alumnos):
            return render_template("nuevo_alumno.html", valores=request.form,
                                   error="Ya existe un alumno registrado con ese DNI."), 409

        alumnos.append({"id": siguiente_alumno_id, "nombres": nombres,
                        "apellidos": apellidos, "dni": dni, "correo": correo})
        siguiente_alumno_id += 1
        flash("Alumno registrado correctamente.", "success")
        return redirect(url_for("listar_alumnos"), code=303)

    return render_template("nuevo_alumno.html", valores={}, error=None)


@app.route("/matriculas")
def listar_matriculas():
    registros = []
    for m in matriculas:
        alumno = buscar_alumno(m["alumno_id"])
        if alumno:
            registros.append({
                **m,
                "nombre_completo": f'{alumno["nombres"]} {alumno["apellidos"]}',
                "dni": alumno["dni"],
                "promedio": round((m["nota1"] + m["nota2"] + m["nota3"]) / 3, 2)
            })
    return render_template("matriculas.html", matriculas=registros, alumnos=alumnos)


@app.route("/matriculas/nueva", methods=["GET", "POST"])
def nueva_matricula():
    global siguiente_matricula_id
    if request.method == "POST":
        alumno_id = request.form.get("alumno_id", type=int)
        curso = request.form.get("curso", "").strip()
        valores_notas = [request.form.get("nota1"), request.form.get("nota2"), request.form.get("nota3")]

        alumno = buscar_alumno(alumno_id) if alumno_id else None
        notas = [nota_valida(v) for v in valores_notas]

        if not alumno:
            return render_template("nueva_matricula.html", alumnos=alumnos, valores=request.form,
                                   error="Seleccione un alumno válido."), 400
        if not curso:
            return render_template("nueva_matricula.html", alumnos=alumnos, valores=request.form,
                                   error="Ingrese el nombre del curso."), 400
        if not all(ok for ok, _ in notas):
            return render_template("nueva_matricula.html", alumnos=alumnos, valores=request.form,
                                   error="Las tres notas deben ser números entre 0 y 20."), 400
        if any(m["alumno_id"] == alumno_id and m["curso"].casefold() == curso.casefold() for m in matriculas):
            return render_template("nueva_matricula.html", alumnos=alumnos, valores=request.form,
                                   error="El alumno ya está matriculado en ese curso."), 409

        matriculas.append({
            "id": siguiente_matricula_id, "alumno_id": alumno_id, "curso": curso,
            "nota1": notas[0][1], "nota2": notas[1][1], "nota3": notas[2][1],
            "fecha": datetime.now().strftime("%d/%m/%Y")
        })
        siguiente_matricula_id += 1
        flash("Matrícula y calificaciones registradas correctamente.", "success")
        return redirect(url_for("listar_matriculas"), code=303)

    return render_template("nueva_matricula.html", alumnos=alumnos, valores={}, error=None)


@app.route("/api/consolidado")
def api_consolidado():
    resultado = []
    for m in matriculas:
        alumno = buscar_alumno(m["alumno_id"])
        if alumno:
            promedio = round((m["nota1"] + m["nota2"] + m["nota3"]) / 3, 2)
            resultado.append({
                "matricula_id": m["id"],
                "alumno": {
                    "id": alumno["id"], "nombres": alumno["nombres"],
                    "apellidos": alumno["apellidos"], "dni": alumno["dni"]
                },
                "curso": m["curso"],
                "notas": {"nota1": m["nota1"], "nota2": m["nota2"], "nota3": m["nota3"]},
                "promedio": promedio,
                "estado": "Aprobado" if promedio >= 11 else "Desaprobado",
                "fecha": m["fecha"]
            })
    return jsonify({"total": len(resultado), "registros": resultado}), 200


@app.errorhandler(404)
def pagina_no_encontrada(error):
    return render_template("404.html"), 404


if __name__ == "__main__":
    app.run(debug=True)
