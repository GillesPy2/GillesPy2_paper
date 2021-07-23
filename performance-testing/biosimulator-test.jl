#! /usr/bin/julia

module main

include("biosimulator_models.jl")

using BioSimulator
using ProgressBars
using PyCall
@pyimport pickle
@pyimport numpy
using Pandas
using .BioSimulatorModels

function mypickle(filename, obj)
    out = open(filename,"w")
    pickle.dump(obj, out)
    close(out)
 end

order = parse(Int, ARGS[1])
realizations = parse(Int, ARGS[2])
trajectories = [2^i for i = 0:order-1]

dump = simulate(VO_Model, Direct(), tfinal = 100.0)
models = [VO_Model, MM_Model, D_Model]
m_names = ["VilarOscillator", "Michaelis_Menten", "Dimerization"]

s = "BioSimulator.jl"
times = Dict([m=>[] for m in m_names])
times["Solver"] = [s for i in 1:length(trajectories)]
times["trajectories"] = trajectories
tspans = [LinRange(0, 200, 201), LinRange(0, 100, 101), LinRange(0, 100, 101)]
tfins = [200, 100, 100]

for (i, m) in enumerate(models)
	println("Biosimulator.jl - ", m_names[i])
	for n_traj in tqdm(trajectories)
        all_times = numpy.zeros(realizations)
        for j in 1:realizations
            stime = time()
            ensemble = [simulate(m, Direct(), tfinal = tfins[i], save_points = tspans[i]) for j = 1:n_traj]
            etime = time()
            elapsed = etime - stime
            all_times[j] = elapsed
            end
		append!(times[m_names[i]], numpy.average(all_times))
	end
end


df = DataFrame(times, index=[times["Solver"], times["trajectories"]], columns=[m for m in m_names])

println()
print(df)
mypickle("/home/smatthe2/performance-testing/bsjl-times.p", df)

print("\n")

end
