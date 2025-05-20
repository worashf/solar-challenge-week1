# Solar Dashboard Deployment Guide

## Requirements
- Python 3.10+
- Streamlit
- Pandas, Matplotlib, Seaborn

## Installation
```bash
pip install -r requirements.txt
```

## Running Locally
```bash
streamlit run app/main.py
```

## Deployment to Streamlit Cloud
1. Create a new app in [Streamlit Community Cloud](https://share.streamlit.io/)
2. Connect your GitHub repository
3. Set main file path to `app/main.py`
4. Deploy!

## Folder Structure
```
├── app/
│   ├── main.py         # Dashboard entry point
│   ├── utils.py        # Data processing
└── data/               # CSV datasets (gitignored)
```