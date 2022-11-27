class Tests():

    def Test4(self):
        # Creando un teacher con un modelo, creando un mock y computando la respuesta
        t4 = Teacher("Parametros del Teacher 4")

        m2 = Model()
        m2.id = 4
        m2.mock(15)
        t4.addModel(m2)

        t4.computeResponse(m2)
        #print(t4.models)
        print(t4.getResults(4))

    
    def Test5(self):
        # Creando un teacher con mas de un modelo
        t5 = Teacher("")

        m3 = Model()
        m3.id = 3
        m3.mock(15)
        t5.addModel(m3)
        print(m3.getResults())

        m4 = Model()
        m4.id = 4
        m4.mock(15)
        t5.addModel(m4)
        print(m4.getResults())

        t5.computeResponse(m4)
        #print(t4.models)
        print(t5.getResults(4))

    def Test6(self):
        # Seteando un modelo con valores conocidos
        t6 = Teacher("")
        m6 = Model()
        m6.id = 6
        m6.mock2(6,8)
        t6.addModel(m6)

        t6.computeResponse(m6)
        print(t6.getResults(6))

        
    def Test7(self):
        # Seteando un modelo con valores conocidos
        t7 = Teacher("")
        m7 = Model()
        m7.id = 7
        m7.mock2(8,8)
        t7.addModel(m7)

        t7.computeResponse(m7)
        print(t7.getResults(7))

    def Test8(self):
        # Seteando un modelo con valores conocidos
        t8 = Teacher("")
        m8 = Model()
        m8.id = 8
        m8.mock2(8,4)
        t8.addModel(m8)

        t8.computeResponse(m8)
        print(t8.getResults(8))

    def TestM2(self):
        # Seteando varios modelos con valores aleatorios
        q = 5
        s = 10
        teachers = []
        for i in range(q):
            t = Teacher("")
            m = Model()
            m.id = i
            m.mock(s)
            t.addModel(m)
            teachers.append(t)

        for i in range(q):
            print(teachers[i].getResults(i))
        #t.computeResponse(m8)
        #print(t.getResults(8))

    def TestM3(self,q,s):
        # Seteando varios modelos con valores aleatorios
        teachers = []
        for i in range(q):
            t = Teacher("")
            m = Model()
            m.id = i
            m.mock(s)
            t.addModel(m)
            teachers.append(t)

    def printTeachers(self,teachers):
        print("Print Teachers content:")
        q = len(teachers)
        for i in range(q):
            print(i+1,":",teachers[i].getResults(i))

    def TestM1(self):
        #c.requestReceived("Test2")

        t1 = Teacher("Parametros del Teacher 1")
        #t1.askForInformationReceived("Modelo1")

        m = Model()
        m.id = 1
        m.results = [0,0.1,0.2,0.3]
        t1.addModel(m)

        #modelo = t1.findModel(1)
        #print("Modelo :")
        #print(modelo.id)
        #print(modelo.getResults())

        t2 = Teacher("Parametros del Teacher 2")
        #t2.askForInformationReceived("Modelo1")
        m2 = Model()
        m2.id = 2
        m2.results = [0,0.5,0.2,0.3]
        t2.addModel(m)

        t3 = Teacher("Parametros del Teacher 3")
        #t3.askForInformationReceived("Modelo1")

        par = {}
        par["teachers"] = [t1,t2,t3]

        c = Curator(par)

        parStu = []
        s = Student(parStu)
        #s.askForInfo("Modelo 1")
        s.addCurator(c)

        infoRequest = {}
        infoRequest["id"] = 1
        r = s.askForInfo(infoRequest,None)
        print(r)
    
    def TestC1(self,q,s):
        m = Model()
        teachers = m.mockTeachers1(q,s)
        self.printTeachers(teachers)
    
    def TestC2(self,q,s):
        m = Model()
        teachers = m.mockTeachers(q,s)
        #self.printTeachers(teachers)
        #print("Asigning teachers to Curator")
        c = Curator("")
        c.setTeachers(teachers)
        
        self.printTeachers(c.getTeachers())
    
    def TestC3(self,parameters):
        c = Curator(parameters)
     