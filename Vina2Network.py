#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import argparse
import subprocess
import sqlite3
import threading
import socket
import sys
import os
from thread import *
import base64
from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer
from pyftpdlib.authorizers import UnixAuthorizer
from pyftpdlib.filesystems import UnixFilesystem
from pyftpdlib.servers import ThreadedFTPServer
from pyftpdlib.servers import MultiprocessFTPServer
from sendfile import sendfile
import ftplib
from ftplib import FTP
import json
import shutil
import string
import random
import os.path
import time
from threading import Timer, Thread, Event

title_screen = '''
==============================================================================
VINA2NETWORK- Networking tool for Autodock Vina
------------------------------------------------------
Authors: Woloski, R.D.; Kremer, F.S.; Eslabão, M.R.; Pinto, L.S.
------------------------------------------------------
Universidade Federal de Pelotas, Center for Technological Development (CDTEC),
Department of Biotechnology and Bioinformatics
==============================================================================
'''
help_screen = '''Script Commands:

-mode        : [Global] Choose between Client and Server
-port        : [Client] Choose the port you wish to connect
-ip          : [Client] Choose the IP address which the client will connect
-token       : [Client] Input the password generated by the server

Vina Commands:

-receptor       : [Server][File] Rigid part of the receptor
-flex           : [Server][File] Flexible side chains, if any
-ligand_dir     : [Server][Path] Ligand folder
-center_x       : [Server] X coordinate of the center
-center_y       : [Server] Y coordinate of the center
-center_z       : [Server] Z coordinate of the center
-size_x         : [Server] Size in the X dimension (Angstroms)
-size_y         : [Server] Size in the Y dimension (Angstroms)
-size_z         : [Server] Size in the Z dimension (Angstroms)
-log            : [Server] Optionally, write log file
-cpu            : [Server] Number of cores to use (default is all cores detected)
-seed           : [Server] Explicit random seed
-exhaustiveness : [Server] Exhaustiveness of the global search
-num_modes      : [Server] Maximum number of binding modes to generate
-energy_range   : [Server] Maximum energy difference between the best binding mode and the worst one'''

print title_screen

class perpetualTimer():

	def __init__(self,t,hFunction):
		self.t=t
		self.hFunction = hFunction
		self.thread = Timer(self.t,self.handle_function)

	def handle_function(self):
		self.hFunction()
		self.thread = Timer(self.t,self.handle_function)
		self.thread.start()

	def start(self):
		self.thread.start()

	def cancel(self):
		self.thread.cancel()



def handler_generation(size=9, chars=string.ascii_uppercase + string.digits):
	return ''.join(random.choice(chars) for i in range (size))

def main():
    authorizer = DummyAuthorizer()
    global authorizer
    authorizer.add_user('client', 'vina2cluster', '.', perm='elradfmwM')
    authorizer.add_anonymous(os.getcwd())
    handler = MyHandler
    handler.authorizer = authorizer
    handler.banner = "Vina2Cluster FTP Server."
    handler.timeout = 30
    address = ('', port)
    server = ThreadedFTPServer(address, handler)
    server.max_cons = 10000
    server.max_cons_per_ip = 10000
    server.serve_forever()

class MyHandler(FTPHandler):


    def on_connect(self):
		pass

    def on_disconnect(self):
    	if self.username == "client":
    		pass
    	else:
    		if os.path.isfile(self.username):
    			os.remove(self.username)
    			pass
    		else:
    			for fname in os.listdir("LigandProcessing"):
    				if fname.startswith(self.username):
    					shutil.move("LigandProcessing/" + fname, "Vina2ClusterLigand")
    					os.rename("Vina2ClusterLigand/" + fname, "Vina2ClusterLigand/" + fname[9::])

        print self.remote_ip, self.remote_port,self.username, "disconnected"
        pass

    def on_login(self, username):
        if username == "client":
        	user_login = handler_generation()
        	user_password = handler_generation()
        	global authorizer
        	authorizer.add_user(user_login, user_password, '.', perm='elradfmwM')
        	credentials = open("Credentials.txt",'w')
        	credentials.write(user_login)
        	credentials.write("\n")
        	credentials.write(user_password)
        	credentials.close()
        else:
        	pass

    def on_logout(self, username):
        pass

    def on_file_sent(self, file):
        pass

    def on_file_received(self, file):
        pass

    def on_incomplete_file_sent(self, file):
        pass

    def on_incomplete_file_received(self, file):
        import os
        os.remove(file)


#ARGUMENT LIST: GENERAL

parser = argparse.ArgumentParser(description='ArgumentosVina')
parser.add_argument('-m', '--mode', choices=['client', 'server'],type=str, required=True)

#ARGUMENT LIST: SERVER

parser.add_argument('-receptor','--receptor', type=str)
parser.add_argument('-ligand_dir','--ligand_dir', type=str)
parser.add_argument('-flex','--flex', type=str)
parser.add_argument('-center_x','--center_x', type=float)
parser.add_argument('-center_y','--center_y', type=float)
parser.add_argument('-center_z','--center_z', type=float)
parser.add_argument('-size_x','--size_x', type=str)
parser.add_argument('-size_y','--size_y', type=str)
parser.add_argument('-size_z','--size_z', type=str)
parser.add_argument('-log','--log', type=str)
parser.add_argument('-seed','--seed', type=int)
parser.add_argument('-exhaustiveness','--exhaustiveness', type=int)
parser.add_argument('-num_modes','--num_modes', type=int)
parser.add_argument('-energy_range','--energy_range', type=int)
parser.add_argument('-config','--config', type=str)
parser.add_argument('-commands','--commands', action='store_true')


#ARGUMENT LIST: CLIENT

parser.add_argument('-ip','--host_ip',type=str)
parser.add_argument('-port','--host_port', type=int)
parser.add_argument('-cpu','--cpu', type=int)
parser.add_argument('-token','--token', type=str)

arguments = parser.parse_args()

#Server argument check

if arguments.commands:
	print help_screen
	sys.exit()

if arguments.mode == 'server':
	if arguments.ligand_dir:
		if os.path.isdir(arguments.ligand_dir):
			pass
		else:
			sys.stderr.write('ERROR: "%s" does not exist\n'%(arguments.ligand_dir))
			sys.exit(1)
	else:
		sys.stderr.write('ERROR: Ligand directory must be specified\n')
		sys.exit(1)

	if arguments.receptor:
		if os.path.isfile(arguments.receptor):
			pass
		else:
			sys.stderr.write('ERROR: "%s" does not exist\n'%(arguments.receptor))
			sys.exit(1)
	else:
		sys.stderr.write('ERROR: Receptor must be specified\n')
		sys.exit(1)

	if arguments.center_x is not None:
		pass
	else:
		sys.stderr.write('ERROR: Center X must be specified\n')
		sys.exit(1)

	if arguments.center_y is not None:
		pass
	else:
		sys.stderr.write('ERROR: Center Y must be specified\n')
		sys.exit(1)

	if arguments.center_z is not None:
		pass
	else:
		sys.stderr.write('ERROR: Center Z must be specified\n')
		sys.exit(1)

	if arguments.size_x is not None:
		pass
	else:
		sys.stderr.write('ERROR: Size X must be specified\n')
		sys.exit(1)

	if arguments.size_y is not None:
		pass
	else:
		sys.stderr.write('ERROR: Size Y must be specified\n')
		sys.exit(1)

	if arguments.size_z is not None:
		pass
	else:
		sys.stderr.write('ERROR: Size Z must be specified\n')
		sys.exit(1)

#Client argument check

if arguments.mode == 'client':

	if arguments.host_ip is not None:
		pass
	else:
		sys.stderr.write('ERROR: Host IP must be specified\n')
		sys.exit(1)

	if arguments.host_port is not None:
		pass
	else:
		sys.stderr.write('ERROR: Host Port must be specified\n')
		sys.exit(1)


if arguments.mode == 'server':
	ligand_list = [os.path.join(arguments.ligand_dir,path) for path in os.listdir(arguments.ligand_dir)]
	ligand_list = [file for file in ligand_list if os.path.isfile(file)]
	connection = sqlite3.connect(':memory:',check_same_thread=False)
	cursor = connection.cursor()
	cursor.execute('''CREATE TABLE ligands (id integer PRIMARY KEY AUTOINCREMENT, file_path text,status text)''')
	connection.commit()
	if "Vina2ClusterLigand" in os.listdir('.'):
		shutil.rmtree("Vina2ClusterLigand")
	os.mkdir("Vina2ClusterLigand")
	for ligand in ligand_list:
		file_name, file_extension = os.path.splitext(ligand)
		if file_extension.lower() ==".pdbqt":
			shutil.copy(ligand, "Vina2ClusterLigand")
		else:
			print 'Error: "%s" is not a valid file extension'%(file_extension)
	dicionario = {'--receptor':arguments.receptor, '--flex':arguments.flex, '--center_x':arguments.center_x, '--center_y':arguments.center_y, '--center_z':arguments.center_z, '--size_x':arguments.size_x, '--size_y':arguments.size_y, '--size_z':arguments.size_z, '--log':arguments.log, '--seed': arguments.seed, '--exhaustiveness': arguments.exhaustiveness, '--num_modes':arguments.num_modes, '--energy_range':arguments.energy_range, '--config':arguments.config}
	print dicionario
	json.dump(dicionario, open("dicionario.json", "w"))
	comandos = ''
	for key in dicionario.keys():
			if dicionario[key] != None:
				comandos += key.replace('-', '') + ' = ' + str(dicionario[key]) + '\n'
	config_file = open("Output.txt",'w')
	config_file.write(comandos)
	config_file.close()
	results_file = open("DockingResults.txt",'w')
	if "LigandProcessing" in os.listdir('.'):
		shutil.rmtree("LigandProcessing")
	os.mkdir("LigandProcessing")
	if "LigandResults" in os.listdir('.'):
		shutil.rmtree("LigandResults")
	os.mkdir("LigandResults")
	port = raw_input("Insert the port you wish to use: ")


	if __name__ == '__main__':
	    main()


if arguments.mode == 'client':


	def doWork():
		ftp.retrbinary('RETR dicionario.json', open('dicionario.json', 'wb').write)


	t = perpetualTimer(10, doWork)
	t.start()

	b = 1
	while True:
		ftp = ftplib.FTP()
		ftp.connect(arguments.host_ip, arguments.host_port)
		ftp.login("client", "vina2cluster")
		ftp.retrbinary('RETR Credentials.txt', open('Credentials.txt', 'wb').write)
		print ftp.getwelcome()
		ftp.quit()
		with open('Credentials.txt') as credential_file:
			lines = credential_file.readlines()
			credential_login = lines[0].split("\n")[0]
			credential_password = lines[1].split("\n")[0]
			print credential_login
			print credential_password
		ftp.connect(arguments.host_ip, arguments.host_port)
		ftp.login(credential_login, credential_password)
		ftp.retrlines('LIST')
		ftp.retrbinary('RETR Output.txt', open('Output.txt', 'wb').write)
		ftp.retrbinary('RETR dicionario.json', open('dicionario.json', 'wb').write)
		with open('dicionario.json') as json_file:
			json_data = json.load(json_file)
		receptor_file = json_data['--receptor']
		print 'Retrieving receptor file ' + receptor_file
		ftp.retrbinary('RETR ' + receptor_file, open(receptor_file, 'wb').write)
		ftp.cwd('Vina2ClusterLigand')
		ftp.retrlines('LIST')
		filename = ftp.nlst()[0]
		print 'Getting ' + filename
		ftp.retrbinary('RETR ' + filename, open(filename, 'wb').write)
		with open("Output.txt", "a") as input_file:
			input_file.write('ligand = %s' %filename)
			input_file.close()
		ftp.delete(filename)
		ftp.cwd('../LigandProcessing')
		ftp.storbinary('STOR ' + filename, open(filename, 'rb'))
		ftp.rename(filename, credential_login + filename)
		ftp.cwd('../')
		ftp.retrbinary('RETR dicionario.json', open('dicionario.json', 'wb').write)


		print "Processing"
		vina_return_code = subprocess.call("vina --config Output.txt",shell=True)
		if vina_return_code == 0:
			print """Done!"""
			ftp.cwd('../LigandResults')
			ftp.storbinary('STOR ' + os.path.splitext(filename)[0] + '_out.pdbqt', open (os.path.splitext(filename)[0] + '_out.pdbqt'))
			ftp.cwd('../LigandProcessing')
			ftp.delete(credential_login + filename)
			resultparse = open (os.path.splitext(filename)[0] + '_out.pdbqt')
			resultline = resultparse.readlines()
			result = resultline[1]
			ftp.cwd('../')
			ftp.retrbinary('RETR DockingResults.txt', open('DockingResults.txt', 'wb').write)
			with open ('DockingResults.txt', 'a') as my_file:
				my_file.write(os.path.splitext(filename)[0] + '		' + result + '\n')
			ftp.storbinary('STOR DockingResults.txt', open('DockingResults.txt', 'rb'))
			with open(credential_login, 'w') as confirmation:
				ftp.storbinary('STOR ' + credential_login, open(credential_login, 'rb'))
			print confirmation
			os.remove(credential_login)
			os.remove(filename)
			os.remove(os.path.splitext(filename)[0] + '_out.pdbqt')
			os.remove('Credentials.txt')
			os.remove('dicionario.json')
			os.remove('Output.txt')
			ftp.quit()
		else:
			print """Something is technically wrong..."""
			ftp.connect(arguments.host_ip, arguments.host_port)
			ftp.login("client", "vina2cluster")
			ftp.cwd('Vina2ClusterLigand')
			ftp.storbinary('STOR ' + filename, open(filename, 'rb'))
			ftp.cwd('../LigandProcessing')
			ftp.delete(filename)
			ftp.quit()
