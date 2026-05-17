import pandas as pd
import numpy as np

print("Creating complete Loan Approval Dataset (614 records)...")
print("=" * 50)

# Set random seed for reproducibility
np.random.seed(42)

# Number of records (same as real dataset)
n = 614

# Create realistic loan data
data = {
    'Loan_ID': [f'LP{str(i+1).zfill(6)}' for i in range(n)],

    # Demographics
    'Gender': np.random.choice(['Male', 'Female'], n, p=[0.8, 0.2]),
    'Married': np.random.choice(['Yes', 'No'], n, p=[0.65, 0.35]),
    'Dependents': np.random.choice(['0', '1', '2', '3+'], n, p=[0.5, 0.25, 0.15, 0.1]),
    'Education': np.random.choice(['Graduate', 'Not Graduate'], n, p=[0.7, 0.3]),
    'Self_Employed': np.random.choice(['Yes', 'No'], n, p=[0.15, 0.85]),

    # Financial
    'ApplicantIncome': np.random.normal(5400, 2200, n).astype(int),
    'CoapplicantIncome': np.random.normal(1800, 1600, n).astype(int),
    'LoanAmount': np.random.normal(145, 55, n).astype(int),
    'Loan_Amount_Term': np.random.choice([360, 180, 120, 60], n, p=[0.55, 0.25, 0.15, 0.05]),

    # Credit
    'Credit_History': np.random.choice([1.0, 0.0], n, p=[0.81, 0.19]),

    # Property
    'Property_Area': np.random.choice(['Urban', 'Semiurban', 'Rural'], n, p=[0.35, 0.35, 0.3])
}

df = pd.DataFrame(data)

# Make income and loan amounts realistic (no negatives)
df['ApplicantIncome'] = df['ApplicantIncome'].clip(lower=150)
df['CoapplicantIncome'] = df['CoapplicantIncome'].clip(lower=0)
df['LoanAmount'] = df['LoanAmount'].clip(lower=9)

# Create Loan_Status based on real-world logic
def determine_loan_status(row):
    score = 0

    # Credit history is most important
    if row['Credit_History'] == 1.0:
        score += 40
    else:
        score -= 30

    # Income and loan amount ratio
    total_income = row['ApplicantIncome'] + row['CoapplicantIncome']
    if total_income > 5000:
        score += 20
    elif total_income > 3000:
        score += 10
    else:
        score -= 10

    # Loan amount vs income
    if row['LoanAmount'] * 1000 < total_income * 3:
        score += 15
    elif row['LoanAmount'] * 1000 > total_income * 8:
        score -= 15

    # Education
    if row['Education'] == 'Graduate':
        score += 10

    # Employment
    if row['Self_Employed'] == 'No':
        score += 5

    # Property area
    if row['Property_Area'] == 'Urban':
        score += 8
    elif row['Property_Area'] == 'Semiurban':
        score += 5

    # Married
    if row['Married'] == 'Yes':
        score += 5

    # Dependents
    if row['Dependents'] == '0':
        score += 5
    elif row['Dependents'] == '3+':
        score -= 5

    # Decision
    return 'Y' if score >= 50 else 'N'

df['Loan_Status'] = df.apply(determine_loan_status, axis=1)

# Save to CSV
df.to_csv('loan_data.csv', index=False)

print(f"\n[SUCCESS] Created loan_data.csv")
print(f"  Total records: {len(df)}")
print(f"  Approved (Y): {(df['Loan_Status'] == 'Y').sum()} ({(df['Loan_Status'] == 'Y').sum()/len(df)*100:.1f}%)")
print(f"  Rejected (N): {(df['Loan_Status'] == 'N').sum()} ({(df['Loan_Status'] == 'N').sum()/len(df)*100:.1f}%)")

print(f"\nFirst 10 rows:")
print(df.head(10).to_string())
