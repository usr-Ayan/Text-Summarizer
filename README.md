#text summarizer


##workflows 

1.update config.yaml
2.update params.yaml
3.update entity.yaml
4.update the configuration manager in src config
5.update the components
6.update the pipeline
7.update our main.py
8.update the app.py
 


 Raw Data → Ingestion → Validation → Transformation → Training → Evaluation
                                             ↓
                                    Fine-tuned Pegasus Model
                                             ↓
                                   FastAPI Backend API
                                             ↓
                                   Streamlit Web UI



| Folder                 | Purpose                                       |
| ---------------------- | --------------------------------------------- |
| `data_ingestion/`      | Raw dataset download & extraction             |
| `data_validation/`     | Dataset integrity checks                      |
| `data_transformation/` | Tokenized & preprocessed dataset              |
| `model_trainer/`       | **Your fine-tuned Pegasus model & tokenizer** |
| `model_evaluation/`    | ROUGE metrics & evaluation outputs            |



🧠 1. What “Summary Length (words)” really means

The slider value (e.g. 183) is not a hard word limit.
It is your target length that the model tries to approximate using these bounds:

min_length = int(target_words * 0.7)
max_length = int(target_words * 1.3)


So when your slider shows:

Summary Length (words): 183


The model is actually allowed to generate between:

min_length ≈ 128
max_length ≈ 237





<!-- folder structure explanation -->


This is actually a **very clean, production-grade ML project structure**.
Let me walk you through it in a way that makes the architecture *click*.

---

# 🧱 Big Picture

Your project follows a **modular ML pipeline architecture**:

```
Research Notebooks  →  Reusable Components  →  Pipeline Stages  →  Artifacts
```

So you experiment in notebooks, then lock the logic into Python modules, and finally run everything as a reproducible pipeline.

---

# 🗂 Root Level

```
artifacts/        → All generated outputs (data, models, metrics)
config/           → Static configuration files
research/         → Experimental notebooks
src/textSummarizer/ → Your actual Python package
main.py           → Pipeline entry point
params.yaml       → Hyperparameters
app.py / ui.py    → Application layer
```

This separation is exactly how serious ML systems are built.

---

# 🧪 `research/` — Experiment Zone

```
research/
 ├─ 01_data_ingestion.ipynb
 ├─ 02_data_validation.ipynb
 ├─ 03_data_transformation.ipynb
 ├─ 04_model_trainer.ipynb
 ├─ 05_model_evaluation.ipynb
```

These are **development notebooks**.
Once logic is correct here, you port it into Python modules inside `src/`.

---

# 🧠 `src/textSummarizer/` — Core Library

This is your **real application code**.

## 🔹 `components/`

Each file is one pipeline stage's business logic:

```
data_ingestion.py      → downloads / loads dataset
data_validation.py     → checks schema, file integrity
data_transformation.py → tokenization, preprocessing
model_trainer.py       → training logic
model_evaluation.py    → metrics computation
```

These contain **pure functions/classes**, no orchestration.

---

## 🔹 `entity/`

Contains **dataclasses** (schemas/contracts):

```
ModelTrainerConfig
DataIngestionConfig
DataValidationConfig
...
```

They define *what configuration looks like*.

---

## 🔹 `config/`

Contains **ConfigurationManager**:

```
configuration.py
```

This is the bridge between YAML files and Python dataclasses.

It reads:

* `config.yaml`
* `params.yaml`

and produces:

* `DataIngestionConfig`
* `ModelTrainerConfig`
* etc.

---

## 🔹 `pipeline/`

This is the **orchestrator**:

```
stage_01_data_ingestion.py
stage_02_data_validation.py
stage_03_data_transformation.py
stage_04_model_trainer.py
stage_05_model_evaluation.py
```

Each stage:

1. Loads config
2. Creates the proper component
3. Executes it
4. Writes artifacts

---

## 🔹 `utils/`

Reusable helpers:

* file IO
* logging
* common utilities

---

## 🔹 `constants/`

Holds static constants (paths, keys, etc.)

---

# 📦 `artifacts/` — Everything Your Pipeline Produces

```
artifacts/
 ├─ data_ingestion/
 │   └─ samsum_dataset/
 ├─ data_transformation/
 │   └─ samsum_dataset/
 ├─ model_trainer/
 │   └─ pegasus-samsum-model/
 │   └─ pegasus-samsum-tokenizer/
 └─ model_evaluation/
     └─ metrics.csv
```

This directory is **fully reproducible output**.
Delete it → run `main.py` → everything rebuilds.

---

# 🧬 How Everything Connects

```
main.py
  ↓
pipeline/stage_01_data_ingestion.py
  ↓
components/data_ingestion.py
  ↓
writes to artifacts/
  ↓
stage_02_data_validation.py
  ↓
...
```

So:

> **Notebooks = where you design**
> **Components = where logic lives**
> **Pipeline = how the system runs**
> **Artifacts = what the system produces**

---

# 🧾 Interview-Level Summary

> This project follows a layered ML architecture:
> research notebooks for experimentation, reusable components for business logic, pipeline stages for orchestration, configuration management for reproducibility, and an artifacts directory for versioned outputs.

---

If you want, next I can show you **exactly where and how to replace the SAMSum dataset with IN-ABS** in this architecture so your whole pipeline becomes a legal summarizer.
