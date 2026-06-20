import pandas as pd
import numpy as np

FILE_PATH = r"C:\Users\emrek\PycharmProjects\Personal Project\Project_data_analysys\student_data_2023_24.csv"


# -------------------------------------------------------------
# FUNCTION 1: DATA LOADING
# -------------------------------------------------------------
def load_data(path, verbose=True):
    try:
        df = pd.read_csv(path)
        if verbose:
            print(f"✅ Data successfully loaded! (Rows: {df.shape[0]}, Columns: {df.shape[1]})")
        return df
    except FileNotFoundError:
        print(f"❌ Error: The file path '{path}' was not found.")
        return None


# -------------------------------------------------------------
# FUNCTION 2: DATA CLEANING
# -------------------------------------------------------------
def clean_data(df, verbose=True):
    df_clean = df.copy()

    if verbose:
        print("\n=== PRE-CLEANING: DATA QUALITY CHECK ===")
        print("Missing values per column:")
        print(df_clean.isnull().sum())
        print(f"\nStatus unique values:   {sorted(df_clean['status'].unique())}")
        print(f"Domicile unique values: {sorted(df_clean['domicile'].unique())}")
        print(f"Department casing issues (sample): {[d for d in df_clean['department'].unique() if d != d.title()][:5]}")
        print("⚠️  Inconsistent casing and typos detected — cleaning required.\n")

    # Cleaning always runs regardless of verbose
    df_clean['status'] = df_clean['status'].str.strip().str.capitalize()
    df_clean['domicile'] = df_clean['domicile'].str.strip().str.capitalize()
    df_clean['department'] = df_clean['department'].str.strip().str.title()
    df_clean['faculty'] = df_clean['faculty'].str.strip().str.title()
    df_clean['status'] = df_clean['status'].replace('Enroled', 'Enrolled')

    if verbose:
        print("=== POST-CLEANING: VERIFICATION ===")
        print(f"Status unique values:   {sorted(df_clean['status'].unique())}")
        print(f"Domicile unique values: {sorted(df_clean['domicile'].unique())}")
        print("✅ Data cleaning complete (Typos fixed & text standardized).\n")

    return df_clean

# -------------------------------------------------------------
# FUNCTION 3: ACCEPTANCE RATE BY FACULTY
# -------------------------------------------------------------
def analyze_acceptance_rate(df, verbose=True):
    faculty_stats = df.groupby('faculty')['status'].apply(
        lambda x: (x == 'Enrolled').mean() * 100
    ).round(1).reset_index()

    faculty_stats.columns = ['Faculty', 'Acceptance Rate (%)']
    faculty_stats = faculty_stats.sort_values('Acceptance Rate (%)', ascending=False)

    if verbose:
        print("\n=== TASK 2: ACCEPTANCE RATE BY FACULTY ===")
        print(faculty_stats.to_string(index=False))
        print("==========================================\n")

    return faculty_stats


# -------------------------------------------------------------
# FUNCTION 4: TOP 3 DEPARTMENTS BY ENROLMENT
# -------------------------------------------------------------
def top_departments(df, n=3, verbose=True):
    enrolled = df[df['status'] == 'Enrolled']
    dept_counts = enrolled.groupby('department').size().reset_index(name='Enrolments')
    dept_counts = dept_counts.sort_values('Enrolments', ascending=False).head(n)

    if verbose:
        print(f"\n=== TASK 3: TOP {n} DEPARTMENTS BY ENROLMENT ===")
        print(dept_counts.to_string(index=False))
        print("=================================================\n")

    return dept_counts


# -------------------------------------------------------------
# FUNCTION 5: HOME vs INTERNATIONAL ACCEPTANCE RATE
# -------------------------------------------------------------
def analyze_domicile_acceptance(df, verbose=True):
    domicile_stats = df.groupby('domicile')['status'].apply(
        lambda x: (x == 'Enrolled').mean() * 100
    ).round(1).reset_index()

    domicile_stats.columns = ['Domicile', 'Acceptance Rate (%)']

    if verbose:
        print("\n=== TASK 4: HOME vs INTERNATIONAL ACCEPTANCE RATE ===")
        print(domicile_stats.to_string(index=False))

        # Calculate the gap
        rates = domicile_stats.set_index('Domicile')['Acceptance Rate (%)']
        if 'Home' in rates and 'International' in rates:
            gap = rates['Home'] - rates['International']
            print(f"\n⚠️  Home students are accepted at {gap:.1f}% higher rate than International students.")
        print("======================================================\n")

    return domicile_stats


# -------------------------------------------------------------
# FUNCTION 6: VISUALISATIONS
# -------------------------------------------------------------
# -------------------------------------------------------------
# FUNCTION 6: VISUALISATIONS (OPTIMIZED FOR CHART B OVERLAP)
# -------------------------------------------------------------
def create_charts(faculty_stats, dept_stats, domicile_stats, verbose=True):
    import matplotlib.pyplot as plt
    import matplotlib.ticker as mticker
    import os, webbrowser

    plt.style.use('seaborn-v0_8-muted')

    # gridspec_kw kullanarak Chart B için dikeyde 2 ayrı bölme açıyoruz (biri tablo, biri bar için)
    fig, axes = plt.subplot_mosaic(
        [['chart_a', 'table_b', 'chart_c'],
         ['chart_a', 'bar_b', 'chart_c']],
        figsize=(24, 8),
        gridspec_kw={'height_ratios': [1, 1]}  # Üst ve alt yarı eşit paylaşılsın
    )

    fig.suptitle('University of Cambridge — Undergraduate Admissions 2023/24',
                 fontsize=16, fontweight='bold', y=1.05)

    # --- CHART A: Acceptance Rate by Faculty ---
    ax1 = axes['chart_a']
    bars = ax1.barh(faculty_stats['Faculty'], faculty_stats['Acceptance Rate (%)'], edgecolor='white')
    ax1.set_title('Acceptance Rate by Faculty', fontweight='bold', fontsize=13, pad=15)
    ax1.set_xlabel('Acceptance Rate (%)', fontsize=11)
    ax1.set_xlim(0, 100)
    ax1.xaxis.set_major_formatter(mticker.FormatStrFormatter('%d%%'))
    ax1.tick_params(axis='both', labelsize=11)
    for bar in bars:
        width = bar.get_width()
        ax1.text(width + 1, bar.get_y() + bar.get_height() / 2, f'{width:.1f}%', va='center', fontsize=11)
    ax1.invert_yaxis()

    # --- CHART B: Top 3 Departments (Table Part) ---
    ax2_table = axes['table_b']
    ax2_table.axis('off')
    table = ax2_table.table(
        cellText=dept_stats.values,
        colLabels=dept_stats.columns,
        loc='center',
        cellLoc='center',
        bbox=[0.0, 0.0, 1.0, 0.8]  # Kutu boyutunu optimize ettik
    )
    table.auto_set_font_size(False)
    table.set_fontsize(12)
    for (row, col), cell in table.get_celld().items():
        if row == 0:
            cell.set_facecolor('#4878CF')
            cell.set_text_props(color='white', fontweight='bold')
        else:
            cell.set_facecolor('#f0f0f0' if row % 2 == 0 else 'white')
    ax2_table.set_title('Top 3 Departments by Enrolment', fontweight='bold', fontsize=13, pad=15)

    # --- CHART B: Top 3 Departments (Mini Bar Part) ---
    ax2_bar = axes['bar_b']
    bars_b = ax2_bar.barh(dept_stats['department'], dept_stats['Enrolments'], edgecolor='white', color='#64B5CD')
    ax2_bar.set_xlabel('Enrolments', fontsize=11)
    ax2_bar.tick_params(axis='both', labelsize=11)
    ax2_bar.set_xlim(0, dept_stats['Enrolments'].max() + 20)
    for bar in bars_b:
        width = bar.get_width()
        ax2_bar.text(width + 1, bar.get_y() + bar.get_height() / 2, str(int(width)), va='center', fontsize=11,
                     fontweight='bold')
    ax2_bar.invert_yaxis()  # En çok kayıt olan en üstte gözüksün

    # --- CHART C: Home vs International ---
    ax3 = axes['chart_c']
    wedges, texts, autotexts = ax3.pie(
        domicile_stats['Acceptance Rate (%)'],
        labels=domicile_stats['Domicile'],
        autopct='%1.1f%%',
        startangle=90,
        wedgeprops=dict(edgecolor='white', linewidth=2)
    )
    for text in texts: text.set_fontsize(12)
    for autotext in autotexts:
        autotext.set_fontsize(12)
        autotext.set_fontweight('bold')
    ax3.set_title('Acceptance Rate: Home vs International', fontweight='bold', fontsize=13, pad=15)

    # Alanlar arası boşluğu otomatik ayarla
    plt.tight_layout()

    output_path = os.path.abspath('admissions_2023_24.png')
    plt.savefig(output_path, dpi=200, bbox_inches='tight')

    if verbose:
        print("✅ Charts saved as 'admissions_2023_24.png'")

    webbrowser.open(output_path)
    plt.show()

# =============================================================
# MAIN ORCHESTRATOR
# =============================================================

# 1. Load data
data = load_data(FILE_PATH, verbose=True)

if data is not None:
    # 2. Clean data
    cleaned_data = clean_data(data, verbose=True)

    # 3. Acceptance rate by faculty
    faculty_stats = analyze_acceptance_rate(cleaned_data, verbose=False)

    # 4. Top 3 departments by enrolment
    dept_stats = top_departments(cleaned_data, n=3, verbose=True)

    # 5. Home vs International acceptance rate
    domicile_stats = analyze_domicile_acceptance(cleaned_data, verbose=True)

    # 6. Visualisations
    create_charts(faculty_stats, dept_stats, domicile_stats, verbose=True)