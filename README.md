#text summarizer


## ##workflows 

1.update config.yaml
2.update params.yaml
3.update entity.yaml
4.update the configuration manager in src config
5.update the components
6.update the pipeline
7.update our main.py
8.update the app.py
## deployment guideline
1.build dockerimage of my source code
2.push your docker image to ecr
3.launch your ec2 machine
4.pull your image from ecr to ec2
5.launch your docker image to ec2


# AWS-CICD-Deployment-with-Github-Actions
## 1. Login to AWS console.
## 2. Create IAM user for deployment
#with specific access

1. EC2 access : It is virtual machine

2. ECR: Elastic Container registry to save your docker image in aws


#Description: About the deployment

1. Build docker image of the source code

2. Push your docker image to ECR

3. Launch Your EC2 

4. Pull Your image from ECR in EC2

5. Lauch your docker image in EC2

#Policy:

1. AmazonEC2ContainerRegistryFullAccess

2. AmazonEC2FullAccess
## 3. Create ECR repo to store/save docker image
- Save the URI: 622004254418.dkr.ecr.eu-north-1.amazonaws.com/text-s
## 4. Create EC2 machine (Ubuntu)
## 5. Open EC2 and Install docker in EC2 Machine:
#optinal

sudo apt-get update -y

sudo apt-get upgrade

#required

curl -fsSL https://get.docker.com -o get-docker.sh

sudo sh get-docker.sh

sudo usermod -aG docker ubuntu

newgrp docker
## 6. Configure EC2 as self-hosted runner:
setting>actions>runner>new self hosted runner> choose os> then run command one by one
## 7. Setup github secrets:
AWS_ACCESS_KEY_ID=

AWS_SECRET_ACCESS_KEY=

AWS_REGION = us-east-1

AWS_ECR_LOGIN_URI = demo>>  566373416292.dkr.ecr.ap-south-1.amazonaws.com

ECR_REPOSITORY_NAME = simple-app



















<!-- 
// -->
## project overview
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
