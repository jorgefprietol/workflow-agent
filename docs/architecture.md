# Arquitectura

![Arquitectura del servicio](diagrams/architecture.svg)

[Abrir SVG](diagrams/architecture.svg) · [Fuente Mermaid](diagrams/architecture.mmd)


Un planificador propone herramientas y un ejecutor aplica el contrato, el presupuesto y las aprobaciones. La persistencia permite reanudar el mismo plan sin repetir una propuesta completada.

<details>
<summary>Versión Mermaid</summary>

```mermaid
flowchart TB
    Client["CLI o consola web"] --> API["API con token e idempotencia"]
    subgraph Local["Servicio local implementado"]
        API --> Planner["Planificador determinista"]
        Planner --> Contract["Herramientas, argumentos y presupuesto"]
        Contract --> Executor["Ejecutor con reanudación"]
        Executor --> Reads["Consulta de pedidos e inventario"]
        Executor --> Approval["Aprobación explícita"]
        Approval --> Draft["Propuesta local"]
        Executor --> DB["Plan, posición y traza en SQLite"]
        Draft --> DB
    end
    subgraph Optional["Componentes opcionales por configurar"]
        N8N["Workflow n8n incluido"]
        Model["Planificador Ollama"]
    end
    N8N -.-> API
    Planner -.-> Model
    Model -.-> Contract
    External["APIs empresariales por conectar"] -.-> Reads
```

</details>

Las líneas continuas muestran el recorrido implementado dentro de cada límite. Las líneas discontinuas indican componentes opcionales, entregados para configurar o aún por conectar; su estado se precisa en [tecnologías](technologies.md).

El plan se serializa con una huella y se conserva antes de ejecutar pasos. La reanudación consulta ese plan persistido, su posición y su presupuesto consumido. Los parámetros nuevos de la solicitud no reemplazan el plan aprobado.

Las herramientas contienen consultas SQL parametrizadas y filtran por tenant. Sólo `demo` recibe pedidos sintéticos. La propuesta verifica de nuevo la disponibilidad; es un borrador y no reserva inventario.

La política de permisos pertenece al ejecutor. El modelo sólo produce una propuesta de plan. Las acciones de aprobación requieren una operación explícita de API; el contenido de una tarea no puede aprobarse a sí mismo. El token compartido autentica al cliente del servicio y debe reemplazarse por identidad y permisos por usuario para un entorno multiusuario.

[Flujo de operación](flow.md) · [Tecnologías y alcance](technologies.md)
