# Virtual Testbed

# Virtual Testbed Tool for Industrial Process Simulation

This repository hosts a virtual testbed designed to simulate industrial processes with MATLAB Simulink and OpenModelica. The testbed focuses on simulating a robotic Automated Industrial Vehicle (AIV) and a chemical storage system, allowing users to model and test complex industrial scenarios within a controlled environment.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Repository Structure](#repository-structure)
- [Getting Started](#getting-started)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Overview

The virtual testbed integrates MATLAB Simulink and OpenModelica models to simulate interactions between an AIV robot, which navigates industrial layouts, and a chemical storage system, where dynamic behaviors are modeled with OpenModelica. This testbed enables the design, testing, and validation of industrial processes, allowing developers to assess performance and safety in a simulated setting.

### Key Simulated Scenarios

- **Chemical Storage Scenario**: A detailed industrial layout with specific process constraints.
- **AIV Scenario**: Custom process flow and storage modeling tailored for a distinct industrial setup.

## Features

- **MATLAB Simulink Integration**: Control and simulate the AIV robot’s navigation and decision-making algorithms.
- **OpenModelica Models**: Simulate the chemical storage and processing, focusing on thermal behavior, safety conditions, and dynamic responses.
- **Configurable Scenarios**: Predefined YAML configuration files for each industrial scenario, providing a range of test cases.
- **Scalable Architecture**: Modular design supports the addition of new processes, robots, or storage systems.
- **Documentation and Versioning**: Track changes and document model versions for consistent testing and evaluation.

## Repository Structure

```
├── cyris/                   # Core framework for the testbed
├── documentazione/          # Documentation files for the setup, usage, and scenarios
├── models/                  # MATLAB Simulink and OpenModelica models
├── old/                     # Deprecated files and legacy models
├── project/                 # Project configuration and dependencies
├── temp/                    # Temporary files and development scripts
├── .gitignore               # Gitignore file for managing excluded files
├── README.md                # Project README
├── scenario_chemicalstorage.yaml # Configuration file for Carmagnani scenario
├── scenario_aiv.yaml      # Configuration file for Depuy scenario
```

## Getting Started

### Prerequisites

1. **VM Images**: please get in touch with us for this.

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo/virtual-testbed.git
   cd virtual-testbed
   ```
2. Install MATLAB and OpenModelica, ensuring that they are available in your PATH.

## Usage

### Configuring a Scenario

1. **Select a Scenario**: Choose a predefined YAML file.
2. **Run the Configuration**:
   Load the chosen configuration file, which sets up the testbed with parameters tailored to the selected scenario.

   ```bash
   python3 ./project/start_scenario.py scenario_chemical.yaml
   ```

### Running Simulations

1. **AIV Simulation**:
   - Open MATLAB and navigate to the `models/` directory.
   - Load the AIV model in Simulink and start the simulation.

2. **Chemical Storage Simulation**:
   - Open OpenModelica and load the chemical storage model from `models/`.
   - Run the simulation to observe dynamic behaviors under various conditions.

### Viewing Results

Simulation results can be viewed within the MATLAB Simulink environment and OpenModelica's plotting tools. Output data files will be stored in `temp/` for further analysis.

## Contributing

Contributions are welcome! Please fork the repository, create a new branch, and submit a pull request with your changes.

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Submit a pull request with a description of your changes.

## License

This project is licensed under the MIT License. See the `LICENSE` file for more details.

---

This README provides an overview of the virtual testbed’s purpose, configuration, and usage. Feel free to extend this with further technical details specific to your implementation needs.
