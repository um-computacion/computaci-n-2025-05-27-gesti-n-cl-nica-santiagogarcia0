import unittest
from datetime import datetime, timedelta

from clinica import (
    Clinica, Paciente, Medico, Especialidad, Turno, Receta,
    PacienteYaRegistradoException,
    MedicoYaRegistradoException,
    PacienteNoEncontradoException,
    MedicoNoEncontradoException,
    EspecialidadDuplicadaException,
    EspecialidadInvalidaException,
    TurnoOcupadoException,
    TurnoInvalidoException,
    RecetaInvalidaException
)

class TestClinica(unittest.TestCase):

    def setUp(self):
        self.clinica = Clinica()

    # --- Pacientes y Médicos ---

    def test_registro_paciente_exitoso(self):
        paciente = Paciente("Juan", "Perez", "12345678", 30)
        self.clinica.agregar_paciente(paciente)
        self.assertIn("12345678", self.clinica.pacientes)

    def test_registro_medico_exitoso(self):
        medico = Medico("Carlos", "Lopez", "M123", [])
        self.clinica.agregar_medico(medico)
        self.assertIn("M123", self.clinica.medicos)

    def test_registro_paciente_duplicado(self):
        paciente1 = Paciente("Juan", "Perez", "12345678", 30)
        paciente2 = Paciente("Ana", "Gomez", "12345678", 25)  # Mismo DNI
        self.clinica.agregar_paciente(paciente1)
        with self.assertRaises(PacienteYaRegistradoException):
            self.clinica.agregar_paciente(paciente2)

    def test_registro_medico_duplicado(self):
        medico1 = Medico("Carlos", "Lopez", "M123", [])
        medico2 = Medico("Luis", "Diaz", "M123", [])  # Mismo número de matrícula
        self.clinica.agregar_medico(medico1)
        with self.assertRaises(MedicoYaRegistradoException):
            self.clinica.agregar_medico(medico2)

    def test_registro_paciente_datos_invalidos(self):
        with self.assertRaises(ValueError):
            paciente = Paciente("", "Perez", "12345678", 30)
            self.clinica.agregar_paciente(paciente)
        with self.assertRaises(ValueError):
            paciente = Paciente("Juan", "", "12345678", 30)
            self.clinica.agregar_paciente(paciente)
        with self.assertRaises(ValueError):
            paciente = Paciente("Juan", "Perez", "", 30)
            self.clinica.agregar_paciente(paciente)

    def test_registro_medico_datos_invalidos(self):
        with self.assertRaises(ValueError):
            medico = Medico("", "Lopez", "M123", [])
            self.clinica.agregar_medico(medico)
        with self.assertRaises(ValueError):
            medico = Medico("Carlos", "", "M123", [])
            self.clinica.agregar_medico(medico)
        with self.assertRaises(ValueError):
            medico = Medico("Carlos", "Lopez", "", [])
            self.clinica.agregar_medico(medico)

    # --- Especialidades ---

    def test_agregar_especialidad_a_medico_exitoso(self):
        medico = Medico("Carlos", "Lopez", "M123", [])
        especialidad = Especialidad("Cardiología", [0, 2, 4])
        self.clinica.agregar_medico(medico)
        self.clinica.agregar_especialidad_a_medico("M123", especialidad)
        self.assertIn(especialidad, self.clinica.medicos["M123"].especialidades)

    def test_agregar_especialidad_duplicada(self):
        medico = Medico("Carlos", "Lopez", "M123", [])
        especialidad = Especialidad("Cardiología", [0, 2, 4])
        self.clinica.agregar_medico(medico)
        self.clinica.agregar_especialidad_a_medico("M123", especialidad)
        with self.assertRaises(EspecialidadDuplicadaException):
            self.clinica.agregar_especialidad_a_medico("M123", especialidad)

    def test_especialidad_dias_invalidos(self):
        with self.assertRaises(EspecialidadInvalidaException):
            Especialidad("Neurología", [-1, 2])
        with self.assertRaises(EspecialidadInvalidaException):
            Especialidad("Dermatología", [0, 7])
        with self.assertRaises(EspecialidadInvalidaException):
            Especialidad("Pediatría", [10])

    def test_agregar_especialidad_medico_inexistente(self):
        especialidad = Especialidad("Cardiología", [0, 2, 4])
        with self.assertRaises(MedicoNoEncontradoException):
            self.clinica.agregar_especialidad_a_medico("M999", especialidad)

    # --- Turnos ---

    def test_agendar_turno_exitoso(self):
        paciente = Paciente("Ana", "Perez", "87654321", 25)
        medico = Medico("Carlos", "Lopez", "M123", [])
        especialidad = Especialidad("Cardiología", [0, 2, 4])
        self.clinica.agregar_paciente(paciente)
        self.clinica.agregar_medico(medico)
        self.clinica.agregar_especialidad_a_medico("M123", especialidad)
        fecha = datetime.now() + timedelta(days=1)
        # Ajusto fecha al próximo día que el médico atiende
        while fecha.weekday() not in especialidad.dias_atencion:
            fecha += timedelta(days=1)

        turno = self.clinica.agendar_turno("87654321", "M123", fecha, "Cardiología")
        self.assertIsInstance(turno, Turno)
        self.assertIn(turno, self.clinica.historia_clinica_turnos("87654321"))

    def test_agendar_turno_paciente_no_encontrado(self):
        medico = Medico("Carlos", "Lopez", "M123", [])
        especialidad = Especialidad("Cardiología", [0, 2, 4])
        self.clinica.agregar_medico(medico)
        self.clinica.agregar_especialidad_a_medico("M123", especialidad)
        fecha = datetime.now() + timedelta(days=1)
        while fecha.weekday() not in especialidad.dias_atencion:
            fecha += timedelta(days=1)
        with self.assertRaises(PacienteNoEncontradoException):
            self.clinica.agendar_turno("00000000", "M123", fecha, "Cardiología")

    def test_agendar_turno_medico_no_encontrado(self):
        paciente = Paciente("Ana", "Perez", "87654321", 25)
        self.clinica.agregar_paciente(paciente)
        fecha = datetime.now() + timedelta(days=1)
        with self.assertRaises(MedicoNoEncontradoException):
            self.clinica.agendar_turno("87654321", "M999", fecha, "Cardiología")

    def test_agendar_turno_turno_ocupado(self):
        paciente1 = Paciente("Ana", "Perez", "87654321", 25)
        paciente2 = Paciente("Juan", "Lopez", "12345678", 30)
        medico = Medico("Carlos", "Lopez", "M123", [])
        especialidad = Especialidad("Cardiología", [0, 2, 4])
        self.clinica.agregar_paciente(paciente1)
        self.clinica.agregar_paciente(paciente2)
        self.clinica.agregar_medico(medico)
        self.clinica.agregar_especialidad_a_medico("M123", especialidad)
        fecha = datetime.now() + timedelta(days=1)
        while fecha.weekday() not in especialidad.dias_atencion:
            fecha += timedelta(days=1)

        self.clinica.agendar_turno("87654321", "M123", fecha, "Cardiología")
        with self.assertRaises(TurnoOcupadoException):
            self.clinica.agendar_turno("12345678", "M123", fecha, "Cardiología")

    def test_turno_especialidad_no_atendida(self):
        paciente = Paciente("Ana", "Perez", "87654321", 25)
        medico = Medico("Carlos", "Lopez", "M123", [])
        especialidad_medico = Especialidad("Cardiología", [0, 2, 4])
        self.clinica.agregar_paciente(paciente)
        self.clinica.agregar_medico(medico)
        self.clinica.agregar_especialidad_a_medico("M123", especialidad_medico)
        fecha_turno = datetime.now() + timedelta(days=1)
        while fecha_turno.weekday() not in especialidad_medico.dias_atencion:
            fecha_turno += timedelta(days=1)
        especialidad_pedido = "Neurología"  # No atendida
        with self.assertRaises(TurnoInvalidoException):
            self.clinica.agendar_turno("87654321", "M123", fecha_turno, especialidad_pedido)

    def test_turno_medico_no_trabaja_ese_dia(self):
        paciente = Paciente("Ana", "Perez", "87654321", 25)
        medico = Medico("Carlos", "Lopez", "M123", [])
        especialidad = Especialidad("Cardiología", [0, 2, 4])
        self.clinica.agregar_paciente(paciente)
        self.clinica.agregar_medico(medico)
        self.clinica.agregar_especialidad_a_medico("M123", especialidad)
        fecha_turno = datetime.now()
        # Avanzo fecha hasta un día que no está en dias_atencion
        while fecha_turno.weekday() in especialidad.dias_atencion:
            fecha_turno += timedelta(days=1)
        with self.assertRaises(TurnoInvalidoException):
            self.clinica.agendar_turno("87654321", "M123", fecha_turno, "Cardiología")

    # --- Recetas ---

    def test_emitir_receta_exitoso(self):
        paciente = Paciente("Ana", "Perez", "87654321", 25)
        medico = Medico("Carlos", "Lopez", "M123", [])
        self.clinica.agregar_paciente(paciente)
        self.clinica.agregar_medico(medico)
        medicamentos = ["Paracetamol", "Ibuprofeno"]
        receta = self.clinica.emitir_receta("87654321", "M123", medicamentos)
        self.assertIsInstance(receta, Receta)
        self.assertIn(receta, self.clinica.historia_clinica_recetas("87654321"))

    def test_emitir_receta_sin_medicamentos(self):
        paciente = Paciente("Ana", "Perez", "87654321", 25)
        medico = Medico("Carlos", "Lopez", "M123", [])
        self.clinica.agregar_paciente(paciente)
        self.clinica.agregar_medico(medico)
        with self.assertRaises(RecetaInvalidaException):
            self.clinica.emitir_receta("87654321", "M123", [])

    def test_emitir_receta_paciente_inexistente(self):
        medico = Medico("Carlos", "Lopez", "M123", [])
        self.clinica.agregar_medico(medico)
        with self.assertRaises(PacienteNoEncontradoException):
            self.clinica.emitir_receta("00000000", "M123", ["Paracetamol"])

    def test_emitir_receta_medico_inexistente(self):
        paciente = Paciente("Ana", "Perez", "87654321", 25)
        self.clinica.agregar_paciente(paciente)
        with self.assertRaises(MedicoNoEncontradoException):
            self.clinica.emitir_receta("87654321", "M999", ["Paracetamol"])

    # --- Historia Clínica ---

    def test_historia_clinica_guarda_turno_y_receta(self):
        paciente = Paciente("Ana", "Perez", "87654321", 25)
        medico = Medico("Carlos", "Lopez", "M123", [])
        especialidad = Especialidad("Cardiología", [0, 2, 4])
        self.clinica.agregar_paciente(paciente)
        self.clinica.agregar_medico(medico)
        self.clinica.agregar_especialidad_a_medico("M123", especialidad)
        fecha = datetime.now() + timedelta(days=1)
        while fecha.weekday() not in especialidad.dias_atencion:
            fecha += timedelta(days=1)
        turno = self.clinica.agendar_turno("87654321", "M123", fecha, "Cardiología")
        medicamentos = ["Paracetamol"]
        receta = self.clinica.emitir_receta("87654321", "M123", medicamentos)
        turnos_hist = self.clinica.historia_clinica_turnos("87654321")
        recetas_hist = self.clinica.historia_clinica_recetas("87654321")
        self.assertIn(turno, turnos_hist)
        self.assertIn(receta, recetas_hist)


if __name__ == '__main__':
    unittest.main()
