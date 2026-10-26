"""Build and install the employee_events SQL package."""

from setuptools import find_packages, setup


setup(
    name="employee_events",
    version="1.0.0",
    description="Reusable SQLite employee and team data API",
    packages=find_packages(),
    include_package_data=True,
    package_data={"employee_events": ["employee_events.db"]},
    install_requires=["pandas>=2.2,<3"],
    python_requires=">=3.10",
)
