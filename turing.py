import json
import argparse

class Command():
	"""Class for storing command info
	"""	
	def __init__(self, data):
		self.current_state = data["current_state"]
		self.current_symbol = data["current_symbol"]
		self.new_symbol	= data["new_symbol"]
		self.direction = data["direction"].upper()
		self.new_state = data["new_state"]

	def print_command_row(self):
		"""Print out command entry
		"""		
		print(	self.current_state, 
				self.current_symbol, 
				self.new_symbol, 
				self.direction, 
				self.new_state)

class Head():
	"""Class for storing head data 
	"""	
	def __init__(self, starting_position, step_limit):
		self.commands = []
		self.state = '0'
		self.counter = 0 		
		self.position = int(starting_position) - 1 # Offsetting for array indexing
		self.cell = ''
		self.halt = False
		self.step_limit = step_limit

	def store_command(self, command):
		"""Storing Command class objects 

		Args:
			command (Command): Command entry
		"""		
		self.commands.append(command)

	def read_cell(self, tape):
		"""Read current tape cell

		Args:
			tape (Tape): Machine tape
		"""		
		self.cell = tape.get_cell(self.position)

	def write_cell(self, tape, symbol):
		"""Wrtie new value into the cell

		Args:
			tape (Tape): Machine tape
			symbol (str): New symbol
		"""		
		tape.write_cell(self.position, symbol)

	def change_position(self, tape, direction):
		"""Move head to a new position

		Args:
			tape (Tape): Machine tape
			direction (str): Position to move
		"""

		# Validate the move, if invalid - halt
		if direction == "L":
			if self.position == 0:
				# Tape overflow
				self.halt = True
			else:
				self.position -= 1

		elif direction == "R":
			if self.position == len(tape.data) - 1:
				# Tape overflow
				self.halt = True
			else:
				self.position += 1

	def change_state(self, state):
		"""Change state or halt

		Args:
			state (str): New state 
		"""		
		if state == 'X': 
			self.halt = True

		self.state = state

	def find_command(self):
		"""Look up command based on state and cell value.
		Halt if command is not found

		Returns:
			Command: Command to execute on current step
		"""		
		for command in self.commands:
			if command.current_state == self.state and command.current_symbol == self.cell: 
				return command

		# Halting if command is not found
		return Command('x', 'x', 'x', 'R', 'X') 

	def update_counter(self):
		"""Update step counter and halt if step limit is exceeded
		"""
		self.counter += 1
		if self.counter >= self.step_limit:
			self.halt = True

	def print_pointer(self):
		"""Print out pointed that shows head's position
		"""		
		print(' ' * self.position + '^')

	def cycle(self, tape):
		"""Perform a single turing machine cycle

		Steps: 
			1. Read cell value and find command to execute
			2. Update cell value
			3. Move the head 
			4. Change the current state
			5. Update step counter  

		Args:
			tape (Tape): Machine tape
		"""		
		self.read_cell(tape)
		command = self.find_command()
		self.write_cell(tape, command.new_symbol)
		self.change_position(tape, command.direction)
		self.change_state(command.new_state)
		self.update_counter()


class Tape():
	"""Class for storing tape data and interacting with it
	"""	
	def __init__(self, data):
		self.data = data

	def __repr__(self):
		return self.data

	def print_tape(self):
		print(self.data)

	def get_cell(self, position):
		"""Return cell value

		Args:
			position (int): head position

		Returns:
			str: cell value
		"""		
		return self.data[position]

	def write_cell(self, position, value):
		"""Update cell value

		Args:
			position (int): head position
			value (str): new value to write
		"""		
		self.data = self.data[:position] + value + self.data[position + 1:]


def init_turing_machine(filename):
	"""Initialize Turing machine:
	1. Read command file contents
	2. Contruct head and tape 
	3. Read commands and store in head

	Args:
		filename (str): path to command file

	Returns:
		dict: tape and head 
	"""	
	with open(filename, 'r') as input_file:
		json_data = json.load(input_file)

	head = Head(json_data['starting_position'], json_data['step_limit'])
	tape = Tape(json_data['tape'])

	for command_data in json_data['commands']:
		command = Command(command_data)
		head.store_command(command)

	data = {
		'tape': tape,
		'head': head,
	}

	return data

def run():
	"""Main function that handles init and running commands
	"""	
	# Parsing command file path 
	parser = argparse.ArgumentParser(description='Simple Python Turing machine ')
	parser.add_argument('-f', '--file', help='Command file path')
	args = parser.parse_args()

	# Initializing data
	data = init_turing_machine(args.file)
	tape = data['tape']
	head = data['head']

	# Main cycle
	while head.halt == False:
		tape.print_tape()
		head.print_pointer()
		head.cycle(tape)

	print(head.counter)


if __name__ == '__main__':
	run()