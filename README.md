# Analyzing Performance of RBF SVM and AdaBoost Machine Learning Models on Varied Linear-Dependency of Features

## Project Overview
Early and accurate breast cancer diagnosis significantly improves patient outcomes, and machine learning models used for this task must handle collinearity between diagnostic features reliably. This project trains a decision tree classifier (baseline), an AdaBoost ensemble, and a Radial Basis Function (RBF) Support Vector Machine on the Breast Cancer Wisconsin (Diagnostic) dataset, comparing performance on the original feature set against a version with collinear features removed. SHAP is then used to explain AdaBoost and RBF SVM predictions on both feature sets, evaluating which model relies on the most relevant features under varying collinearity. 

## Collinearity Between Dataset Features
![Collinearity Between Dataset Features](collinearity.png) 

## Tech Stack
* **Programming Languages and Software**: Python, Google Collab, Overleaf

## Conclusion
Overall, the best performing model was the RBF SVM model on the original dataset. The worst performing model with the lowest f1-score for the malignant class was the
decision tree trained on features with the correlation weight greater than 0.97 were removed. This seems to imply that the intrinsic structure of the RBF SVM allows for multicollinearity to exist without a sacrifice to model performance.
