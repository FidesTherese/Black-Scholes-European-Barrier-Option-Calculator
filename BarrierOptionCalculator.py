import numpy as np
from scipy.stats import norm

# Define class
class BarrierOption:
    # Define endogenous parameters
    def __init__(self, spot, strike, barrier, maturity, rate, volatility, dividend):
        self.S = spot
        self.E = strike
        self.B = barrier
        self.T = maturity / 365 # Annualize
        self.r = rate
        self.sigma = volatility
        self.q = dividend # Dividend yield or foreign exchange interest. Usually, this variable will be set as zero
        # Define exogenous parameters
        self.a = (self.B/self.S)**(-1+(2*(self.r-self.q))/(self.sigma**2))
        self.b = (self.B/self.S)**(1+(2*(self.r-self.q))/(self.sigma**2))
        self.d1 = (np.log(self.S/self.E) + (self.r - self.q + 0.5*self.sigma**2) * self.T) / (self.sigma*np.sqrt(self.T))
        self.d2 = (np.log(self.S/self.E) + (self.r - self.q - 0.5*self.sigma**2) * self.T) / (self.sigma*np.sqrt(self.T))
        self.d3 = (np.log(self.S/self.B) + (self.r - self.q + 0.5*self.sigma**2) * self.T) / (self.sigma*np.sqrt(self.T))
        self.d4 = (np.log(self.S/self.B) + (self.r - self.q - 0.5*self.sigma**2) * self.T) / (self.sigma*np.sqrt(self.T))
        self.d5 = (np.log(self.S/self.B) - (self.r - self.q - 0.5*self.sigma**2) * self.T) / (self.sigma*np.sqrt(self.T))
        self.d6 = (np.log(self.S/self.B) - (self.r - self.q + 0.5*self.sigma**2) * self.T) / (self.sigma*np.sqrt(self.T))
        self.d7 = (np.log((self.S*self.E)/self.B**2) - (self.r - self.q - 0.5*self.sigma**2) * self.T) / (self.sigma*np.sqrt(self.T))
        self.d8 = (np.log((self.S*self.E)/self.B**2) - (self.r - self.q + 0.5*self.sigma**2) * self.T) / (self.sigma*np.sqrt(self.T))

    def up_and_out_call(self):
        if self.S >= self.B:
            return 0.0 # Knock out immediately
        else:
            term1 = self.S*np.exp(-self.q*self.T)*(norm.cdf(self.d1)-norm.cdf(self.d3)-self.b*(norm.cdf(self.d6)-norm.cdf(self.d8)))
            term2 = self.E*np.exp(-self.r*self.T)*(norm.cdf(self.d2)-norm.cdf(self.d4)-self.a*(norm.cdf(self.d5)-norm.cdf(self.d7)))
            V_uaoc = term1 - term2
            return V_uaoc

    def up_and_in_call(self, knock_in: bool):
        if knocked_in: # Knock-in immediately, and barrier option becomes vanilla call option
            d1 = (np.log(self.S/self.E) + (self.r - self.q + 0.5 * (self.sigma**2)) * self.T) / (self.sigma * np.sqrt(self.T))
            d2 = d1 - self.sigma*(np.sqrt(self.T))
            V_vc = self.S * np.exp(-self.q * self.T) * norm.cdf(d1) - self.E * np.exp(-self.r * self.T) * norm.cdf(d2)
            return V_vc
        else:
            term1 = self.S * np.exp(-self.q * self.T) * (norm.cdf(self.d3) + self.b * (norm.cdf(self.d6) - norm.cdf(self.d8)))
            term2 = self.E * np.exp(-self.r * self.T) * (norm.cdf(self.d4) + self.a * (norm.cdf(self.d5) - norm.cdf(self.d7)))
            V_uaic = term1 - term2
            return V_uaic

    def down_and_out_call(self):
        if self.S <= self.B:
            return 0.0 # Knock out immediately
        elif self.S > self.B and self.E > self.B:
            term1 = self.S * np.exp(-self.q * self.T) * (norm.cdf(self.d1) - self.b * (1 - norm.cdf(self.d8)))
            term2 = self.E * np.exp(-self.r * self.T) * (norm.cdf(self.d2) - self.a * (1 - norm.cdf(self.d7)))
            V_daoc = term1 - term2
            return V_daoc
        elif self.S > self.B and self.E <= self.B:
            term1 = self.S * np.exp(-self.q * self.T) * (norm.cdf(self.d3) - self.b * (1 - norm.cdf(self.d6)))
            term2 = self.E * np.exp(-self.r * self.T) * (norm.cdf(self.d4) - self.a * (1 - norm.cdf(self.d5)))
            V_daoc = term1 - term2
            return V_daoc

    def down_and_in_call(self, knock_in: bool):
        if knocked_in: # Knock-in immediately, and barrier option becomes vanilla call option
            d1 = (np.log(self.S/self.E) + (self.r - self.q + 0.5 * (self.sigma**2)) * self.T) / (self.sigma * np.sqrt(self.T))
            d2 = d1 - self.sigma*(np.sqrt(self.T))
            V_vc = self.S * np.exp(-self.q * self.T) * norm.cdf(d1) - self.E * np.exp(-self.r * self.T) * norm.cdf(d2)
            return V_vc
        else:
            if self.S > self.B and self.E > self.B:
                term1 = self.S * np.exp(-self.q * self.T) * self.b * (1 - norm.cdf(self.d8))
                term2 = self.E * np.exp(-self.r * self.T) * self.a * (1 - norm.cdf(self.d7))
                V_daic = term1 - term2
                return V_daic
            elif self.S > self.B and self.E <= self.B:
                term1 = self.S * np.exp(-self.q * self.T) * (norm.cdf(self.d1) - norm.cdf(self.d3) + self.b * (1 - norm.cdf(self.d6)))
                term2 = self.E * np.exp(-self.r * self.T) * (norm.cdf(self.d2) - norm.cdf(self.d4) + self.a * (1 - norm.cdf(self.d5)))
                V_daic = term1 - term2
                return V_daic

    def down_and_out_put(self):
        if self.S <= self.B:
            return 0.0 # Knock out immediately
        else:
            term1 = -self.S * np.exp(-self.q * self.T) * (norm.cdf(self.d3) - norm.cdf(self.d1) - self.b * (norm.cdf(self.d8) - norm.cdf(self.d6)))
            term2 = self.E * np.exp(-self.r * self.T) * (norm.cdf(self.d4) - norm.cdf(self.d2) - self.a * (norm.cdf(self.d7) - norm.cdf(self.d5)))
            V_daop = term1 + term2
            return V_daop

    def down_and_in_put(self, knocked_in: bool):
        if knocked_in: # Knock-in immediately, and barrier option becomes vanilla put option
            V_vp = -self.S*np.exp(-self.q * self.T)*norm.cdf(-self.d1) + self.E*np.exp(-self.r * self.T)*norm.cdf(-self.d2)
            return V_vp
        else:
            term1 = -self.S * np.exp(-self.q * self.T) * (1 - norm.cdf(self.d3) + self.b * (norm.cdf(self.d8) - norm.cdf(self.d6)))
            term2 = self.E * np.exp(-self.r * self.T) * (1 - norm.cdf(self.d4) + self.a * (norm.cdf(self.d7) - norm.cdf(self.d5)))
            V_daip = term1 + term2
            return V_daip

    def up_and_out_put(self):
        if self.S >= self.B:
            return 0.0 # Knock out immediately
        elif self.S < self.B and self.E > self.S:
            term1 = -self.S * np.exp(-self.q * self.T) * (1 - norm.cdf(self.d3) - self.b * norm.cdf(self.d6))
            term2 = self.E * np.exp(-self.r * self.T) * (1 - norm.cdf(self.d4) - self.a * norm.cdf(self.d5))
            V_uaop = term1 + term2
            return V_uaop
        elif self.S < self.B and self.E <= self.S:
            term1 = -self.S * np.exp(-self.q * self.T) * (1 - norm.cdf(self.d1) - self.b * norm.cdf(self.d8))
            term2 = self.E * np.exp(-self.r * self.T) * (1 - norm.cdf(self.d2) - self.a * norm.cdf(self.d7))
            V_uaop = term1 + term2
            return V_uaop

    def up_and_in_put(self, knocked_in: bool):
        if knocked_in:
            V_vp = -self.S * np.exp(-self.q * self.T) * norm.cdf(-self.d1) + self.E * np.exp(-self.r * self.T) * norm.cdf(-self.d2)
            return V_vp
        else:
            if self.S < self.B and self.E > self.B:
                term1 = -self.S * np.exp(-self.q * self.T) * (norm.cdf(self.d3) - norm.cdf(self.d1) + self.b * norm.cdf(self.d6))
                term2 = self.E * np.exp(-self.r * self.T) * (norm.cdf(self.d4) - norm.cdf(self.d2) + self.a * norm.cdf(self.d5))
                V_uaip = term1 + term2
                return V_uaip
            elif self.S < self.B and self.E <= self.B:
                term1 = -self.S * np.exp(-self.q * self.T) * self.b * norm.cdf(self.d8)
                term2 = self.E * np.exp(-self.r * self.T) * self.a * norm.cdf(self.d7)
                V_uaip = term1 + term2
                return V_uaip