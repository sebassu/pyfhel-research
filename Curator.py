class Curator():
    def __init__(self,parameters):
        super(Curator, self).__init__()
        #self.HEC = Pyfhel(context_params={'scheme':'ckks', 'n':2**13, 'scale':2**30, 'qi_sizes':[30]*5}) 
        self.data = {}
        #print(type(parameters["teachers"]))
        if len(parameters)==0 or not "teachers" in parameters:
            self.id = uuid.uuid4()
            self.teachers = []
        else:
            print(parameters["teachers"])
            if len(parameters["teachers"]) > 0:
                self.teachers = parameters["teachers"]
            else:
                self.teachers = []
        
        self.results = []
        #print(f"Curator created !!!")
        #print("Parameters:")
        #print(parameters)
        
    def createTeachers(self, size):
        for i in range(size):
            t = Teacher()
            self.teachers.append(t)
    
    def addTeacher(self,teacher):
        self.teachers.append(teacher)
    
    def setTeachers(self,teacherList):
        self.teachers = teacherList
    
    def getTeachers(self):
        return self.teachers
    
    def getInfo(self,info):
        self.results = []
        modelId = info["id"]
        for t in self.teachers:
            self.results.append(t.getResults(modelId))
        return self.prepareData(self.results)
        #return self.results
    
    def getInfoNew(self,info):
        HE_client = Pyfhel(context_params={'scheme':'ckks', 'n':2**13, 'scale':2**30, 'qi_sizes':[30]*5})
        HE_client.keyGen()             # Generates both a public and a private key
        HE_client.relinKeyGen()
        HE_client.rotateKeyGen()
        r = requests.post('http://127.0.0.1:5000/fhe_mse',
        json={
            'context': s_context.decode('cp437'),
            'pk': s_public_key.decode('cp437'),
            'rlk':s_relin_key.decode('cp437'),
            'rtk':s_rotate_key.decode('cp437'),
            'cx': s_cx.decode('cp437'),
        })
        c_res = PyCtxt(pyfhel=HE_client, bytestring=r.text.encode('cp437'))


    
    def prepareData(self, data):
        #Evaluar escenarios de envío de claves hacia el Student desde el Curator
        
        self.data = data
        #HE.keyGen()             # Generates both a public and a private key
        #HE.relinKeyGen()
        #HE.rotateKeyGen()
        #cx = HE.encrypt(data)

        # Serializing data and public context information
        #self.data["s_context"]    = HE.to_bytes_context()
        #self.data["s_public_key"] = HE.to_bytes_public_key()
        #self.data["s_relin_key"]  = HE.to_bytes_relin_key()
        #self.data["s_rotate_key"] = HE.to_bytes_rotate_key()
        #self.data["s_cx"]         = cx.to_bytes()
        print("Preparing Data !!")
        return self.data
        
    def requestReceived(self, student, nombreModelo ):
        print("Request Received !!!")
        print("Input   : ", nombreModelo)
        print("Student : ", student)
    
    def addNoise():
        pass
    
    def prepareResponse(self, data):
        for t in self.teachers:
            self.results.append(t.computeResponse())
        return self.results