# Misinformation Spread in Social Networks
## A Monte Carlo Simulation
Developed by Akanksha Agrawal and Sara Kiel as a Final Project in Spring 2025 for IS597PR - Programming and Quality in Analytics. Course taught by John Weible. 

## Overview
This project simulates the spread of fake and factual news across a synthetic social network using Monte Carlo methods. Agents represent social media users, each assigned roles such as influencers, fact-checkers, susceptible users, or regular users. The goal is to model how misinformation diffuses through a realistic social graph and to evaluate how different conditions - like user type distribution, trust, and fact-checking interventions - affect the reach and speed of information.

## Final Project Report
A comprehensive explanation of the model structure, simulation design, and experimental findings can be found in the document titled “Final Project Report” located in this repository, or view it directly here.

## How to Run
To run the baseline simulation and all hypothesis tests consecutively, simply execute the `main.py` file. However, due to the long runtime of each experiment, we recommend running one segment at a time by commenting out the others.

For example, if you want to run Hypothesis 2, please comment out the baseline, Hypothesis 1, and Hypothesis 3 sections in `main.py`.

This manual toggling approach helps manage runtime and system resources. We are aware of this limitation and plan to improve it in future versions by making adjustments, such as adding a progress bar to track simulation status or optimizing runtime performance across experiments

