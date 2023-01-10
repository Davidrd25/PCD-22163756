#importamos las librerias que vamos a utilizar
import threading
import sys
import socket
import pickle
import os

class Cliente():

	#Creación de la variable nickname para que el usuaurio introduzca su nombre 
	def __init__(self, nickname=input("Introduzca el nickname del cliente: "), host=input("Intoduzca la IP del servidor ?  "), port=int(input("Intoduzca el PUERTO del servidor ?  "))):
		self.s = socket.socket()
		self.s.connect((host, int(port)))
		self.nickname=nickname
		self.s.send(nickname.encode())
		print('\n\tProceso con PID = ',os.getpid(), '\n\tHilo PRINCIPAL con ID =',threading.currentThread().getName(), '\n\tHilo en modo DAEMON = ', threading.currentThread().isDaemon(),'\n\tTotal Hilos activos en este punto del programa =', threading.active_count())
		threading.Thread(target=self.recibir, daemon=True).start()

		while True:
			//Introducimos dentro del input la variable nickname para que muestre el nombre elegido por el usuario
			msg = input('\nNickname: ' + self.nickname + '\nEscriba texto ?   ** Enviar = ENTER   ** Salir Chat = 1 \n')
			if msg != '1' : self.enviar(msg)
			else:
				print(" **** Me piro vampiro; cierro socket y mato al CLIENTE con PID = ", os.getpid())
				self.s.close()
				sys.exit()

	def recibir(self):
		print('\nHilo RECIBIR con ID =',threading.currentThread().getName(), '\n\tPertenece al PROCESO con PID', os.getpid(), "\n\tHilos activos TOTALES ", threading.active_count())
		while True:
			try:
				data = self.s.recv(32)
				if data: print(pickle.loads(data))
			except: pass
	#Con esto editamos el el formato de los mensajes que vamos a mostrar por terminal, para que aparezca antes del texto el nombre del usuario que ha enviado X mensaje
	def enviar(self, msg):
		mensaje = f"{self.nickname}: {msg}"
		self.s.send(pickle.dumps(mensaje))

arrancar = Cliente()

		