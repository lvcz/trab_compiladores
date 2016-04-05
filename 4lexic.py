#!/usr/bin/python
# -*- coding: latin-1 -*-

import sys, getopt

# ==================================================================== #
### Variáveis Globais 

file_in  = 'test.c'
file_out = 'saida.tokens'

# ==================================================================== #
### Parse dos nomes de arquivos de entrada e saida na linha de comado

def get_cmdline_args(argv):

	global file_in, file_out

	try:
		opts, args = getopt.getopt(argv,"hi:o:q:",["ifile=","ofile=","quiet="])
	except getopt.GetoptError:
		print 'Usage: ' + sys.argv[0] + ' [-q] -i <inputfile> -o <outputfile>'
		sys.exit(2)

	for opt, arg in opts:
		if opt == '-h':
			print 'Usage: ' + sys.argv[0] + '[-q] -i <inputfile> -o <outputfile>'
			sys.exit()
		elif opt in ("-i", "--ifile"):
			file_in  = arg
		elif opt in ("-o", "--ofile"):
			file_out = arg
# ==================================================================== #
### Funcao get_token() : Retorna um token do arquivo a cada chamada

def get_token(f):
	data_type  = ['int', 'char', 'float', 'const', 'string']
	spec_chars = ['{', '}', '[', ']', '(', ')', ';', '"', '\'']
	op_arit    = ['+', '++', '-', '--', '*', '/', '#']
	op_logic   = ['>', '<', '>=', '<=', '==', '!', '!=']
	reserved   = ['for', 'while', 'do', 'if', 'else', 'main']
	separators = [';', ',']
	ign_list   = [' ', '\t', '\n']

	while True:
		ch = f.read(1)
		if ch not in ign_list:
			break

	if not ch:
		return "EOF"

	### Operadores aritmeticos ###
	if ch in op_arit:
		tk = ch
		if tk in ['/', '+', '-']:
			tk += f.read(1)
			# Trata se eh comentario de bloco - ERROR DE COMENTARIO TRATA AQUI
			if tk == '/*':
				while tk != '*/':
					ch = f.read(1)
					if not ch:
						return "EOF"
					tk = tk[1:] + ch
				return get_token(f)
			# Trata operadores com dois caracteres: ++ e --
			if tk in op_arit:
				return "<op_arit;%s>" % (tk)
			else:
				f.seek(f.tell() - 1)
		# Operadores de um soh caractere
		return "<op_arit;%s>" % (ch)
		
	### Operadores logicos e atribuicao
	if ch in op_logic or ch == '=':
		tk = ch + f.read(1)
		if tk in op_logic:
			return "<op_log;%s>" % (tk)
		else:
			f.seek(f.tell() - 1)
			if ch == '=':
				return "<attrib;%s>" % (ch)
			else:
				return "<op_log;%s>" % (ch)

	### Caracteres especiais ###
	if ch in spec_chars:
		tk = ch
		return "<%s;>" % (tk)

	### Numeros (inteiros e ponto flutuante) ### ERRO
	if ch.isdigit():
		tk = ch
		while ch.isdigit() or ch == '.':
			ch = f.read(1)
			tk += ch
		tk = tk[:-1]
		f.seek(f.tell() - 1)
		return "<num;%s>" % (tk)


	### Tipos de dados, Palavras reservadas, Identificadores ###
	if ch.isalpha():
		tk = ch
		while ch and ch not in separators and ch not in spec_chars and ch not in ign_list:
			ch = f.read(1)
			tk += ch
		tk = tk[:-1]
		f.seek(f.tell() - 1)
		if tk in data_type:
			return "<type;%s>" % (tk)
		elif tk in reserved: 
			return "<reserved;%s>" % (tk)
		else:
			return "<id;%s>" % (tk)


	### Nenhuma das opcoes acima
	return ch


# ==================================================================== #
### Rotina principal -> Main ========================================= #


if __name__ == "__main__":
	
	if (len(sys.argv) > 1):
		get_cmdline_args(sys.argv[1:])

	with open(file_in) as f:

		while True:

			token = get_token(f)

			if token == 'EOF':
				break

			print token

# ==================================================================== #
# ==================================================================== #
