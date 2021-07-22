#! /usr/bin/env python3
import json
import sys
import zlib
 
import base45
import cbor2
from cose.messages import CoseMessage
import qrtools
from pyzbar.pyzbar import decode

qr = qrtools.QR()
if qr.decode(sys.argv[1]):
    payload = qr.data[4:]
    #print(payload)
 
    # decode Base45 (remove HC1: prefix)
    decoded = base45.b45decode(payload)
 
    # decompress using zlib
    decompressed = zlib.decompress(decoded)
    
    # decode COSE message (no signature verification done)
    cose = CoseMessage.decode(decompressed)
    
    # decode the CBOR encoded payload and print as json
    print(json.dumps(cbor2.loads(cose.payload), indent=2))
