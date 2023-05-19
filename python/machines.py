class Machine:
    'A class to describe a computer in a computing center.'

    def __init__(self,name,power,hspec,ncores,memory,network,diskspace,height,cost):
        self.name = name                   # to identify
        self.power = float(power)          # in kW
        self.hspec = float(hspec)          # [kHSPEC26]
        self.ncores = int(ncores)          # [-]
        self.memory = float(memory)        # [GB]
        self.network = float(network)      # [Gb/sec]
        self.diskspace = float(diskspace)  # [TB]
        self.height = int(height)          # [U]
        self.cost = float(cost)            # [k$]

    def show(self):
        print(" Machine: %s\n  Pw: %.2f kW HSP: %.0f kHSPEC NC: %d RAM: %.2f GB IO: %.2f Gb/s Disk: %.0f GB Height: %d U Cost: %.2f k$"\
            %(self.name,self.power,self.hspec,self.ncores,self.memory,self.network,self.diskspace,self.height,self.cost))
