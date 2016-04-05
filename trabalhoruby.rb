#!/usr/bin/ruby
#TODO:
require 'set'

data_type  = ['int', 'char', 'float', 'const', 'string']
spec_chars = ['{', '}', '[', ']', '(', ')', ';', '"', '\'']
op_arit    = ['+', '++', '-', '--', '*', '/', '#']
op_logic   = ['>', '<', '>=', '<=', '==', '!', '!=']
reserved   = ['for', 'while', 'do', 'if', 'else', 'main']
separators = [';', ',']
inv_char  = ['@', '$', '`', ',']

def processa(arquivo,tipo)
arquivo.each do|x|
	tipo.each do |y|
		if(x.include? y)
		
			if x.split(/#{y}/).first().to_s.length >0
			arquivo.insert( arquivo.index(x)-1 , x.split(/#{y}/).first())
			end
			if x.split(/#{y}/).last().to_s.length >0
			arquivo.insert( arquivo.index(x)+1 , x.split(/#{y}/).last())
			end
			arquivo[arquivo.index(x)]=x[y]
			
			
		end
	end
	
end


end

input = $stdin.read

arqFormat=input.gsub("\n","").gsub(" ","").split(/(;)/)





arqFormat.each do|x|

	if(x.include? '/*' or x.include? '*/')
		if(x.include? '/*' and x.include? '*/')
			if(x.split("/*").first().to_s.length >0)
			
				arqFormat.insert( arqFormat.index(x)-1 , x.split("/*").first())
			end
			if x.split("*/").last().to_s.length >0
			
				arqFormat.insert( arqFormat.index(x)+1 , x.split("*/").last())
			end	
			arqFormat.delete_at(arqFormat.index(x))
		end		
	end
	end




processa(arqFormat,data_type)
processa(arqFormat,reserved)
processa(arqFormat,op_logic)





print arqFormat
puts



