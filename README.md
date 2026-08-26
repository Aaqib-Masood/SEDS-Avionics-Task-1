# SEDS-Avionics-Task-1
1. The code first extracts the data from the cvs file and converts it into a more easily computable format. Then, for each point, it takes a rolling median of the 5 nearest points to avoid outliers and decides whether it is corrupted data by creating a baseline from the Median of Absolute Differences (MAD).
2. Then removing and interpolates the outliers and data that could not be converted to numbers.
3. Finally, smoothing out the curve by taking a rolling mean for every point.
