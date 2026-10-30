import numpy as np
import matplotlib.pyplot as plt
from src.models.neural_mass import NeuralMassModel
from src.controllers.dbs_controller import DBSController

# Simulation Parameters
dt = 0.001
T = 10.0
time = np.arange(0, T, dt)
N = len(time)

model = NeuralMassModel(dt=dt)
controller = DBSController(pulse_frequency=130, dt=dt)

# Inputs and State Storage
beta_drive = 1.2 * np.sin(2 * np.pi * 20 * time)
x_cont = np.zeros(N)
x_adap = np.zeros(N)
dbs_cont = np.zeros(N)
dbs_adap = np.zeros(N)

# Simulation Loop
for t in range(1, N):
    ext_input = beta_drive[t-1] + np.random.normal(0, 0.1)
    
    # Continuous DBS
    dbs_cont[t] = controller.get_continuous_stim(t)
    x_cont[t], _ = model.step(x_cont[t-1], 0.0, ext_input, dbs_cont[t-1])
    
    # Adaptive DBS
    window = x_adap[max(0, t-100):t]
    beta_power = np.std(window) if len(window) > 10 else 0
    dbs_adap[t] = controller.get_adaptive_stim(t, beta_power, threshold=0.3)
    x_adap[t], _ = model.step(x_adap[t-1], 0.0, ext_input, dbs_adap[t-1])

# Calculate Energy Reduction
e_cont = np.sum(dbs_cont**2) * dt
e_adap = np.sum(dbs_adap**2) * dt
reduction = (1 - e_adap / e_cont) * 100

print(f"Continuous DBS Energy: {e_cont:.3f}")
print(f"Adaptive DBS Energy:   {e_adap:.3f}")
print(f"Energy Reduction:      {reduction:.2f}%")

# Plotting the results
plt.figure(figsize=(12, 8))

plt.subplot(3, 1, 1)
plt.plot(time, beta_drive, color='gray', linestyle='--', label='Pathological Beta Drive')
plt.plot(time, x_cont, color='red', label='Continuous DBS STN Firing')
plt.ylabel('Activity')
plt.legend(loc='upper right')
plt.title(f'Adaptive DBS Energy Simulation (Energy Saved: {reduction:.1f}%)')

plt.subplot(3, 1, 2)
plt.plot(time, x_adap, color='blue', label='Adaptive DBS STN Firing')
plt.ylabel('Activity')
plt.legend(loc='upper right')

plt.subplot(3, 1, 3)
plt.plot(time, dbs_cont, color='salmon', label='Continuous Pulses', alpha=0.6)
plt.plot(time, dbs_adap, color='dodgerblue', label='Adaptive Pulses', alpha=0.8)
plt.xlabel('Time (s)')
plt.ylabel('Stimulation')
plt.legend(loc='upper right')

plt.tight_layout()
plt.savefig('figures/dbs_comparison.png', dpi=300)
plt.show()