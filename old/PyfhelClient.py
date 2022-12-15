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