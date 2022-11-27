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