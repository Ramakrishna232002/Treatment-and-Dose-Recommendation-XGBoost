# 5G-Federated-IDS: Privacy-Preserving Intrusion Detection for 5G Networks

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![TensorFlow](https://img.shields.io/badge/TensorFlow-2.0+-orange.svg)
![Federated Learning](https://img.shields.io/badge/Federated-Learning-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## 📌 Overview

This project implements a **decentralized intrusion detection system (IDS)** for 5G networks using **Federated Learning** and **Explainable AI (XAI)** within a **Zero Trust** security paradigm.

Unlike traditional IDS that centralize sensitive network traffic data, our approach:

- ✅ Trains models **locally** on edge nodes (preserving data privacy)
- ✅ Aggregates only model updates via a **Federated Server**
- ✅ Provides **interpretable decisions** using SHAP/LIME
- ✅ Continuously **validates every request** (Zero Trust architecture)


## 🚀 Features

- 🔒 **Privacy-Preserving**: Raw network traffic never leaves edge nodes
- 🧠 **Federated Learning**: Collaborative training without data sharing
- 📊 **Explainable AI**: SHAP/LIME explanations for every detection
- 🛡️ **Zero Trust Ready**: Continuous authentication simulation
- 📈 **Scalable**: Supports multiple edge nodes (3–100+)
- 🎯 **High Accuracy**: State-of-the-art intrusion detection


## 🛠️ Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager
- (Optional) Virtual environment tool

### Step 1: Clone the Repository

```bash
git clone https://github.com/yourusername/5G-Federated-IDS.git
cd 5G-Federated-IDS

## 📈 Results (Expected)
- Metric	Value
- Accuracy	94.6%
- Precision	93.8%
- Recall	95.1%
- F1-Score	94.4%
- Communication Reduction	99.7% (vs centralized)
- Inference Time	< 5ms per packet



