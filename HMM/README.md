# Applications of the Viterbi Algorithm and the EM Algorithm

ASR Homework 2  |  2023/11/11

## Task

The content of the homework involves two problems related to statistical models and algorithms:

### Problem 1: Teacher-mood-model

This problem describes a scenario where a school teacher gives three different types of homework assignments (A, B, and C) that vary in the time required for completion. The mood of the teacher (good, neutral, bad), which is not directly observed, influences the type of assignment given. Mood changes occur only overnight.

Model parameters include:

- Observations: {A, B, C}
- States: {good, neutral, bad}
- Transition probabilities between states
- Emission probabilities within each state

Using these parameters, a Hidden Markov Model (HMM) can be constructed. Given a sequence of homework assignments over a week, the task is to determine the most likely sequence of the teacher's moods using the Viterbi algorithm.

### Problem 2: EM Algorithm for a 1D Laplacian Mixture Model

This problem requires deriving the Expectation-Maximization (EM) algorithm for a one-dimensional Laplacian mixture model. Given *n* observations, the goal is to fit a mixture of *m* Laplacian distributions characterized by their density functions. The mixture weights are a convex combination, and the scale parameters are known and fixed.

Tasks include:

- Introducing latent variables for applying the EM procedure.
- Outlining the steps of the EM algorithm for the model and providing an approach for computing updates, especially when they cannot be written analytically. The hint suggests recalling a property of functions that facilitates optimization.

The goal is to estimate the parameters of the mixture model that best explain the observed data.

## Files

```bash
MFCC
│---hw6_solutions.pdf   # reference material
└─--Report.docx 		# Lab Report in Chinese

```

This assignment references the following links:

1. https://las.inf.ethz.ch/courses/introml-f18/hw/hw6_solutions.pdf
2. https://blog.csdn.net/v_JULY_v/article/details/81708386?ops_request_misc=%257B%2522request%255Fid%2522%253A%2522169969596616800222872034%2522%252C%2522scm%2522%253A%252220140713.130102334..%2522%257D&request_id=169969596616800222872034&biz_id=0&utm_medium=distribute.pc_search_result.none-task-blog-2~all~top_positive~default-1-81708386-null-null.142^v96^pc_search_result_base3&utm_term=EM%E7%AE%97%E6%B3%95&spm=1018.2226.3001.4187
3. https://speech.xmu.edu.cn/2020/0630/c18207a406063/page.htm