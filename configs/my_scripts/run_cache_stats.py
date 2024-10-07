import m5
import os
from m5.objects import *
from caches import *

system = System()

system.clk_domain = SrcClockDomain()
system.clk_domain.clock = "1GHz"
system.clk_domain.voltage_domain = VoltageDomain()

system.cpu_clk_domain = SrcClockDomain()
system.cpu_clk_domain.clock = "1600MHz"
system.cpu_clk_domain.voltage_domain = VoltageDomain()

system.mem_mode = "atomic"
system.mem_ranges = [AddrRange("8192MB")]  

system.cpu = AtomicSimpleCPU()
system.cpu.clk_domain = system.cpu_clk_domain 

system.cpu.icache = L1ICache()
system.cpu.dcache = L1DCache()

system.cpu.icache.connectCPU(system.cpu)
system.cpu.dcache.connectCPU(system.cpu)

system.l2bus = L2XBar()

system.cpu.icache.connectBus(system.l2bus)
system.cpu.dcache.connectBus(system.l2bus)

system.l2cache = L2Cache()
system.l2cache.connectCPUSideBus(system.l2bus)

system.cpu.branchPred = TAGE()

system.membus = SystemXBar()

system.l2cache.connectMemSideBus(system.membus)

system.cpu.createInterruptController()
system.cpu.interrupts[0].pio = system.membus.mem_side_ports
system.cpu.interrupts[0].int_requestor = system.membus.cpu_side_ports
system.cpu.interrupts[0].int_responder = system.membus.mem_side_ports

system.mem_ctrl = MemCtrl()
system.mem_ctrl.dram = DDR3_1600_8x8()
system.mem_ctrl.dram.range = system.mem_ranges[0]
system.mem_ctrl.port = system.membus.mem_side_ports

system.system_port = system.membus.cpu_side_ports

thispath = os.path.dirname(os.path.realpath(__file__))
binary = os.path.join("/home/prateek/Desktop/IITD-Projects/gem5/configs/my_scripts/ijk")

system.workload = SEWorkload.init_compatible(binary)

process = Process()
process.cmd = [binary]
system.cpu.workload = process
system.cpu.createThreads()

root = Root(full_system=False, system=system)
m5.instantiate()

print(f"Beginning simulation!")
exit_event = m5.simulate()

m5.stats.dump()
m5.stats.reset()

print(f"Exiting @ tick {m5.curTick()} because {exit_event.getCause()}")