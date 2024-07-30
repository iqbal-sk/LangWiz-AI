# LangWiz-AI

## Language Translation Project

### Description

This project is focused on building a language translation system using data from Europarl and WMT Chat Task datasets. It involves extracting, transforming, and pre-processing data, followed by training machine translation models. The project leverages DVC (Data Version Control) for managing data and pipeline steps, ensuring reproducibility. The experiments and evaluations are conducted within the research folder.

### Features

- Data extraction and transformation pipelines using DVC
- Preprocessing and tokenization of French, German, and Bulgarian datasets
- Training of machine translation models
- Evaluation metrics including BLEU and SACREBLEU scores

### Requirements

- Python 3.11
- DVC 3.51
- Git

### Steps

1. Clone the repository:
    ```bash
    git clone https://github.com/iqbal-sk/LangWiz-AI
    cd your-project-directory
    ```
2. Create and activate a virtual environment:
    ```bash
    python -m venv venv
    source venv/bin/activate
    ```
3. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```
4. Install DVC, Initialize and Data Extraction:
    ```bash
    pip install dvc
    dvc init
    dvc repro
    ```

In the **research** directory we have uploaded all the experiments we performed for Language Translation Task.
