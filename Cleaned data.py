# Importing pandas to read the CSV file and matplotlib to plot the graph
import pandas as pd
import matplotlib.pyplot as plt

# Reading the csv file
df = pd.read_csv("Depth Data_cleaned.csv")

# Making the plot interactable
plt.ion()

# Setting up the size of the window and axis for the plot
fig, ax = plt.subplots(figsize=(10, 5))

# Creating an empty variable to define the depth values
depth_values = []


# Looping through the rows of the dataframe to get the depth values and plot them, but there is only one value to go through.
for _, row in df.iterrows():

    depth = row["Depth (m)"]
    depth_values.append(depth)

    # Clearing the plot every time a new vale is plotted
    ax.clear()
    ax.plot(depth_values, marker=".", color="blue")

    # Setting the labels and title of the graph
    ax.set_xlabel("Time (seconds)")
    ax.set_ylabel("Depth (m)")
    ax.set_title("Live Depth Measurement")
    ax.grid(True)

    #Giving a delay of one second between each value
    plt.pause(1)
plt.ioff()
plt.show()