import pandas as pd
import numpy as np

df = pd.read_csv('loan_data.csv')

total = len(df)
approved = (df['Loan_Status'] == 'Y').sum()
rejected = (df['Loan_Status'] == 'N').sum()
avg_income = int(df['ApplicantIncome'].mean())
avg_loan = int(df['LoanAmount'].mean())
good_credit = int((df['Credit_History'] == 1.0).sum() / total * 100)

# Build table rows
rows_html = ''
for _, row in df.iterrows():
    status_class = 'approved' if row['Loan_Status'] == 'Y' else 'rejected'
    status_label = 'Approved' if row['Loan_Status'] == 'Y' else 'Rejected'
    rows_html += f"""
        <tr>
            <td><span class="loan-id">{row['Loan_ID']}</span></td>
            <td>{row['Gender']}</td>
            <td>{row['Married']}</td>
            <td>{row['Dependents']}</td>
            <td>{row['Education']}</td>
            <td>{row['Self_Employed']}</td>
            <td><strong>${row['ApplicantIncome']:,}</strong></td>
            <td>${row['CoapplicantIncome']:,}</td>
            <td>${row['LoanAmount']}K</td>
            <td>{int(row['Loan_Amount_Term'])} mo</td>
            <td>{'✔' if row['Credit_History'] == 1.0 else '✘'}</td>
            <td>{row['Property_Area']}</td>
            <td><span class="badge {status_class}">{status_label}</span></td>
        </tr>"""

html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>Loan Approval Dataset</title>
  <style>
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}

    body {{
      font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
      background: #0f1117;
      color: #e2e8f0;
      padding: 32px 24px;
      min-height: 100vh;
    }}

    .header {{
      text-align: center;
      margin-bottom: 36px;
    }}
    .header h1 {{
      font-size: 2rem;
      font-weight: 700;
      color: #f8fafc;
      letter-spacing: 0.5px;
    }}
    .header p {{
      color: #94a3b8;
      margin-top: 6px;
      font-size: 0.95rem;
    }}

    .stats {{
      display: flex;
      gap: 16px;
      justify-content: center;
      flex-wrap: wrap;
      margin-bottom: 36px;
    }}
    .stat-card {{
      background: #1e2330;
      border: 1px solid #2d3748;
      border-radius: 12px;
      padding: 20px 28px;
      text-align: center;
      min-width: 140px;
    }}
    .stat-card .value {{
      font-size: 1.8rem;
      font-weight: 700;
      color: #60a5fa;
    }}
    .stat-card .value.green  {{ color: #34d399; }}
    .stat-card .value.red    {{ color: #f87171; }}
    .stat-card .value.yellow {{ color: #fbbf24; }}
    .stat-card .label {{
      font-size: 0.8rem;
      color: #94a3b8;
      margin-top: 4px;
      text-transform: uppercase;
      letter-spacing: 0.5px;
    }}

    .table-wrapper {{
      overflow-x: auto;
      border-radius: 12px;
      border: 1px solid #2d3748;
    }}

    .search-bar {{
      display: flex;
      align-items: center;
      gap: 12px;
      margin-bottom: 16px;
      flex-wrap: wrap;
    }}
    .search-bar input {{
      background: #1e2330;
      border: 1px solid #2d3748;
      border-radius: 8px;
      color: #e2e8f0;
      padding: 8px 14px;
      font-size: 0.9rem;
      outline: none;
      width: 240px;
    }}
    .search-bar input:focus {{ border-color: #60a5fa; }}
    .search-bar select {{
      background: #1e2330;
      border: 1px solid #2d3748;
      border-radius: 8px;
      color: #e2e8f0;
      padding: 8px 12px;
      font-size: 0.9rem;
      outline: none;
      cursor: pointer;
    }}
    .search-bar label {{ color: #94a3b8; font-size: 0.85rem; }}

    table {{
      width: 100%;
      border-collapse: collapse;
      font-size: 0.875rem;
    }}
    thead tr {{
      background: #1a1f2e;
    }}
    thead th {{
      padding: 14px 16px;
      text-align: left;
      font-size: 0.75rem;
      font-weight: 600;
      text-transform: uppercase;
      letter-spacing: 0.6px;
      color: #64748b;
      border-bottom: 1px solid #2d3748;
      white-space: nowrap;
    }}
    tbody tr {{
      border-bottom: 1px solid #1e2330;
      transition: background 0.15s;
    }}
    tbody tr:hover {{ background: #1e2330; }}
    tbody td {{
      padding: 12px 16px;
      color: #cbd5e1;
      white-space: nowrap;
    }}

    .loan-id {{
      font-family: monospace;
      font-size: 0.8rem;
      color: #60a5fa;
    }}
    .badge {{
      display: inline-block;
      padding: 3px 10px;
      border-radius: 20px;
      font-size: 0.75rem;
      font-weight: 600;
    }}
    .badge.approved {{ background: rgba(52,211,153,0.15); color: #34d399; }}
    .badge.rejected {{ background: rgba(248,113,113,0.15); color: #f87171; }}

    .footer {{
      text-align: center;
      margin-top: 28px;
      color: #475569;
      font-size: 0.8rem;
    }}

    #row-count {{ color: #94a3b8; font-size: 0.85rem; align-self: center; margin-left: auto; }}
  </style>
</head>
<body>

  <div class="header">
    <h1>Loan Approval Dataset</h1>
    <p>614 applicant records — generated with realistic approval logic</p>
  </div>

  <div class="stats">
    <div class="stat-card">
      <div class="value">{total}</div>
      <div class="label">Total Records</div>
    </div>
    <div class="stat-card">
      <div class="value green">{approved}</div>
      <div class="label">Approved</div>
    </div>
    <div class="stat-card">
      <div class="value red">{rejected}</div>
      <div class="label">Rejected</div>
    </div>
    <div class="stat-card">
      <div class="value yellow">{approved*100//total}%</div>
      <div class="label">Approval Rate</div>
    </div>
    <div class="stat-card">
      <div class="value">${avg_income:,}</div>
      <div class="label">Avg Income</div>
    </div>
    <div class="stat-card">
      <div class="value">${avg_loan}K</div>
      <div class="label">Avg Loan</div>
    </div>
    <div class="stat-card">
      <div class="value">{good_credit}%</div>
      <div class="label">Good Credit</div>
    </div>
  </div>

  <div class="search-bar">
    <input type="text" id="searchInput" placeholder="Search any field..." onkeyup="filterTable()"/>
    <label>Status:</label>
    <select id="statusFilter" onchange="filterTable()">
      <option value="">All</option>
      <option value="Approved">Approved</option>
      <option value="Rejected">Rejected</option>
    </select>
    <label>Area:</label>
    <select id="areaFilter" onchange="filterTable()">
      <option value="">All</option>
      <option value="Urban">Urban</option>
      <option value="Semiurban">Semiurban</option>
      <option value="Rural">Rural</option>
    </select>
    <span id="row-count"></span>
  </div>

  <div class="table-wrapper">
    <table id="loanTable">
      <thead>
        <tr>
          <th>Loan ID</th>
          <th>Gender</th>
          <th>Married</th>
          <th>Dependents</th>
          <th>Education</th>
          <th>Self Employed</th>
          <th>Applicant Income</th>
          <th>Coapplicant Income</th>
          <th>Loan Amount</th>
          <th>Term</th>
          <th>Credit</th>
          <th>Property Area</th>
          <th>Status</th>
        </tr>
      </thead>
      <tbody id="tableBody">
        {rows_html}
      </tbody>
    </table>
  </div>

  <div class="footer">
    Generated on 2026-05-17 &nbsp;|&nbsp; Loan Approval Prediction Dataset
  </div>

  <script>
    function filterTable() {{
      const search = document.getElementById('searchInput').value.toLowerCase();
      const status = document.getElementById('statusFilter').value;
      const area   = document.getElementById('areaFilter').value;
      const rows   = document.getElementById('tableBody').getElementsByTagName('tr');
      let visible  = 0;
      for (let r of rows) {{
        const text = r.innerText.toLowerCase();
        const matchSearch = text.includes(search);
        const matchStatus = !status || text.includes(status.toLowerCase());
        const matchArea   = !area   || text.includes(area.toLowerCase());
        r.style.display = (matchSearch && matchStatus && matchArea) ? '' : 'none';
        if (r.style.display === '') visible++;
      }}
      document.getElementById('row-count').innerText = visible + ' rows shown';
    }}
    filterTable();
  </script>

</body>
</html>"""

with open('loan_report.html', 'w') as f:
    f.write(html)

print("Created loan_report.html — open it in your browser!")
