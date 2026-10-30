import numpy as np

class DBSController:
    def __init__(self, pulse_frequency=130, pulse_amplitude=1.0, dt=0.001):
        self.dt = dt
        self.amplitude = pulse_amplitude
        self.step_interval = int((1.0 / pulse_frequency) / dt)

    def get_continuous_stim(self, t_step):
        """Continuous high-frequency stimulation pulse train."""
        return self.amplitude if (t_step % self.step_interval == 0) else 0.0

    def get_adaptive_stim(self, t_step, beta_power, threshold):
        """Adaptive stimulation: fires pulse only when beta-band power exceeds threshold."""
        if beta_power > threshold and (t_step % self.step_interval == 0):
            return self.amplitude
        return 0.0