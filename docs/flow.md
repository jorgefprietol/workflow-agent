# Flujo de operación

![Flujo de operación](diagrams/flow.svg)

[Abrir SVG](diagrams/flow.svg) · [Fuente Mermaid](diagrams/flow.mmd)


<details>
<summary>Versión Mermaid</summary>

```mermaid
flowchart TD
    Start["Recibir tarea o plan"] --> Validate["Validar herramientas y argumentos"]
    Validate --> Save["Persistir plan, huella y presupuesto"]
    Save --> Step["Cargar siguiente paso persistido"]
    Step --> Budget{"¿Alcanza el presupuesto restante?"}
    Budget -->|No| Exhausted["Detener por presupuesto agotado"]
    Budget -->|Sí| Write{"¿Escritura sin aprobación?"}
    Write -->|Sí| Approval["Esperar aprobación o rechazo explícito"]
    Approval -->|Aprobar y reanudar| Step
    Write -->|No| Execute["Ejecutar herramienta permitida"]
    Execute --> Trace["Registrar resultado, tiempo y unidades"]
    Trace --> More{"¿Quedan pasos?"}
    More -->|Sí| Step
    More -->|No| Complete["Finalizar sin repetir la propuesta"]
```

</details>

- El plan admite hasta seis pasos y una única escritura al final. El modelo no define permisos del ejecutor.
- La reanudación utiliza plan y posición guardados; no reinicia unidades consumidas ni sustituye el plan por parámetros nuevos.
- `proposal.create` comprueba existencias y crea sólo un borrador local. No reserva ni modifica inventario.

Las operaciones del dominio se guardan junto a auditoría y respuesta idempotente en la transacción del servicio local. Un error revierte los cambios de esa solicitud.

[Arquitectura](architecture.md) · [Tecnologías y alcance](technologies.md)
