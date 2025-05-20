##  FinPlanAI – Intelligent Financial Planning Dashboard

FinPlanAI is a modular Streamlit-based web app that enables users to perform advanced financial analysis including budgeting, forecasting, investment analysis, capital budgeting, and dividend reinvestment simulations. It supports data uploads, interactive charts, and downloadable reports.

---

###  Features

* **Budget Planner**: Visualize income, expenses, and savings.
* **Financial Forecasting**: Predict future budgets with customizable growth rates.
* **Investment Analysis**: Calculate ROI, CAGR, visualize performance.
* **Capital Budgeting**: Run NPV, IRR, and Monte Carlo simulations.
* **Dividend Simulator**: Project reinvested vs. cash-out scenarios.
* **Summary Report**: Downloadable, aggregated insights across all modules.

---

###  Technologies Used

* Python
* [Streamlit](https://streamlit.io/)
* Pandas
* Plotly

---

###  Project Structure

```
FinPlanAI/
├── app.py
├── modules/
│   ├── budget_planner.py
│   ├── forecasting.py
│   ├── investment_analysis.py
│   ├── capital_budgeting.py
│   ├── dividend_simulation.py
│   └── summary_report.py
├── utils/
│   └── file_handler.py
├── sample_data/
│   ├── budget.csv
│   ├── investments.csv
│   ├── projects.csv
│   └── dividends.csv
└── README.md
```

---

###  Installation

1. Clone the repo:

```bash
git clone https://github.com/MillicentPatrick/FinPlanAI.git
cd FinPlanAI
```

2. Create a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Run the app:

```bash
streamlit run app.py
```

---

###  Sample Data

Sample CSV files are located in the `sample_data/` folder for testing all modules.

---

###  Deployment

You can deploy this app using [Streamlit Cloud](https://streamlit.io/cloud) or any platform supporting Python web apps.

---

###  License

This project is licensed under the MIT License. Feel free to use, modify, and distribute with attribution.
