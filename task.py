## Importing libraries and files
from crewai import Task
from agents import financial_analyst, verifier, risk_assessor, investment_advisor
from tools import (
    search_tool, 
    FinancialDocumentTool,
    FinancialAnalysisTool,
    InvestmentAnalysisTool,
    RiskAssessmentTool,
    VerificationAndSynthesisTool
)

document_tool = FinancialDocumentTool()
financial_tool = FinancialAnalysisTool()
risk_tool = RiskAssessmentTool()
investment_tool = InvestmentAnalysisTool()
verification_tool = VerificationAndSynthesisTool()


# Financial Analysis Task
financial_analysis = Task(
    description=(
        "Analyze the financial document located at the provided file path: '{file_path}'. "
        "Use the Financial Document Reader tool to extract the full content, then use the "
        "Parallel Financial Analysis Tool to process this data simultaneously with other specialists. "
        "Focus on extracting key financial metrics, figures, and statements. "
        "Your analysis must be comprehensive and ready for verification by the lead specialist."
    ),
    expected_output=(
        "A detailed financial analysis report that includes: "
        "- Key financial metrics and ratios "
        "- Revenue and profitability analysis "
        "- Cash flow and liquidity assessment "
        "- Balance sheet analysis "
        "- Financial health indicators "
        "This output will be used by the verification specialist to create the final comprehensive report."
    ),
    agent=financial_analyst,
    tools=[document_tool, financial_tool],
    async_execution=True,
)

risk_assessment = Task(
    description=(
        "Conduct a comprehensive risk assessment of the financial document at '{file_path}'. "
        "Use the Financial Document Reader tool to extract the full content, then use the "
        "Parallel Risk Assessment Tool to evaluate risks simultaneously with other specialists. "
        "Identify market risks, financial risks, operational risks, and credit risks. "
        "Provide detailed risk analysis with mitigation strategies."
    ),
    expected_output=(
        "A comprehensive risk assessment report that includes: "
        "- Market risk analysis "
        "- Financial risk evaluation "
        "- Operational risk assessment "
        "- Credit risk analysis "
        "- Risk mitigation recommendations "
        "This output will be used by the verification specialist to create the final comprehensive report."
    ),
    agent=risk_assessor,
    tools=[document_tool, risk_tool],
    async_execution=True,
)

investment_analysis = Task(
    description=(
        "Develop investment strategies and recommendations based on the financial document at '{file_path}'. "
        "Use the Financial Document Reader tool to extract the full content, then use the "
        "Parallel Investment Analysis Tool to provide investment advice simultaneously with other specialists. "
        "Create actionable investment recommendations with supporting rationale."
    ),
    expected_output=(
        "A comprehensive investment analysis report that includes: "
        "- Investment thesis and recommendations "
        "- Buy/Hold/Sell recommendations "
        "- Target price analysis "
        "- Investment timeline "
        "- Portfolio allocation suggestions "
        "- Strategic insights and growth prospects "
        "This output will be used by the verification specialist to create the final comprehensive report."
    ),
    agent=investment_advisor,
    tools=[document_tool, investment_tool],
    async_execution=True,
)

verification = Task(
    description=(
        "Receive and verify the results from all parallel specialist analyses. "
        "Use the Verification and Synthesis Tool to compile the financial analysis, risk assessment, "
        "and investment analysis into a single comprehensive report. "
        "Cross-reference all findings against the original document at '{file_path}' to ensure accuracy. "
        "Create a final, polished report that synthesizes all specialist insights."
    ),
    expected_output=(
        "A final comprehensive financial analysis report that includes: "
        "- Executive summary "
        "- Verified financial analysis section "
        "- Verified risk assessment section "
        "- Verified investment recommendations section "
        "- Cross-verification results "
        "- Final recommendations and disclaimer "
        "This should be a complete, professional report ready for stakeholders."
    ),
    agent=verifier,
    tools=[document_tool, verification_tool],
    async_execution=False, # runs after all parallel tasks complete
    context=[financial_analysis, risk_assessment, investment_analysis]
)