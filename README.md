# Research and Data Analyst — Student Admissions Pipeline

A modular, config-driven Python pipeline for analysing student admissions data. Built as part of interview preparation for the Research and Data Analyst role at the University of Cambridge (Education Services).

---

## Features

- **Automated data loading** with error handling
- **Data cleaning** — standardises casing, fixes typos, detects missing values
- **Acceptance rate analysis** by faculty
- **Top N departments** by enrolment
- **Home vs International** student acceptance rate comparison
- **Visualisation** — three-panel chart (bar, table + mini bar, pie chart)
- **Config-driven pipeline** — change dataset by editing `config.py` only

---

## Project Structure

```
├── config.py                  # All settings — edit this for a new dataset
├── main.py                    # Main pipeline — load, clean, analyse, visualise
├── student_data_2023_24.csv   # Demo dataset (1,200 synthetic student records)
└── README.md
```

---

## Getting Started

### Requirements

```bash
pip install pandas numpy matplotlib
```

### Run

```bash
python main.py
```

---

## Configuration

To use a different dataset, only edit `config.py`:

```python
CONFIG = {
    'file_path':      'your_data.csv',
    'status_col':     'status',          # Column indicating admission outcome
    'enrolled_value': 'Enrolled',        # Value that means accepted
    'domicile_col':   'domicile',        # Column for home/international
    'department_col': 'department',
    'faculty_col':    'faculty',
    'group_by_col':   'faculty',         # Column used for acceptance rate grouping
    'top_n_depts':    3,                 # How many top departments to display
    'typo_map': {
        'Enroled': 'Enrolled'            # Known typos to fix after cleaning
    },
    'chart_title':  'Your Chart Title',
    'output_file':  'output.png',
}
```

`main.py` requires no changes.

---

## Output

The pipeline produces:

- Console logs with pre/post cleaning verification
- Acceptance rate tables by faculty and domicile
- A three-panel PNG chart saved to the working directory

---

## Demo Dataset

`student_data_2023_24.csv` contains 1,200 synthetic undergraduate records across 5 faculties and 20 departments, with intentional data quality issues (inconsistent casing, typos, missing values) for demonstration purposes.

---

## Author

Emre Kiziltas — [github.com/emrekiziltas](https://github.com/emrekiziltas)
