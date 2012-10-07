
# the length of connection queue
listenbacklog = 10

# listen address
listenaddress = ("127.0.0.1",6667)

# list of memcachedb instances
mcdbs = ["127.0.0.1:21201"]

#max length of enums (based on memcachedb settings)
maxenumlen = 10

#are we in debug mode?
debug = False
nodebug = {
#"persistence":7,
#'phaseinit':7,
'registry':6,
'*':3,
}

testloops = 100
