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
        
        #return self.Curator.getInfo(info)
        return self.Curator.getInfoNew(info)
    
    def addCurator(self,curator):
        self.Curator = curator
    
    def shareKey(self,key):
        pass