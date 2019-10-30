Acabo de terminar de revisar una cosita vieja que me acorde que tenia el lunes mientras estabamos en la clase.

Adjunto un programa en python que sirve para graficar en 3D elementos opticos y ver que pasa con la polarizacion.

Para ejecutarse necesita python instalado (en principio el 2,7) pero importante que el matplotlib no este actualizado porque cambiaron algo y con la version nueva no anda. Con la 1.4 si. En la compu del cuartito del fondo (creo que el 7) el lunes cree un enviroment donde funciona. Sino se puede crear con  conda en unos pocos minutos. https://conda.io/docs/user-guide/tasks/manage-environments.html en ese caso les conviene crear un enviroment limpio e instalar el numpy el scipy y el matplolib=1.4

Lo que les mando es el codigo y un monton de ejemplos que habia armado mas unos nuevos que arme recien (del 100 al 105).

Para ejecutarlo ponen "python nombrearchivo numeroejemplo". Dentro del archivo van a encontrar los ejemplos con leves explicaciones de que son. Tambien hay una nomenclatura relativamente sencilla para crear objetos (ondas, polarizadores, laminas) donde pueden modificar los objetos (fases orientaciones, tamaños, etc) como prefieran.

Si van a armar ejemplos mas raros me acuerdo que en algunos casos (laminas donde los ejes rapidos y lentos forman angulos no de 90 con los "ejes del programa") habia algun error en las cuentas que nunca lo logre corregir. Pero salvo eso se podria usar para poner mas ejemplos que los armados.

Obviamente esta a medio hacer el codigo y es probable que muchas cosas convenga rediseñarlas desde cero (fue mi primer prueba de programar objetos en python), cualquier cosa aca hay un repo donde todavia no subi los ultimos cambios

https://github.com/IonatanPerez/OndasPolarizacion

Lo comparto por si les sirve

Ioni