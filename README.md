# Aircraft Performance Analysis Toolkit

## Final Report
[Final Report](/honorable-mention-undergraduate-team-aircraft-university-of-illinois-urbana-champaign.pdf)

## Description

This repository contains a collection of Python scripts designed for analyzing various aspects of aircraft performance. It utilizes a set of predefined aircraft parameters (aerodynamics, mass, propulsion, atmospheric conditions) to perform calculations related to cruise performance, payload-range capabilities, flight envelope, and more.

## Core Modules

The primary calculations are handled by the following Python scripts:

### Key Scripts and Their Outputs

*   **`parameters/param.py`**: Defines the core aircraft parameters (aerodynamic coefficients, weights, engine specifics, standard atmospheric conditions) and saves them to a binary file (`parameters/params`) using `pickle` for use by other modules.
    * **Run with**: `python parameters/param.py`
    * **Output**: Creates or updates the `parameters/params` binary file with aircraft parameters.
    * **Console output**: Progress messages ("Loading file...", "Dumping data to file...", "Closing file...").

*   **`cruise.py`**: Calculates cruise performance metrics. It includes classes for:
    *   `conditions`: Determines atmospheric properties (temperature, pressure, density) at a given altitude.
    *   `speed`: Converts between different speed measures (KCAS, KTAS, Mach number).
    *   `coefficients`: Calculates aerodynamic coefficients (CL, CD, L/D), drag, and stall speed based on flight conditions and weight.
    *   `power`: Computes power required and power available based on flight conditions.
    * **Note**: This file primarily provides classes used by other scripts rather than generating output directly.

*   **`payload_range.py`**: Calculates and plots the payload-range diagram for the aircraft, illustrating the trade-off between payload weight and achievable range.
    * **Run with**: `python payload_range.py`
    * **Output**: Displays a plot showing:
      * Maximum payload range
      * Ferry mission range (60% payload)
      * Zero payload range
    * **Console output**: Prints the calculated ranges for max payload, ferry payload, and no payload in nautical miles.

*   **`flight_envelope.py`**: Calculates and plots the aircraft's flight envelope (operating limits based on speed and altitude).
    * **Run with**: `python flight_envelope.py`
    * **Output**: Displays a plot of altitude vs. Mach number showing:
      * Stall speed boundaries
      * Top speed boundaries
      * Maximum altitude limit
    * Uses multiprocessing to efficiently calculate the altitude limits at different speeds.

*   **`speed_range.py`**: Analyzes the range achievable at different speeds.
    * **Run with**: `python speed_range.py`
    * **Output**: Displays a plot of range vs. Mach number at a fixed altitude (18,000 ft).
    * **Console output**: Prints the Mach number and range (in nautical miles) for the maximum range condition.

*   **`bfl.py`**: Calculates Balanced Field Length (takeoff distance).
    * **Run with**: `python bfl.py`
    * **Output**: Prints the calculated Balanced Field Length in feet to the console.
    * Uses a specialized formula based on aircraft parameters like weight, lift coefficients, engine power, and air density.

*   **`actual_TO.py`**: Calculates actual takeoff performance.
    * **Run with**: `python actual_TO.py`
    * **Output**: Prints the calculated takeoff distance in feet to the console.
    * Takes into account factors like thrust, ground effects, and takeoff speed.

*   **`aero_inputs.py`**: Analyzes power requirements at different airspeeds.
    * **Run with**: `python aero_inputs.py`
    * **Output**: Displays a plot of power required (hp) vs. airspeed (KTAS) at 10,000 ft altitude with:
      * Current power required curve
      * Maximum engine power limit
      * Vertical line indicating maximum speed
    * **Console output**: For each velocity, prints the lift coefficient, velocity, and power required.

*   **`flight_coefficients.py`**: Analyzes and plots lift-to-drag ratios.
    * **Run with**: `python flight_coefficients.py`
    * **Output**: Displays a plot of lift-to-drag ratios (CL/CD and CL^(1/2)/CD) vs. Mach number, with the maximum values marked.
    * **Console output**: Prints the Mach numbers where each ratio is maximized.

*   **`equation_testing.py`**: Used for testing takeoff performance calculations.
    * **Run with**: `python equation_testing.py`
    * **Output**: Prints the calculated takeoff speed (in feet per second) to the console.
    * Similar to `actual_TO.py` but with slightly different parameters for testing purposes.

## Parameters

Aircraft parameters are centralized in `parameters/param.py`. This script defines dictionaries for:

*   `aero`: Aerodynamic properties (reference area, span, aspect ratio, Oswald efficiency factor, etc.).
*   `mass`: Weight properties (fuel weight, payload weight, empty weight, MTOW).
*   `prop`: Propulsion system properties (engine power, efficiency, specific fuel consumption).
*   `cond`: Standard atmospheric conditions at sea level.

These parameters are pickled into the `parameters/params` file, which is then loaded by the calculation modules.

## Dependencies

The scripts rely on the following Python libraries:

*   `numpy`: For numerical calculations.
*   `matplotlib`: For plotting results (e.g., payload-range diagram).
*   `pickle`: For saving and loading the parameter data.

Ensure these libraries are installed in your Python environment. You can typically install them using pip:
```bash
pip install numpy matplotlib
```
(`pickle` is part of the standard Python library).

## Usage

1.  **Parameter Setup**: Run `parameters/param.py` once initially (or whenever parameters need updating) to generate the `parameters/params` file.
    ```bash
    python parameters/param.py
    ```
2.  **Run Analysis Scripts**: Execute the desired analysis script directly. For example, to generate the payload-range diagram:
    ```bash
    python payload_range.py
    ```
    Similarly, run other scripts like `cruise.py`, `flight_envelope.py`, etc., as needed. Some scripts may generate plots or print results to the console.

*Note: Some scripts might contain commented-out sections or require specific inputs/modifications to run specific analyses.*

This project was created for AE442/AE443 Systems Design
