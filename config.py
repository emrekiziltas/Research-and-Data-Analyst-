# =============================================================
# CONFIG — Only this file needs to change for a new dataset
# =============================================================

CONFIG = {
    # -------------------------
    # File
    # -------------------------
    'file_path': r"C:\Users\emrek\PycharmProjects\Personal Project\Project_data_analysys\student_data_2023_24.csv",

    # -------------------------
    # Column Names
    # -------------------------
    'status_col':     'status',
    'domicile_col':   'domicile',
    'department_col': 'department',
    'faculty_col':    'faculty',

    # -------------------------
    # Business Logic
    # -------------------------
    'enrolled_value': 'Enrolled',       # The value that means "accepted"
    'typo_map': {
        'Enroled': 'Enrolled'           # Known typos to fix after capitalizing
    },

    # -------------------------
    # Analysis Settings
    # -------------------------
    'group_by_col':  'faculty',         # Column used for acceptance rate grouping
    'domicile_home': 'Home',            # Value representing home students
    'domicile_intl': 'International',   # Value representing international students
    'top_n_depts':   3,                 # How many top departments to show

    # -------------------------
    # Output
    # -------------------------
    'chart_title':  'University of Cambridge — Undergraduate Admissions 2023/24',
    'output_file':  'admissions_2023_24.png',
}
