import torch
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Create a 3D tensor with dimensions 3 (width) x 3 (height) x 12 (depth) filled with the value 10
cube = torch.full((3, 3, 11), 10.0, dtype=torch.float)

# Apply the linear inflation algorithm
n_slices = cube.shape[2]
center_idx = n_slices // 2
max_weight = 1.0

if n_slices % 2 == 0:
    weights_left = [max_weight - max_weight * abs(i - center_idx + 1) / center_idx for i in range(center_idx)]
    weights_right = list(reversed(weights_left))
    weights = weights_left + weights_right
else:
    weights = [max_weight - max_weight * abs(i - center_idx) / center_idx for i in range(n_slices)]

for i, weight in enumerate(weights):
    cube[:, :, i] *= weight

# Visualize the cube
fig = plt.figure()
ax = fig.add_subplot(111, projection="3d")

x, y, z = torch.meshgrid(torch.arange(cube.shape[0]), torch.arange(cube.shape[1]), torch.arange(cube.shape[2]))
x, y, z = x.numpy().flatten(), y.numpy().flatten(), z.numpy().flatten()
c = cube.numpy().flatten()

scatter = ax.scatter(x, y, z, c=c, cmap="viridis", marker="o", s=100)
ax.set_xlabel("Width")
ax.set_ylabel("Height")
ax.set_zlabel("Depth")

# Display the value of each point
for i in range(len(x)):
    ax.text(x[i], y[i], z[i], f"{c[i]:.1f}", fontsize=8)

plt.show()