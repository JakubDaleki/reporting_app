import pytest
from datetime import datetime
from services.report_generator import ReportGenerator
from models.report import Report


@pytest.fixture()
def report_gen():
    return ReportGenerator()


def test_future_date(report_gen):
    """Check if report is empty for future date"""
    date_format = "%Y-%m-%d"
    report_date = datetime.strptime("2030-08-01", date_format).date()
    assert report_gen.generate(report_date) == Report()


def test_existing_date(report_gen):
    """Check if the date that exists in csv generates non-empty report"""
    date_format = "%Y-%m-%d"
    report_date = datetime.strptime("2019-08-01", date_format).date()
    assert report_gen.generate(report_date) != Report()


def test_customer_count(report_gen):
    """Check if customer count for past date is correct"""
    date_format = "%Y-%m-%d"
    report_date = datetime.strptime("2019-08-01", date_format).date()
    assert report_gen.generate(report_date).customers == 9


def test_too_old_date(report_gen):
    """Check if report is empty for future date"""
    date_format = "%Y-%m-%d"
    report_date = datetime.strptime("1900-01-01", date_format).date()
    assert report_gen.generate(report_date) == Report()