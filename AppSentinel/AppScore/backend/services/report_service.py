"""
Security Score Card - Reporting Service

Provides comprehensive reporting functionality including team reports,
application reports, and vulnerability reports with various output formats.

Authors:
    Clement Ellango
    Carolina Clement

Copyright (c) 2024. All rights reserved.
"""

from typing import Dict, List
import pandas as pd
from datetime import datetime
from fpdf import FPDF
import csv
import io
from models.application import Application
from models.team import Team
from models.score_history import ScoreHistory
from sqlalchemy.orm import Session
from sqlalchemy import desc

class ReportService:
    def __init__(self, session: Session):
        self.session = session

    def generate_team_report(self, team_name: str) -> Dict:
        """Generate a detailed report for all applications in a team."""
        team = self.session.query(Team).filter(Team.name == team_name).first()
        if not team:
            raise ValueError(f"Team {team_name} not found")

        applications = team.applications.all()
        report_data = {
            "team_name": team.name,
            "report_date": datetime.utcnow().isoformat(),
            "applications": []
        }

        for app in applications:
            app_data = {
                "name": app.name,
                "description": app.description,
                "security_score": app.security_score,
                "last_scored": app.last_scored.isoformat() if app.last_scored else None,
                "score_history": [
                    {
                        "score": sh.score,
                        "date": sh.created_at.isoformat()
                    } for sh in app.score_history.order_by(desc(ScoreHistory.created_at)).limit(5)
                ]
            }
            report_data["applications"].append(app_data)

        return report_data

    def generate_application_report(self, app_id: int) -> Dict:
        """Generate a detailed report for a specific application."""
        app = self.session.query(Application).filter(Application.id == app_id).first()
        if not app:
            raise ValueError(f"Application with ID {app_id} not found")

        report_data = {
            "application_name": app.name,
            "description": app.description,
            "team": app.team.name,
            "current_score": app.security_score,
            "last_scored": app.last_scored.isoformat() if app.last_scored else None,
            "score_history": [
                {
                    "score": sh.score,
                    "date": sh.created_at.isoformat()
                } for sh in app.score_history.order_by(desc(ScoreHistory.created_at)).all()
            ],
            "report_date": datetime.utcnow().isoformat()
        }

        return report_data

    def generate_vulnerability_report(self, app_id: int) -> Dict:
        """Generate a vulnerability report for a specific application."""
        app = self.session.query(Application).filter(Application.id == app_id).first()
        if not app:
            raise ValueError(f"Application with ID {app_id} not found")

        # This would be expanded to include actual vulnerability data from security tools
        report_data = {
            "application_name": app.name,
            "team": app.team.name,
            "vulnerabilities": [
                {
                    "severity": "Critical",
                    "description": "SQL Injection vulnerability in login form",
                    "discovered_date": "2024-01-01",
                    "status": "Open"
                },
                # Add more sample vulnerabilities
            ],
            "report_date": datetime.utcnow().isoformat()
        }

        return report_data

    def convert_to_pdf(self, report_data: Dict, report_type: str) -> bytes:
        """Convert report data to PDF format."""
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)

        # Add title
        pdf.set_font("Arial", "B", 16)
        title = f"{report_type} Report"
        pdf.cell(200, 10, txt=title, ln=1, align="C")
        
        # Add report date
        pdf.set_font("Arial", size=10)
        pdf.cell(200, 10, txt=f"Generated on: {report_data['report_date']}", ln=1, align="L")

        # Add content based on report type
        if report_type == "Team":
            self._add_team_report_content(pdf, report_data)
        elif report_type == "Application":
            self._add_application_report_content(pdf, report_data)
        elif report_type == "Vulnerability":
            self._add_vulnerability_report_content(pdf, report_data)

        return pdf.output(dest='S').encode('latin-1')

    def convert_to_csv(self, report_data: Dict, report_type: str) -> bytes:
        """Convert report data to CSV format."""
        output = io.StringIO()
        writer = csv.writer(output)

        if report_type == "Vulnerability":
            # Write headers
            writer.writerow(["Application", "Severity", "Description", "Discovered Date", "Status"])
            
            # Write vulnerability data
            for vuln in report_data["vulnerabilities"]:
                writer.writerow([
                    report_data["application_name"],
                    vuln["severity"],
                    vuln["description"],
                    vuln["discovered_date"],
                    vuln["status"]
                ])

        return output.getvalue().encode('utf-8')

    def _add_team_report_content(self, pdf: FPDF, data: Dict):
        """Add team report specific content to PDF."""
        pdf.set_font("Arial", "B", 14)
        pdf.cell(200, 10, txt=f"Team: {data['team_name']}", ln=1, align="L")

        for app in data["applications"]:
            pdf.set_font("Arial", "B", 12)
            pdf.cell(200, 10, txt=f"Application: {app['name']}", ln=1, align="L")
            
            pdf.set_font("Arial", size=10)
            pdf.cell(200, 10, txt=f"Security Score: {app['security_score']}", ln=1, align="L")
            pdf.cell(200, 10, txt=f"Last Scored: {app['last_scored']}", ln=1, align="L")
            pdf.cell(200, 10, txt="", ln=1, align="L")  # Add spacing

    def _add_application_report_content(self, pdf: FPDF, data: Dict):
        """Add application report specific content to PDF."""
        pdf.set_font("Arial", "B", 14)
        pdf.cell(200, 10, txt=f"Application: {data['application_name']}", ln=1, align="L")
        
        pdf.set_font("Arial", size=10)
        pdf.cell(200, 10, txt=f"Team: {data['team']}", ln=1, align="L")
        pdf.cell(200, 10, txt=f"Current Score: {data['current_score']}", ln=1, align="L")
        pdf.cell(200, 10, txt=f"Last Scored: {data['last_scored']}", ln=1, align="L")

        # Add score history
        pdf.set_font("Arial", "B", 12)
        pdf.cell(200, 10, txt="Score History", ln=1, align="L")
        
        for history in data['score_history']:
            pdf.set_font("Arial", size=10)
            pdf.cell(200, 10, txt=f"Date: {history['date']}, Score: {history['score']}", ln=1, align="L")

    def _add_vulnerability_report_content(self, pdf: FPDF, data: Dict):
        """Add vulnerability report specific content to PDF."""
        pdf.set_font("Arial", "B", 14)
        pdf.cell(200, 10, txt=f"Application: {data['application_name']}", ln=1, align="L")
        
        pdf.set_font("Arial", size=10)
        pdf.cell(200, 10, txt=f"Team: {data['team']}", ln=1, align="L")

        # Add vulnerabilities
        pdf.set_font("Arial", "B", 12)
        pdf.cell(200, 10, txt="Vulnerabilities", ln=1, align="L")
        
        for vuln in data['vulnerabilities']:
            pdf.set_font("Arial", "B", 10)
            pdf.cell(200, 10, txt=f"Severity: {vuln['severity']}", ln=1, align="L")
            pdf.set_font("Arial", size=10)
            pdf.cell(200, 10, txt=f"Description: {vuln['description']}", ln=1, align="L")
            pdf.cell(200, 10, txt=f"Discovered: {vuln['discovered_date']}", ln=1, align="L")
            pdf.cell(200, 10, txt=f"Status: {vuln['status']}", ln=1, align="L")
            pdf.cell(200, 10, txt="", ln=1, align="L")  # Add spacing
