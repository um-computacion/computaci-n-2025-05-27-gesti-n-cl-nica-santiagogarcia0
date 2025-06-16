import unittest
from clinica import (
    Paciente, Medico, Especialidad, Turno, Receta, HistoriaClinica, Clinica,
    PacienteYaExisteError, PacienteNoExisteError,
    MedicoYaExisteError, MedicoNoExisteError,
    TurnoDuplicadoError, EspecialidadInvalidaError,
    RecetaInvalidaError
)

class TestClinica(unittest.TestCase):
    def setUp(self):
        self.clinica = Clinica()
        self.paciente = Paciente("12345678", "Juan Pérez", "01/01/1980")
        self.especialidad = Especialidad("Clínica Médica", ["Lunes", "Miércoles"])
        self.medico = Medico("M001", "Dr. House", [self.especialidad])
        self.clinica.registrar_paciente(self.paciente)
        self.clinica.registrar_medico(self.medico)

    def test_registrar_paciente_duplicado(self):
        with self.assertRaises(PacienteYaExisteError):
            self.clinica.registrar_paciente(Paciente("12345678", "Otro Nombre", "02/02/1990"))

    def test_registrar_medico_duplicado(self):
        with self.assertRaises(MedicoYaExisteError):
            self.clinica.registrar_medico(Medico("M001", "Otro Médico", [self.especialidad]))

    def test_agendar_turno_ok(self):
        turno = self.clinica.agendar_turno("12345678", "M001", "2025-06-20", "10:00")
        self.assertIsInstance(turno, Turno)
        self.assertEqual(len(self.clinica.turnos), 1)

    def test_agendar_turno_con_paciente_inexistente(self):
        with self.assertRaises(PacienteNoExisteError):
            self.clinica.agendar_turno("99999999", "M001", "2025-06-20", "10:00")

    def test_agendar_turno_con_medico_inexistente(self):
        with self.assertRaises(MedicoNoExisteError):
            self.clinica.agendar_turno("12345678", "X001", "2025-06-20", "10:00")

    def test_agendar_turno_duplicado(self):
        self.clinica.agendar_turno("12345678", "M001", "2025-06-20", "10:00")
        with self.assertRaises(TurnoDuplicadoError):
            self.clinica.agendar_turno("12345678", "M001", "2025-06-20", "10:00")

    def test_recetar_medicamento_ok(self):
        receta = self.clinica.recetar_medicamento("12345678", "M001", "Paracetamol", "2025-06-20")
        self.assertIsInstance(receta, Receta)

    def test_recetar_con_datos_invalidos(self):
        with self.assertRaises(PacienteNoExisteError):
            self.clinica.recetar_medicamento("00000000", "M001", "Ibuprofeno", "2025-06-20")

    def test_obtener_historia_clinica(self):
        self.clinica.recetar_medicamento("12345678", "M001", "Paracetamol", "2025-06-20")
        historia = self.clinica.obtener_historia_clinica("12345678")
        self.assertIsInstance(historia, HistoriaClinica)
        self.assertEqual(len(historia.recetas), 1)

    def test_obtener_especialidad_disponible_ok(self):
        especialidad = self.clinica.obtener_especialidad_disponible(self.medico, "Lunes")
        self.assertEqual(especialidad.tipo, "Clínica Médica")

    def test_obtener_especialidad_disponible_fail(self):
        with self.assertRaises(EspecialidadInvalidaError):
            self.clinica.obtener_especialidad_disponible(self.medico, "Domingo")

    def test_listados(self):
        self.assertEqual(len(self.clinica.obtener_turnos()), 0)
        self.assertIn("12345678", self.clinica.pacientes)
        self.assertIn("M001", self.clinica.medicos)

if __name__ == '__main__':
    unittest.main()
