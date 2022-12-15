USE_REAL_SERVER: bool = True

import numpy as np
import uuid
from Pyfhel import Pyfhel
from src.student import Student

if USE_REAL_SERVER:
    try:
        import requests
    except ImportError:
        print("This demo requires the `requests` python module (install with pip). Exiting.")
        exit(0)

n_students = 2
n_teachers = 5
students = []
processes = []

# %%
# 1. Create students
# -----------------------

print(f"[Main] Creating {n_students} students")

student1 = Student(uuid.uuid4())
student2 = Student(uuid.uuid4())

# %%
# 2. Setup Server
# -----------------------

if(USE_REAL_SERVER):
    import subprocess, os
    from pathlib import Path
    import time

    dir = Path(os.path.realpath("__file__")).parent
    print(f"[Main] Launching Curator (could be launched separately)...")

    process_curator = subprocess.Popen(
        ["python", str(dir / "src//curator.py")],
        stderr=subprocess.STDOUT,
    )
    processes.append(process_curator)
    time.sleep(6)       # Wait for server initialization
    print("[Main] Curator initialized...")


    print(f"[Main] Launching {n_teachers} Teachers ...")

    process_Teacher1 = subprocess.Popen(
            ["python", str(dir / "src//teacher.py"),'-p',str(5010)],
            stderr=subprocess.STDOUT,
        )
    processes.append(process_Teacher1)
    time.sleep(6)       # Wait for server initialization
    print(f"[Main] Teacher 1 initialized...")

    process_Teacher1 = subprocess.Popen(
            ["python", str(dir / "src//teacher.py"),'-p',str(5010)],
            stderr=subprocess.STDOUT,
        )
    processes.append(process_Teacher1)
    time.sleep(6)       # Wait for server initialization
    print(f"[Main] Teacher 1 initialized...")

    process_Teacher2 = subprocess.Popen(
            ["python", str(dir / "src//teacher.py"),'-p',str(5011)],
            stderr=subprocess.STDOUT,
        )
    processes.append(process_Teacher2)
    time.sleep(6)       # Wait for server initialization
    print(f"[Main] Teacher 2 initialized...")

    process_Teacher3 = subprocess.Popen(
            ["python", str(dir / "src//teacher.py"),'-p',str(5012)],
            stderr=subprocess.STDOUT,
        )
    processes.append(process_Teacher3)
    time.sleep(6)       # Wait for server initialization
    print(f"[Main] Teacher 3 initialized...")

    process_Teacher4 = subprocess.Popen(
            ["python", str(dir / "src//teacher.py"),'-p',str(5013)],
            stderr=subprocess.STDOUT,
        )
    processes.append(process_Teacher4)
    time.sleep(6)       # Wait for server initialization
    print(f"[Main] Teacher 4 initialized...")
        

else:
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
    s_context    = HE_student.to_bytes_context()
    s_public_key = HE_student.to_bytes_public_key()
    x = np.array([0,9,14])
    print(f"[Curator] Mock started!...")
    print(f"[Teacher] Mock started!...")
    print("[Main] Curator initialized...")

# %%
# 3. Launch a request to the server
# ----------------------------------------
#  We map the bytes into strings based on https://stackoverflow.com/a/27527728
if(USE_REAL_SERVER):
    expected1 = student1.run()
    print(f"[Student 1] Response received! Argmax result is {expected1}")

    expected2 = student2.run()
    print(f"[Student 2] Response received! Argmax result is {expected2}")

    expected1_2 = student1.run()
    print(f"[Student 1] Response received! Argmax result is {expected1_2}")


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

    res = HE_student.decrypt(c_res)[:3]

    # Checking result
    expected = np.argmax(res)
    print(f"[Student] Response received! Argmax result is {expected}")

# %% 5. Stop server
if USE_REAL_SERVER:
    for process in processes:
        process.kill()

# sphinx_gallery_thumbnail_path = 'static/thumbnails/encrypting.jpg'