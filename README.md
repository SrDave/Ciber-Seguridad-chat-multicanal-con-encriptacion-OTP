# Aplicación de chat multiusuario
El  desarrollo de una aplicación de chat multiusuario con comunicaciones cifradas va a consistir en desarrollar la aplicación de chat y hacer la incorporación del cifrado.  Sin embargo, es posible que haya notado que los sockets descritos hasta el momento tienen una limitación muy notable. Básicamente, un servidor solo es capaz de atender a un cliente simultáneamente. Además, las comunicaciones con dicho servidor deben producirse de manera muy pautada entre ambos y típicamente según la secuencia enviar-recibir-enviar… en el cliente y recibir-enviar-recibir… en el servidor. Esto ocurre de este modo puesto que existe una serie de funciones a las que se conoce como bloqueantes y que paralizan la ejecución del programa hasta que ocurre el suceso esperado. Un tipo de función bloqueante bien conocido es la lectura de teclado, dado que el programa se paraliza hasta que el usuario escribe por el teclado. Así pues, un programa que está esperando a que el usuario escriba algo por teclado no puede, con los conocimientos que dispone hasta ahora, recibir información por un determinado socket. O también las funciones recv (o read) y accept, dado que recv paraliza la ejecución del programa hasta que el otro extremo del socket envía información o cierra el socket y accept la paraliza hasta que se conecta un cliente. Además de estas limitaciones, resulta impensable por ejemplo diseñar un servidor que se quede paralizado si un determinado cliente no envía ninguna información cuando el servidor está esperándola con un recv.

Por todos los motivos expuestos, dentro de la programación con sockets se ha definido la función `select`, que permite monitorizar eventos en diferentes descriptores simultáneamente. Además, otra utilidad de la función `select` es evitar el bloqueo indefinido de ciertas funciones que utilizamos, como read y accept, saliendo de dicho bloqueo en el caso de no recibir peticiones en un plazo determinado mediante el uso de un temporizador. La llamada select puede estar esperando la aparición de los tres tipos siguientes de sucesos:
- Lectura de un descriptor dado.
- Escritura de un descriptor dado.
- Existencia de una condición excepcional sobre un descriptor de un recurso para el que existe este concepto (por ejemplo, existencia de un "mensaje urgente").

La definición de select en Python es:

`ready_to_read, ready_to_write, in_error = select.select(potential_readers, potential_writers, potential_errs, timeout)`

Para comprobar cada uno de los tres tipos de sucesos, se define para cada tipo una lista, de manera que select devuelve los descriptores que deben atenderse porque ha sucedido algún evento en ellos. Es decir, a select se le introducen tres listas de descriptores que debe monitorizar, devolviendo otras tres listas que serán subconjuntos (posiblemente vacíos) de dichas listas.

Por otro lado, tal y como se ha explicado, la función select permite introducir un temporizador como argumento opcional (timeout). Dicho temporizador, especificado en segundos, define el tiempo que permitimos a la función select estar bloqueada. Es decir, si transcurrido el tiempo no ha ocurrido ningún cambio en ningún descriptor que monitoriza select, la función finaliza.

Aunque ya se ha nombrado, conviene destacar la posibilidad de añadir el teclado como descriptor para ser controlado por la función select, lo cual resulta muy útil, en el caso que nos ocupa, para la programación del cliente de la aplicación de chat. Así pues, se puede emplear la función select para que cada cliente sea capaz de atender simultáneamente el socket que tiene establecido con el servidor y el teclado, dado que un cliente puede recibir mensajes del otro extremo y debe estar preparado para leer el teclado en cualquier momento para el envío de mensajes. La manera de realizarlo es introduciendo el descriptor de teclado en la lista de entradas de manera similar a como si de un socket se tratase (con la diferencia de que hay que leer de teclado cada vez que select indique que hay que realizar una acción sobre dicho descriptor, cuando con un socket lo que hay que hacer es recibir información del socket o aceptar una nueva conexión si se trata de un socket de escucha). Sin embargo, es muy importante notar que esta posibilidad de introducir el teclado como un descriptor de socket no es posible realizarla si emplea el sistema operativo Windows (sí que es posible en Linux y en Mac).

El empleo de hilos en Python puede hacerse de manera muy sencilla empleando el módulo threading. Para lanzar un nuevo hilo debe invocar el método Thread, el cual recibe como parámetros la función a ejecutar en ese hilo junto con los parámetros de entrada en forma de tupla. Un ejemplo de esta llamada es:

`nuevo_hilo=threading.Thread(target=funcion, args=(param, ))`

Una vez descritos los métodos que permiten que su servidor y cliente pueden atender varios sockets y el teclado simultáneamente, se describe en mayor detalle la aplicación chat a realizar. Dicha aplicación, que debe programarse en Python 3 y emplear el protocolo TCP, funcionará con la arquitectura cliente-servidor. Si, por ejemplo, existen dos usuarios (de nombre Alice y Bob) ambos estarán conectados al servidor y cada vez que Alice (Bob) envíe un mensaje por teclado, se lo enviará al servidor y este lo reenviará a Bob (Alice). En la figura siguiente se muestra un ejemplo de funcionamiento de la aplicación. Aunque se muestren dos usuarios (Alice y Bob), hay que destacar que los programas desarrollados deben poder admitir a un número indeterminado de usuarios.

# CIFRADO OTP
El cifrador One-Time Pad (OTP) es un cifrador incondicionalmente seguro y que tiene una implementación muy sencilla. De hecho, se basa en el uso de XOR y, para ello, puede hacer uso de la siguiente función escrita en Python:

def xor_bytes(key_stream, message):

  length = min(len(key_stream), len(message))
  
  return bytes([key_stream[i] ^ message[i] for i in range(length)])
