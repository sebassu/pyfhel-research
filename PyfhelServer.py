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