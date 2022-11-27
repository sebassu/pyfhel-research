import numpy as np
import uuid
from flask import Flask
from Pyfhel import Pyfhel, PyCtxt
from base64 import decodebytes

app = Flask(__name__)

@app.route('/fhe_mse', methods=['POST'])

class Model():
    def __init__(self):
        super(Model,self).__init__()
        self.id = 0
        self.results = []
    
    #def __init__(self,id,results):
    #    super(Model,self).__init__()
    #    self.id = id
    #    self.results = results
    
    def setId(self,id):
        self.id = id
    
    def setResults(self,res):
        self.results = res
    
    def getResults(self):
        return self.results
    
    def addResult(self,result):
        self.results.append(result)
    
    def mock(self,size,debugMode=False):
        if debugMode :
            print("Size : ", size)
        random = np.random.rand(size)
        maxValue = np.argmax(random)
        values = np.zeros(size)
        if debugMode :
            print("Máximo Valor : ",maxValue)
        values[maxValue] = 1
        self.setResults(values)

    def mock2(self,size,pos,):
        if pos>=size:
            print("Invalid position : ", pos , " - Size : ", size)
        else:
            print("Size : ", size)
            values = np.zeros(size)
            print(maxValue)
            values[pos] = 1
            self.setResults(values)
            
    def mockTeachers(self,qty,size,):
        # Seteando varios modelos con valores aleatorios
        teachers = []
        for i in range(qty):
            t = Teacher("")
            m = Model()
            m.id = i
            m.mock(size)
            t.addModel(m)
            teachers.append(t)
        return teachers

class PyfhelClient():
    def __init__(self,parameters):
        super(PyfhelClient, self).__init__()
        if "Student" not in parameters:
            sPars = {}
            self.Student = Student(sPars)
        else:
            self.Student = parameters["Student"]
        
    
    def initHE():
        self.HE.keyGen()             # Generates both a public and a private key
        self.HE.relinKeyGen()
        self.HE.rotateKeyGen()
        
        
class PyfhelServer():
    def __init__(self,parameters):
        super(PyfhelServer, self).__init__()
        if len(parameters)==0 or not "Curator" in parameters:
            cPar = {}
            self.Curator = Curator(cPar)
        else:
            self.Curator = parameters["Curator"]
    
    def associateCurator(self,curator):
        self.Curator = curator
    
    
    def post(self):
        print("Received Request!")

        # Read all bytestrings
        HE_server = Pyfhel()
        HE_server.from_bytes_context(request.json.get('context').encode('cp437'))
        HE_server.from_bytes_public_key(request.json.get('pk').encode('cp437'))
        HE_server.from_bytes_relin_key(request.json.get('rlk').encode('cp437'))
        HE_server.from_bytes_rotate_key(request.json.get('rtk').encode('cp437'))
        cx = PyCtxt(pyfhel=HE_server, bytestring=request.json.get('cx').encode('cp437'))
        print(f"[Server] received HE_server={HE_server} and cx={cx}")

        # Encode weights in plaintext
        ptxt_w = HE_server.encode(w)
        
        #######################################                                  
        # Agregar Operaciones a realizar acá
        #######################################
                
        return c_mean.to_bytes().decode('cp437')

    def start(self,port=None):
        ### Averiguar como utilizar modo debug de Flask
        if (port is None):
            app.run(host='0.0.0.0', port=5000) # Run, accessible via http://localhost:5000/
        else:
            app.run(host='0.0.0.0', port=port)
        #pass
    
    def stopServer(self,port=None):
        if port is None:
            app.stop(host='0.0.0.0',port=5000)
        else:
            app.stop(host='0.0.0.0',port=port)
    
    def stop(self):
        #app.stop()       ???????
        pass

class PyfhelPlatform():
    def __init__(self,parameters):
        super(PyfhelPlatform,self).__init__()
        self.servers = []
        self.clients = []
        if len(parameters)==0 or parameters["ServersQ"] is None:
            print("Error Initializing platform, please specify Servers quantity")
        else:
            qServers = parameters["ServersQ"]
            if parameters["key_gen"] is None:
                key_gen = parameters["key_gen"]
            else:
                key_gen = True
            if "context_params" not in parameters:
                context_params = {'scheme':'ckks', 'n':2**13, 'scale':2**30, 'qi_sizes':[30]*5}  
            else:
                context_params= parameters["context_params"]
                #print(context_params)
            print("Cantidad de Servidores a crear : ",qServers)
            for i in range(qServers):
                print("Initializing Server : ",i)
                server = PyfhelServer(context_params)
                self.servers.append(server)
        print(self.servers)
    
    def startServers(self,initialPort=5000):
        qServers = len(self.servers)
        print("Cantidad de Servidores: ",qServers)
        for i in range(qServers):
                print("Starting Server : ",i)
                server = self.servers[i]
                server.start(initialPort+i)
    
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
        
    
class Teacher():
    def __init__(self,parameters):
        super(Teacher, self).__init__()
        self.models = []
        #print(f"Teacher Created !!!")
        #print("Parameters:")
        #print(parameters)
    
    def addModel(self,model):
        self.models.append(model)
    
    def findModel(self,modelId):
        #print("findModel : ", modelId)
        #print("Lista Modelos")
        #print(self.models)
        #m = [m for m in self.models if m.id==modelId ]
        for m in self.models:
            if m.id == modelId:
                #print(m , " Encontrado")
                return m
        return None
    
    def getResults(self,modelId):
        #print("                        mId : ", modelId)
        m = self.findModel(modelId)
        if m is not None:
            return m.getResults()
        #print("Model : ",modelId, " not found.")
    
    def askForInformationReceived(self,info):
        print("Ask for Information Received!!!")
        print(info)
    
    def computeResponse(self, model):
        model = self.findModel(model.id)
        results = []
        modelResults = model.getResults()
        if len(modelResults)>0:
            results = np.argmax(modelResults)
        return results
            

class Student():
    def __init__(self,parameters):
        super(Student,self).__init__()
        #self.HEC = Pyfhel(context_params={'scheme':'ckks', 'n':2**13, 'scale':2**30, 'qi_sizes':[30]*5})
        self.id = 0
        self.Curator = None
        #if parameters["Curator"] is None:
        #    self.Curator = Curator()
        #else:
        #self.Curator = parameters["Curator"] 
        #print(f"Student created!!!")
        #print("Parameters:")
        #print(parameters)
    
    def askForInfo(self,info,key):
        # Encriptar los datos y enviar los datos con ruido incluído
        #print("Info request:")
        #print (f"{'Info:':<30}{info:<40}")
        
        return self.Curator.getInfo(info)
    
    def addCurator(self,curator):
        self.Curator = curator
    
    def shareKey(self,key):
        pass