#! /usr/bin/julia

module BioSimulatorModels
using BioSimulator

export MM_Model, D_Model, VO_Model

# initialize
MM_Model = Network("Michaelis_Menten")

# species definitions; add components with <=
MM_Model <= Species("A", 301)
MM_Model <= Species("B", 120)
MM_Model <= Species("C", 0)
MM_Model <= Species("D", 0)

# reaction definitions
MM_Model <= Reaction("r1", 0.0017, "A + B --> C")
MM_Model <= Reaction("r2", 0.5, "C --> A + B")
MM_Model <= Reaction("r3", 0.1, "C --> B + D")

D_Model = Network("Dimerization")

# species definitions; add components with <=
D_Model <= Species("monomer", 30)
D_Model <= Species("dimer", 0)

# reaction definitions
D_Model <= Reaction("creation", 0.005, "monomer + monomer --> dimer")
D_Model <= Reaction("dissociation", 0.08, "dimer --> monomer + monomer")

# initialize
VO_Model = Network("VilarOscillator")

# species definitions; add components with <=
VO_Model <= Species("Da", 1)
VO_Model <= Species("Da_prime", 0)
VO_Model <= Species("Ma", 0)
VO_Model <= Species("Dr", 1)
VO_Model <= Species("Dr_prime", 0)
VO_Model <= Species("Mr", 0)
VO_Model <= Species("C", 10)
VO_Model <= Species("A", 10)
VO_Model <= Species("R", 10)

# reaction definitions
VO_Model <= Reaction("s_Da", 50.0, "Da_prime --> Da")
VO_Model <= Reaction("s_Da_prime", 100.0, "Da + A --> Da_prime")
VO_Model <= Reaction("s_Dr", 100.0, "Dr_prime --> Dr")
VO_Model <= Reaction("s_Dr_prime", 1.0, "Dr + A --> Dr_prime")
VO_Model <= Reaction("s_Ma1", 500.0, "Da_prime --> Da_prime + Ma")
VO_Model <= Reaction("s_Ma2", 50.0, "Da --> Da + Ma")
VO_Model <= Reaction("a_Ma", 10.0, "Ma --> 0")
VO_Model <= Reaction("s_A1", 50.0, "Ma --> A + Ma")
VO_Model <= Reaction("s_A2", 50.0, "Da_prime --> Da_prime + A")
VO_Model <= Reaction("s_A3", 50.0, "Dr_prime --> Dr_prime + A")
VO_Model <= Reaction("a_A", 2.0, "A --> 0")
VO_Model <= Reaction("s_C", 2.0, "A + R --> C")
VO_Model <= Reaction("s_Mr1", 50.0, "Dr_prime --> Dr_prime + Mr")
VO_Model <= Reaction("s_Mr2", 0.01, "Dr --> Dr + Mr")
VO_Model <= Reaction("a_Mr", 0.5, "Mr --> 0")
VO_Model <= Reaction("s_R1", 5.0, "Mr --> Mr + R")
VO_Model <= Reaction("a_R", 0.2, "R --> 0")
VO_Model <= Reaction("s_R2", 1.0, "C --> R")

end
