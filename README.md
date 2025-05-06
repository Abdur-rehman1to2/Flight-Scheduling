# Flight Scheduling Project

## Description

This project implements an improved flight scheduling algorithm using the **Shortest Job First (SJF)** non-preemptive approach. It schedules flights based on their arrival times and durations while avoiding unnecessary delays when no competing flights are present. The result is an optimized schedule with calculated turnaround and waiting times for each flight.

## Features

- Command-line interface for entering flight data
- Validates arrival time and duration inputs (HH:MM format)
- Applies improved SJF scheduling without artificial waiting
- Calculates and displays:
  - Start time
  - Completion time
  - Turnaround time
  - Waiting time
- Displays average turnaround and waiting times
- Clearly formatted scheduling summary table

## Technologies Used

- Python 3.x

## Getting Started

### Prerequisites

Ensure Python 3 is installed on your machine:

```bash
python --version
