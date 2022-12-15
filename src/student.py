import numpy as np
from Pyfhel import Pyfhel, PyCtxt
try:
    import requests
except ImportError:
    print("This demo requires the `requests` python module (install with pip). Exiting.")
    exit(0)

class Student:
    def __init__(self,id):
        self.id = id
        self.n_classes = 3
        self.HE = self.init_pyhel_session()

    
    def init_pyhel_session(self):
        # Generate Pyfhel session
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
        return HE_student

    def data(self):
        x = np.array([0,9,14])
        noise_1 = np.random.laplace(0., 1./0.05)
        noise_2 = np.random.laplace(0., 1./0.05)
        noise_3 = np.random.laplace(0., 1./0.05)
        noise = np.array([noise_1, noise_2, noise_3])

        x = x + noise
        return x
    
    def ser_context_public_key(self):
        # Serializing context and public key
        s_context    = self.HE.to_bytes_context()
        s_public_key = self.HE.to_bytes_public_key()
        return s_context,s_public_key

    def run(self):
        x = self.data()
        r_pk = requests.post('http://127.0.0.1:5000/get_pk')

        HE_request = Pyfhel()
        HE_request.from_bytes_context(r_pk.json().get('context').encode('cp437'))
        HE_request.from_bytes_public_key(r_pk.json().get('pk').encode('cp437'))

        cx = HE_request.encrypt(x)

        noise = np.random.laplace(0., 1./0.05)
        noise = np.array([noise])

        cx_noise = cx + noise
        s_cx = cx_noise.to_bytes()

        print(f"[Student {self.id}] Sending HE_student={self.HE} and cx={cx_noise}")

        s_context, s_public_key = self.ser_context_public_key()

        r = requests.post('http://127.0.0.1:5000/fhe_mse',
            json={
                'context': s_context.decode('cp437'),
                'pk': s_public_key.decode('cp437'),
                'cx': s_cx.decode('cp437'),
                'id': '2f1759fc-7c98-11ed-a1eb-0242ac120002'
            })
        c_res = PyCtxt(pyfhel=self.HE, bytestring=r.text.encode('cp437'))

        res = self.HE.decrypt(c_res)[:self.n_classes]

        # Checking result
        expected = np.argmax(res)
        return expected