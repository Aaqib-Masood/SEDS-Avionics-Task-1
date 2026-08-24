# SEDS-Avionics-Task-1
There are two different codes for this task
Cleaned data is a practice code for me to learn plotting data with Matplotlib. It uses Depth Data_cleaned to plot, which has the irregularities removed
It just imports pandas and matplotlib, reads the cvs file, and creates the graph window. Then it iterates through each row(I used only one) and plots the pure depth values from which I manually removed the errors.
Raw data uses the original cvs file and properly plots it in a window.
It first extracts the data from the cvs file and converts it into a more easily computable format. Then for each point, it takes a rolling median of the 5 nearest points to avoid outliers and decides whether it is corrupted data by creating a baseline from the Median of Absolute Differences (MAD).
Then removing and interpolates the outliers and data that could not be converted to numbers.
Finally smoothing out the curve by taking a rolling mean for every point

Both of these codes are mostly AI-generated, but they are not directly copy-pasted from the source, and I learned the gist of the code behind it as a reverse learning process.
