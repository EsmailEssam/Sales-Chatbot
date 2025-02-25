from setuptools import setup, find_packages

setup(
    name="sales agent",
    version="0.1.0",
    author="Your Name",
    author_email="your_email@example.com",
    description="A brief description of your project",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/your_project",
    packages=find_packages(),
    install_requires=[
        "numpy",  # List dependencies here
        "pandas",
    ],
    python_requires=">=3.10",
)
