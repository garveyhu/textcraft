from setuptools import setup, find_packages

setup(
    name='langchain_experiment',
    version='0.0.1',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=[
        'fastapi',
        'uvicorn',
        'langchain==0.0.235',
        'openai',
        'python-multipart',
        'tiktoken',
        'websocket-client',
        'transformers',
        'pinecone-client'
    ]
)
