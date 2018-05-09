from layout import Layout
from tools import plot_layout, plot_energies


file_paths = ['star.txt', 'square.txt', 'star++.txt', 'dog.txt']

for file_path in file_paths:
    # read the file into your layout class
    layout = Layout(file_path)
    # run the normal layout for 1000 iterations and store the total energies
    energies_normal = layout.layout(1000)
    # plot the normal layout
    plot_layout(layout, '')
    # run the simulated annealing layout for 1000 iterations and store the total energies
    energiesSA = layout.simulated_annealing_layout(1000)
    # plot the simulated annealing layout
    plot_layout(layout, '')
    # plot the total energies of the normal layout and the simulated annealing layout
    plot_energies(energies_normal, '', '')
    plot_energies(energiesSA, '', '')
