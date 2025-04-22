from setuptools import setup, find_packages

setup(
    name='sales-chatbot',
    version='0.1.0',
    description='A chatbot for sales assistance',
    author='Your Name',
    author_email='your.email@example.com',
    packages=find_packages(),
    install_requires=[
        'openai',
        'python-dotenv',
        'flask',
        'pytest',
    ],
    python_requires='>=3.8',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
    ],
)