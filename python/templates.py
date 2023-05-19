import machine

# costs
cost_srv = 5.0     # server basis
cost_10gb = 0.1    # various network cards
cost_25gb = 0.5 
cost_100gb = 1.0
cost_tb = 0.01552  # one TB of spinning disk

disk_size = 20  # [TB]
useable = 0.75  # erasure coding 0.75 * disk_space is useable

class Templates:
    'A class to describe a computing center.'

    def __init__(self):
        self.machine_templates = {}
        # Machine(name,power,hspec,ncores,memory,network,diskspace,height,cost)

        # existing workers
        worker_016  = machine.Machine('wrk016',0.75,'TmpType', 400, 16,   24.0,  0,0,2, 3.0)
        worker_040  = machine.Machine('wrk040',0.75,'TmpType', 500, 40,  132.0,  0,0,2, 3.6) 
        worker_048  = machine.Machine('wrk048',0.75,'TmpType', 500, 40,   98.0,  0,0,2, 4.2) 
        worker_064  = machine.Machine('wrk064',0.75,'TmpType', 600, 64,  132.0,  0,0,2, 7.0) 
        # new potential worker (provides only CPU) # https://www.thinkmate.com/system/rax-qt12-21e4
        worker_064  = machine.Machine('wrk064',1.00,'TmpType',1000,128,128*2.0,  0,0,1, 8.5) # conserv. price
        worker_128  = machine.Machine('wrk128',1.00,'TmpType',1000,128,128*2.0,  0,0,1,14.0) # ThinkMate
        worker_256  = machine.Machine('wrk256',1.70,'TmpType',1000,256,256*2.0,  0,0,1,23.0) # 1U
        worker_384  = machine.Machine('wrk384',2.00,'TmpType',1000,384,384*2.0,  0,0,1,37.0) 
    
        # new potential storage (provides only storage)
        store_11    = machine.Machine('str11', 0.50,'TmpType',   0,  0,    32.,  0,11*disk_size*useable,2,cost_srv+11*disk_size*cost_tb)
        store_22    = machine.Machine('str22', 0.50,'TmpType',   0,  0,    32.,  0,22*disk_size*useable,2,cost_srv++22*disk_size*cost_tb)
    
        # new potential network (provides only external network)
        network_010 = machine.Machine('ntw010',0.50,'TmpType',   0,  0,    32., 10,0,1,cost_srv+cost_10gb)
        network_025 = machine.Machine('ntw025',0.50,'TmpType',   0,  0,    32., 25,0,1,cost_srv+cost_25gb)
        network_100 = machine.Machine('ntw100',0.50,'TmpType',   0,  0,    32.,100,0,1,cost_srv+cost_100gb)
        
        self.add_machine(worker_016)
        self.add_machine(worker_040)
        self.add_machine(worker_048)
        self.add_machine(worker_064)
    
        self.add_machine(worker_128)
        self.add_machine(worker_256)
        self.add_machine(worker_384)
    
        self.add_machine(store_11)
        self.add_machine(store_22)
        
        self.add_machine(network_010)
        self.add_machine(network_025)
        self.add_machine(network_100)

    def show(self):
        print("Available templates")
        print(self.machine_templates)

    def add_machine(self,machine):
        name = machine.name
        self.machine_templates[name] = machine
        
##===================================================================================================
## M A I N [for testing only]
##===================================================================================================
#if __name__ == "__main__":
