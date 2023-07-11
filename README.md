## Reporting application for Suade Labs

Install required packages:

```shell
python3 -m pip install -r requirements.txt'
```

To run the app open app directory and to run:

```shell
uvicorn main:app --reload
```

Visit http://localhost:8000/api/report/2019-08-01 to view report for 2019-08-01

To run tests run:

```shell
python3 -m pytest
```
