import numpy as np
from scipy.stats import norm

def black_scholes_call(S, K, r, T, sigma):

    d1 = ( np.log(S/K) + (r + sigma**2/2)*T ) / (sigma * np.sqrt(T))
    d2 = d1 - sigma*np.sqrt(T)   
    
    C = S * norm.cdf(d1) - K * np.exp(-r*T) * norm.cdf(d2)
    delta = norm.cdf(d1)
    theta = -(S * norm.pdf(d1) * sigma) / (2 * np.sqrt(T)) - r * K * np.exp(-r*T) * norm.cdf(d2)
    theta = theta / 250
    return C, delta, theta

if __name__ == "__main__":
    price, delta, theta = black_scholes_call(S=600, K=620, r=0.05, T=0.25, sigma=0.2)
    print(f"price={price}, delta={delta}, theta={theta}")