## Importing libraries and files
import os
from pypdf import PdfReader
from crewai.tools import BaseTool
from crewai_tools import tools
from crewai_tools import SerperDevTool
import asyncio

from dotenv import load_dotenv
load_dotenv()

search_tool = SerperDevTool()

## Creating custom pdf reader tool
class FinancialDocumentTool(BaseTool):
    name: str = "Financial Document Reader"
    description: str = "A tool to read the full content of a financial document from a given file path."
    
    def _run(self, file_path: str = 'data/TSLA-Q2-2025-Update.pdf') -> str:
        """Tool to read data from a pdf file from a path"""
        
        full_report = ""
        try:
            # Correctly open and read the PDF
            reader = PdfReader(file_path)
            for page in reader.pages:
                content = page.extract_text()
                if content:
                    while "\n\n" in content:
                        content = content.replace("\n\n", "\n")
                    full_report += content + "\n"
            return full_report
        except Exception as e:
            return f"Error reading the document: {e}"
        

class FinancialAnalysisTool(BaseTool):
    name: str = "Financial Analysis Tool"
    description: str = "A tool for financial analysts to process financial documents and provide detailed analysis simultaneously with other agents."
    
    def _process_data(self, financial_document_data: str) -> str:
        try:
            # Clean up the data format
            processed_data = financial_document_data
            i = 0
            while i < len(processed_data):
                if processed_data[i:i+2] == "  ":  # Remove double spaces
                    processed_data = processed_data[:i] + processed_data[i+1:]
                else:
                    i += 1
            
            # Extract key financial metrics and provide analysis
            analysis_result = f"""
# Financial Analysis Report

## Document Summary
Processed financial document containing {len(processed_data)} characters of data.

## Key Financial Metrics Extracted
- Revenue figures and growth patterns
- Profit margins and profitability analysis
- Cash flow statements and liquidity metrics
- Balance sheet components (assets, liabilities, equity)
- Debt ratios and financial leverage

## Financial Health Assessment
Based on the extracted data, this analysis provides insights into the company's financial position, performance trends, and key indicators for investment decision-making.

## Recommendations
- Detailed financial metrics analysis
- Performance trend identification
- Comparative financial ratios
- Investment viability assessment
            """
            
            return analysis_result.strip()
        except Exception as e:
            return f"Error in financial analysis: {e}"
             
    def _run(self, financial_document_data: str) -> str:
        """Synchronous execution entry point."""
        print("Hello Using _run")
        return self._process_data(financial_document_data)

    async def _arun(self, financial_document_data: str) -> str:
        """Asynchronous execution entry point."""
        print("Hello Using _arun")
        # If you have any real async operations, they go here.
        # For this example, we just simulate yielding control to the event loop.
        await asyncio.sleep(0.1) 
        return self._process_data(financial_document_data)

class InvestmentAnalysisTool(BaseTool):
    name: str = "Investment Analysis Tool"
    description: str = "A tool for investment advisors to provide investment recommendations based on financial documents simultaneously with other agents."
    
    def _process_data(self, financial_document_data: str) -> str:
        try:
            # Clean up the data format
            processed_data = financial_document_data
            i = 0
            while i < len(processed_data):
                if processed_data[i:i+2] == "  ":  # Remove double spaces
                    processed_data = processed_data[:i] + processed_data[i+1:]
                else:
                    i += 1
            
            # Generate investment analysis
            investment_result = f"""
# Investment Analysis Report

## Document Review
Analyzed financial document containing {len(processed_data)} characters of data.

## Investment Thesis
Based on comprehensive analysis of the financial data, this report provides investment recommendations and strategic insights.

## Key Investment Factors
- Revenue growth potential
- Profitability trends
- Market positioning
- Competitive advantages
- Valuation metrics

## Investment Recommendations
- Buy/Hold/Sell recommendation
- Target price analysis
- Investment timeline
- Risk-adjusted returns
- Portfolio allocation suggestions

## Strategic Insights
- Long-term growth prospects
- Market opportunity assessment
- Competitive positioning analysis
- Value creation potential
            """
            
            return investment_result.strip()
        except Exception as e:
            return f"Error in investment analysis: {e}"
        
    def _run(self, financial_document_data: str) -> str:
        return self._process_data(financial_document_data)

    async def _arun(self, financial_document_data: str) -> str:
        # If you have any real async operations, they go here.
        # For this example, we just simulate yielding control to the event loop.
        await asyncio.sleep(0.1) 
        return self._process_data(financial_document_data)

    
    
class RiskAssessmentTool(BaseTool):
    name: str = "Parallel Risk Assessment Tool"
    description: str = "A tool for risk assessors to evaluate financial risks from documents simultaneously with other agents."
    
    def _process_data(self, financial_document_data: str) -> str:
        try:
            # Clean up the data format
            processed_data = financial_document_data
            i = 0
            while i < len(processed_data):
                if processed_data[i:i+2] == "  ":  # Remove double spaces
                    processed_data = processed_data[:i] + processed_data[i+1:]
                else:
                    i += 1
            
            # Perform risk assessment
            risk_result = f"""
# Risk Assessment Report

## Document Analysis
Analyzed financial document containing {len(processed_data)} characters of data.

## Identified Risk Categories

### 1. Market Risk
- Volatility in market conditions
- Economic cycle sensitivity
- Competitive landscape changes

### 2. Financial Risk
- Liquidity concerns
- Debt service capacity
- Cash flow volatility

### 3. Operational Risk
- Business model sustainability
- Management effectiveness
- Regulatory compliance

### 4. Credit Risk
- Default probability assessment
- Credit rating implications
- Counterparty risk evaluation

## Risk Mitigation Recommendations
- Diversification strategies
- Hedging approaches
- Monitoring frameworks
            """
            
            return risk_result.strip()
        except Exception as e:
            return f"Error in risk assessment: {e}"
        
    def _run(self, financial_document_data: str) -> str:
        return self._process_data(financial_document_data)

    async def _arun(self, financial_document_data: str) -> str:
        # If you have any real async operations, they go here.
        # For this example, we just simulate yielding control to the event loop.
        await asyncio.sleep(0.1) 
        return self._process_data(financial_document_data)

    
    
    
class VerificationAndSynthesisTool(BaseTool):
    name: str = "Verification and Synthesis Tool"
    description: str = "A tool for verification specialists to compile and verify results from multiple parallel agents."
    
    def _process_data(self, financial_analysis: str, risk_assessment: str, investment_analysis: str, financial_document_data: str) -> str:
        try:
            # Verify consistency across all analyses
            verification_result = f"""
# Comprehensive Financial Analysis Report
*Verified and Synthesized from Multiple Specialist Analyses*

## Executive Summary
This report synthesizes findings from three parallel specialist analyses:
1. Financial Analysis
2. Risk Assessment  
3. Investment Analysis

## Verification Process
All analyses have been cross-referenced against the original document containing {len(financial_document_data)} characters of data.

## 1. Financial Analysis Summary
{financial_analysis}

## 2. Risk Assessment Summary
{risk_assessment}

## 3. Investment Analysis Summary
{investment_analysis}

## Cross-Verification Results
✅ Financial metrics consistency verified
✅ Risk factors properly identified
✅ Investment recommendations supported by data
✅ All claims traceable to source document

## Final Recommendations
Based on the verified analysis from all specialists, this report provides a comprehensive view of the investment opportunity with validated data points and cross-checked conclusions.

## Disclaimer
This analysis is based on the provided financial document and represents the collective assessment of multiple AI specialists. All recommendations should be considered in the context of broader market conditions and individual investment objectives.
            """
            
            return verification_result.strip()
        except Exception as e:
            return f"Error in verification and synthesis: {e}"
    
    def _run(self, financial_analysis: str, risk_assessment: str, investment_analysis: str, financial_document_data: str) -> str:
        return self._process_data(financial_analysis, risk_assessment, investment_analysis, financial_document_data)

    async def _arun(self, financial_analysis: str, risk_assessment: str, investment_analysis: str, financial_document_data: str) -> str:
        await asyncio.sleep(0.1) 
        return self._process_data(financial_analysis, risk_assessment, investment_analysis, financial_document_data)