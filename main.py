import subprocess
import os
import time
import math
import sqlite3

conn = sqlite3.connect('system_stats.db')
c = conn.cursor()

def startup():
	config_result = subprocess.run(["perl", "ReadConfig.pl"], capture_output=True, text=True)

	config = config_result.stdout.split("\n")

	c.execute('''
	    CREATE TABLE IF NOT EXISTS stats (
	        id INTEGER PRIMARY KEY AUTOINCREMENT,
	        cpu_usage REAL,
	        memory_usage REAL
	    )
	''')

	return config


def get_data():
	data_result = subprocess.run(["bash", "getdata.sh"], capture_output=True, text=True)

	data = data_result.stdout.split("\n")

	return data


def log_data(data):
    c.execute('''
        INSERT INTO stats (cpu_usage, memory_usage) 
        VALUES (?, ?)
    ''', (data[0], data[1]))
    
    conn.commit()



def check_notifications(cpu, mem, config):
	print("\n\nAlerts:")
	
	if cpu > config[3]:
		print("CPU usage exceeds threshold (" + cpu + "%)")
  
	if mem > config[4]:
		print("Memory usage exceeds threshold (" + mem + "%)")

	if cpu < config[3] and mem < config[4]:
		print("No Alerts! System is good!")


def print_all_stats():
    c.execute('SELECT * FROM stats')
    rows = c.fetchall()

    for row in rows:
        print(row)


def print_graph(data, letter):
	graph = [['', '', '', '', '', '', '', '', '', ''],['', '', '', '', '', '', '', '', '', ''],['', '', '', '', '', '', '', '', '', ''],['', '', '', '', '', '', '', '', '', ''],['', '', '', '', '', '', '', '', '', '']]
	
	for i in range(10):
		v = math.floor(data[i]/10/2)

		graph[v][i] = letter

	for a in range(4, -1, -1):
		print(str((a+1)*20) + "%", end=' ')
		for b in range(10):

			d = graph[a][b]
			if d == '':
				print(" ", end=' ')
			else: 
				print(d, end=' ')

		print("\n", end='')



def graph():
	c.execute('SELECT cpu_usage, memory_usage FROM stats ORDER BY id DESC LIMIT 10')
	rows = c.fetchall()[::-1]

	cpu_usages = [row[0] for row in rows]
	memory_usages = [row[1] for row in rows]

	print("\nCPU:")
	print_graph(cpu_usages, 'c')
	print("\nMEMORY:")
	print_graph(memory_usages, 'm')

		




def display_data(cpu, mem, config):
	print("System Info (" + config[0] + ")\n")
	print("CPU: " + config[1])
	print("Max memory: " + config[2] + " GB\n\n")
	print("CPU Usage: " + cpu + "%")
	print("Memory Usage: " + mem + "%")

	graph()

	#print_all_stats()

	check_notifications(cpu, mem, config)

	
config = startup()

while True:
	os.system('clear')
	data = get_data()
	display_data(data[0], data[1], config)
	log_data(data)
	time.sleep(2)
