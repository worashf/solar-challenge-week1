name: CI  
on: [push, pull_request]  
jobs:  
  test:  
    runs-on: ubuntu-latest  
    steps:  
      - uses: actions/checkout@v4  
      - uses: actions/setup-python@v4  
        with:  
          python-version: "3.12.7"  
      - run: pip install -r requirements.txt  
      - run: python --version  