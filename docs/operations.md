# Operación

Ejecute cada solicitud con una clave de idempotencia propia y reutilícela sólo para reentregar el mismo cuerpo. Mantenga la misma base entre `run`, `approve` y `execute`. La demo temporal termina al salir y no sirve para reanudar con otra llamada.

`waiting_approval` conserva dos lecturas y un paso pendiente en el ejemplo. `approved` habilita la escritura del plan; `rejected`, `budget_exhausted` y `completed` son estados terminales. El registro `approved_by` proviene del cliente autenticado mediante token compartido, no de una identidad individual validada.

La traza contiene datos sintéticos de pedidos e inventario. Si se reemplaza por datos reales, aplique minimización, política de retención y permisos de consulta. No publique `var/`, tokens ni trazas de clientes en Git.

Las unidades consumidas permiten comparar planes bajo una política estable. Para calcular coste monetario deben añadirse uso real del proveedor, precio vigente y coste de los sistemas externos; el servicio no convierte unidades en dinero.

Antes de conectar un ERP, pruebe reintentos simultáneos, pérdida de respuesta tras escritura, inventario cambiante y denegación de permisos. La propuesta local no demuestra una integración ERP desplegada.
