# SPL-Analytics-ML-Approach

In this project, we apply a range of machine learning techniques to analyze over two decades of football data from the Saudi Professional League (SPL), starting from the year 2000. Our goal is to build a functional system that provides data-driven predictions.

## Project Title

Predictive Analytics for the Saudi Professional League (SPL), 2000–Present

## Motivation

The aim of this project is to apply machine learning methods introduced in class to a real-world problem by building a functional advice/action-suggestion system. We focus on the Saudi Professional League (SPL) to generate actionable guidance—such as match outcome expectations, opponent-specific tactics, or lineup insights—grounded in historical data and model outputs.

We will develop the system incrementally over five phases:

1. Problem Understanding and Data Exploration: Define the scope of the advice system for football analytics; collect and explore SPL datasets (≥ several hundred rows); handle missing values, engineer features (e.g., form, head-to-head, venue effects), and visualize relationships; ensure the data can be read and processed in Python or R.
2. Supervised Learning: Train and compare models for classification (e.g., match result) and regression (e.g., goals/points); quantify performance with appropriate metrics (accuracy, log-loss, MAE, etc.).
3. Unsupervised Learning: Discover segments and styles (teams/players/tactics) via clustering or dimensionality reduction to enrich recommendations.
4. Integrating Generative AI: Convert model outputs and uncertainties into clear, context-aware natural-language advice and explanations.
5. Final Submission and Presentation: Organize phase deliverables in this GitHub repo for easy review and present the final system and findings.

Across phases, we will evaluate and compare alternative approaches, integrate them into a robust pipeline, and prioritize interpretability and reproducibility. The repository will be structured to reflect phase-wise progress and facilitate instructor review.

## Group Members

| Name                  | Student ID |
| --------------------- | ---------- |
| Faisal AlBader        | 443102460  |
| Monther Mohsen Batais | 443106846  |
| Khaled Mohammed Alawi | 443106841  |

## Dataset

- Source CSVs: `Dataset/Saudi-Professional-League-Datasets-master/Saudi-Professional-League-Datasets-master/*.csv`
- Compiled raw file: `Dataset/SPL_raw.csv` (union of all source CSVs; preserves original columns; adds season metadata: `season_label`, `season_start_year`, `season_end_year`, `stage`, `source_file`).
- Normalized file: `Dataset/SPL_raw_normalized.csv` (consistent schema across seasons with columns: `match_id,date,time,home_team,away_team,home_score,away_score,stadium,city,round,referee_name,attendance,season_label,season_start_year,season_end_year,stage,source_file`).

To regenerate the compiled and normalized datasets:

```powershell
python ".\scripts\merge_spl_csvs.py"
```

## Quick Start

1. **Set up dependencies**
   ```powershell
   python -m pip install -r requirements.txt
   ```
2. **Regenerate data artifacts (optional)** using the command above.
3. **Explore Phase 01 notebook**: open `Phase01_Data_Exploration.ipynb` to review dataset goals, EDA, and preprocessing steps.

## Repository Structure

- `Dataset/` – raw SPL CSVs and generated aggregates.
- `scripts/merge_spl_csvs.py` – merges yearly CSVs and creates normalized dataset.
- `scripts/print_versions.py` – helper to record installed library versions.
- `Phase01_Data_Exploration.ipynb` – Phase 1 deliverable covering goal, EDA, and preprocessing.
- `requirements.txt` – pinned Python packages used across notebooks/scripts.
- `SWE485 Project Description (ML) Fall 25.pdf` – course project brief.

## Phase Deliverables (Completed)

- **Phase 1**
  - Documented dataset goal and provenance.
  - Computed descriptive statistics and visualized distributions, missing values, and class balance.
  - Established preprocessing pipeline (null handling, typing, derived outcomes).

## Roadmap

- **Phase 2**: Train supervised models (classification/regression) and benchmark metrics.
- **Phase 3**: Apply unsupervised learning for segmentation and tactic discovery.
- **Phase 4**: Integrate generative AI components for narrative insights.
- **Phase 5**: Final integration, evaluation, and presentation package.

## References

- Saudi Professional League Datasets (FS/SS feeds): https://github.com/alitif/Saudi-Professional-League-Datasets
