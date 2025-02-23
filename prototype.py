import matplotlib.pyplot as plt
import matplotlib.animation as animation
import serial
import numpy as np
import argparse

parser = argparse.ArgumentParser(description='Plot FFT of incoming data')
parser.add_argument('--port', type=str, default='COM3', help='Serial port')

args = parser.parse_args()

ser = serial.Serial(args.port, 128000, timeout=1)

window_size = 200  # doubled from 100
x_data = list(range(window_size))
y_data = [0] * window_size

fig, ax = plt.subplots()
line, = ax.plot([], [], label="FFT Magnitude")
# Initialize peaks_line with marker dots (or thin bars) for the peak values
peaks_line, = ax.plot([], [], 'r--', label="Peaks", linewidth=1)
ax.set_xlabel('Frequency')
ax.set_ylabel('Magnitude')
ax.legend()

# For each FFT bin, track (peak_value, hold_frames)
num_bins = window_size//2 + 1  # rfft output length
peaks_info = [(0, 0) for _ in range(num_bins)]
peak_hold_frames = 2    # Number of animation frames to hold the peak (~1 second at 50ms/frame)
decay_multiplier = 0.9   # Exponential decay factor once hold expires

def animate(frame):
    global peaks_info
    updated = False

    while ser.inWaiting() > 0:
        data_line = ser.readline().decode('utf-8').strip()
        try:
            new_value = int(data_line)
        except Exception:
            new_value = 0

        # Shift data for a sliding window effect
        y_data.pop(0)
        y_data.append(new_value)
        x_data.pop(0)
        x_data.append(x_data[-1] + 1)
        updated = True

    if updated:
        # Convert current y_data to a numpy array
        y_array = np.array(y_data)
        # Compute FFT using only positive frequencies
        fft_vals = np.fft.rfft(y_array)
        # Get the magnitude of FFT values
        fft_magnitude = np.abs(fft_vals)
        # Compute frequency bins (assuming unit sample spacing; adjust d if required)
        freq = np.fft.rfftfreq(window_size, d=1./256000)
        
        # Update main FFT line data
        line.set_data(freq, fft_magnitude)
        ax.set_xlim(freq[0], freq[-1])
        ax.set_ylim(0, 20000)

        # Update peaks_info for each frequency bin.
        new_peaks_info = []
        for idx, current in enumerate(fft_magnitude):
            old_val, hold = peaks_info[idx]
            if current > old_val:
                # New peak: update value and reset hold counter
                new_peak = current
                new_hold = peak_hold_frames
            else:
                if hold > 0:
                    # Continue holding without decaying
                    new_peak = old_val
                    new_hold = hold - 1
                else:
                    # Exponential decay
                    new_peak = old_val * decay_multiplier
                    new_hold = 0
            new_peaks_info.append((new_peak, new_hold))
        peaks_info = new_peaks_info
        # Extract the current peak values to update the peaks_line
        peaks_values = [val for val, _ in peaks_info]
        peaks_line.set_data(freq, peaks_values)

    return line, peaks_line

ani = animation.FuncAnimation(fig, animate, interval=50, cache_frame_data=False)
plt.show()