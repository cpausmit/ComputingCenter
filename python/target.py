import range

class Target:
    'A class to describe a target design for a computing center.'

    def __init__(self,power_string,cost_string,hspec_string,ncores_string,network_string,diskspace_string):
        self.power_range = range.Range(power_string)
        self.cost_range = range.Range(cost_string)
        self.hspec_range = range.Range(hspec_string)
        self.ncores_range = range.Range(ncores_string)
        self.network_range = range.Range(network_string)
        self.diskspace_range = range.Range(diskspace_string)

    def show(self):
        print(" Design target:")
        print("  Power: (%s) kW   Cost: (%s) k$ )"%(self.power_range.string,self.cost_range.string))
        print("  HSP: (%s)  Cores: (%s)  Network: (%s)  Storage: (%s) TB" \
              %(self.hspec_range.string,self.ncores_range.string,self.network_range.string,self.diskspace_range.string))
