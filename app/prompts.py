from langchain.prompts import PromptTemplate
from langchain.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
from textwrap import dedent
from typing import List, Optional

# Schema for column descriptions
class ColumnMetadata(BaseModel):
    column_name: str
    data_type: str
    column_description: str

# Schema for the full response
class TableMetadata(BaseModel):
    table_description: str = Field(description="High-level description of what the table contains")
    columns: list[ColumnMetadata]

class GeneratedQuestion(BaseModel):
    question: str = Field(description="The actual question text")
    category: str = Field(description="Category of the question (single_column, multi_column, table_purpose, data_type, business_logic)")
    source_columns: List[str] = Field(description="List of column names that this question was generated from")
# Parser based on schema
output_parser = PydanticOutputParser(pydantic_object=TableMetadata)

# Prompt template with strict JSON format
template_str = dedent("""
You are a data documentation assistant.
Given a table name and its columns with sample values, generate structured JSON output with:
1. table_description: A short, high-level summary of what the table likely contains. This will be 
used for semantic search so ensure that you include all relevant keywords.
2. columns: A list of column descriptions. Include context from sample values to make descriptions
more specific and accurate. This will be used for semantic search so ensure that you include all 
relevant keywords.

Return only valid JSON, like this:
```json
{{
  "table_description": "Your description here",
  "columns": [
    {{
      "column_name": "name",
      "data_type": "type",
      "column_description": "description"
    }}
  ]
}}
```

Table name: {table_name}
Columns:
{column_list}
""")

QUESTION_CATEGORY_PROMPTS = {
    "single_column": """
Generate a straightforward question that focuses on a single column from the table.
The question should be clear and direct but avoid explicitly using the exact column name.
Example: Instead of "What is the Total_Employees for each credit union?", use "How many people work at each credit union?"
""",
    
    "multi_column": """
Generate a question that requires analyzing relationships between 2-3 columns.
Focus on business insights and avoid using exact column names.
Example: Instead of "Compare Total_Assets and Net_Income", use "How profitable are larger credit unions compared to smaller ones?"
NOTE: Strictly limit to a maximum of 2-3 columns including any identifier columns. 
Maximum doesnt mean you need to utilize more columns, focus on good and practical questions
""",
    "table_purpose": """
Generate a high-level business question about the overall purpose or patterns in the data.
Example: "What trends can we observe in the lending patterns of credit unions?"
or "How do credit unions manage their delinquent loans compared to their total loan portfolio?"
NOTE: Strictly limit to a maximum of 2-3 columns including any identifier columns
""",
    
    "business_logic": """
Generate a complex business question that requires understanding multiple aspects of credit union operations.
Focus on strategic insights, risk assessment, or operational efficiency.
Example: "Which credit unions are most efficient at generating income relative to their size and employee count?"
or "How does the mix of different loan types affect a credit union's overall financial health?"
NOTE: Strictly limit to a maximum of 4-5 columns including any identifier columns. 
Maximum doesnt mean you need to utilize more columns, focus on good business questions
"""
}

question_generation_template = dedent("""
You are a data analyst tasked with generating diverse questions about a database table.
Generate ONE question that a user might ask about this data, along with metadata about the question.

Table Information:
- Name: {table_name}
- Description: {table_description}

Available Columns:
{columns_info}

Previously Generated Questions (avoid semantic duplicates):
{previous_questions}

Generate a question from this category: {target_category}

{category_prompt}

Ensure the question:
1. Is realistic and relevant to the data
2. Requires the specified category of thinking
3. Can be answered using only the available columns
4. Has clear required columns listed
5. Has appropriate confidence level (higher for direct lookups, lower for complex analysis)
                                      
Return the response in this exact JSON format:
{{
    "question": "Your generated question",
    "category": "category_name",
    "source_columns": ["list of single column/multi columns needed to answer"]
}}
""")

# Create the prompt
METADATA_PROMPT = PromptTemplate(
    template=template_str,
    input_variables=["table_name", "column_list"],
    output_parser=output_parser
)

QUESTION_GENERATOR_PROMPT = PromptTemplate(
    template=question_generation_template,
    input_variables=[
        "table_name",
        "table_description",
        "columns_info",
        "previous_questions",
        "target_category",
        "category_prompt"
    ]
)

