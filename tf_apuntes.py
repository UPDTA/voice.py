#-*- coding: utf-8 -*-
# Apuntes para el deep learning de tensor flow
# Por favor, si quieres entender algo leete los comentarios

__autor__ = "Diego Morell"

import tensorflow as tf
import numpy as np

""" Creación de Constantes """
# El valor que retorna el constructor es el valor de la constante.
# Los valores de la constante son : constant(value, dtype=None, shape=None, name='Const')
# creamos constantes a=2 y b=3
a = tf.constant(2)
b = tf.constant(3)

# creamos matrices de 3x3
matriz1 = tf.constant([[1, 3, 2],
                       [1, 0, 0],
                       [1, 2, 2]])

matriz2 = tf.constant([[1, 0, 5],
                       [7, 5, 0],
                       [2, 1, 1]])

""" Realizamos algunos cálculos con estas constantes """
suma = tf.add(a, b)
mult = tf.mul(a, b)
cubo_a = a**3

# suma de matrices
suma_mat = tf.add(matriz1, matriz2)


# producto de matrices
mult_mat = tf.matmul(matriz1, matriz2)

""" Todo en TensorFlow ocurre dentro de una Sesión """
""" Creación de una sesión """

# creamos la sesion y realizamos algunas operaciones con las constantes
# La sesión se crea con el objeto Session()
# y lanzamos la sesión
with tf.Session() as sess: # Crea una sesión y la llama sess 
    print("Suma de las constantes: {}".format(sess.run(suma)))
    print("Multiplicación de las constantes: {}".format(sess.run(mult)))
    print("Constante elevada al cubo: {}".format(sess.run(cubo_a)))
    print("Suma de matrices: \n{}".format(sess.run(suma_mat)))
    print("Producto de matrices: \n{}".format(sess.run(mult_mat)))
# Un apunte importante es que en TensorFlow todo funciona mediante sesiones
# por lo que las abrimos con 'with' para que después de ejecutarse el código se cierren

""" Creación de variables """

# Creamos una variable y la inicializamos con 0
estado = tf.Variable(0, name="contador")

# Creamos la op que le va a sumar uno a la Variable `estado`.

uno = tf.constant(1)
nuevo_valor = tf.add(estado, uno)
actualizar = tf.assign(estado, nuevo_valor)

# Las Variables deben ser inicializadas por la operación `init` luego de 
# lanzar el grafo.  Debemos agregar la op `init` a nuestro grafo.
init = tf.initialize_all_variables()

# Lanzamos la sesion y ejecutamos las operaciones
with tf.Session() as sess:
    # Ejecutamos la op `init`
    sess.run(init)
    # imprimir el valor de la Variable estado.
    print(sess.run(estado))
    # ejecutamos la op que va a actualizar a `estado`.
    for _ in range(3):
        sess.run(actualizar)
        print(sess.run(estado))

""" Variable Simbólicas (contenedores) """

# Ejemplo variables simbólicas en los grafos
# El valor que devuelve el constructor representa la salida de la 
# variable (la entrada de la variable se define en la sesion)

# Creamos un contenedor del tipo float. Un tensor de 4x4.
x = tf.placeholder(tf.float32, shape=(4, 4))
y = tf.matmul(x, x)

with tf.Session() as sess:
#    print(sess.run(y))  # ERROR: va a fallar porque no alimentamos a x.
    rand_array = np.random.rand(4, 4) # Crea una matriz aleatoria de 4x4 utilizando numpy
    print(sess.run(y, feed_dict={x: rand_array}))  # ahora esta correcto.


""" Neurona AND """ 

#Neurona con TensorFlow
# Defino las entradas
entradas = tf.placeholder("float", name='Entradas')
datos = np.array([[0, 0]
                 ,[1, 0]
                 ,[0, 1]
                 ,[1, 1]])

# Defino las salidas
uno = lambda: tf.constant(1.0)
cero = lambda: tf.constant(0.0)

with tf.name_scope('Pesos'):
    # Definiendo pesos y sesgo
    pesos = tf.placeholder("float", name='Pesos')
    sesgo = tf.placeholder("float", name='Sesgo')

with tf.name_scope('Activacion'):
    # Función de activación
    activacion = tf.reduce_sum(tf.add(tf.matmul(entradas, pesos), sesgo))

with tf.name_scope('Neurona'):
    # Defino la neurona
    def neurona():
        return tf.case([(tf.less(activacion, 0.0), cero)], default=uno)
    
    # Salida
    a = neurona()

# path de logs
logs_path = '/tmp/tensorflow_logs/neurona'

# Lanzar la Sesion
with tf.Session() as sess:
    # para armar el grafo
    summary_writer = tf.train.SummaryWriter(logs_path, 
                                             graph=sess.graph)
    # para armar tabla de verdad
    x_1 = []
    x_2 = []
    out = []
    act = []
    for i in range(len(datos)):
        t = datos[i].reshape(1, 2)
        salida, activ = sess.run([a, activacion], feed_dict={entradas: t,
                                        pesos:np.array([[1.],[1.]]),
                                        sesgo: -1.5})
        # armar tabla de verdad en DataFrame
        x_1.append(t[0][0])
        x_2.append(t[0][1])
        out.append(salida)
        act.append(activ)
    tabla_info = np.array([x_1, x_2, act, out]).transpose()
    tabla = pd.DataFrame(tabla_info, 
                         columns=['x1', 'x2', 'f(x)', 'x1 AND x2'])
tabla