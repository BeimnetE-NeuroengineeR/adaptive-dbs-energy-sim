import numpy as np

class NeuralMassModel:
    def __init__(self, dt=0.001, tau_e=0.01, tau_i=0.02):
        self.dt = dt
        self.tau_e = tau_e  # Time constant for excitatory population (STN)
        self.tau_i = tau_i  # Time constant for inhibitory population (GPe)
        
        # Connectivity weights
        self.w_ee = 1.5
        self.w_ei = 2.5
        self.w_ie = 1.5
        self.w_ii = 0.0

    def activation_function(self, x):
        """Sigmoidal firing rate response function."""
        return 1.0 / (1.0 + np.exp(-x))

    def step(self, x_prev, y_prev, ext_input, dbs_current):
        """
        Perform a single forward Euler integration step.
        """
        # Excitatory population update
        net_e = self.w_ee * x_prev - self.w_ei * y_prev + ext_input - dbs_current
        dx = (-x_prev + self.activation_function(net_e)) / self.tau_e
        
        # Inhibitory population update
        net_i = self.w_ie * x_prev - self.w_ii * y_prev
        dy = (-y_prev + self.activation_function(net_i)) / self.tau_i
        
        x_next = x_prev + dx * self.dt
        y_next = y_prev + dy * self.dt
        
        return x_next, y_next