# Tecnologías y alcance

Python 3.10+, SQLite y herramientas de negocio permitidas. La planificación Ollama es opcional; se incluyen workflow n8n, Docker y CI.

| Tecnología | Estado | Uso en este proyecto |
| --- | --- | --- |
| Python 3.10+ / API HTTP / CLI | Implementado | Planificación local y ciclo run, approve, reject, execute y get. |
| SQLite / consultas parametrizadas | Implementado | Pedidos y existencias sintéticas, planes, propuestas y trazas por tenant. |
| JSON / SHA-256 | Implementado | Contrato de herramientas, serialización y huella del plan persistido. |
| Presupuesto en tool_units | Implementado | Límite interno acumulado por herramienta; no representa dinero ni tokens. |
| Ollama / salida estructurada | Opcional | Propone pasos que deben superar las mismas validaciones del ejecutor. |
| n8n / Docker Compose | Archivos incluidos | Puente HTTP y empaquetado local; configuración y runtime deben validarse. |
| unittest / GitHub Actions | Implementado | Herramientas permitidas, aprobación, presupuesto, reanudación y HTTP. |
| ERP e identidad empresarial | Por conectar | Las herramientas operan sobre SQLite; el token compartido no identifica aprobadores humanos. |

“Implementado” describe código disponible y comprobable en el repositorio. “Opcional” requiere un proveedor configurado; “incluido” identifica un archivo o adaptador entregado, sin afirmar una integración externa ejecutada.

[Arquitectura](architecture.md) · [Flujo de operación](flow.md) · [Integraciones](integrations.md)
