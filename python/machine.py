class Machine:
    'A class to describe a computer in a computing center.'

    def __init__(self,name,power,cputype,hspec,ncores,memory,network,diskspace,height,cost):
        self.name = name                   # to identify
        self.power = float(power)          # [kW]
        self.cputype = cputype             # string
        self.hspec = float(hspec)          # [kHSPEC26]
        self.ncores = int(ncores)          # [-]
        self.memory = float(memory)        # [GB]
        self.network = float(network)      # [Gb/sec]
        self.diskspace = float(diskspace)  # [TB]
        self.height = int(height)          # [U]
        self.cost = float(cost)            # [k$]

    def load_from_string(self,string):
        f = string.split(' ')
        # hibat0143 Intel(R)_Xeon(R)_Silver_4116_2.10GHz 48 96 5 45.5 1000baseT/Full 1100 530
        self.name = f[0]
        self.power = float(f[7])/1000
        self.cputype= f[1]
        self.hspec = float(f[8])
        self.ncores = int(f[2])
        self.memory = float(f[3])
        self.network = 1                        # f[6]
        self.diskspace = float(f[5])
        self.height = 2                         # all workers are two U
        self.cost = 5                           # this is probably a reasonable value on average
        return

    def show(self):
        print(" %s"%self.string())
        
    def string(self):
        return "Machine: %s -- Pw: %.2f kW  CPU: %s  HSP: %.0f kHSPEC  NC: %d  RAM: %.2f GB  IO: %.2f Gb/s  Disk: %.0f GB  Height: %d U  Cost: %.2f k$"%(self.name,self.power,self.cputype,self.hspec,self.ncores,self.memory,self.network,self.diskspace,self.height,self.cost)

    def copy(self,name):
        return Machine(name,self.power,self.cputype,self.hspec,self.ncores,self.memory,self.network,self.diskspace,self.height,self.cost)
