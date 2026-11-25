We are given 10 video recordings under different conditions. Each video records flying insects(bark beetles which are 5mm wide). The video files are preprocessed, and for the sake of simplicity I distributed them into 3 folders representing different preprocessing methods:

1. TMPv - temmporal max pooling over strength of motion
2. TMPt - over time
3. Multiplication of the previous two

We should come up with a macine learning based method to compute a binary mask for each frame, to detect the insects

1 - insects
0 - background

Subtle Points:
The insects appear close and far to the camera, sometimes,their trails are long and smooth, sometimes abrupted and short. The model should be able to understand if the signal comes from a trajectory, do the time encodings change consistently along the trajectory, does the pattern resemble path trail or vegetation oscillation.