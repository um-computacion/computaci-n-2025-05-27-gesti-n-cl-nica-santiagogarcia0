[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/y_fEcNZn)
# 🏥 Sistema de Gestión para una Clínica

## 👤 Información del Alumno

### 📋 Datos Personales
- **Nombre y Apellido**: [Completar con nombre y apellido]
- **Ciclo Lectivo**: 2025
- **Carrera**: [Completar con nombre de la carrera]

## ⏰ Información Importante sobre la Entrega

### 📅 Fechas Clave
- **Fecha límite de entrega**: 17 de junio de 2025
- **Fecha sugerida de entrega**: Semana del 10 de junio de 2025

### 📝 Consideraciones
Se recomienda encarecidamente a los estudiantes:

- Completar el trabajo práctico lo antes posible, idealmente para la semana del 10 de junio.
- Utilizar la clase de la semana próxima para resolver dudas y realizar ajustes finales.
- No postergar la entrega hasta el último momento, ya que no se aceptarán entregas después de la fecha límite establecida.

### ⚠️ Requisitos Académicos
En virtud de los estándares académicos establecidos y la importancia de mantener un nivel adecuado de participación:

- La entrega oportuna y completa de este trabajo práctico es un requisito fundamental para continuar con el cursado.
- Los estudiantes que no cumplan con los requisitos de entrega en tiempo y forma deberán recursar la materia en el próximo ciclo lectivo.
- Esta medida busca asegurar que todos los estudiantes alcancen los objetivos de aprendizaje establecidos para la materia.

### 📚 Instrucciones para el Desarrollo
**IMPORTANTE**: Antes de comenzar con el desarrollo del trabajo práctico:

- Lea detalladamente la consigna completa que se presenta a continuación.
- Asegúrese de comprender todos los requisitos y especificaciones técnicas.
- Consulte cualquier duda con los docentes durante la clase de la semana próxima.
- La implementación debe cumplir con todos los puntos especificados en la consigna.

---

## 📝 Consigna 

### 🎯 Objetivo

Desarrollar un sistema de gestión para una **clínica médica** utilizando programación orientada a objetos en Python. El sistema debe permitir:

- Registrar y administrar **pacientes** y **médicos**.
- Gestionar las **especialidades médicas** de cada profesional y sus **días de atención**.
- Agendar **turnos** entre pacientes y médicos respetando disponibilidad, especialidad y horarios.
- Emitir **recetas médicas**.
- Mantener una **historia clínica** para cada paciente, con registro de turnos y recetas.

---
### 🚨 Requisitos técnicos

- El sistema debe implementar:
  - Clases para `Paciente`, `Medico`, `Turno`, `Receta`, `Especialidad`, `HistoriaClinica`, y una clase principal `Clinica`.
  - Validaciones estrictas desde el **modelo** (no desde la interfaz de consola).
  - **Excepciones personalizadas** para manejar.
- Debe incluir una **interfaz de consola (CLI)** para interactuar con el sistema.
- Debe incluir **pruebas unitarias** usando `unittest`.

---

### 📦 Entregables

1. Código fuente del sistema con separación clara entre modelo y CLI.
2. Pruebas unitarias que cubran los casos principales y errores.
3. Documentación breve de:
   - Cómo ejecutar el sistema.
   - Cómo ejecutar las pruebas.
   - Explicación de diseño general.

---

# 📦 Clases y Responsabilidades

## 👤 Clase Paciente

Representa a un paciente de la clínica.

### 🔐 Atributos Privados
- `__nombre__`: `str` — Nombre completo del paciente.
- `__dni__`: `str` — DNI del paciente (identificador único).
- `__fecha_nacimiento__`: `str` — Fecha de nacimiento del paciente en formato `dd/mm/aaaa`.

### ⚙️ Métodos

#### 📄 Acceso a Información
- `obtener_dni() -> str`:  Devuelve el DNI del paciente.  

#### 🧾 Representación
- `__str__() -> str`:  Representación en texto del paciente.  

## 🩺 Clase Medico

Representa a un médico del sistema, con sus especialidades y matrícula profesional.

### 🔐 Atributos Privados
- `__nombre__`: `str` — Nombre completo del médico.
- `__matricula__`: `str` — Matrícula profesional del médico (clave única).
- `__especialidades__`: `list[Especialidad]` — Lista de especialidades con sus días de atención.

### ⚙️ Métodos

#### ✔️ Registro de Datos
- `agregar_especialidad(especialidad: Especialidad)`: Agrega una especialidad a la lista del médico.

#### 📄 Acceso a Información
- `obtener_matricula() -> str`: Devuelve la matrícula del médico.
- `obtener_especialidad_para_dia(dia: str) -> str | None`: Devuelve el nombre de la especialidad disponible en el día especificado, o `None` si no atiende ese día.

#### 🧾 Representación
- `__str__() -> str`: Representación legible del médico, incluyendo matrícula y especialidades.


## 🩺 Clase Especialidad

Representa una especialidad médica junto con los días de atención asociados.

### 🔐 Atributos Privados
- `__tipo__`: `str` — Nombre de la especialidad (por ejemplo, "Pediatría", "Cardiología").
- `__dias__`: `list[str]` — Lista de días en los que se atiende esta especialidad, en minúsculas.

### ⚙️ Métodos

#### 📄 Acceso a Información
- `obtener_especialidad() -> str`: Devuelve el nombre de la especialidad.

#### ✅ Validaciones
- `verificar_dia(dia: str) -> bool`: Devuelve `True` si la especialidad está disponible en el día proporcionado (no sensible a mayúsculas/minúsculas), `False` en caso contrario.

#### 🧾 Representación
- `__str__() -> str`: Devuelve una cadena legible con el nombre de la especialidad y los días de atención (por ejemplo: `"Pediatría (Días: lunes, miércoles, viernes)"`).


## 📅 Clase Turno

Representa un turno médico entre un paciente y un médico para una especialidad específica en una fecha y hora determinada.

### 🔐 Atributos Privados
- `__paciente__`: `Paciente` — Paciente que asiste al turno.
- `__medico__`: `Medico` — Médico asignado al turno.
- `__fecha_hora__`: `datetime` — Fecha y hora del turno.
- `__especialidad__`: `str` — Especialidad médica del turno.

### ⚙️ Métodos

#### 📄 Acceso a Información
- `obtener_medico() -> Medico`: Devuelve el médico asignado al turno.
- `obtener_fecha_hora() -> datetime`: Devuelve la fecha y hora del turno.

#### 🧾 Representación
- `__str__() -> str`: Devuelve una representación legible del turno, incluyendo paciente, médico, especialidad y fecha/hora.


## 💊 Clase Receta

Representa una receta médica emitida por un médico a un paciente, incluyendo los medicamentos recetados y la fecha de emisión.

### 🔐 Atributos Privados
- `__paciente__`: `Paciente` — Paciente al que se le emite la receta.
- `__medico__`: `Medico` — Médico que emite la receta.
- `__medicamentos__`: `list[str]` — Lista de medicamentos recetados.
- `__fecha__`: `datetime` — Fecha de emisión de la receta (automáticamente asignada con `datetime.now()`).

### ⚙️ Métodos

#### 🧾 Representación
- `__str__() -> str`: Devuelve una representación en cadena de la receta.

## 📋 Clase HistoriaClinica

Clase que almacena la información médica de un paciente: turnos y recetas.

### 🔐 Atributos Privados
- `__paciente__`: `Paciente` — Paciente al que pertenece la historia clínica.
- `__turnos__`: `list[Turno]` — Lista de turnos agendados del paciente.
- `__recetas__`: `list[Receta]` — Lista de recetas emitidas para el paciente.

### ⚙️ Métodos

#### ✔️ Registro de Datos
- `agregar_turno(turno: Turno)`: Agrega un nuevo turno a la historia clínica.
- `agregar_receta(receta: Receta)`: Agrega una receta médica a la historia clínica.

#### 📄 Acceso a Información
- `obtener_turnos() -> list[Turno]`: Devuelve una copia de la lista de turnos del paciente.
- `obtener_recetas() -> list[Receta]`: Devuelve una copia de la lista de recetas del paciente.

#### 🧾 Representación
- `__str__() -> str`: Devuelve una representación textual de la historia clínica, incluyendo turnos y recetas.


## 🏥 Clase Clinica

Clase principal que representa el sistema de gestión de la clínica.

### 🔐 Atributos Privados
- `__pacientes__`: `dict[str, Paciente]` — Mapea DNI del paciente a su objeto correspondiente.
- `__medicos__`: `dict[str, Medico]` — Mapea matrícula de médico a su objeto correspondiente.
- `__turnos__`: `list[Turno]` — Lista de todos los turnos agendados.
- `__historias_clinicas__`: `dict[str, HistoriaClinica]` — Mapea DNI a su historia clínica.

### ⚙️ Métodos

#### ✔️ Registro y Acceso
- `agregar_paciente(paciente: Paciente)`: Registra un paciente y crea su historia clínica.
- `agregar_medico(medico: Medico)`: Registra un médico.
- `obtener_pacientes() -> list[Paciente]`: Devuelve todos los pacientes registrados.
- `obtener_medicos() -> list[Medico]`: Devuelve todos los médicos registrados.
- `obtener_medico_por_matricula(matricula: str) -> Medico`: Devuelve un médico por su matrícula.

#### 📆 Turnos
- `agendar_turno(dni: str, matricula: str, especialidad: str, fecha_hora: datetime)`: Agenda un turno si se cumplen todas las condiciones.
- `obtener_turnos() -> list[Turno]`: Devuelve todos los turnos agendados.

#### 📑 Recetas e Historias Clínicas
- `emitir_receta(dni: str, matricula: str, medicamentos: list[str])`: Emite una receta para un paciente.
- `obtener_historia_clinica(dni: str) -> HistoriaClinica`: Devuelve la historia clínica completa de un paciente.

#### ✅ Validaciones y Utilidades
- `validar_existencia_paciente(dni: str)`: Verifica si un paciente está registrado.
- `validar_existencia_medico(matricula: str)`: Verifica si un médico está registrado.
- `validar_turno_no_duplicado(matricula: str, fecha_hora: datetime)`: Verifica que no haya un turno duplicado.
- `obtener_dia_semana_en_espanol(fecha_hora: datetime) -> str`: Traduce un objeto `datetime` al día de la semana en español.
- `obtener_especialidad_disponible(medico: Medico, dia_semana: str) -> str`: Obtiene la especialidad disponible para un médico en un día.
- `validar_especialidad_en_dia(medico: Medico, especialidad_solicitada: str, dia_semana: str)`: Verifica que el médico atienda esa especialidad ese día.


---

## ⚠️ Excepciones Personalizadas  
El sistema utiliza **excepciones personalizadas** para representar errores específicos del dominio de la clínica. Estas excepciones son lanzadas por la clase `Clinica` cuando ocurre una situación inválida o inesperada, como por ejemplo:

- `PacienteNoEncontradoException`
- `MedicoNoDisponibleException`
- `TurnoOcupadoException`
- `RecetaInvalidaException`

La clase `CLI` **captura estas excepciones** usando bloques `try-except` y muestra mensajes claros y amigables para el usuario final, evitando que el programa se detenga o muestre trazas técnicas.

---

## 💻 Interfaz de Consola (CLI)

La clase **CLI** actúa como la interfaz de usuario por consola para interactuar con el sistema de gestión de la clínica representado por la clase **Clinica**.

### 🎯 Propósito 

- Mostrar un menú interactivo con las opciones disponibles para el usuario.
- Solicitar datos por consola para cada operación.
- Llamar a los métodos correspondientes de la clase **Clinica** para realizar las acciones solicitadas.
- No realizar validaciones de negocio ni lógica compleja; esas responsabilidades están en la clase **Clinica**.
- Gestionar errores y excepciones que ocurren en **Clinica** para mostrar mensajes claros al usuario.

---

### 🔄 Flujo principal

Al ejecutar el programa, se muestra un menú con opciones numeradas, por ejemplo:
 
```text
--- Menú Clínica ---
1) Agregar paciente
2) Agregar médico
3) Agendar turno
4) Agregar especialidad
5) Emitir receta
6) Ver historia clínica
7) Ver todos los turnos
8) Ver todos los pacientes
9) Ver todos los médicos
0) Salir
```

El menú se muestra en un bucle continuo hasta que el usuario elige salir (`0`).

---

### ⚙️ Operaciones principales

- **Agregar paciente**  
  Solicita nombre, DNI y fecha de nacimiento, crea un objeto `Paciente` y lo registra en la clínica.

- **Agregar médico**  
  Solicita nombre y matrícula, y las especialidades con sus días de atención. Registra el médico en la clínica.

- **Agendar turno**  
  Solicita DNI de paciente, matrícula de médico, especialidad y fecha/hora. Intenta agendar el turno validando que no haya conflictos.

- **Agregar especialidad a médico**  
  Permite añadir especialidades y días de atención a un médico ya registrado.

- **Emitir receta**  
  Solicita DNI de paciente, matrícula de médico y medicamentos, luego registra la receta.

- **Ver historia clínica**  
  Muestra la historia clínica completa de un paciente (turnos y recetas).

- **Ver listados completos**  
  Muestra todos los turnos, pacientes o médicos registrados.

---

### ⚠️ Manejo de errores

Cuando una operación falla por razones como datos inválidos o entidades inexistentes, **CLI** captura las excepciones lanzadas por **Clinica** y muestra mensajes amigables en consola.


## 🧪 Unit Testing

El sistema debe incluir pruebas unitarias utilizando el módulo `unittest`, que validan el correcto funcionamiento de las operaciones del modelo, especialmente los casos esperados y los errores posibles.

### ✅ Casos de prueba cubiertos

#### 👥 Pacientes y Médicos

- ✅ Registro exitoso de pacientes y médicos.
- ❌ Prevención de registros duplicados (por DNI o matrícula).
- ⚠️ Verificación de errores por datos faltantes o inválidos.

#### 🩺 Especialidades

- ✅ Agregar especialidades nuevas a un médico ya registrado.
- ❌ Evitar duplicados de especialidad en el mismo médico.
- ❌ Detección de especialidades con días de atención inválidos.
- ⚠️ Error si se intenta agregar especialidad a un médico no registrado.

#### 📅 Turnos

- ✅ Agendamiento correcto de turnos si el médico está disponible y la especialidad es válida.
- ❌ Evitar turnos duplicados (mismo médico y fecha/hora).
- ❌ Error si el paciente o médico no existen.
- ❌ Error si el médico no atiende la especialidad solicitada.
- ❌ Error si el médico no trabaja ese día de la semana.

#### 💊 Recetas

- ✅ Emisión de recetas para un paciente válido por un médico válido.
- ❌ Error si alguno no existe.
- ❌ Error si no hay medicamentos listados.

#### 📘 Historia Clínica

- ✅ Confirmar que los turnos y recetas se guardan correctamente en la historia clínica del paciente.

---
