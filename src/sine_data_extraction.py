import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from scipy.fftpack import fft, fftfreq
import csv


def fit_sinusoidal(x, A, B, C, D):
    return A * np.sin(B * x + C) + D


def generate_parameters_from_sine(x_data, y_data):
    """Fits a sine curve to the data.

    Args:
        x_data (List): _description_
        y_data (List): _description_

    Returns:
        List: [Amplitude, Horizontal stretch, Horizontal Shift, Vertical Shift]
    """

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

    initial_guess = [A_est, B_est, C_est, D_est]
    sine_curve_params, covariance = curve_fit(
        fit_sinusoidal, x_data, y_data, p0=initial_guess, maxfev=5000
    )

    # Extract estimated parameters
    A_fit, B_fit, C_fit, D_fit = sine_curve_params
    print(
        f"Estimated Parameters:\n A = {A_fit:.3f}, B = {B_fit:.3f}, C = {C_fit:.3f}, D = {D_fit:.3f}"
    )
    return sine_curve_params


def plot_sine_estimation(x_data, y_data, sine_curve_params):
    """
    Plots the data, and the estimation of parameters of the data.

    Args:
        x_data (List): Independant variable
        y_data (List): Dependant variable
        sine_curve_params (List): [Amplitude, Horizontal stretch, Horizontal Shift, Vertical Shift]
    """

    [A_fit, B_fit, C_fit, D_fit] = sine_curve_params
    plt.figure(figsize=(8, 5))
    plt.scatter(x_data, y_data, label="Noisy Data", color="red", s=10)

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


if __name__ == "__main__":
    columns_to_extract = ["Time", "HipTor_L"]
    with open("data/Collin_treadwalk_2_AntData_2025_03_06_15_41.csv", "r") as file:
        reader = csv.DictReader(file)

        # generate_parameters_from_sine(x_data, y_data)
