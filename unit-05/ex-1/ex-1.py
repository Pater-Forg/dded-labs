from scipy import integrate
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

class Thermodynamic:
    def __init__(self, name: str):
        cols = ['Compound', '$\\Delta H_f$', '$S_f$', 'A', 'B', 'C', 'D', '$T_1$', '$T_2$']
        data = pd.read_csv('unit-04/ex-3/test-tab-04.csv', usecols=cols)
        compound_data = data.loc[data['Compound'] == name]
        self.Name = name
        self.Delta_H = float(compound_data['$\\Delta H_f$'].values[0])
        self.Delta_S = float(compound_data['$S_f$'].values[0]) * 1e-3
        self.A = float(compound_data['A'].values[0])
        self.B = float(compound_data['B'].values[0])
        self.C = float(compound_data['C'].values[0])
        self.D = float(compound_data['D'].values[0])
        self.T_min = float(compound_data['$T_1$'].values[0])
        self.T_max = float(compound_data['$T_2$'].values[0])

    def heat_capacity(self, T: float) -> float:
        return 1e-3 * (self.A + self.B * 1e-3 * T + self.C * 1e5 * np.pow(T, -2) + self.D * 1e-6 * np.pow(T, 2))

    def enthalpy(self, T: float):
        return self.Delta_H + integrate.quad(self.heat_capacity, 298, T)[0]

    def entropy(self, T: float):
        return self.Delta_S + integrate.quad(lambda x: self.heat_capacity(x) / x, 298, T)[0]

    def gibbs_energy(self, T: float):
        return self.enthalpy(T) - T * self.entropy(T)

def process_reaction(T_list: np.ndarray, Delta_H_298: float, Delta_S_298: float, Delta_C_p_T: callable) -> tuple[np.ndarray, np.ndarray]:
    Delta_H_list = []
    Delta_G_list = []
    for T in T_list:
        Delta_H_T = Delta_H_298 + integrate.quad(Delta_C_p_T, 298, T)[0]
        Delta_S_T = Delta_S_298 + integrate.quad(lambda x: Delta_C_p_T(x) / x, 298, T)[0]
        Delta_G_T = Delta_H_T - T * Delta_S_T
        Delta_H_list.append(Delta_H_T)
        Delta_G_list.append(Delta_G_T)
    return np.array(Delta_H_list), np.array(Delta_G_list)

def hydrogen_combustion_reaction(T_list: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    # 2H2 + O2 = 2H2O
    hydrogen = Thermodynamic('Hydrogen')
    oxygen = Thermodynamic('Oxygen')
    water = Thermodynamic('Water')
    Delta_H_298 = 2 * water.Delta_H - 2 * hydrogen.Delta_H - oxygen.Delta_H     
    Delta_S_298 = 2 * water.Delta_S - 2 * hydrogen.Delta_S - oxygen.Delta_S
    Delta_C_p_T = lambda T: 2 * water.heat_capacity(T) - 2 * hydrogen.heat_capacity(T) - oxygen.heat_capacity(T)
    return process_reaction(T_list, Delta_H_298, Delta_S_298, Delta_C_p_T)

def carbon_monoxide_combustion_reaction(T_list: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    # 2CO + O2 = 2CO2
    carbon_monoxide = Thermodynamic('Carbon Monoxide')
    oxygen = Thermodynamic('Oxygen')
    carbon_dioxide = Thermodynamic('Carbon Dioxide')
    Delta_H_298 = 2 * carbon_dioxide.Delta_H - 2 * carbon_monoxide.Delta_H - oxygen.Delta_H
    Delta_S_298 = 2 * carbon_dioxide.Delta_S - 2 * carbon_monoxide.Delta_S - oxygen.Delta_S
    Delta_C_p_T = lambda T: 2 * carbon_dioxide.heat_capacity(T) - 2 * carbon_monoxide.heat_capacity(T) - oxygen.heat_capacity(T)
    return process_reaction(T_list, Delta_H_298, Delta_S_298, Delta_C_p_T)

def main():
    N = 10
    T_min = 300
    T_max = 700
    T_list = np.linspace(T_min, T_max, N)

    hydrogen_Delta_H, hydrogen_Delta_G = hydrogen_combustion_reaction(T_list)
    carbon_monoxide_Delta_H, carbon_monoxide_Delta_G = carbon_monoxide_combustion_reaction(T_list)
    
    hydrogen_ECE = hydrogen_Delta_G / hydrogen_Delta_H * 100
    carbon_monoxide_ECE = carbon_monoxide_Delta_G / carbon_monoxide_Delta_H * 100

    fig1, (ax_Delta_H, ax_Delta_G) = plt.subplots(1, 2)
    fig1.set_figheight(4)
    fig1.set_figwidth(8)

    ax_Delta_H.plot(T_list, hydrogen_Delta_H, label='H2')
    ax_Delta_H.plot(T_list, carbon_monoxide_Delta_H, label='CO')
    ax_Delta_H.set_title('dH [kJ/mol]')
    ax_Delta_H.set_xlabel('T, K')
    ax_Delta_H.legend()

    ax_Delta_G.plot(T_list, hydrogen_Delta_G, label='H2')
    ax_Delta_G.plot(T_list, carbon_monoxide_Delta_G, label='CO')
    ax_Delta_G.set_title('dG [kJ/mol]')
    ax_Delta_G.set_xlabel('T, K')
    ax_Delta_G.legend()

    fig1.savefig('unit-05/ex-1/dH_dG.png')

    T_max = 1100
    T_list = np.linspace(T_min, T_max, N)
    
    plt.figure()
    plt.plot(T_list, hydrogen_ECE, label='H2')
    plt.plot(T_list, carbon_monoxide_ECE, label='CO')
    plt.title('Идеальный КПД, %')
    plt.xlabel('T, K')
    plt.legend()

    plt.savefig('unit-05/ex-1/ECE.png')

    print('Готово!')

if __name__ == "__main__":
    main()