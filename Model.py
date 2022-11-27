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