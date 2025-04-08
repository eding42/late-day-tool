# late-day-tool

The Late-Day Tool is a utility designed to help manage and track coding and homework assignment late-day usage for CMPSC 32 students. 

## Features
- Tracks late-day usage for students.
- Takes in Gradescope assignment grades CSV file as input 
- Processes assignments based on assignment lateness (as calculated by Gradescope).
- Generates reports on late days already used.

## Future
- Automatically email each student if they are close to running out of late days.
- More robust CSV parsing
- Keep track of students already contacted.
- Command line option for assignment grace period.
- Complete refactor of codebase to be more modular.

## Usage
1. Clone the repository:
   ```bash
   git clone git@github.com:eding42/late-day-tool.git
2. Run the tool with the required input files:
    ```bash
    python grades.py <input_file>

## Requirements
 
No additional packages besides Python's built-in CSV, Math and ArgParse modules are required. 