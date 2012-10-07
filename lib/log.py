
import sys
from syslog import *
from srv import config
import inspect

openlog(sys.argv[0],LOG_PID|LOG_NDELAY|LOG_NOWAIT)

def log(priority, eventtype, subjectum, objectum, **attrs):
	attlist = []
	for (k, v) in attrs.items():
		attlist.append(" %s=%s"%(k,v))
	attstring = ",".join(attlist)
	message="event=%s, prio=%s, subject=%s, object=%s,%s"%(eventtype, priority, subjectum, objectum, attstring)
	if config.debug:
		sys.stderr.write(message+'\n')
	syslog(priority,message)

def debug(section,level,**attrs):
	if config.debug and ((config.debug.has_key(section) and config.debug[section] >= level) or (config.debug.has_key('*') and config.debug['*'] >= level)):
		log(LOG_DEBUG,"debug/%s/%s"%(section,level),inspect.stack()[1][3],inspect.stack()[3][4],**attrs)

