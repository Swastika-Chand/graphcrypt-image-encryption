GraphCrypt — Graph-Based Image Encryption System

GraphCrypt is a secure image encryption and decryption system, a technical exploration into the versatility of Graph Theory, demonstrating how classical algorithms can be applied to non-traditional data structures like digital images.
Rather than focusing exclusively on cryptography, this project investigates how an image can be modeled as a graph to perform structured, deterministic data permutations. By treating pixels as nodes and their relationships as edges, we utilize Minimum Spanning Tree (MST) and Depth First Search (DFS) to traverse and reorder visual data.
The project serves as a case study illustrating how foundational graph algorithms can be used in image encrpytion and decryption.

Core Algorithmic Approach
-This project demonstrates the practical application of Graph Theory in image processing:
-Graph Representation: Interprets a digital image as a weighted graph where each pixel is a node and adjacency forms the edges.
-Structural Backbone (MST): Uses the Minimum Spanning Tree to identify a stable, connected structure based on pixel intensity differences.
-Linearization (DFS): Employs a Depth-First Search traversal to generate a unique 1D sequence from the 2D pixel grid.
-Data Transformation: Uses the resulting traversal order to permute pixel positions across RGB channels, providing a case study in data scrambling.

Security & Performance Metrics
While the primary focus is algorithmic, the transformation quality and security strength are validated through rigorous statistical metrics:
-Information Entropy: Analyzed to ensure high randomness and a uniform pixel distribution in the encrypted image, making it resistant to statistical attacks.
-NPCR (Number of Pixel Change Rate): Measures the sensitivity of the encryption to even the slightest change in the original image.
-UACI (Unified Average Changing Intensity): Evaluates the average intensity difference between two images to ensure strong diffusion.
-Deterministic Recovery: Ensures that the graph structure allows for perfect, lossless reconstruction (decryption) of the original data.

Tech Stack
### Backend
- Python
- Flask
- OpenCV
- NumPy
### Frontend
- HTML
- CSS
- JavaScript
