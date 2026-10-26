# Workflow Agent

Orquestador de herramientas de negocio con planes explícitos, presupuesto acumulado y aprobación de escrituras. Consulta pedidos e inventario sintéticos y puede preparar una propuesta local sin modificar existencias ni invocar servicios externos.

## Contexto y confidencialidad

Este caso de uso forma parte de mi experiencia en soluciones implementadas en producción durante trabajos de consultoría. La versión pública es una implementación independiente con datos sintéticos que permite revisar la arquitectura, los flujos y los controles. Por confidencialidad, no se incluyen la identidad del cliente, su código ni sus registros operativos.

## Diseño y tecnologías

Python 3.10+, SQLite y herramientas de negocio permitidas. La planificación Ollama es opcional; se incluyen workflow n8n, Docker y CI.

[Diagrama de arquitectura](docs/architecture.md) · [Diagrama del flujo](docs/flow.md) · [Tecnologías y alcance](docs/technologies.md)

## Ejecutar

Requiere Python 3.10 o posterior; el modo local usa la biblioteca estándar.

```powershell
python -m app demo
python -m unittest discover -s tests -v
$env:SERVICE_TOKEN = 'una-clave-local-de-al-menos-24-caracteres'
python -m app serve
```

Abra `http://127.0.0.1:8080` para inspeccionar solicitudes y respuestas. `demo` utiliza una base temporal. Para continuar un plan entre comandos:

```powershell
python -m app run --input data/run.json --key run-demo-001
```

La respuesta contiene el identificador persistente de la ejecución. En la base del servicio, las operaciones `approve` y `execute` deben referirse a ese identificador.

## Herramientas y controles

| Herramienta | Argumento | Unidades | Permiso |
| --- | --- | --- | --- |
| `order.lookup` | `order_id` | 1 | Lectura |
| `stock.lookup` | `sku` | 1 | Lectura |
| `proposal.create` | `order_id` | 3 | Escritura con aprobación |

Las unidades son un presupuesto interno de herramientas, no un precio monetario ni un conteo de tokens. El plan admite hasta seis pasos y una única escritura al final. Las herramientas y sus argumentos se validan antes de iniciar la ejecución.

El ejemplo se detiene en `waiting_approval` tras las lecturas. Para aprobarlo, envíe:

```json
{"action":"approve","tenant":"demo","id":"<id-de-la-ejecucion>","actor":"reviewer","reason":"Pedido y alcance revisados"}
```

Después, envíe `{"action":"execute","tenant":"demo","id":"<id-de-la-ejecucion>"}`. Se crea un borrador local si sigue existiendo inventario suficiente. La ejecución terminada puede consultarse y reintentarse sin crear una segunda propuesta. `reject` impide la escritura. Un presupuesto agotado no se reinicia al reanudar.

| Acción | Resultado |
| --- | --- |
| `plan` | Vista previa sin crear ejecución |
| `run` | Planifica y ejecuta hasta terminar o requerir aprobación |
| `get` | Consulta plan, estado y traza |
| `approve` / `reject` | Registra decisión, operador y motivo |
| `execute` | Reanuda el plan persistido |

## Modelo opcional e integración

`MODEL_BACKEND=local` construye un plan reproducible a partir de un pedido `ORDER-0000`. Con `MODEL_BACKEND=ollama`, `OLLAMA_URL` y `OLLAMA_MODEL`, el modelo propone el plan mediante salida estructurada. Ambos recorridos pasan por la misma lista de herramientas y validaciones. No se ejecuta shell, SQL aportado por el usuario, código dinámico ni solicitudes HTTP arbitrarias.

`POST /api/run` requiere token Bearer e `Idempotency-Key`. `GET /health` comprueba el proceso y `GET /api/metrics` devuelve métricas locales. El flujo n8n incluido permite invocar la API; conectores de ERP e identidad empresarial deben configurarse fuera del modo de demostración.

## Evidencia disponible

Cada paso conserva resultado, duración y unidades consumidas. Estas trazas permiten revisar éxito técnico y presupuesto por tarea. No representan ahorro económico, coste de inferencia ni resultados de clientes. La aprobación documenta una decisión con el token compartido del servicio; no sustituye un sistema de roles por usuario.

[Arquitectura](docs/architecture.md) · [Decisiones](docs/decisions.md) · [Operación](docs/operations.md) · [Referencias](docs/references.md)
