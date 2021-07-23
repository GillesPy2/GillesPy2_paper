#! /usr/local/bin/julia

module main

include("biosimulator_models.jl")

using PyCall
using BioSimulator
using ProgressBars
using Pandas
using .BioSimulatorModels

@pyimport pickle
@pyimport numpy

function mypickle(filename, obj)
    out = open(filename,"w")
    pickle.dump(obj, out)
    close(out)
 end

function getformulapart(p, o)
    if length(p) > 0
	part = []
    	for (s, r) in p
	    part = vcat(part, [string(s, "_", o) for rt = 0: r-1])
    	end
    	return join(part, " + ")
    else
	return "0"
    end
 end

function getformula(r, o)
    reactants = getformulapart(r.reactants, o)
    products = getformulapart(r.products, o)
    formula = join([reactants, products], " --> ")
    return formula
 end

function getsystemsize(m)
    size = length(m.species_list) + length(m.reaction_list)
    return size
 end

order = parse(Int, ARGS[1])
realizations = parse(Int, ARGS[2])

dump = simulate(VO_Model, Direct(), tfinal = 100.0)
models = [VO_Model, MM_Model, D_Model]
m_names = ["VilarOscillator", "Michaelis_Menten", "Dimerization"]

system_sizes = [string([getsystemsize(m) * 2^i for m in models]) for i = 0: order-1]

s = "BioSimulator.jl"
times = Dict([m=>[] for m in m_names])
times["Solver"] = [s for i in 1:length(system_sizes)]
times["system_sizes"] = system_sizes
println(system_sizes)
tspans = [LinRange(0, 200, 201), LinRange(0, 100, 101), LinRange(0, 100, 101)]
tfins = [200, 100, 100]

for (i, m) in enumerate(models)
    println(string(s, " - ", m_names[i]))
    for o in tqdm([o for o=0:order-1])
    	if o > 0
	    n_s = [Species(string(n, "_", o), s.population) for (n, s) in m.species_list]
	    [m <= s for s in n_s]
	    n_r = [Reaction(string(n, "_", o), r.rate, getformula(r, o)) for (n, r) in m.reaction_list]
	    [m <= r for r in n_r]
	end
        all_times = numpy.zeros(realizations)
        for j in 1:realizations
            stime = time()
            result = simulate(m, Direct(), tfinal = tfins[i], save_points = tspans[i])
	    etime = time()
            elapsed = etime - stime
            all_times[j] = elapsed
        end
	append!(times[m_names[i]], numpy.average(all_times))
    end
end

df = DataFrame(times, index=[times["Solver"], times["system_sizes"]], columns=[m for m in m_names])

println()
print(df)
mypickle("/home/brumsey/system-testing/bsjl-times.p", df)

print("\n")

end
