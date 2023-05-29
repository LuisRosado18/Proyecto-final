# Proyecto-final
Los nodos en una red de sensores generalmente tienen recursos limitados de energía. El programa se puede adaptar para simular el consumo de energía de los sensores y evaluar el impacto de diferentes estrategias de ahorro de energía, como el enrutamiento optimizado, el apagado de nodos inactivos o el uso de técnicas de recolección de energía.

 ![NaiveRepentantDuckbillcat-size_restricted](https://github.com/LuisRosado18/Proyecto-final/assets/75033260/0b8d9e41-9620-4b06-b2fd-3723a6f68200)
 
El código implementa una simulación de un sistema distribuido con comunicación de nodos mediante mensajes. Los nodos realizan tareas periódicas de latido, replicación, detección de fallas y recuperación de nodos. Al final, se selecciona un líder en función de ciertos criterios.
Al tener un líder, el sistema puede ser más resiliente a fallos. Si un nodo falla o se desconecta, el líder puede tomar medidas para gestionar la situación, redistribuir tareas y coordinar la recuperación del sistema.

El método detect_failed_nodes se encarga de detectar nodos que pueden haber fallado. Con una probabilidad del 50%, marca un nodo como sospechoso de haber fallado si cumple ciertas condiciones. Esto permite detectar posibles fallas en los nodos y tomar medidas para su recuperación.

El método recover_failed_nodes se encarga de recuperar los nodos que han sido marcados como fallidos. Itera sobre los nodos fallidos y, con una probabilidad del 50%, los marca como recuperados. Además, envía un mensaje de recuperación al líder si corresponde. Esto permite restaurar los nodos fallidos y devolverlos al estado activo.

El método fail_node permite marcar un nodo como fallido, desactivándolo y agregándolo a la lista de nodos fallidos. Por otro lado, el método recover se encarga de recuperar un nodo que ha sido marcado como fallido, restaurando su estado activo y eliminando las marcas de fallido y sospechoso.

El método replicate se ejecuta en el nodo primario y se encarga de realizar la replicación de datos a otros nodos activos. Con una probabilidad del 20%, envía mensajes de replicación a los nodos activos para mantener los datos replicados y tolerar posibles fallas en los nodos.

El intercambio de mensajes entre los nodos, como los mensajes de latido, replicación, falla y recuperación, permite la comunicación y coordinación entre los nodos del sistema. Además, se utilizan mensajes de confirmación (por ejemplo, "HeartbeatAck" y "ReplicateAck") para asegurar que los nodos estén informados sobre el estado de los otros nodos y puedan tomar acciones adecuadas.
