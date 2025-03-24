import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from scipy.fftpack import fft, fftfreq


# Define the true sinusoidal function
def true_sinusoidal(x, A, B, C, D):
    return A * np.sin(B * x + C) + D


# Generate synthetic data
np.random.seed(42)
x_data = np.linspace(0, 10, 100)  # X values
A_true, B_true, C_true, D_true = 5, 2 * np.pi / 3, 0.5, 3  # True parameters
y_data = true_sinusoidal(x_data, A_true, B_true, C_true, D_true) + np.random.normal(
    0.0, 1, len(x_data)
)
print(type(x_data))

# **Step 1: Estimate Frequency Using FFT**
N = len(x_data)
T = x_data[1] - x_data[0]  # Sampling interval
fft_y = fft(y_data - np.mean(y_data))  # Remove DC component
freqs = fftfreq(N, T)[: N // 2]  # Only take positive frequencies
fft_magnitudes = np.abs(fft_y[: N // 2])  # Get magnitudes

# Find dominant frequency (avoid 0 Hz)
peak_freq = freqs[np.argmax(fft_magnitudes[1:]) + 1]
B_est = 2 * np.pi * peak_freq  # Convert to angular frequency

# **Step 2: Estimate Amplitude, Phase, and Offset**
A_est = (max(y_data) - min(y_data)) / 2
D_est = np.mean(y_data)
C_est = 0  # Can be adjusted manually


# **Step 3: Use Curve Fitting with Better Initial Guess**
def fit_sinusoidal(x, A, B, C, D):
    return A * np.sin(B * x + C) + D


initial_guess = [A_est, B_est, C_est, D_est]
params, covariance = curve_fit(
    fit_sinusoidal, x_data, y_data, p0=initial_guess, maxfev=5000
)

# Extract estimated parameters
A_fit, B_fit, C_fit, D_fit = params
print(
    f"Estimated Parameters:\n A = {A_fit:.3f}, B = {B_fit:.3f}, C = {C_fit:.3f}, D = {D_fit:.3f}"
)

# **Step 4: Plot Results**
plt.figure(figsize=(8, 5))
plt.scatter(x_data, y_data, label="Noisy Data", color="red", s=10)
plt.plot(
    x_data,
    true_sinusoidal(x_data, A_true, B_true, C_true, D_true),
    label="True Function",
    linestyle="dashed",
    color="black",
)
plt.plot(
    x_data,
    fit_sinusoidal(x_data, A_fit, B_fit, C_fit, D_fit),
    label="Fitted Function",
    color="blue",
)

plt.legend()
plt.xlabel("x")
plt.ylabel("y")
plt.title("Improved Sinusoidal Function Fitting")
plt.show()
