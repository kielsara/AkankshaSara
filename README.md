# Misinformation Spread in Social Networks
## A Monte Carlo Simulation
Developed by Akanksha Agrawal and Sara Kiel as a Final Project in Spring 2025 for IS597PR - Programming and Quality in Analytics. Course taught by John Weible. 

## Overview
This project simulates the spread of fake and factual news across a synthetic social network using Monte Carlo methods. Agents represent social media users, each assigned roles such as influencers, fact-checkers, susceptible users, or regular users. The goal is to model how misinformation diffuses through a realistic social graph and to evaluate how different conditions - like user type distribution, trust, and fact-checking interventions - affect the reach and speed of information.

## Final Project Report
A comprehensive explanation of the model structure, simulation design, experimental findings, and references can be found in the document titled “Final Project Report” located in this repository, or view it directly [here](https://github.com/kielsara/MisinformationSpread/blob/main/IS597PR%20Final%20Project%20Report.pdf).

## How to Run
### 1. Clone the repository
```bash
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name
```
### 2. Set up the environment
```bash
pip install -r requirements.txt
```
### 3. Run the simulation
To run the full set of experiments:
```bash
python main.py
```
> **Note:** We recommend running **one section at a time** due to long runtimes.
> For example, if testing Hypothesis 2, comment out Baseline, Hypothesis 1, and Hypothesis 3 in `main.py`.

This manual toggling approach helps manage runtime and system resources. We are aware of this limitation and plan to improve it in future versions by making adjustments, such as adding a progress bar to track simulation status or optimizing runtime performance across experiments