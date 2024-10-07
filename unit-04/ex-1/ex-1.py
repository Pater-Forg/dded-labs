from scipy import integrate
import numpy as np    

def integral_1():
    func = lambda x: 1.0 / (x * np.sqrt(1 + np.log(x)))
    a = 1
    b = np.exp(3)
    true_val = 2.0
    result, _ = integrate.quad(func, a, b)
    error = np.abs(result - true_val)
    print(f"==========\n1. Result = {result}, error = {error}")

def integral_2():
    func = lambda x, t: (np.exp(-x) - np.exp(-t * x)) / x
    a = 1e-10
    b = np.inf
    ts = np.linspace(1, 3, 3)
    true_vals = np.log(ts)
    results = [integrate.quad(func, a, b, args=(t,))[0] for t in ts]
    errors = np.abs(results - true_vals)
    print(f"==========\n2. Results = {results}, errors = {errors}")

def integral_3():
    func = lambda x: np.pow(x, 1 / np.pi) / x / (1 + x)
    a = 1e-10
    b = np.inf
    true_val = np.pi / np.sin(1)
    result, _ = integrate.quad(func, a, b)
    error = np.abs(result - true_val)
    print(f"==========\n3. Result = {result}, error = {error}")

def integral_4():
    func = lambda x: np.exp(-np.pow(x, 2))
    a = np.negative(np.inf)
    b = np.inf
    true_val = np.sqrt(np.pi)
    result, _ = integrate.quad(func, a, b)
    error = np.abs(result - true_val)
    print(f"==========\n4. Result = {result}, error = {error}")

def integral_5():
    func = lambda x, y: x * np.pow(y, 2)
    a1 = 0
    b1 = 2
    a2 = lambda y: 2 - y
    b2 = lambda y: np.sqrt(4 - np.pow(y, 2))
    true_val = 8 / 5
    result, _ = integrate.dblquad(func, a1, b1, a2, b2)
    error = np.abs(result - true_val)
    print(f"==========\n5. Result = {result}, error = {error}")

if __name__=="__main__":
    integral_1()
    integral_2()
    integral_3()
    integral_4()
    integral_5()