# Quantum Network Multiple-Entanglement Routing Framework

This project implements a Sequential Multi-path Scheduling Algorithm (SMPSA) for quantum networks, based on the research paper "A Multiple-Entanglement Routing Framework for Quantum Networks" by Nguyen et al. The framework enables k-entangled routing to establish multiple quantum paths between source-destination pairs in a network.

## Overview

The algorithm provides:
- Multiple-entanglement routing capabilities for quantum networks
- Network simulation with configurable number of nodes
- Qubit assignment and entanglement management
- Path discovery and scheduling between source-destination pairs
- Performance analysis and metrics collection

## Features

- Dynamic network construction with customizable node count
- Automatic qubit assignment and entanglement generation
- Sequential multi-path scheduling for source-destination pairs
- Network visualization capabilities (optional)
- Performance metrics tracking including:
  - Number of nodes
  - Number of source-destination pairs
  - Minimum/maximum qubits assigned per node
  - Minimum/maximum entangled qubits per node
  - Achieved k-paths

## Usage

The main functionality is implemented in the `sequential_multipath_scheduling` function, which can be executed through the `run_sequential_multipath` function. The framework:

1. Builds a quantum network with specified dimensions
2. Assigns and entangles qubits across the network
3. Generates random source-destination pairs
4. Computes multiple entangled paths
5. Collects and saves performance metrics

Results are automatically saved to CSV files in the `results/sequential_multipath/` directory. Optional network visualizations can be generated in the `visualization/sequential_multipath/` directory.

## Dependencies

- NetworkX
- NumPy
- Pandas
- Matplotlib
- NetSquid (for quantum network simulation)

## Output

The framework generates comprehensive performance metrics including:
- Network topology information
- Qubit allocation statistics
- Entanglement success rates
- Path multiplicity (k) achievements

Results are saved in CSV format for further analysis and visualization.
