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