# Decisiones

| Decisión | Motivo | Consecuencia |
| --- | --- | --- |
| Herramientas cerradas con argumentos exactos | Reducir superficie de ejecución | Añadir una herramienta requiere código y revisión |
| Una escritura al final | Hacer el alcance aprobado fácil de revisar | No admite sagas con varias escrituras |
| Presupuesto acumulado | Evitar que un reintento reactive recursos consumidos | Una ejecución agotada termina sin seguir |
| Plan persistido con huella | Vincular aprobación y ejecución | Cambiar el plan exige crear otra ejecución |
| Propuesta sin reserva | Separar preparación y compromiso comercial | Un sistema ERP real debe reservar atómicamente |

La ejecución es transaccional en SQLite. Un adaptador remoto necesitaría idempotencia de destino, un outbox y compensaciones para efectos que no puedan revertirse con la transacción local.
