#-*- coding: utf-8 -*-

from random import randint
nsal_usuario = 0
nrec_usuario = 0
nsal_enemigo = 0
nrec_enemigo = 0
hpmb_usuario = (50)
hpmb_enemigo_facil = 20
hprec_enemigo = 1
salud_actual_usuario = 50
hprb_usuario= (50)
salud_actual_enemigo = 50
dificultad = 1
victorias = 0
lvl = 1
xp_ganada = 0
limite_xp = 50
xp_reiniciado = 0
randxp = 0
nivel = 1
xp_ganada = 1
nfuer_usuario = 0
#<seccion de salud>


def saludm_usuario():
	saludm = hpmb_usuario + (3*nsal_usuario)
	return saludm


def saludrec_usuario():
	saludrec = hprp_usuario + (2*nrec_usuario)
	return saludrec


def saludrec_usuario():
	saludrec_enemigo = hprp_enemigo + (2*nrec_enemigo)
	return saludrec_enemigo
#</seccion de salud>


def ataque_del_enemigo():
	global ataque_enemigo
	global salud_actual_usuario
	print("El enemigo ataca!")
	salud_actual_usuario -= ataque_enemigo
	print("Tu salud disminuye en ", ataque_enemigo)
    
def recuperacion_por_nivel():
	global salud_actual_usuario
	salud_actual_usuario = saludm_usuario()
    
def enemigo_facil():
	global ataque_enemigo
	global lvl_enemigo
	global saludm_enemigo
	global xp_ganada
	lvl_enemigo = randint(1,5)
	saludm_enemigo = hpmb_enemigo_facil + (3*lvl_enemigo)
	ataque_enemigo = 10 + lvl_enemigo
	xp_ganada = randint(15, 35)


def lvl_up():
	while 1:
		atributo_a_mejorar = input("¿Que atributo deseas mejorar?\n")
		if atributo_a_mejorar in['salud','Salud']:
			global nsal_usuario
			nsal_usuario = nsal_usuario + 1
			recuperacion_por_nivel()
			break
		elif atributo_a_mejorar in['recuperacion', 'Recuperacion', 'recuperación', 'recuperacion']:
			global nrec_usuario
			nrec_usuario = nrec_usuario + 1
			recuperacion_por_nivel()
			print(salud_actual_usuario)
			break
		elif atributo_a_mejorar in['fuerza', 'Fuerza']:
			global nfuer_usuario
			nfuer_usuario += 1
			break
		else:
			print("Ese no es un atributo disponible.")


def comprobacion_de_nivel():
	global xp_reiniciado
	global limite_xp
	global nivel
	while xp_reiniciado >= limite_xp:
		recuperacion_por_nivel()
		xp_reiniciado -= limite_xp
		limite_xp *= 1.5
		nivel += 1
		print("¡Has subido de nivel!\n¡Tu nuevo nivel es ", nivel, "!")
		lvl_up()
    	
    	
def combate():
	global nivel
	if 5 > nivel:
		enemigo_facil()
	global dificultad
	global salud_actual_enemigo
	global salud_actual_usuario
	salud_actual_enemigo = saludm_enemigo
	while 1:   	 
		if salud_actual_usuario > 0 and salud_actual_enemigo > 0:
			print("\nTu salud es ", salud_actual_usuario, "\nLa salud del enemigo es, ", salud_actual_enemigo)
			print("1. Atacar \n2. Recuperarte")
			accion = input("¿Qué quieres hacer? \n")
			if accion in['atacar', 'Atacar']:
				salud_actual_enemigo -= 10 + 3*nfuer_usuario
				print("La salud enemiga ha disminuido", 10+3 * nfuer_usuario)
				if salud_actual_enemigo > 0:
					ataque_del_enemigo()
				elif accion == "10100":
					salud_actual_enemigo = 0
			elif accion in['recuperarme','Recuperarme', 'recuperarte', 'Recuperarte']:
				if salud_actual_usuario == saludm_usuario():
					print("Tu salud ya está al máximo, haz otra cosa.")
				else:
					recuperacion = (10 + 2*nrec_usuario)
					if salud_actual_usuario < (saludm_usuario() - recuperacion):
						salud_actual_usuario += recuperacion
						print("Recuperas", recuperacion, "puntos de salud.")
						ataque_del_enemigo()
					else:
						salud_actual_usuario = saludm_usuario()
						ataque_del_enemigo()
			else:
				print("Elije una opcion.")
		elif salud_actual_enemigo < 0 or salud_actual_enemigo == 0:
			print("El enemigo ha muerto")
			global xp_reiniciado
			global randxp
			global xp_ganada
			if dificultad == 1:
				xp_reiniciado += xp_ganada
				print("¡Has obtenido ", xp_ganada, " puntos de experiencia!")
				xp_ganada = 0
				comprobacion_de_nivel()
				break


print(nivel)
while True:
	combate()
