# Crossref API JSON Format

This repository contains the complete JSON format specification for the Crossref API, which is essential for making advanced custom API calls. The models have been scraped from the official Crossref API documentation at [api.crossref.org/swagger-ui](https://api.crossref.org/swagger-ui/index.html#/).

## Why This Repository?

While Crossref provides excellent API services, comprehensive documentation of their JSON format structure can be challenging to find. This repository aims to fill that gap by providing:

- Complete JSON format models for all Crossref API endpoints
- A reference for developers working with Crossref API responses
- Python scripts to update the models by scraping the latest documentation

## Contents

- `Crossref API JSON Format.json` - The main JSON format specification
- Python scraping scripts to update the models
- Additional documentation and examples

## Usage

You can use these JSON models as a reference when:
- Parsing Crossref API responses
- Building type-safe API clients
- Understanding the structure of Crossref's data model
- Creating strongly-typed interfaces for your applications

## Updating the Models

The repository includes Python scripts that can scrape the latest version of the JSON format from Crossref's official documentation. You can run these scripts to ensure you're working with the most up-to-date model:

1. Navigate to the scripts directory
2. Run the Python scraper
3. The JSON models will be updated automatically

## Contributing

Contributions are welcome! Here are some ways you can help:
- Improve the documentation
- Enhance the scraping scripts
- Add examples and use cases
- Report any discrepancies between the models and actual API responses
- Suggest additional features or improvements

## License

[MIT License](LICENSE)

## Disclaimer

This is an unofficial repository and is not affiliated with or endorsed by Crossref. The JSON models are derived from publicly available API documentation.
