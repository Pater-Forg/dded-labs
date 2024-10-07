from scipy import integrate
import numpy as np
import matplotlib.pyplot as plt

def model(V: float,
         rho: float,
         k_B: float,
         T: np.array,
         theta_D: float):
    const = 9 * V * rho * k_B / np.pow(theta_D, 3)
    integral_func = lambda x: np.pow(x, 4) * np.exp(x) / np.pow(np.exp(x) - 1, 2)
    model_func = lambda T_i: const * np.pow(T_i, 3) * integrate.quad(integral_func, 1e-10, theta_D / T_i)[0]
    return [model_func(T_i) for T_i in T]

def save_plot(T, C_V):
    plt.figure()
    plt.grid()
    plt.plot(T, C_V)
    plt.xlabel('T, K')
    plt.ylabel('C_V, J/mol/K')
    plt.title('Теплоемкость алюминия от температуры')
    plt.savefig('unit-04/ex-2/plot.png')
    
def main():
    V = 1
    rho = 6.022e23
    theta_D = 428
    k_B = 1.3806e-23
    T_min = 2
    T_max = 500
    N = 20
    T = np.linspace(T_min, T_max, N)
    C_V = model(V, rho, k_B, T, theta_D)
    save_plot(T, C_V)
    print("Готово!")

if __name__ == "__main__":
    main()
