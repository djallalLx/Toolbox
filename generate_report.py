# generate_report.py
from fpdf import FPDF
import json
import os

class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, 'Intrusion Test Toolbox Report', 0, 1, 'C')
        self.ln(10)
        
    def chapter_title(self, title):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, title, 0, 1, 'L')
        self.ln(5)
    
    def chapter_body(self, body):
        self.set_font('Arial', '', 12)
        self.multi_cell(0, 10, body)
        self.ln()

log_file = 'actions_log.json'

def generate_report():
    # Check if the log file exists, create it if it doesn't
    if not os.path.exists(log_file):
        with open(log_file, 'w') as file:
            json.dump([], file)
        print(f"{log_file} created as it did not exist.")

    # Read log file
    with open(log_file, 'r') as file:
        logs = json.load(file)

    # Debug: Check if logs were read correctly
    print(f"Logs read: {logs}")

    # Create instance of PDF class
    pdf = PDF()

    # Add a page
    pdf.add_page()

    # Set title
    pdf.set_title('Intrusion Test Toolbox Report')

    # Add Introduction
    pdf.chapter_title('Introduction')
    pdf.chapter_body('This report provides a summary of the modules used and the actions performed during the intrusion tests.')

    # Add log entries to the report
    for log in logs:
        module = log['module']
        action = log['action']
        timestamp = log['timestamp']
        pdf.chapter_title(module)
        pdf.chapter_body(f"Action: {action}\nTimestamp: {timestamp}")

    # Save the PDF
    pdf_output_path = 'intrusion_test_toolbox_detailed_report.pdf'
    pdf.output(pdf_output_path)

    # Debug: Confirm PDF creation
    print(f"PDF report generated at {pdf_output_path}")

    return pdf_output_path

# Test generate_report function
if __name__ == "__main__":
    generate_report()
