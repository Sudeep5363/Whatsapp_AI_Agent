"""
Setup configuration for WhatsApp AI Agent Bot
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="whatsapp-ai-agent-bot",
    version="2.0.0",
    author="Sudeep",
    author_email="sudeep@example.com",
    description="Automated WhatsApp bot with AI-powered keyword-based replies",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Sudeep5363/Whatsapp_AI_Agent",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Communications :: Chat",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.8",
    install_requires=[
        "selenium>=4.15.2",
        "webdriver-manager>=4.0.1",
    ],
    entry_points={
        "console_scripts": [
            "whatsapp-bot=whatsapp_bot:main_loop",
            "whatsapp-agent=agent:test_agent",
        ],
    },
    include_package_data=True,
    zip_safe=False,
)
