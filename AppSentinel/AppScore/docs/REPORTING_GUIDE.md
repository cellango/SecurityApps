# Security Score Card - Reporting Guide

Authors: Clement Ellango, Carolina Clement  
Copyright (c) 2024. All rights reserved.

## Overview

The Security Score Card system provides comprehensive reporting capabilities to help teams and security analysts track and analyze security metrics across applications. This guide explains the available reports, their contents, and how to generate them.

## Available Reports

### 1. Team Report

The Team Report provides a comprehensive view of all applications belonging to a specific team, including their security scores and recent history.

**Contents:**
- Team details
- List of all applications
- Current security scores
- Score history (last 5 entries per application)
- Last assessment dates

**Access Methods:**
```bash
# JSON Format
GET /api/reports/team/{team_name}

# PDF Format
GET /api/reports/team/{team_name}?format=pdf
```

### 2. Application Report

The Application Report provides detailed security information about a specific application.

**Contents:**
- Application details
- Team association
- Current security score
- Complete score history
- Last assessment date
- Security metrics

**Access Methods:**
```bash
# JSON Format
GET /api/reports/application/{application_id}

# PDF Format
GET /api/reports/application/{application_id}?format=pdf
```

### 3. Vulnerability Report

The Vulnerability Report focuses on security vulnerabilities and findings for a specific application. This report is available in multiple formats to facilitate different use cases.

**Contents:**
- Application identification
- Team information
- List of vulnerabilities
  - Severity levels
  - Descriptions
  - Discovery dates
  - Current status
- Risk metrics

**Access Methods:**
```bash
# JSON Format
GET /api/reports/vulnerabilities/{application_id}

# PDF Format
GET /api/reports/vulnerabilities/{application_id}?format=pdf

# CSV Format
GET /api/reports/vulnerabilities/{application_id}?format=csv
```

## Using the Reports

### Command Line Examples

1. Generate a Team Report:
```bash
# Get JSON response
curl http://localhost:5000/api/reports/team/Engineering

# Download PDF
curl http://localhost:5000/api/reports/team/Engineering?format=pdf -o engineering_team_report.pdf
```

2. Generate an Application Report:
```bash
# Get JSON response
curl http://localhost:5000/api/reports/application/123

# Download PDF
curl http://localhost:5000/api/reports/application/123?format=pdf -o application_report.pdf
```

3. Generate a Vulnerability Report:
```bash
# Get JSON response
curl http://localhost:5000/api/reports/vulnerabilities/123

# Download PDF
curl http://localhost:5000/api/reports/vulnerabilities/123?format=pdf -o vulnerabilities.pdf

# Download CSV
curl http://localhost:5000/api/reports/vulnerabilities/123?format=csv -o vulnerabilities.csv
```

### API Response Formats

#### JSON Format
All reports are available in JSON format by default. This is useful for:
- Integrating with other tools
- Custom processing of report data
- Building custom visualizations

#### PDF Format
PDF reports are formatted for readability and include:
- Professional formatting
- Clear section headers
- Tables and lists
- Report metadata (generation date, report type)

#### CSV Format (Vulnerability Report Only)
The CSV format is specifically available for vulnerability reports to facilitate:
- Import into spreadsheet applications
- Data analysis
- Integration with email systems
- Bulk processing of vulnerability data

## Best Practices

1. **Report Generation**
   - Generate reports during off-peak hours for large teams
   - Cache report results when possible
   - Use appropriate formats for your use case

2. **Data Usage**
   - Store downloaded reports securely
   - Regularly generate reports for compliance purposes
   - Use CSV format for data analysis
   - Use PDF format for sharing with stakeholders

3. **Automation**
   - Set up automated report generation for regular reviews
   - Use the JSON format for automated processing
   - Implement automated alerts based on report findings

## Troubleshooting

Common issues and solutions:

1. **Report Generation Fails**
   - Verify team name or application ID exists
   - Check API endpoint URL
   - Ensure proper authentication

2. **PDF Generation Issues**
   - Check available disk space
   - Verify file permissions
   - Ensure proper encoding for special characters

3. **CSV Format Issues**
   - Check for special characters in data
   - Verify file extension
   - Use proper CSV parsing libraries

## Support

For additional support or to report issues with the reporting system:
1. Submit an issue in the project repository
2. Contact the security team
3. Check the API documentation for updates

## Future Enhancements

Planned enhancements for the reporting system:
1. Additional export formats (Excel, HTML)
2. Custom report templates
3. Scheduled report generation
4. Email integration for automated report distribution
5. Interactive dashboard views
