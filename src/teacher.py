USE_REAL_SERVER: bool = True

if not USE_REAL_SERVER:
    exit() # skip demo if not running on real server mode

import getopt, sys
import numpy as np
import random
from Pyfhel import Pyfhel, PyCtxt
from base64 import decodebytes
try:
    from flask import Flask, request
except ImportError:
    print("This demo requires the `flask` python module (install with pip). Exiting.")
    exit(0)
try:
    import requests
except ImportError:
    print("This demo requires the `requests` python module (install with pip). Exiting.")
    exit(0)

port = 5010
host = '127.0.0.1'

# Remove 1st argument from the
# list of command line arguments
argumentList = sys.argv[1:]

# Options
options = "h:p:"
 
# Long options
long_options = ["Host=", "Port="]
 
try:
    # Parsing argument
    arguments, values = getopt.getopt(argumentList, options, long_options)
     
    # checking each argument
    for currentArgument, currentValue in arguments:
 
        if currentArgument in ("-h", "--Host"):
            host = currentValue
            print(host)
             
        elif currentArgument in ("-p", "--Port"):
            port = currentValue
             
except getopt.error as err:
    # output error, and return with an error code
    print (str(err))

url = 'http://' + host + ':' + str(port)

list = [[0.,0.,1.], [0.,1.,0.],[1.,0.,0.]]
we = random.choice(list)

w = np.array(we, dtype=np.float64)

HE_teacher = Pyfhel()
ckks_params = {'scheme': 'CKKS', 'n': 2**14, 'scale': 2**30, 'qi_sizes': [60, 30, 30, 30, 60] }
HE_teacher.contextGen(**ckks_params)  # Generate context for bfv scheme
HE_teacher.keyGen()             # Key Generation: generates a pair of public/secret keys
HE_teacher.rotateKeyGen()

s_context    = HE_teacher.to_bytes_context()
s_public_key = HE_teacher.to_bytes_public_key()

print(f"[Teacher {url}] Request to be added to the curator")
r = requests.post('http://127.0.0.1:5000/add_teacher',
    json={
        'context': s_context.decode('cp437'),
        'pk': s_public_key.decode('cp437'),
        'url': url,
    })

# Quick setup of the server using flask
app = Flask(__name__)

@app.route('/predict', methods=['POST'])
def post():
    print(f'[Teacher {url}] Received Request')

    HE_student = Pyfhel()
    HE_student.from_bytes_context(request.json.get('context').encode('cp437'))
    HE_student.from_bytes_public_key(request.json.get('pk').encode('cp437'))
    cx = PyCtxt(pyfhel=HE_teacher, bytestring=request.json.get('cx').encode('cp437'))
    data = HE_teacher.decrypt(cx)[:3]

    print(f"[Teacher {url}] received HE_student={HE_student} and data={data}")
    print(f"[Teacher {url}] predictions result={w}")

    ctx = HE_student.encrypt(w)

    print(f"[Teacher {url}] Responding with ctx = {ctx}")
    return ctx.to_bytes().decode('cp437')

  
app.run(host='0.0.0.0', port=port) # Run, accessible via http://localhost:5010/

# sphinx_gallery_thumbnail_path = 'static/thumbnails/clientServer.png'