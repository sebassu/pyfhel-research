USE_REAL_SERVER: bool = True

# %%
# 1. Setup Client
# --------------------------
import numpy as np
import asyncio
from Pyfhel import Pyfhel, PyCtxt
if USE_REAL_SERVER:
    try:
        import requests
    except ImportError:
        print("This demo requires the `requests` python module (install with pip). Exiting.")
        exit(0)

# Generate Pyfhel session
print(f"[Student] Initializing Pyfhel session and data...")
HE_student = Pyfhel()           # Creating empty Pyfhel object
ckks_params = {
    'scheme': 'CKKS',   # can also be 'ckks'
    'n': 2**14,         # Polynomial modulus degree. For CKKS, n/2 values can be
                        #  encoded in a single ciphertext. 
                        #  Typ. 2^D for D in [10, 16]
    'scale': 2**30,     # All the encodings will use it for float->fixed point
                        #  conversion: x_fix = round(x_float * scale)
                        #  You can use this as default scale or use a different
                        #  scale on each operation (set in HE.encryptFrac)
    'qi_sizes': [60, 30, 30, 30, 60] # Number of bits of each prime in the chain. 
                        # Intermediate values should be  close to log2(scale)
                        # for each operation, to have small rounding errors.
}
HE_student.contextGen(**ckks_params)  # Generate context for bfv scheme
HE_student.keyGen()             # Key Generation: generates a pair of public/secret keys
HE_student.rotateKeyGen()

n_classes = 3

# Generate and encrypt data
x = np.array([0,9,14])

# Serializing context and public key
s_context    = HE_student.to_bytes_context()
s_public_key = HE_student.to_bytes_public_key()



# %%
# 2. Setup Server
# -----------------------

print(f"[Student] Launching Curator (could be launched separately)...")
if(USE_REAL_SERVER):
    import subprocess, os
    from pathlib import Path
    import time

    dir = Path(os.path.realpath("__file__")).parent

    process_curator = subprocess.Popen(
        ["python", str(dir / "curator.py")],
        stderr=subprocess.STDOUT,
    )
    time.sleep(6)       # Wait for server initialization
    print("[Student] Curator initialized...")

    process_Teacher_1 = subprocess.Popen(
        ["python", str(dir / "teacher1.py")],
        stderr=subprocess.STDOUT,
    )
    time.sleep(6)       # Wait for server initialization
    print("[Student] Teacher 1 initialized...")

    process_Teacher_2 = subprocess.Popen(
        ["python", str(dir / "teacher2.py")],
        stderr=subprocess.STDOUT,
    )
    time.sleep(6)       # Wait for server initialization
    print("[Student] Teacher 2 initialized...")

    process_Teacher_3 = subprocess.Popen(
        ["python", str(dir / "teacher3.py")],
        stderr=subprocess.STDOUT,
    )
    time.sleep(6)       # Wait for server initialization
    print("[Student] Teacher 3 initialized...")

    process_Teacher_4 = subprocess.Popen(
        ["python", str(dir / "teacher4.py")],
        stderr=subprocess.STDOUT,
    )
    time.sleep(6)       # Wait for server initialization
    print("[Student] Teacher 4 initialized...")

    process_Teacher_5 = subprocess.Popen(
        ["python", str(dir / "teacher5.py")],
        stderr=subprocess.STDOUT,
    )
    time.sleep(6)       # Wait for server initialization
    print("[Student] Teacher 5 initialized...")
else:
    print(f"[Curator] Mock started!...")
    print("[Student] Curator initialized...")

# %%
# 3. Launch a request to the server
# ----------------------------------------
#  We map the bytes into strings based on https://stackoverflow.com/a/27527728
if(USE_REAL_SERVER):

    print(f"[Student] Requests the public key from the Curator")
    r_pk = requests.post('http://127.0.0.1:5000/get_pk')


    HE_request = Pyfhel()
    HE_request.from_bytes_context(r_pk.json().get('context').encode('cp437'))
    HE_request.from_bytes_public_key(r_pk.json().get('pk').encode('cp437'))

    cx = HE_request.encrypt(x)

    noise = np.random.laplace(0., 1./0.05)
    noise = np.array([noise])

    cx_noise = cx + noise
    s_cx = cx_noise.to_bytes()
    

    
    print(f"[Student] Sending HE_student={HE_student} and cx={cx_noise}")

    r = requests.post('http://127.0.0.1:5000/fhe_mse',
        json={
            'context': s_context.decode('cp437'),
            'pk': s_public_key.decode('cp437'),
            'cx': s_cx.decode('cp437'),
        })
    c_res = PyCtxt(pyfhel=HE_student, bytestring=r.text.encode('cp437'))
else: # Mocking server code (from Demo_5bis_CS_Server.py)
    # Read all bytestrings
    HE_server = Pyfhel()
    HE_server.from_bytes_context(s_context)
    HE_server.from_bytes_public_key(s_public_key)
    print(f"[Server] received HE_server={HE_server} and x={x}")

    # Encode weights in plaintext
    arr_1 = np.array([0., 0., 1.], dtype=np.float64)
    arr_2 = np.array([0., 1., 0.], dtype=np.float64)
    arr_3 = np.array([0., 0., 1.], dtype=np.float64)
    arr_4 = np.array([1., 0., 0.], dtype=np.float64)
    arr_5 = np.array([0., 0., 1.], dtype=np.float64)

    ctx_1 = HE_server.encrypt(arr_1)
    ctx_2 = HE_server.encrypt(arr_2)
    ctx_3 = HE_server.encrypt(arr_3)
    ctx_4 = HE_server.encrypt(arr_4)
    ctx_5 = HE_server.encrypt(arr_5)

    count = ctx_1 + ctx_2 + ctx_3 + ctx_4 + ctx_5

    noise_1 = np.random.laplace(0., 1./0.05)
    noise_2 = np.random.laplace(0., 1./0.05)
    noise_3 = np.random.laplace(0., 1./0.05)
    noise = np.array([noise_1, noise_2, noise_3])

    dp_count = count + noise


    print(f"[Curator] Sum computed! Responding: result={dp_count}")

    c_res = dp_count.copy() # Copying with a single command

# %%
# 4. Process Response
# --------------------------
# Decrypting result
res = HE_student.decrypt(c_res)[:n_classes]

print(res)
# Checking result
expected = np.argmax(res)
print(f"[Student] Response received! Argmax result is {expected}")


# %% 5. Stop server
if USE_REAL_SERVER:
    process_curator.kill()
    process_Teacher_1.kill()
    process_Teacher_2.kill()
    process_Teacher_3.kill()
    process_Teacher_4.kill()
    process_Teacher_5.kill()

# sphinx_gallery_thumbnail_path = 'static/thumbnails/encrypting.jpg'