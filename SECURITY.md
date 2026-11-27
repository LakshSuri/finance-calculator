# Security Policy

## Supported Versions

Security maintenance applies to the current version of the main branch and the latest stable release, when available.

## Reporting a Vulnerability

Please report suspected security vulnerabilities through GitHub's private vulnerability reporting feature.

Include the following information:

- A description of the vulnerability.
- The affected module or functionality.
- Steps necessary to reproduce the issue.
- The potential impact.
- Relevant software and dependency versions.

Do not include passwords, authentication tokens, personal financial information, or other sensitive data.

Please avoid publicly disclosing unresolved security vulnerabilities.

## Security Practices

The project incorporates the following development practices:

- Numerical input validation.
- Automated mathematical and application testing.
- Continuous integration through GitHub Actions.
- Version-pinned Python dependencies.
- Automated dependency update proposals.
- Restricted GitHub Actions permissions.
- Local exclusion of calculation history and credentials.
- Separation of mathematical calculations from the application interface.

## Data Privacy

The command-line application stores calculation history locally. This file is excluded from version control.

The web application does not intentionally persist visitor calculation inputs in local history files or an application database.

Users should avoid entering confidential financial information.

## Scope and Limitations

Finance Calculator is an educational financial mathematics project.

The software provides deterministic calculations under hypothetical assumptions and is not intended for financial decision-making, transaction processing, or the storage of sensitive financial records.

Automated testing and security controls reduce certain risks but do not guarantee that the software is free of vulnerabilities.