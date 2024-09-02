import m5
from m5.objects import *
import os

system = System()

system.clk_domain = SrcClockDomain()
system.clk_domain.clock = "1GHz"  
system.clk_domain.voltage_domain = VoltageDomain()

system.cpu_clk_domain = SrcClockDomain()
system.cpu_clk_domain.clock = "3200MHz"
system.cpu_clk_domain.voltage_domain = VoltageDomain()

system.mem_mode = "atomic"
system.mem_ranges = [AddrRange("512MB")]  

system.cpu = AtomicSimpleCPU()
system.cpu.clk_domain = system.cpu_clk_domain  

system.membus = SystemXBar()

system.cpu.icache_port = system.membus.cpu_side_ports
system.cpu.dcache_port = system.membus.cpu_side_ports

system.cpu.createInterruptController()

system.cpu.interrupts[0].pio = system.membus.mem_side_ports
system.cpu.interrupts[0].int_requestor = system.membus.cpu_side_ports
system.cpu.interrupts[0].int_responder = system.membus.mem_side_ports

system.mem_ctrl = MemCtrl()
system.mem_ctrl.dram = HBM_1000_4H_1x64()
system.mem_ctrl.dram.range = system.mem_ranges[0]
system.mem_ctrl.port = system.membus.mem_side_ports

system.system_port = system.membus.cpu_side_ports

thispath = os.path.dirname(os.path.realpath(__file__))
binary = os.path.join("/home/prateek/Desktop/IITD-Projects/gem5/configs/my_scripts/mm")

system.workload = SEWorkload.init_compatible(binary)

process = Process()
process.cmd = [binary]
system.cpu.workload = process
system.cpu.createThreads()

root = Root(full_system=False, system=system)
m5.instantiate()

print(f"Beginning simulation!")
exit_event = m5.simulate()
print(f"Exiting @ tick {m5.curTick()} because {exit_event.getCause()}")
