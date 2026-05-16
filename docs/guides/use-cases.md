# Use Cases

## 1. Product & Batch Traceability

Register every product with SKU and category. Create production batches linked to products. Track quantity produced, status (in_production → in_qa → passed / failed → shipped), and production dates.

## 2. Inspection Logging

Quality inspectors log checks per batch:
- Visual inspection, dimensional checks, functional tests, etc.
- Result: **pass**, **fail**, or **pending**
- Inspector name and timestamp for full audit trail

## 3. AI-Powered Defect Classification

When a defect is found, describe it in natural language:
> *"deep scratch on polished aluminum surface after CNC operation"*

The AI engine returns:
- **Defect type:** `surface_scratch`
- **Severity:** `low`
- **Recommended action:** *Review polishing process; check conveyor belt for debris.*
- **Confidence score:** 85%

This accelerates root-cause analysis and standardizes defect taxonomy across teams.

## 4. Real-Time Quality Dashboard

The dashboard aggregates live data:
- Total inspections & pass rate
- Defects by severity (low / medium / high / critical)
- Top defect types ranked by frequency
- Batches by status distribution
- Recent inspections table

No manual spreadsheet updates. No mock data. Every number comes from the database.

## 5. Zero-to-Value in 48 Hours

1. Spin up with `docker compose up`
2. Add your first product
3. Create a batch and run an inspection
4. Log a defect with AI suggest
5. Share the dashboard with stakeholders

## Industry Fit

- **Mid-market manufacturers** (100–2,000 employees)
- **Contract manufacturers** managing multiple product lines
- **Quality consulting firms** deploying standardized QMS templates
