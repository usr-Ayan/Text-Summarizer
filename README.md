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