from datetime import datetime
from typing import List


# Excepciones personalizadas
class PacienteYaRegistradoException(Exception):
    pass


class MedicoYaRegistradoException(Exception):
    pass


class PacienteNoEncontradoException(Exception):
    pass


class MedicoNoEncontradoException(Exception):
    pass


class EspecialidadDuplicadaException(Exception):
    pass


class EspecialidadInvalidaException(Exception):
    pass


class TurnoOcupadoException(Exception):
    pass


class TurnoInvalidoException(Exception):
    pass


class RecetaInvalidaException(Exception):
    pass


# Clases base

class Paciente:
    def __init__(self, nombre: str, apellido: str, dni: str, edad: int):
        if not nombre or not apellido or not dni:
            raise ValueError("Nombre, apellido y dni no pueden estar vacíos")
        self._nombre = nombre
        self._apellido = apellido
        self._dni = dni
        self._edad = edad

    @property
    def nombre(self):
        return self._nombre

    @property
    def apellido(self):
        return self._apellido

    @property
    def dni(self):
        return self._dni

    @property
    def edad(self):
        return self._edad


class Especialidad:
    def __init__(self, nombre: str, dias_atencion: List[int]):
        if not nombre:
            raise EspecialidadInvalidaException("El nombre de especialidad no puede estar vacío")
        if not all(isinstance(d, int) and 0 <= d <= 6 for d in dias_atencion):
            raise EspecialidadInvalidaException("Los días de atención deben ser enteros entre 0 y 6")
        self._nombre = nombre
        self._dias_atencion = dias_atencion

    @property
    def nombre(self):
        return self._nombre

    @property
    def dias_atencion(self):
        return self._dias_atencion

    def __eq__(self, other):
        if not isinstance(other, Especialidad):
            return False
        return self.nombre == other.nombre

    def __hash__(self):
        return hash(self.nombre)


class Medico:
    def __init__(self, nombre: str, apellido: str, matricula: str, especialidades: List[Especialidad]):
        if not nombre or not apellido or not matricula:
            raise ValueError("Nombre, apellido y matrícula no pueden estar vacíos")
        self._nombre = nombre
        self._apellido = apellido
        self._matricula = matricula
        self._especialidades = list(especialidades) if especialidades else []

    @property
    def nombre(self):
        return self._nombre

    @property
    def apellido(self):
        return self._apellido

    @property
    def matricula(self):
        return self._matricula

    @property
    def especialidades(self):
        return self._especialidades

    def agregar_especialidad(self, especialidad: Especialidad):
        if especialidad in self._especialidades:
            raise EspecialidadDuplicadaException(f"Especialidad '{especialidad.nombre}' ya existe para este médico")
        self._especialidades.append(especialidad)


class Turno:
    def __init__(self, paciente: Paciente, medico: Medico, fecha: datetime, especialidad: Especialidad):
        self._paciente = paciente
        self._medico = medico
        self._fecha = fecha
        self._especialidad = especialidad

    @property
    def paciente(self):
        return self._paciente

    @property
    def medico(self):
        return self._medico

    @property
    def fecha(self):
        return self._fecha

    @property
    def especialidad(self):
        return self._especialidad

    def __eq__(self, other):
        if not isinstance(other, Turno):
            return False
        return (
            self.paciente.dni == other.paciente.dni and
            self.medico.matricula == other.medico.matricula and
            self.fecha == other.fecha and
            self.especialidad.nombre == other.especialidad.nombre
        )

    def __hash__(self):
        return hash((self.paciente.dni, self.medico.matricula, self.fecha, self.especialidad.nombre))


class Receta:
    def __init__(self, paciente: Paciente, medico: Medico, medicamentos: List[str]):
        if not medicamentos or not isinstance(medicamentos, list) or len(medicamentos) == 0:
            raise RecetaInvalidaException("La receta debe contener al menos un medicamento")
        self._paciente = paciente
        self._medico = medico
        self._medicamentos = medicamentos

    @property
    def paciente(self):
        return self._paciente

    @property
    def medico(self):
        return self._medico

    @property
    def medicamentos(self):
        return self._medicamentos

    def __eq__(self, other):
        if not isinstance(other, Receta):
            return False
        return (
            self.paciente.dni == other.paciente.dni and
            self.medico.matricula == other.medico.matricula and
            self.medicamentos == other.medicamentos
        )

    def __hash__(self):
        return hash((self.paciente.dni, self.medico.matricula, tuple(self.medicamentos)))


class Clinica:
    def __init__(self):
        self.pacientes = {}  # dni -> Paciente
        self.medicos = {}    # matricula -> Medico
        self._turnos = []    # lista de Turnos
        self._recetas = []   # lista de Recetas

    def agregar_paciente(self, paciente: Paciente):
        if paciente.dni in self.pacientes:
            raise PacienteYaRegistradoException(f"Paciente con DNI {paciente.dni} ya registrado")
        self.pacientes[paciente.dni] = paciente

    def agregar_medico(self, medico: Medico):
        if medico.matricula in self.medicos:
            raise MedicoYaRegistradoException(f"Médico con matrícula {medico.matricula} ya registrado")
        self.medicos[medico.matricula] = medico

    def agregar_especialidad_a_medico(self, matricula_medico: str, especialidad: Especialidad):
        if matricula_medico not in self.medicos:
            raise MedicoNoEncontradoException(f"Médico con matrícula {matricula_medico} no encontrado")
        medico = self.medicos[matricula_medico]
        medico.agregar_especialidad(especialidad)

    def agendar_turno(self, dni_paciente: str, matricula_medico: str, fecha: datetime, nombre_especialidad: str) -> Turno:
        # Validaciones iniciales
        if dni_paciente not in self.pacientes:
            raise PacienteNoEncontradoException(f"Paciente con DNI {dni_paciente} no encontrado")
        if matricula_medico not in self.medicos:
            raise MedicoNoEncontradoException(f"Médico con matrícula {matricula_medico} no encontrado")

        paciente = self.pacientes[dni_paciente]
        medico = self.medicos[matricula_medico]

        # Verifico que el médico tenga esa especialidad
        especialidad = None
        for esp in medico.especialidades:
            if esp.nombre == nombre_especialidad:
                especialidad = esp
                break

        if especialidad is None:
            raise TurnoInvalidoException(f"Médico no atiende la especialidad {nombre_especialidad}")

        # Verifico que la fecha sea un día que el médico atiende
        if fecha.weekday() not in especialidad.dias_atencion:
            raise TurnoInvalidoException(f"El médico no trabaja ese día ({fecha.strftime('%A')})")

        # Verifico que el turno no esté ocupado (para el mismo médico y fecha)
        for turno_existente in self._turnos:
            if (turno_existente.medico.matricula == matricula_medico and
                    turno_existente.fecha == fecha):
                raise TurnoOcupadoException("El turno está ocupado para ese médico y fecha")

        turno = Turno(paciente, medico, fecha, especialidad)
        self._turnos.append(turno)
        return turno

    def emitir_receta(self, dni_paciente: str, matricula_medico: str, medicamentos: List[str]) -> Receta:
        if dni_paciente not in self.pacientes:
            raise PacienteNoEncontradoException(f"Paciente con DNI {dni_paciente} no encontrado")
        if matricula_medico not in self.medicos:
            raise MedicoNoEncontradoException(f"Médico con matrícula {matricula_medico} no encontrado")

        if not medicamentos or len(medicamentos) == 0:
            raise RecetaInvalidaException("La lista de medicamentos no puede estar vacía")

        paciente = self.pacientes[dni_paciente]
        medico = self.medicos[matricula_medico]

        receta = Receta(paciente, medico, medicamentos)
        self._recetas.append(receta)
        return receta

    def historia_clinica_turnos(self, dni_paciente: str) -> List[Turno]:
        return [t for t in self._turnos if t.paciente.dni == dni_paciente]

    def historia_clinica_recetas(self, dni_paciente: str) -> List[Receta]:
        return [r for r in self._recetas if r.paciente.dni == dni_paciente]


# Interfaz por consola (opcional si se requiere)
class CLI:
    def __init__(self, clinica):
        self._clinica = clinica

    def ejecutar(self):
        while True:
            print("\n--- Sistema de Gestión Clínica ---")
            print("1. Agregar paciente")
            print("2. Agregar médico")
            print("3. Agregar especialidad a médico")
            print("4. Agendar turno")
            print("5. Emitir receta")
            print("6. Ver historia clínica")
            print("0. Salir")

            opcion = input("Seleccione una opción: ")

            if opcion == "1":
                nombre = input("Nombre del paciente: ")
                dni = input("DNI del paciente: ")
                fecha_str = input("Fecha de nacimiento (YYYY-MM-DD): ")
                fecha = datetime.strptime(fecha_str, "%Y-%m-%d")
                paciente = Paciente(nombre, dni, fecha)
                try:
                    self._clinica.agregar_paciente(paciente)
                    print("Paciente agregado con éxito.")
                except ValueError as e:
                    print("Error:", e)

            elif opcion == "2":
                nombre = input("Nombre del médico: ")
                matricula = input("Matrícula: ")
                medico = Medico(nombre, matricula)
                try:
                    self._clinica.agregar_medico(medico)
                    print("Médico agregado con éxito.")
                except ValueError as e:
                    print("Error:", e)

            elif opcion == "3":
                matricula = input("Matrícula del médico: ")
                nombre_esp = input("Nombre de la especialidad: ")
                dias = input("Días disponibles (separados por coma, en inglés): ").split(",")
                especialidad = Especialidad(nombre_esp, [d.strip() for d in dias])
                try:
                    self._clinica.agregar_especialidad_a_medico(matricula, especialidad)
                    print("Especialidad agregada al médico.")
                except Exception as e:
                    print("Error:", e)

            elif opcion == "4":
                dni = input("DNI del paciente: ")
                matricula = input("Matrícula del médico: ")
                especialidad = input("Especialidad: ")
                fecha_str = input("Fecha del turno (YYYY-MM-DD HH:MM): ")
                fecha = datetime.strptime(fecha_str, "%Y-%m-%d %H:%M")
                try:
                    self._clinica.agendar_turno(dni, matricula, especialidad, fecha)
                    print("Turno agendado con éxito.")
                except Exception as e:
                    print("Error:", e)

            elif opcion == "5":
                dni = input("DNI del paciente: ")
                matricula = input("Matrícula del médico: ")
                medicamentos = input("Medicamentos (separados por coma): ").split(",")
                medicamentos = [m.strip() for m in medicamentos]
                try:
                    self._clinica.emitir_receta(dni, matricula, medicamentos)
                    print("Receta emitida con éxito.")
                except Exception as e:
                    print("Error:", e)

            elif opcion == "6":
                dni = input("DNI del paciente: ")
                try:
                    print(self._clinica.ver_historia_clinica(dni))
                except Exception as e:
                    print("Error:", e)

            elif opcion == "0":
                print("Saliendo del sistema.")
                break

            else:
                print("Opción inválida.")


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
