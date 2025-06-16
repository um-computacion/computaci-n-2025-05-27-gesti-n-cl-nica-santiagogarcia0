import unittest
from datetime import datetime
from typing import List, Dict

# =======================
# Excepciones personalizadas
# =======================
class PacienteYaExisteError(Exception): pass
class MedicoYaExisteError(Exception): pass
class PacienteNoExisteError(Exception): pass
class MedicoNoExisteError(Exception): pass
class TurnoDuplicadoError(Exception): pass
class RecetaInvalidaError(Exception): pass
class EspecialidadInvalidaError(Exception): pass

# =======================
# Clases principales
# =======================
class Paciente:
    def __init__(self, dni: str, nombre: str, fecha_nacimiento: str):
        self.dni = dni
        self.nombre = nombre
        self.fecha_nacimiento = fecha_nacimiento

    def __str__(self):
        return f"{self.nombre} (DNI: {self.dni}, Nac.: {self.fecha_nacimiento})"

class Especialidad:
    def __init__(self, tipo: str, dias_disponibles: List[str]):
        self.tipo = tipo
        self.dias_disponibles = dias_disponibles

    def agregar_dia(self, dia: str):
        if dia.lower() not in [d.lower() for d in self.dias_disponibles]:
            self.dias_disponibles.append(dia)

    def esta_disponible(self, dia: str) -> bool:
        return any(d.lower() == dia.lower() for d in self.dias_disponibles)

    def __str__(self):
        dias_str = ", ".join(self.dias_disponibles) if self.dias_disponibles else "Sin días disponibles"
        return f"{self.tipo} (Días: {dias_str})"

class Medico:
    def __init__(self, matricula: str, nombre: str, especialidades: List[Especialidad]):
        self.matricula = matricula
        self.nombre = nombre
        self.especialidades = especialidades

    def agregar_especialidad(self, especialidad: Especialidad):
        self.especialidades.append(especialidad)

    def obtener_especialidad_para_dia(self, dia: str):
        for e in self.especialidades:
            if e.esta_disponible(dia):
                return e
        return None

    def __str__(self):
        especialidades_str = "; ".join(str(e) for e in self.especialidades)
        return f"Dr. {self.nombre} (Matrícula: {self.matricula}) - Especialidades: {especialidades_str}"

class Turno:
    def __init__(self, paciente: Paciente, medico: Medico, fecha: str, hora: str):
        self.paciente = paciente
        self.medico = medico
        self.fecha = fecha
        self.hora = hora

    def __str__(self):
        return f"Turno: {self.fecha} {self.hora} - {self.paciente.nombre} con {self.medico.nombre}"

class Receta:
    def __init__(self, paciente: Paciente, medico: Medico, medicamento: str, fecha: str):
        self.paciente = paciente
        self.medico = medico
        self.medicamento = medicamento
        self.fecha = fecha

    def __str__(self):
        return f"{self.fecha}: {self.medicamento} recetado por {self.medico.nombre} a {self.paciente.nombre}"

class HistoriaClinica:
    def __init__(self, paciente: Paciente):
        self.paciente = paciente
        self.recetas: List[Receta] = []

    def agregar_receta(self, receta: Receta):
        self.recetas.append(receta)

    def __str__(self):
        if not self.recetas:
            return f"Historia clínica de {self.paciente.nombre}: Sin recetas"
        recetas_str = "\n".join(str(r) for r in self.recetas)
        return f"Historia clínica de {self.paciente.nombre}:\n{recetas_str}"

class Clinica:
    def __init__(self):
        self.pacientes: Dict[str, Paciente] = {}
        self.medicos: Dict[str, Medico] = {}
        self.turnos: List[Turno] = []
        self.historias: Dict[str, HistoriaClinica] = {}

    def registrar_paciente(self, paciente: Paciente):
        if paciente.dni in self.pacientes:
            raise PacienteYaExisteError("Paciente ya registrado")
        self.pacientes[paciente.dni] = paciente
        self.historias[paciente.dni] = HistoriaClinica(paciente)

    def registrar_medico(self, medico: Medico):
        if medico.matricula in self.medicos:
            raise MedicoYaExisteError("Médico ya registrado")
        self.medicos[medico.matricula] = medico

    def agendar_turno(self, dni: str, matricula: str, fecha: str, hora: str) -> Turno:
        if dni not in self.pacientes:
            raise PacienteNoExisteError("Paciente no encontrado")
        if matricula not in self.medicos:
            raise MedicoNoExisteError("Médico no encontrado")

        paciente = self.pacientes[dni]
        medico = self.medicos[matricula]
        nuevo_turno = Turno(paciente, medico, fecha, hora)

        for t in self.turnos:
            if t.medico.matricula == matricula and t.fecha == fecha and t.hora == hora:
                raise TurnoDuplicadoError("El médico ya tiene un turno en ese horario")

        self.turnos.append(nuevo_turno)
        return nuevo_turno

    def recetar_medicamento(self, dni: str, matricula: str, medicamento: str, fecha: str) -> Receta:
        if dni not in self.pacientes:
            raise PacienteNoExisteError("Paciente no encontrado")
        if matricula not in self.medicos:
            raise MedicoNoExisteError("Médico no encontrado")
        if not medicamento:
            raise RecetaInvalidaError("El medicamento no puede estar vacío")

        receta = Receta(self.pacientes[dni], self.medicos[matricula], medicamento, fecha)
        self.historias[dni].agregar_receta(receta)
        return receta

    def obtener_historia_clinica(self, dni: str) -> HistoriaClinica:
        if dni not in self.historias:
            raise PacienteNoExisteError("Paciente no encontrado")
        return self.historias[dni]

    def obtener_turnos(self) -> List[Turno]:
        return self.turnos

    def obtener_especialidad_disponible(self, medico: Medico, dia: str) -> Especialidad:
        especialidad = medico.obtener_especialidad_para_dia(dia)
        if especialidad is None:
            raise EspecialidadInvalidaError("El médico no tiene especialidad para ese día")
        return especialidad

# =======================
# Interfaz CLI
# =======================
class CLI:
    def __init__(self):
        self.clinica = Clinica()

    def mostrar_menu(self):
        print("\n" + "=" * 50)
        print("\U0001F3E5 SISTEMA DE GESTIÓN DE CLÍNICA MÉDICA")
        print("=" * 50)
        print("1. Agregar paciente")
        print("2. Agregar médico")
        print("3. Agendar turno")
        print("4. Emitir receta")
        print("5. Ver historia clínica")
        print("6. Ver todos los turnos")
        print("7. Ver todos los pacientes")
        print("8. Ver todos los médicos")
        print("9. Ver médico por matrícula")
        print("10. Agregar especialidad")
        print("11. Obtener especialidad disponible")
        print("12. Salir")
        print("=" * 50)

    def agregar_paciente(self):
        print("\n--- AGREGAR PACIENTE ---")
        dni = input("DNI: ")
        nombre = input("Nombre completo: ")
        fecha_nacimiento = input("Fecha de nacimiento (dd/mm/aaaa): ")
        paciente = Paciente(dni, nombre, fecha_nacimiento)
        try:
            self.clinica.registrar_paciente(paciente)
            print(f"Paciente {nombre} agregado exitosamente.")
        except PacienteYaExisteError as e:
            print(f"Error: {e}")

    def agregar_medico(self):
        print("\n--- AGREGAR MÉDICO ---")
        matricula = input("Matrícula: ")
        nombre = input("Nombre completo: ")
        especialidad_nombre = input("Especialidad principal: ")
        especialidad = Especialidad(especialidad_nombre, [])
        medico = Medico(matricula, nombre, [especialidad])
        try:
            self.clinica.registrar_medico(medico)
            print(f"Dr. {nombre} agregado exitosamente.")
        except MedicoYaExisteError as e:
            print(f"Error: {e}")

    def agendar_turno(self):
        print("\n--- AGENDAR TURNO ---")
        try:
            dni = input("DNI del paciente: ")
            matricula = input("Matrícula del médico: ")
            fecha = input("Fecha (YYYY-MM-DD): ")
            hora = input("Hora (HH:MM): ")
            turno = self.clinica.agendar_turno(dni, matricula, fecha, hora)
            print("Turno agendado exitosamente:")
            print(turno)
        except (PacienteNoExisteError, MedicoNoExisteError,
                TurnoDuplicadoError, EspecialidadInvalidaError, ValueError) as e:
            print(f"Error: {e}")

    def emitir_receta(self):
        print("\n--- EMITIR RECETA ---")
        try:
            dni = input("DNI del paciente: ")
            matricula = input("Matrícula del médico: ")
            medicamento = input("Medicamento recetado: ")
            fecha = input("Fecha de la receta (YYYY-MM-DD): ")
            receta = self.clinica.recetar_medicamento(dni, matricula, medicamento, fecha)
            print("Receta emitida exitosamente:")
            print(receta)
        except (PacienteNoExisteError, MedicoNoExisteError, RecetaInvalidaError) as e:
            print(f"Error: {e}")

    def ver_historia_clinica(self):
        print("\n--- VER HISTORIA CLÍNICA ---")
        dni = input("DNI del paciente: ")
        try:
            historia = self.clinica.obtener_historia_clinica(dni)
            print(historia)
        except PacienteNoExisteError as e:
            print(f"Error: {e}")

    def ver_todos_los_turnos(self):
        print("\n--- TODOS LOS TURNOS ---")
        turnos = self.clinica.obtener_turnos()
        if turnos:
            for i, turno in enumerate(turnos, 1):
                print(f"{i}. {turno}")
        else:
            print("No hay turnos registrados.")

    def ver_todos_los_pacientes(self):
        print("\n--- TODOS LOS PACIENTES ---")
        if self.clinica.pacientes:
            for i, paciente in enumerate(self.clinica.pacientes.values(), 1):
                print(f"{i}. {paciente}")
        else:
            print("No hay pacientes registrados.")

    def ver_todos_los_medicos(self):
        print("\n--- TODOS LOS MÉDICOS ---")
        if self.clinica.medicos:
            for i, medico in enumerate(self.clinica.medicos.values(), 1):
                print(f"{i}. {medico}")
        else:
            print("No hay médicos registrados.")

    def buscar_medico_por_matricula(self, matricula: str):
        try:
            medico = self.clinica.medicos[matricula]
            print(f"\nMédico encontrado: {medico}")
        except KeyError:
            print("Error: Médico no encontrado.")

    def agregar_especialidad(self):
        print("\n--- AGREGAR ESPECIALIDAD ---")
        matricula = input("Matrícula del médico: ")
        tipo = input("Tipo de especialidad: ")
        print("Ingrese los días disponibles (uno por línea, Enter vacío para terminar):")
        dias = []
        while True:
            dia = input("Día: ").strip()
            if not dia:
                break
            dias.append(dia)

        try:
            medico = self.clinica.medicos[matricula]
            especialidad = Especialidad(tipo, dias)
            medico.agregar_especialidad(especialidad)
            print(f"Especialidad '{tipo}' agregada exitosamente.")
        except KeyError:
            print("Error: Médico no encontrado.")

    def obtener_especialidad_disponible(self):
        print("\n--- OBTENER ESPECIALIDAD DISPONIBLE ---")
        matricula = input("Matrícula del médico: ")
        dia_semana = input("Día de la semana: ")
        try:
            medico = self.clinica.medicos[matricula]
            especialidad = self.clinica.obtener_especialidad_disponible(medico, dia_semana)
            print(f"Especialidad disponible: {especialidad}")
        except (KeyError, EspecialidadInvalidaError) as e:
            print(f"Error: {e}")

    def ejecutar(self):
        while True:
            self.mostrar_menu()
            opcion = input("Seleccione una opción (1-12): ").strip()
            if opcion == "1":
                self.agregar_paciente()
            elif opcion == "2":
                self.agregar_medico()
            elif opcion == "3":
                self.agendar_turno()
            elif opcion == "4":
                self.emitir_receta()
            elif opcion == "5":
                self.ver_historia_clinica()
            elif opcion == "6":
                self.ver_todos_los_turnos()
            elif opcion == "7":
                self.ver_todos_los_pacientes()
            elif opcion == "8":
                self.ver_todos_los_medicos()
            elif opcion == "9":
                matricula = input("Ingrese matrícula del médico: ")
                self.buscar_medico_por_matricula(matricula)
            elif opcion == "10":
                self.agregar_especialidad()
            elif opcion == "11":
                self.obtener_especialidad_disponible()
            elif opcion == "12":
                print("¡Gracias por usar el sistema de la clínica!")
                break
            else:
                print("Opción inválida. Ingrese un número del 1 al 12.")

# =======================
# Función principal
# =======================
def main():
    print("Bienvenido al Sistema de Gestión de Clínica Médica!")
    print("\n¿Qué desea hacer?")
    print("1. Ejecutar la aplicación")
    print("2. Ejecutar tests unitarios")
    print("3. Salir")

    opcion = input("Seleccione una opción (1-3): ").strip()

    if opcion == "1":
        cli = CLI()
        cli.ejecutar()
    elif opcion == "2":
        print("\nEjecutando tests unitarios...")
        unittest.main(argv=[''], exit=False, verbosity=2)
    elif opcion == "3":
        print("¡Hasta luego!")
    else:
        print("Opción inválida")

if __name__ == "__main__":
    main()
