# PaySim Mobile Money Fraud Investigation
### A SQL-Based Fraud Analytics Portfolio Project

> "I Know How Criminals Think. I Build Systems That Catch Them."

---

### Project Overview

Mobile money in Kenya (such as M-Pesa) process millions of transactions daily, but fraud remains a persistent threat. This project investigates transaction data from the PaySim synthetic dataset to answer one question: How does fraud actually happen in a mobile money ecosystem, and why does the current detection system fail to catch it? The analysis moves from understanding normal transaction behavior to identifying fraud patterns, profiling victims, and evaluating system performance.

### Dataset

PaySim is a synthetic mobile money transaction dataset modeled on real M-Pesa logs. It contains 6,362,620 transactions across 31 days (744 hourly steps). Each transaction includes type (CASH_IN, CASH_OUT, TRANSFER, PAYMENT, DEBIT), amount, sender and receiver balances before and after, and two flags: isFraud (actual fraud) and isFlaggedFraud (system detection). The data is synthetic but designed to mirror real-world behavior.

### Project Structure

- **Chapter 1 — Scene Setting:** Establishes normal transaction patterns (volume, value, time)
- **Chapter 2 — Crime Discovery:** Identifies scale and distribution of fraud across transaction types
- **Chapter 3 — Pattern Analysis:** Examines balance behavior, amount structuring, and mule accounts
- **Chapter 4 — Victim Profile:** Profiles who gets targeted and the financial impact distribution
- **Chapter 5 — System Response:** Evaluates detection system performance using confusion matrix metrics
- **Chapter 6 — Conclusions and Recommendations:** Synthesizes findings and proposes actionable changes

### Key Findings

- **Chapter 1:** The normal ecosystem is dominated by CASH_OUT and PAYMENT (69% of all transactions combined), but TRANSFER carries the highest average value (KSh 910,647) — fraudsters later exploit TRANSFER precisely because it is designed for high-value movement.

- **Chapter 2:** Fraud is 100% concentrated in TRANSFER and CASH_OUT — zero fraud occurs in PAYMENT, DEBIT, or CASH_IN — confirming fraud follows a deliberate two-stage sequence: move money first, then withdraw it.

- **Chapter 3:** Fraudulent transactions drain 88% of victim account balances on average, hit the exact system limit of KSh 10 million, and include zero-value probes — clear evidence fraudsters test and exploit system rules.

- **Chapter 4:** The top 8.99% of victims (those losing over KSh 5 million) account for roughly half of all fraud losses (KSh 6.06 billion) — fraud harm is concentrated, not evenly distributed.

- **Chapter 5:** The detection system catches only 16 out of 8,213 fraud cases (0.19% recall) — despite 99.87% accuracy, the system is functionally blind to almost all actual fraud.

### Tools Used

- **MySQL** — Data storage and SQL queries for aggregation and filtering
- **Jupyter Notebook** — Interactive environment for markdown documentation and SQL execution
- **SQL (%%sql magic)** — All analysis performed using SQL queries with CASE WHEN statements for conditional aggregation
- **Python** — Database connection module (db_connect.py) and environment management

### How to Run
1. Clone this repository
2. Load `data/paysim.csv` into MySQL as table `paysim` 
   using LOAD DATA INFILE or MySQL Workbench import wizard
3. Open any notebook in the `notebooks/` folder
4. In the first code cell run:
```python
   from db_connect import connect_to_db
   engine, conn = connect_to_db()
```
5. Enter your MySQL database name and password when prompted
6. Open notebooks in order from `01_scene_setting.ipynb` 
   to `06_conclusions.ipynb`

### Author

**Vincent Kiptoo**

- Background: Criminology and Penology degree + ALX Data Analytics certification
- Focus: Bridging behavioral criminology with transaction data analysis for fraud detection

[LinkedIn](https://www.linkedin.com/in/vincentkiptoo/) | 
[GitHub](https://github.com/Vincent-kiptoo)