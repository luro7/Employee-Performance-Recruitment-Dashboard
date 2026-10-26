"""Build configuration for the reusable employee_events Python package."""

from pathlib import Path

from setuptools import find_packages, setup


HERE = Path(__file__).resolve().parent

setup(
    name="employee_events",
    version="0.1.0",
    description="SQLite query API for employee and team performance data",
    packages=find_packages(),
    include_package_data=True,
    package_data={"employee_events": ["employee_events.db"]},
    install_requires=["pandas>=2.2,<3"],
    python_requires=">=3.10",
)
