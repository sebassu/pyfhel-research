USE_REAL_SERVER: bool = True

if not USE_REAL_SERVER:
    exit() # skip demo if not running on real server mode

import numpy as np
from math import log
from Pyfhel import Pyfhel, PyCtxt
try:
    from flask import Flask, request, jsonify
except ImportError:
    print("This demo requires the `flask` python module (install with pip). Exiting.")
    exit(0)
try:
    import requests
except ImportError:
    print("This demo requires the `requests` python module (install with pip). Exiting.")
    exit(0)

HE_curator = Pyfhel()
ckks_params = {'scheme': 'CKKS', 'n': 2**14, 'scale': 2**30, 'qi_sizes': [60, 30, 30, 30, 60] }
HE_curator.contextGen(**ckks_params)  # Generate context for bfv scheme
HE_curator.keyGen()             # Key Generation: generates a pair of public/secret keys
HE_curator.rotateKeyGen()

s_context    = HE_curator.to_bytes_context()
s_public_key = HE_curator.to_bytes_public_key()
private_budget = 1000000
p_budget = [20.756462732485115]
list_teachers = []
students = {}

def privacy_loss_calculation(t, gamma, delta):
  result = []
  for l in range(1,1000):
    value = 1/l*(2*t*gamma*gamma*l*(l+1)-log(delta)) 
    result.append(value)
  return min(result)

def get_private_budget():
    return p_budget[0]

def update_private_budget(pb):
    p_budget[0] = p_budget[0] - pb

def exist_student(id):
    print(students.keys)
    if id in students:
        return True
    else:
        return False

def add_student(id, pk):
    students[id] = (pk, private_budget)

def get_pb():
    _,s_pb = students.get(id)
    return s_pb

def modify_pb(id):
    s_pk,s_pb = students.get(id)
    if s_pb > 0:
        new_pb = s_pb-1000
    students[id] = (s_pk, new_pb)
    return new_pb


def predictions(s_context_student, s_public_key_student, cx_response):
    
    cx_student = HE_curator.decrypt(cx_response)
    HE_response = Pyfhel()
    HE_response.from_bytes_context(s_context_student)
    HE_response.from_bytes_public_key(s_public_key_student)

    print(f"[Curator] received HE_response={HE_response} and cx={cx_response}")

    count = HE_response.encrypt(np.array([0., 0., 0.], dtype=np.float64))

    for teacher in list_teachers:
        url = teacher[0]
        HE_teacher = teacher[1]
        cx = HE_teacher.encrypt(cx_student)
        s_cx = cx.to_bytes()
        print(f"[Curator] request the prediction from the teacher {url}")
        r = requests.post(url+'/predict',
            json={
                'context': s_context_student.decode('cp437'),
                'pk': s_public_key_student.decode('cp437'),
                'cx': s_cx.decode('cp437'),
            })
        c_res = PyCtxt(pyfhel=HE_response, bytestring=r.text.encode('cp437'))
        print(f"[Curator] recive cx = {c_res}")
        count = count + c_res

    return count
    

# Quick setup of the server using flask
app = Flask(__name__)

@app.route('/fhe_mse', methods=['POST'])
def post():
    print("[Curator] Received Request for fhe_mse!")

    # Read all bytestrings
    s_context_student = request.json.get('context').encode('cp437')
    s_public_key_student = request.json.get('pk').encode('cp437')
    cx_response = PyCtxt(pyfhel=HE_curator, bytestring=request.json.get('cx').encode('cp437'))
    id = request.json.get('id')
    
    if exist_student(id):
        print(f"[Curator] The student already exists. ")
    else:
        add_student(id, s_public_key_student)
        print(f"[Curator] The student is new, it was added. ")
    
    pl = privacy_loss_calculation(1,0.05,pow(10,-5))

    if (pl > get_private_budget()):
        print("[Curator] The loss of privacy of these queries exceeds the privacy budget.")
        res = np.array([-1.0], dtype=np.float64)
        HE_response = Pyfhel()
        HE_response.from_bytes_context(s_context_student)
        HE_response.from_bytes_public_key(s_public_key_student)
        ctx = HE_response.encrypt(res)
        return ctx.to_bytes().decode('cp437') 
    else:
        count = predictions(s_context_student, s_public_key_student, cx_response)

        sensitivity = 1.0 / 5

        noise = np.random.laplace(0., sensitivity/0.05,3)

        dp_count = count + noise

        update_private_budget(pl)
        print(f"[Curator] Private Budget: {get_private_budget()}")
        print(f"[Curator] Sum computed! Responding: {dp_count}")

        # Serialize encrypted result and answer it back
        return dp_count.to_bytes().decode('cp437')

@app.route('/get_pk', methods=['POST'])
def get_pk():
    print("[Curator] Received Request for get_pk!")
    print("[Curator] Responding with the public key")
    return jsonify(
            context=s_context.decode('cp437'),
            pk=s_public_key.decode('cp437'),
            )

@app.route('/add_teacher', methods=['POST'])
def add_teacher():
    print("[Curator] Received Request for add teacher!")
    
    HE_teacher = Pyfhel()
    HE_teacher.from_bytes_context(request.json.get('context').encode('cp437'))
    HE_teacher.from_bytes_public_key(request.json.get('pk').encode('cp437'))
    url = request.json.get('url')

    teacher = (url,HE_teacher)

    list_teachers.append(teacher)

    print(f"[Curator] Teacher {url} added")
    return 'Teacher added'

  
app.run(host='0.0.0.0', port=5000) # Run, accessible via http://localhost:5000/

# sphinx_gallery_thumbnail_path = 'static/thumbnails/clientServer.png'