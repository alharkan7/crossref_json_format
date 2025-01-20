# Contributing to Crossref API JSON Format

First off, thank you for considering contributing to the Crossref API JSON Format project! It's people like you that make this resource valuable for the community.

## How Can I Contribute?

### Reporting Discrepancies

If you find any differences between our JSON models and the actual Crossref API responses:
1. Check that you're using the latest version of the models
2. Create an issue describing:
   - The endpoint you're accessing
   - The expected JSON structure
   - The actual JSON structure you're receiving
   - Any relevant API call details

### Improving Documentation

Documentation improvements are always welcome:
1. Add examples of how to use specific parts of the JSON model
2. Clarify existing documentation
3. Add use cases and best practices

### Enhancing the Scraper

If you want to improve the Python scraping scripts:
1. Fork the repository
2. Create a new branch for your feature
3. Add appropriate error handling and logging
4. Test your changes thoroughly
5. Submit a pull request with a clear description of your changes

## Development Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/crossref_json_model.git
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Install Chrome WebDriver (required for Selenium)

## Running the Scraper

1. Update the chrome_driver_path in the script if necessary
2. Run the scraping script:
   ```bash
   python 1-Get\ JSON\ Raw/crossref_json_model.py
   ```

## Pull Request Process

1. Update the README.md with details of changes if applicable
2. Update the documentation if you're changing functionality
3. Make sure your code follows the existing style
4. Create a pull request with a clear title and description

## Code of Conduct

### Our Pledge

We pledge to make participation in our project a harassment-free experience for everyone, regardless of age, body size, disability, ethnicity, gender identity and expression, level of experience, nationality, personal appearance, race, religion, or sexual identity and orientation.

### Our Standards

Examples of behavior that contributes to creating a positive environment include:
* Using welcoming and inclusive language
* Being respectful of differing viewpoints and experiences
* Gracefully accepting constructive criticism
* Focusing on what is best for the community

### Our Responsibilities

Project maintainers are responsible for clarifying the standards of acceptable behavior and are expected to take appropriate and fair corrective action in response to any instances of unacceptable behavior.

## Questions?

Feel free to create an issue if you have any questions about contributing!
