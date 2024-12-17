# HyperDeck Formatter and File Runner

This repository provides scripts to format HyperDeck media and automate file execution tasks. It includes two key scripts: `format_hyperdecks.py` for managing HyperDeck devices and `run_file.sh` for executing automated shell commands.

---

## Table of Contents

- [Overview](#overview)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
  - [Formatting HyperDeck Media](#formatting-hyperdeck-media)
  - [Running the File Automation Script](#running-the-file-automation-script)
- [Contributing](#contributing)
- [License](#license)

---

## Overview

- **`format_hyperdecks.py`**: A Python script that formats HyperDeck media devices.
- **`run_file.sh`**: A shell script that automates the execution specifically for use in Companion with a Streamdeck button.

---

## Requirements

To run the scripts, ensure you have the following:

### General Requirements:
- Python 3.x
- Bash shell (Linux/macOS compatible)
- HyperDeck connected over the appropriate interface (if formatting devices)

### Python Libraries:
- `argparse` (for command-line argument parsing)
- Additional libraries as defined in `format_hyperdecks.py`

---

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/<your-username>/hyperdeck-formatter-runner.git
   cd hyperdeck-formatter-runner

   
## Usage
1. Formatting HyperDeck Media

Run the format_hyperdecks.py script to format HyperDeck media devices.

Syntax:

python format_hyperdecks.py --device <DEVICE_NAME> --format <FORMAT_TYPE>

Example:

python format_hyperdecks.py --device /dev/sdb --format exFAT

Arguments:

    --device: Path to the device (e.g., /dev/sdb).
    --format: File system format (e.g., exFAT, NTFS).

2. Running the File Automation Script

Execute run_file.sh for running automated workflows.

Syntax:

bash run_file.sh <FILE_NAME>

Example:

bash run_file.sh my_script.sh

Ensure the file specified is executable. To make a file executable:

chmod +x my_script.sh



## Contributing

Contributions are welcome! Please follow these steps:

    Fork the repository.
    Create a new branch for your feature/fix.
    Submit a pull request with a descriptive title and detailed description.

### License

This project is licensed under the MIT License. See the LICENSE file for more details.
Contact

For any questions, please open an issue on the repository.

