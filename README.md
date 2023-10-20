# Pharmokinetics Modelling Project

Solving a Pharmacokinetics (PK) model

## Table of Contents
- [Introduction](#introduction)
- [Features](#features)
- [Getting Started](#getting-started)
  - [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Introduction

This repository contains a python library that can specify, solve and visualise the solution of a PK model describing either an intravenous bolus dosing protocol or a subcutaneous dosing.

## Features

The library has the ability to specify:
- the form of the PK model
- the type of dosing: intravenous bolus versus subcutaneous
- the number of peripheral compartments: 2 for intravenous, or 3 for subcutaneous dosing
- the dosing protocol: steady application of a steady dose between two timepoints t0 and t1; and/or an instantaneous application of specific doses at specific timepoints

For a full description of the module, visit the website https://github.com/SanazKaz/PK-software-project

## Getting Started

### Installation

To install the project: 
'pip install .'

## Usage

To use the project:
```
from pkmodel import Protocol, Model, Solution
protocol = Protocol('intravenous', [(2, 4), (3, 1)], (0, 5), 4)
model = Model(Q_p1 = 1.0, V_c = 1.0, V_p1 = 1.0, CL = 1.0, k_a = 1.0)
solution = Solution(model, protocol)
solution.solve()

```

## Contributing

Submit bug reports and feature suggestions, or track changes in the https://github.com/SanazKaz/PK-software-project/issues

## License

This project is covered under MIT License



