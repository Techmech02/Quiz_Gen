# Quiz_Gen 📝

> An adaptive **quiz-generation engine** that classifies MCQs by Bloom's level and serves each student the next-best question based on their weak areas.

![Python](https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white)
![PyTorch](https://img.shields.io/badge/PyTorch-EE4C2C?style=flat-square&logo=pytorch&logoColor=white)
![Transformers](https://img.shields.io/badge/Transformers-FFD21E?style=flat-square&logo=huggingface&logoColor=black)
![SQLite](https://img.shields.io/badge/SQLite-07405E?style=flat-square&logo=sqlite&logoColor=white)

---

## ✨ Features

- 🏷️ **MCQ classification** (`models/mcq_classifier.py`) — categorizes questions (topic / Bloom level) using a Transformer model.
- 🎯 **Adaptive selection** (`models/quiz_selector.py`) — tracks each student's answers in SQLite and picks the next question by targeting topics they get wrong.
- 👩‍💼 **Admin tooling** (`scripts/admin_upload.py`, `scripts/admin_interface.py`) — create the MCQ schema and bulk-upload questions from CSV.
- 🧑‍🎓 **Student CLI** (`scripts/student_interface.py`) — runs an interactive quiz session and records progress.

---

## 🗂️ Structure

```
Quiz_Gen/
├── data/admin_mcqs.csv      # Question bank (CSV)
├── models/
│   ├── mcq_classifier.py    # Transformer-based MCQ classifier
│   └── quiz_selector.py     # Adaptive next-question selection + progress tracking
├── scripts/
│   ├── admin_upload.py      # Create tables + load MCQs from CSV
│   ├── admin_interface.py   # Admin entry point
│   └── student_interface.py # Interactive student quiz
└── requirements.txt
```

**Data model** (`mcqs` table): `id, question, option_1..4, answer, topic, bloom_level`; student responses are stored in `student_progress`.

---

## 🚀 Getting started

```bash
git clone https://github.com/Techmech02/Quiz_Gen.git
cd Quiz_Gen

python -m venv venv && source venv/bin/activate
pip install -r requirements.txt        # torch, transformers (sqlite3 ships with Python)

# 1) Initialize DB + upload the question bank
python scripts/admin_upload.py

# 2) Take an adaptive quiz
python scripts/student_interface.py
```

> Note: `requirements.txt` lists `sqlite3`, which is part of the Python standard library — no separate install is needed.

---

## 🧩 Related

- **[PARAKH-ML-MODEL](https://github.com/Techmech02/PARAKH-ML-MODEL)** & **[Parakh-DL](https://github.com/Techmech02/Parakh-DL)** — the larger PARAKH adaptive-assessment platform this prototype fed into.

---

<sub>Built by <a href="https://github.com/Techmech02">@Techmech02</a>.</sub>
