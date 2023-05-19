import os,sys
import machine
import range
import target
import templates

# Basic configuration parameters
year_hrs = 24*30*12
lbs_to_ton = 0.0004535924

# Facility costs - Bates
cost_kwh_ba = 0.0001362 # [k$] cost kWh, https://findenergy.com/providers/middleton-electric/
usage_ba = 1.0          # fraction of power used (CPU running 100%?)
pue_ba = 2.0            # power utilization effectiveness
c_intensity_ba = 0.719  # lbs per kWh
c_tax_ba = 0.234        # [k$] carbon tax per ton of carbon produced

# Facility costs - Holyoke
cost_kwh_hy = 0.0000898109 # [k$] cost kWh, 
usage_hy = 1.0          # fraction of power used (CPU running 100%?)
pue_hy = 1.14           # power utilization effectiveness
c_intensity_hy = 0.05   # lbs per kWh
c_tax_hy = 0.234        # [k$] carbon tax per ton of carbon produced

# Hardware costs
cost_srv = 5.0         # server basis
cost_10gb = 0.1        # various network cards
cost_25gb = 0.5 
cost_100gb = 1.0
cost_tb = 0.01552      # one TB of spinning disk (from the web)

disk_size = 20         # [TB]
useable = 0.75         # erasure coding 0.75 * disk_space is useable

class Computing_center:
    'A class to describe a computing center.'

    def __init__(self,name,cost_kwh,usage,pue,carbon_intensity,carbon_tax):
        self.name = name          # to identify
        # infrastructure
        self.cost_kwh = cost_kwh  # electricity cost per kilo Watt hour
        self.usage = usage        # fraction of power usage (CPU mostly)
        self.pue = pue            # power utilization effectivness:
                                  # https://en.wikipedia.org/wiki/Power_usage_effectiveness
        self.carbon_intensity = carbon_intensity  # pounds of carbon produced per kWh
        self.carbon_tax = carbon_tax              # dollars to pay per ton of carbon produced
        # hardware
        self.machine_groups = {} # dictionary:  key==name - value==dictionary of machines
        self.cost_group = {}     # cummulative hardware cost of this group
        self.nmachines = 0       # total number of machines
        self.ncores = 0          # total number of cores for processing
        self.power = 0.          # [kW]
        self.network = 0.        # networking to the outside world [Gb/s]
        self.diskspace = 0.      # total amount of disk for mass storage [TB]
        self.cost = 0.           # cost of the hardware, once [k$]
        self.height = 0          # height taken in rack [U]

    def add_group(self,name):
        machines = {}
        self.machine_groups[name] = machines
        self.cost_group[name] = 0
        return self.machine_groups[name]

    def add_machine(self,group_name,machine):
        self.machine_groups[group_name][machine.name] = machine
        self.cost_group[group_name] += machine.cost

        self.nmachines += 1
        self.ncores += machine.ncores
        self.power += machine.power
        self.network += machine.network
        self.diskspace += machine.diskspace
        self.cost += machine.cost
        self.height += machine.height

    def compare(self,center):
        print(f" Comparison: %s versus %s"%(self.name,center.name))
        print(f" -----------\n")
        print(f" Once                    %7s  %7s - Difference"%(self.name,center.name))
        print(f"  -->  hardware cost:    %4.0f k$  %4.0f k$ - %4.0f k$"%
              (self.cost,center.cost,self.cost-center.cost))
        print(f" Yearly")
        print(f"  -->  electricity cost: %4.0f k$  %4.0f k$ - %4.0f k$"%
              (self.cost_electricity(),center.cost_electricity(),
               self.cost_electricity()-center.cost_electricity()))
        print(f"  -->  carbon cost:      %4.0f k$  %4.0f k$ - %4.0f k$"%
              (self.cost_carbon(),center.cost_carbon(),self.cost_carbon()-center.cost_carbon()))
        print()
        
        return

    def cost_electricity(self):
        cost = self.power*self.usage*self.pue*year_hrs*self.cost_kwh # per year
        return cost

    def cost_carbon(self):
        carbon_produced = self.power*self.usage*self.pue*year_hrs*self.carbon_intensity # per year
        cost = carbon_produced*lbs_to_ton*self.carbon_tax
        return cost
    
    def design_center(self,templates,target,worker,store,network):
        i = 0
        while not target.diskspace_range.inside(self.diskspace):
            name = "%s:%03d"%(templates.machine_templates[store].name,i)
            self.add_machine('storage',templates.machine_templates[store].copy(name))
            i+=1
        i = 0
        while not target.ncores_range.inside(self.ncores):
            name = "%s:%03d"%(templates.machine_templates[worker].name,i)
            self.add_machine('worker',templates.machine_templates[worker].copy(name))
            i+=1
        i = 0
        while not target.network_range.inside(self.network):
            name = "%s:%03d"%(templates.machine_templates[network].name,i)
            self.add_machine('network',templates.machine_templates[network].copy(name))
            i+=1

        return
    
    def show(self):

        print("\n Computing Center: %s"%(self.name))
        print(  " =================\n")
        
        print(f" Components:")
        print(f" -----------")
        for group_key in sorted(self.machine_groups):
            group = self.machine_groups[group_key]
            print(f"  Group: {group_key} N: {len(group)} -- {self.cost_group[group_key]} k$")
            for machine_key in group:
                print("   %s"%group[machine_key].string())
                break
        
        print( "")
        print(f" Basic configuration:")
        print(f" --------------------")
        print(f"  power [kW]:      nominal  {self.power:.0f}  used: {self.power*self.usage:.0f}  (usage: {self.usage:.3f})")
        print(f"  energy/yr [kWh]: computer {self.power*self.usage*year_hrs:.0f}  all: {self.power*self.usage*self.pue*year_hrs:.0f} (pue: {self.pue:.2f})")
        print(f"  carbon_intensity: {self.carbon_intensity:.2f} lbs/kWh  carbon_tax: {self.carbon_tax*1000:.0f} $/ton")
        print(f"  nracks: {self.height/40.}  nmachines: {self.nmachines}")
        print(f"  ncores: {self.ncores}  network: {self.network:.0f} Gb/s  diskspace: {self.diskspace:.0f} TB")
        print(f"  -->  hardware cost:    %4.0f k$ once"%(self.cost))
        print(f"  -->  electricity cost: %4.0f k$ per year"%(self.cost_electricity()))
        print(f"  -->  carbon cost:      %4.0f k$ per year"%(self.cost_carbon()))
        print()
        
#===================================================================================================
# M A I N [for testing only]
#===================================================================================================
if __name__ == "__main__":
    from optparse import OptionParser
    # define and get all command line arguments
    parser = OptionParser()
    # machine templates
    parser.add_option("-n","--network",dest="network",default='ntw010',help="network machines")
    parser.add_option("-w","--worker",dest="worker",default='wrk128',help="worker machines")
    parser.add_option("-s","--storage",dest="storage",default='str22',help="storage machines")
    # design target specs (example: --power 100:500)
    parser.add_option("-p","--power",dest="power",default='-',help="power range (def.: - no range")
    parser.add_option("-c","--cost",dest="cost",default='-',help="cost range (def.: - no range")
    parser.add_option("-e","--hspec",dest="hspec",default='-',help="hspec range (def.: - no range")
    parser.add_option("-o","--ncores",dest="ncores",default='24000:25000',help="ncores range (def.: - no range")
    parser.add_option("-d","--diskspace",dest="diskspace",default='17000:17200',help="diskspace range (def.: - no range")
    parser.add_option("-g","--gbs",dest="gbs",default='380:490',help="gbs range (def.: - no range")
    (options, args) = parser.parse_args()

    # real bates
    realistic_power_usage = 0.60
    real_pue = 1.50
    bates = Computing_center('Bates',cost_kwh_ba,realistic_power_usage,real_pue,c_intensity_ba,c_tax_ba)
    bates.add_group('bat')

    # read all available hardware servers from Tier-2
    with open("%s/doc/bates-tier2-nodes.dat"%(os.getenv('CC_BASE')),"r") as fH:
        data = fH.read()
    for string in data.split("\n"):
        if len(string) < 1 or string[0] == '#':
            continue
        m = machine.Machine('tmp',0,'type',0,0,0,0,0,0,0)
        m.load_from_string(string)
        bates.add_machine('bat',m)
        #m.show()
    bates.show()
    
    
    # read all available server templates
    templates = templates.Templates()

    # define the design targets
    target = target.Target(options.power,options.cost,options.hspec,options.ncores,options.gbs,options.diskspace)
    target.show()
    
    #fake_bates = Computing_center("Bates'",cost_kwh_ba,usage_ba,pue_ba,c_intensity_ba,c_tax_ba)
    #fake_bates.add_group('storage')
    #fake_bates.add_group('worker')
    #fake_bates.add_group('network')
    #fake_bates.design_center(templates,target,options.worker,options.storage,options.network)
    ##fake_bates.show()

    holyoke = Computing_center("Holyoke",cost_kwh_hy,usage_hy,pue_hy,c_intensity_hy,c_tax_hy)
    holyoke.add_group('storage')
    holyoke.add_group('worker')
    holyoke.add_group('network')
    holyoke.design_center(templates,target,options.worker,options.storage,options.network)
    holyoke.show()
    
    bates.compare(holyoke)
