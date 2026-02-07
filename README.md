# GraphCrypt — Graph-Based Image Encryption System

GraphCrypt is a secure image encryption and decryption system and a technical exploration of the versatility of **Graph Theory**, demonstrating how classical algorithms can be applied to non-traditional data structures such as digital images.

Rather than focusing exclusively on cryptography, this project investigates how an image can be modeled as a graph to perform **structured, deterministic data transformations**. By treating pixels as nodes and their relationships as edges, the system applies **Minimum Spanning Tree (MST)** and **Depth First Search (DFS)** to traverse and reorder visual data.

This project serves as a case study illustrating how foundational graph algorithms can be used for **image encryption and reversible data transformation**.

---

## Core Algorithmic Approach

This project demonstrates the practical application of Graph Theory in image processing:

- **Graph Representation**  
  A digital image is interpreted as a weighted graph where each pixel is a node and adjacency relationships form the edges.

- **Structural Backbone (MST)**  
  A Minimum Spanning Tree is constructed to establish a stable, connected structure based on pixel intensity differences.

- **Linearization (DFS)**  
  Depth-First Search traversal is applied to generate a unique one-dimensional traversal sequence from the two-dimensional pixel grid.

- **Data Transformation**  
  The traversal order is used to permute pixel positions across RGB channels, enabling deterministic image scrambling and reconstruction.

---

## Security & Performance Metrics

While the primary focus of the project is algorithmic design, the transformation quality and robustness are evaluated using standard encryption metrics:

- **Information Entropy**  
  Measures randomness and uniform pixel distribution in the encrypted image.

- **NPCR (Number of Pixel Change Rate)**  
  Evaluates sensitivity to small changes in the original image.

- **UACI (Unified Average Changing Intensity)**  
  Quantifies average intensity differences to assess diffusion strength.

- **Deterministic Recovery**  
  Ensures lossless and exact reconstruction of the original image using the same graph structure and traversal order.

---

## Tech Stack

### Backend
- Python  
- Flask  
- OpenCV  
- NumPy  

### Frontend
- HTML  
- CSS  
- JavaScript  

---
