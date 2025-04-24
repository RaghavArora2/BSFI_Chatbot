# Sample Insurance Policies Directory

This directory contains sample insurance policy documents that are used as the knowledge base for the AI-powered insurance policy chatbot.

## Files

The following PDF files will be generated automatically by the application if they don't exist:

- `auto_insurance.pdf`: Contains information about auto insurance coverage, premiums, and claims process
- `health_insurance.pdf`: Contains information about health insurance plans, coverage options, and enrollment
- `home_insurance.pdf`: Contains information about home insurance coverage, premiums, and claims process
- `life_insurance.pdf`: Contains information about life insurance policy types, premiums, and benefits

## How It Works

When the application starts, it checks for the existence of these PDF files. If they don't exist, it automatically generates them using the built-in content template in the `document_processor.py` module.

You can replace these sample files with actual insurance policy documents to customize the knowledge base according to your specific needs.
