from scipy import integrate
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

class Thermodynamic:
    def __init__(self, name: str, filepath: str):
        cols = ['Compound', '$\\Delta H_f$', '$S_f$', 'A', 'B', 'C', 'D', '$T_1$', '$T_2$']
        data = pd.read_csv(filepath, usecols=cols)
        compound_data = data.loc[data['Compound'] == name]
        self.Name = name
        self.Delta_H = compound_data['$\Delta H_f$']
        self.Delta_S = compound_data['$S_f$']
        self.A = compound_data['A']
        self.B = compound_data['B']
        self.C = compound_data['C']
        self.D = compound_data['D']
        self.T_min = compound_data['$T_1$']
        self.T_max = compound_data['$T_2$']

    def heat_capacity(self, T: float) -> float:
        return self.A + self.B * 1e-3 * T + self.C * 1e5 * np.pow(T, -2) + self.D * 1e-6 * np.pow(T, 2)

    def enthalpy(self, T: float):
        return self.Delta_H + integrate.quad(self.heat_capacity, 298, T)[0]

    def entropy(self, T: float):
        return self.Delta_S + integrate.quad(lambda x: self.heat_capacity(x) / x, 298, T)[0]

    def gibbs_energy(self, T: float):
        return self.enthalpy(T) - T * self.entropy(T)

def proccess(compounds: list[Thermodynamic]):
    N = 20
    fig, (entalpy_ax, entropy_ax, gibbs_ax) = plt.subplots(1, 3)
    for compound in compounds:
        T = np.linspace(compound.T_min, compound.T_max, N)
        entalpy = [1e-3*compound.enthalpy(T_i) for T_i in T]
        entalpy_ax.plot(T, entalpy, label=compound.Name)
    for compound in compounds:
        T = np.linspace(compound.T_min, compound.T_max, N)
        entropy = [compound.entropy(T_i) for T_i in T]
        entropy_ax.plot(T, entropy, label=compound.Name)
    for compound in compounds:
        T = np.linspace(compound.T_min, compound.T_max, N)
        gibbs = [1e-3*compound.gibbs_energy(T_i) for T_i in T]
        gibbs_ax.plot(T, gibbs, label=compound.Name)

    entalpy_ax.set_title('H [kJ/mol]')
    entalpy_ax.set_xlabel('T, K')
    entalpy_ax.legend()
    entropy_ax.set_title('S [J/mol/K]')
    entropy_ax.set_xlabel('T, K')
    entropy_ax.legend()
    gibbs_ax.set_title('dG [kJ/mol]')
    gibbs_ax.set_xlabel('T, K')
    gibbs_ax.legend()
    fig.set_figheight(7)
    fig.set_figwidth(25)
    fig.savefig('unit-04/ex-3/plot.png')

def main():
    filepath = 'unit-04/ex-3/test-tab-04.csv'
    hydrogen = Thermodynamic('Hydrogen', filepath)
    oxygen = Thermodynamic('Oxygen', filepath)
    methane = Thermodynamic('Methane', filepath)
    carbon_monoxide = Thermodynamic('Carbon Monoxide', filepath)
    carbon_dioxide = Thermodynamic('Carbon Dioxide', filepath)

    proccess([
        hydrogen, oxygen, methane, carbon_monoxide, carbon_dioxide
    ])

    print('Готово!')

if __name__ == '__main__':
    main()