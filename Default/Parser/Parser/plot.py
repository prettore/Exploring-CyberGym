import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(0, 10, 100)
y1 = np.sin(x)
y2 = np.cos(x)

plt.figure(figsize=(10, 4)) # Create a figure

plt.subplot(1, 2, 1) # Create the first subplot (1 row, 2 columns, position 1)
plt.plot(x, y1)
plt.title("Sine Wave")

#plt.subplot(1, 2, 2) # Create the second subplot (1 row, 2 columns, position 2)
#plt.plot(x, y2, color='orange')
#plt.title("Cosine Wave")

plt.tight_layout() # Adjust subplot parameters for a tight layout
plt.show()
