import yaml
import sys
import codecs
import _properties
import _util
import _from
import _to
	
input_file = sys.argv[1]
output_file = sys.argv[2]
stream = open(input_file, 'r',encoding='utf-8')
packet_list = yaml.load(stream)
stream.close()
f = codecs.open(output_file, 'w', encoding='utf-8')
f.write('// Automatic generate by PacketGenerator.\n')
f.write('using System;\n')
f.write('using System.Collections.Generic;\n')
f.write('\nnamespace SomeNameSpace')

f.write('\n{')

#pop common header
common_header = packet_list.get('Header',{})
if common_header is not None:
	del packet_list['Header']

#sort packet names
sorted_packet_names = sorted(packet_list)

#make messageType enum
f.write ( _util.make_message_types(sorted_packet_names) )

#make message instance maker
f.write ( _util.make_message_instance_maker(sorted_packet_names) )

for packet_name in sorted_packet_names:
	packet = packet_list[packet_name]
	# Comment
	if packet.get('comment') is not None:
		f.write('\n// %s'%(packet['comment']))
	# class declare
	f.write('\t\npublic class %sGameMessage : ISomeInterface'%(packet_name))
	f.write('\t\n{')
	#header added
	fields = common_header.get('fields',[])+packet.get('fields',[])

	# class member
	f.write( _properties.make_fields(packet_name, fields) )

	#make each message class
	to_byte_array = _to.make_to_byte_array(fields)
	if to_byte_array is not None :
		f.write( to_byte_array )
	
	# FromByteArray method implementation
	_from.make_from_byte_array(f, fields)

	# Length property getter implementation
	_properties.make_message_length(f, fields)
	
	#end of class
	f.write('\n}\n')

#end of namespace
f.write('\n}')
f.close()
print ('Generate Success.')
