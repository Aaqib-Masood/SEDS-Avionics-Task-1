# Importing Pandas to read the cvs file, numpy to process the data, and matplotlib to plot and animate the graph
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

#=====================================
# Loading and processing the cvs file
#=====================================

# Loading and reading the cvs file
df = pd.read_csv("Depth Data.csv")

# Extracts the Point column from the cvs file and stores it as a Numpy array.
time = df["Point"].to_numpy()

# Extracts the Depth (m) column from the cvs file and converts it to numeric values, coercing any errors to NaN. Then, it converts the resulting Series to a Numpy array of type float.
depth = pd.to_numeric(df["Depth (m)"], errors="coerce").to_numpy(dtype=float)

#==================================================================
# Cleaning corrupted sensor data and interpolating suitable values
#==================================================================

# Using a rolling median to smooth out corrupted data and noise.

# For rolling median, we create a Pandas Series from the depth array.
depth_series = pd.Series(depth)

# Taking a given point as a center and taking median of a "window" of points centered around it. Only considering the median as valid if a minimum of 1 valus is valid
rolling_median = depth_series.rolling(
    window = 5,
    center = True,
    min_periods = 1
).median()

difference = abs(depth_series - rolling_median)

# Taking a median of the absolute difference (mad)
mad = difference.rolling(
    window = 5,
    center = True,
    min_periods = 1
).median()

# Avoiding division by zero
mad = mad.replace(0, np.nan)

# Marking outliers and data which could not be converted to numbers as bad data
outlier_threshold = 7
outliers = difference > (outlier_threshold * mad)

invalid = depth_series.isna()

# Combining the two data sets, while replacing all NaN with False in outliers dataset
bad_data = invalid + outliers.fillna(False)

# Replacing the bad data with NaN
clean_data = depth_series.copy()
clean_data[bad_data] = np.nan

# Replacing all NaNs with a suitable approximate value

# Interpolate estimates a suitable value of a bad reading from surrounding values
clean_data = clean_data.interpolate(
    method="linear",
    limit_direction="both"
)

#==================================================================
# Taking a rolling mean to smooth out the curve and reduce noise
#==================================================================

smooth_window = 5

smoothed_data = clean_data.rolling(
    window=smooth_window,
    center=True,
    min_periods=1
).mean()

#=====================
#Setting up the graph
#=====================

fig, ax = plt.subplots(figsize = (10, 5))
ax.set_title("Ship Depth Sensor",
             fontsize = 16,
             fontweight = "bold")

ax.set_ylabel("Time(sec)", fontsize = 12)
ax.set_xlabel("Depth (m)", fontsize = 12)

ax.grid(True, alpha=0.3)

# Setting the time limit from start to finish
ax.set_xlim(time[0], time[-1])

# Defining a safe depth for the ship to be in
safe_depth = -150

# Setting the space around the depth values
min_depth = min(clean_data.min(), safe_depth)
max_depth = max(clean_data.max(), safe_depth)

padding = (max_depth - min_depth) * 0.10

ax.set_ylim(
    min_depth - padding,
    max_depth + padding
)

# Plotting both the raw data and the smooth data for comparision
raw_line, = ax.plot(
    [],
    [],
    linestyle=":",
    linewidth=1,
    alpha=0.35,
    label="Raw sensor data"
)
smooth_line, = ax.plot(
    [],
    [],
    linewidth=2.5,
    label="Smoothed depth"
)

# Safety threshold
ax.axhline(
    safe_depth,
    linestyle="--",
    linewidth=2,
    label=f"Safety threshold ({safe_depth} m)"
)

# Text showing current depth and warning text
current_text = ax.text(
    0.02,
    0.95,
    "",
    transform=ax.transAxes,
    fontsize=12,
    verticalalignment="top"
)
warning_text = ax.text(
    0.5,
    0.05,
    "",
    transform=ax.transAxes,
    horizontalalignment="center",
    fontsize=14,
    fontweight="bold"
)
ax.legend(loc="upper right")

# ============================================================
# Animating the graph
# ============================================================

# Taking frames from the beginning starting from 0
def update(frame):
    current_time = time[:frame + 1]
    
    current_raw = depth[:frame + 1]
    
    current_smooth = smoothed_data.iloc[:frame + 1]

    # Update raw data line
    raw_line.set_data(
        current_time,
        current_raw
        )
    
        # Update smoothed line
    smooth_line.set_data(
        current_time,
        current_smooth
        )
    
        # Current smoothed depth
    current_depth = current_smooth.iloc[-1]
    
        # Display current depth
    current_text.set_text(
        f"Time: {time[frame]} s\n"
        f"Depth: {current_depth:.2f} m"
        )

    if current_depth > safe_depth:
    
        warning_text.set_text(
            "Warning : Shallow water - Intervention required"
    )
    
    else:
    
        warning_text.set_text("")
    
    return (
        raw_line,
        smooth_line,
        current_text,
        warning_text
    )

# Starting the animation
animation = FuncAnimation(
    fig,
    update,
    frames=len(time),
    interval=10,       # 1000 ms = 1 second
    blit=False,
    repeat=False
)

plt.tight_layout()

plt.show()