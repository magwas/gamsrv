import struct

"""
	the requests (terminal -> server) look like this:
	name length format meaning
  head 4      !I     always 0xdeadbeef
	id   4      !I     terminal ID
	seq  4      !I     sequence value
	phs  2      !H     game phase
	ne   2      !H     number of values
	val  ne*6   ne*!Hi key,value
	tlen 2      !H     length of token
	tok  tlen   s      token

	the response (server -> terminal) looks like this:
  head 4      !I     always 0xdeadbeef
	seq  4      !I     sequence value
	ne   2      !H     number of values
	val  ne*6   ne*!Hi key,value

"""

class ProtocolError(Exception):
	pass

class Proto:
	def encode(self,sock,seq,vals):
		s=struct.pack("!IIH",0xdeadbeef,seq,len(vals))
		for k,v in vals.items():
			s += struct.pack("!Hi",k,v)
		sock.sendall(s)
		return s

	def decode(self,sock,validator):
		print "header"
		header=sock.recv(16)
		print header
		if len(header) < 16:
			raise ProtocolError("short packet")
		head,pktid,seq,phs,ne = struct.unpack("!IIIHH",header)
		validator.validateHeader(pktid,seq,phs,ne)
		if ( head != 0xdeadbeef ):
			raise ProtocolError("no dead beef")
		print "element"
		valbuf=sock.recv(ne*6+2)
		if len(valbuf) < (ne*6+2):
			raise ProtocolError("short val+tlen")
		vals={}
		for i in range(ne):
			key,value = struct.unpack("!Hi",valbuf[i*6:(i+1)*6])
			validator.validateKeyValue(phs,key,value)
			vals[key] = value
		tokenlen = struct.unpack("!H",valbuf[-2:])[0]
		validator.validateTokenLen(tokenlen)
		print "token", tokenlen
		token = None
		if tokenlen:
			token = sock.recv(tokenlen)
		print "all read"
		validator.validateToken(token)
		return (seq,phs,vals,token)
