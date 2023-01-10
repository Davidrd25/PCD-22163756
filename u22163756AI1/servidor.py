#Importamos las librerias

import socket
import threading
import sys
import pickle
import os

class Servidor():

	def __init__(self, host=socket.gethostname(), port=int(input("Que puerto desea usar ? "))):

		self.clientes = []
		#Creación de un array para poder tener una lista con todos los usuarios que se vayan iniciando en el servidor
		self.nickname = []
		print('\nSu IP actual es : ',socket.gethostbyname(host))
		print('\n\tProceso con PID = ',os.getpid(), '\n\tHilo PRINCIPAL con ID =',threading.currentThread().getName(), '\n\tHilo en modo DAEMON = ', threading.currentThread().isDaemon(), '\n\tTotal Hilos activos en este punto del programa =', threading.active_count())
		self.s = socket.socket()
		self.s.bind((str(host), int(port)))
		self.s.listen(30)
		self.s.setblocking(False)

		threading.Thread(target=self.aceptarC, daemon=True).start()
		threading.Thread(target=self.procesarC, daemon=True).start()

		while True:
			msg = input('\n << SALIR = 1 >> \n')
			if msg == '1':
				print(" **** Me piro vampiro; cierro socket y mato SERVER con PID = ", os.getpid())
				self.s.close()
				sys.exit()
			else: pass

	def aceptarC(self):
		print('\nHilo ACEPTAR con ID =',threading.currentThread().getName(), '\n\tHilo en modo DAEMON = ', threading.currentThread().isDaemon(),'\n\tPertenece al PROCESO con PID', os.getpid(), "\n\tHilos activos TOTALES ", threading.active_count())
		
		while True:
			try:
				conn, addr = self.s.accept()
				print(f"\nConexion aceptada via {addr}\n")
				conn.setblocking(False)
				self.clientes.append(conn)
				data = conn.recv(32).decode()
				if data:
					#Con esta variable nickname conseguimos que se vayan guardando los usuarios
					nickname = data
					print("Usuario conectado: ", nickname)
					self.nickname.append(nickname)
			except: pass

	def procesarC(self):
		print('\nHilo PROCESAR con ID =',threading.currentThread().getName(), '\n\tHilo en modo DAEMON = ', threading.currentThread().isDaemon(),'\n\tPertenece al PROCESO con PID', os.getpid(), "\n\tHilos activos TOTALES ", threading.active_count())
		while True:
			if len(self.clientes) > 0:
				for c in self.clientes:
					try:
						data = c.recv(32)
						if data: self.broadcast(data,c)
						#Creamos el fichero nuevo con nuestro numero de expediente
						with open('u22163756AI1.txt', 'a') as f:
							#Con esta funcion conseguimos introducir el contenido que se encuentra en la variable data
							f.write(pickle.loads(data) + '\n')
					except: pass

	def broadcast(self, msg, cliente):
		for c in self.clientes:
			#Añadimos la variable self.nickname para poder mostrar el numero de ususarios que se encuentran en linea
			print("Clientes conectados Right now = ", len(self.clientes), ' ', self.nickname, '\t El mensaje es de: ', pickle.loads(msg))
			try:
				if c != cliente: 
					print(pickle.loads(msg))
					c.send(msg)
			except: self.clientes.remove(c)

arrancar = Servidor() 