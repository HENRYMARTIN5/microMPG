import matplotlib.pyplot as plt
import matplotlib.animation as animation
import serial
import numpy as np

ser = serial.Serial('COM7', 256000, timeout=1)

window_size = 100
x_data = list(range(window_size))
y_data = [0] * window_size

fig, ax = plt.subplots()
line, = ax.plot([], [])
ax.set_xlabel('Frequency')
ax.set_ylabel('Magnitude')

def animate(frame):
    lines_read = 0
    updated = False

    while ser.inWaiting() > 0:
        data_line = ser.readline().decode('utf-8').strip()
        try:
            new_value = int(data_line)
        except Exception:
            new_value = 0
        lines_read += 1

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
        # Get the magnitude of fft values
        fft_magnitude = np.abs(fft_vals)
        # Compute frequency bins (assuming a unit sample spacing;
        # update d=1./fs if you know the actual sample rate)
        freq = np.fft.rfftfreq(window_size, d=1./256000)
        
        line.set_data(freq, fft_magnitude)
        ax.set_xlim(freq[0], freq[-1])
        ax.set_ylim(0, 1500)

    return line,

ani = animation.FuncAnimation(fig, animate, interval=50, cache_frame_data=False)
plt.show()