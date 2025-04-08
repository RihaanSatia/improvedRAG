from langchain.prompts import PromptTemplate
from langchain.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
from textwrap import dedent

# Schema for column descriptions
class ColumnMetadata(BaseModel):
    column_name: str
    data_type: str
    column_description: str

# Schema for the full response
class TableMetadata(BaseModel):
    table_description: str = Field(description="High-level description of what the table contains")
    columns: list[ColumnMetadata]

# Parser based on schema
output_parser = PydanticOutputParser(pydantic_object=TableMetadata)

# Prompt template with strict JSON format
template_str = dedent("""
You are a data documentation assistant.
Given a table name and its columns, generate structured JSON output with:
1. table_description: A short, high-level summary of what the table likely contains. This will be 
used for semantic search so ensure that you include all relevant keywords.
2. columns: A list of column descriptions. This will be used for semantic search so ensure that 
you include all relevant keywords.

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

# Create the prompt
METADATA_PROMPT = PromptTemplate(
    template=template_str,
    input_variables=["table_name", "column_list"],
    output_parser=output_parser
)