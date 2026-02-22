---
name: word-template-generator
description: This skill should be used when the user wants to process Word document templates, extract placeholders, or generate Word documents based on templates.
version: 1.0.0
---

# Word Template Generator Skill

## ⚠️ Execution Environment Disclaimer

**This skill provides guidance and generates structured data for Word document processing.**

**Important Limitations:**
- Claude is a text-based AI model and **cannot directly execute Python code**
- Claude **cannot directly manipulate .docx binary files** - these require specialized libraries
- All Python code examples in this skill are **reference implementations** for an external runtime
- Actual Word document processing requires:
  - A Python runtime environment
  - Dependencies: `python-docx`, `docxtpl`, `openpyxl`, `pandas`, `pillow`

**What Claude DOES:**
- Extract and structure data from user input/materials into validated JSON context
- Analyze template requirements and placeholder mapping
- Generate structured output that a runtime tool can consume

**What an External Tool DOES:**
- Execute Python code to read/write .docx files
- Use `python-docx` for document manipulation
- Use `docxtpl` for Jinja2 template rendering
- Handle binary file operations and image processing

---

## Overview

This skill guides the processing of Word document templates through a clear separation of concerns:
- **Claude's Role**: Generate validated context JSON from user input and materials
- **Tool's Role**: Execute docx rendering using the provided context

The workflow covers:
- Analyzing Word template structure and placeholders
- Extracting and structuring data from materials
- Generating validated JSON context for template rendering
- Providing reference implementations for runtime execution

## Trigger Conditions

**Trigger this skill when**:
- User provides a Word template file and asks to fill/generate a document
- User provides a "materials folder" and asks to generate documents based on a template
- User says "help me generate a Word document" and mentions a template
- User asks to "generate Word based on template" + mentions material location
- User mentions "Word template", "docx template", "fill template"
- User asks to batch generate Word documents
- User says "use these materials to generate document" and provides a template
- User asks to "process Word template", "parse docx template", or "extract placeholders from Word"

## Architecture & Responsibilities

```
┌─────────────────┐      ┌──────────────────┐      ┌─────────────────┐
│   User Input    │ ──▶ │   Claude (LLM)   │ ──▶ │  Context JSON   │
│  + Template     │      │  - Extract data  │      │  - Structured   │
│  + Materials    │      │  - Validate      │      │  - Validated    │
└─────────────────┘      └──────────────────┘      └─────────────────┘
                                                              │
                                                              ▼
┌─────────────────┐      ┌──────────────────┐      ┌─────────────────┐
│ Generated .docx │ ◀── │   Runtime Tool   │ ◀── │  Template .docx │
│   - Rendered    │      │  - python-docx   │      │  - Jinja2       │
│   - Formatted   │      │  - docxtpl       │      │  - Placeholders │
└─────────────────┘      └──────────────────┘      └─────────────────┘
```

### Claude's Responsibilities (This Skill)
1. **Parse Template Requirements**: Analyze placeholders and their types
2. **Extract Data**: Process user input and materials folders
3. **Validate Structure**: Ensure data matches JSON Schema requirements
4. **Generate Context JSON**: Produce structured, validated output

### Runtime Tool's Responsibilities
1. **Read .docx Files**: Use `python-docx` to access template content
2. **Render Templates**: Use `docxtpl` with Jinja2 syntax
3. **Process Images**: Handle image embedding and formatting
4. **Save Output**: Generate the final .docx file

---

## JSON Schema Reference

The context JSON passed to the runtime tool MUST conform to this schema:

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "Word Template Context",
  "description": "Context data for Word template rendering",
  "type": "object",
  "properties": {
    "title": {
      "type": "string",
      "description": "Document title or heading"
    },
    "content": {
      "type": "string",
      "description": "Main content text"
    },
    "items": {
      "type": "array",
      "description": "List of items for table/loop rendering",
      "items": {
        "type": "object",
        "properties": {
          "name": {
            "type": "string",
            "description": "Item name or identifier"
          },
          "value": {
            "oneOf": [
              {"type": "string"},
              {"type": "number"},
              {"type": "boolean"}
            ],
            "description": "Item value"
          },
          "description": {
            "type": "string",
            "description": "Optional item description"
          },
          "price": {
            "type": "number",
            "description": "Price for numeric items"
          },
          "qty": {
            "type": "number",
            "description": "Quantity"
          }
        },
        "required": ["name"]
      }
    },
    "image": {
      "type": "object",
      "description": "Image placeholder data",
      "properties": {
        "path": {
          "type": "string",
          "description": "Absolute or relative path to image file"
        },
        "width": {
          "type": "number",
          "description": "Image width in inches (optional)"
        },
        "height": {
          "type": "number",
          "description": "Image height in inches (optional)"
        }
      },
      "required": ["path"]
    },
    "metadata": {
      "type": "object",
      "description": "Document metadata",
      "properties": {
        "date": {
          "type": "string",
          "format": "date",
          "description": "Document date (ISO 8601 format)"
        },
        "author": {
          "type": "string",
          "description": "Document author"
        },
        "version": {
          "type": "string",
          "description": "Document version"
        },
        "contract_no": {
          "type": "string",
          "description": "Contract or reference number"
        }
      }
    },
    "party_a": {
      "type": "string",
      "description": "First party name (for contracts)"
    },
    "party_b": {
      "type": "string",
      "description": "Second party name (for contracts)"
    },
    "is_vip": {
      "type": "boolean",
      "description": "VIP status flag for conditional rendering"
    },
    "total_amount": {
      "type": "number",
      "description": "Calculated total amount"
    }
  },
  "additionalProperties": true
}
```

### Supported Data Types

| Placeholder Type | JSON Type | Example |
|-----------------|-----------|---------|
| Simple text | `string` | `"Hello World"` |
| Numbers | `number` | `123.45` |
| Booleans | `boolean` | `true` |
| Lists/Arrays | `array` | `[{"name": "A"}, {"name": "B"}]` |
| Objects | `object` | `{"path": "/img/logo.png"}` |
| Images (path) | `string` | `"/path/to/image.png"` |
| Images (object) | `object` | `{"path": "/img.png", "width": 2.5}` |

---

## Claude Output Format Examples

### Example 1: Simple Contract Context

**Claude generates this JSON:**
```json
{
  "contract_no": "HT-2026-001",
  "party_a": "Zhang San Company",
  "party_b": "Li Si Enterprise",
  "date": "2026-02-22",
  "title": "Service Agreement"
}
```

### Example 2: Invoice with Table Data

**Claude generates this JSON:**
```json
{
  "invoice_no": "INV-001",
  "items": [
    {"name": "Product A", "qty": 2, "price": 100, "total": 200},
    {"name": "Product B", "qty": 3, "price": 50, "total": 150}
  ],
  "total_amount": 350
}
```

### Example 3: Report with Mixed Content

**Claude generates this JSON:**
```json
{
  "title": "Quarterly Sales Report",
  "project_info": "Analysis of Q1 2026 sales performance across all regions...",
  "data_items": [
    {"name": "Region A", "value": 125000},
    {"name": "Region B", "value": 98000},
    {"name": "Region C", "value": 156000}
  ],
  "chart_image": {
    "path": "/Users/user/materials/chart.png",
    "width": 6,
    "height": 3
  },
  "metadata": {
    "date": "2026-02-22",
    "author": "Sales Department",
    "version": "1.0"
  }
}
```

---

## Workflow

### Phase 1: Template Analysis

1. Receive the Word template file path from the user
2. **Claude's Task**: Guide the user to identify placeholders
3. Identify placeholder types:
   - Simple variables: `{{name}}`
   - Lists/loops: `{% for item in items %}...{% endfor %}`
   - Conditions: `{% if condition %}...{% endif %}`
   - Table rows: `{%tr for item in items %}...{%tr endfor %}`

**Note**: Actual parsing requires runtime execution. Claude guides the process and generates expected context structure.

1. Receive the Word template file path from the user
2. Use python-docx to read document content
3. Extract placeholders (`{{variable_name}}`)
4. Identify placeholder types:
   - Simple variables: `{{name}}`
   - Lists/loops: `{% for item in items %}...{% endfor %}`
   - Conditions: `{% if condition %}...{% endif %}`

### Phase 2: Materials Folder Processing (Core Feature)

**Claude's Task**: Guide the user through materials organization and generate context JSON.

1. **Materials Folder Structure Analysis**
   - Scan and categorize files by type
   - Identify potential placeholder-to-file mappings
   - Flag missing or ambiguous mappings

2. **Smart Data Extraction Guidance**
   - Match placeholder names with filenames (e.g., `{{contract_info}}` matches `contract_info.txt`)
   - Structure data according to JSON Schema
   - Validate data types and required fields

3. **Data Mapping Strategy**
   ```
   Placeholder Naming Convention (Recommended):
   - {{name}} -> name.txt or read from name.xlsx
   - {{items}} -> items.xlsx or items.csv (table data → JSON array)
   - {{logo}} -> logo.png (image path or object)
   - {{content}} -> content.docx (embed other Word content)
   ```

**Claude's Output**: Structured context JSON conforming to the schema

---

### Phase 3: Context Generation & Validation

**Claude's Task**: Produce validated JSON context.

1. **Collect Data** from:
   - User input (direct text/values)
   - Material files (read and structured)
   - Default values where appropriate

2. **Validate Against Schema**:
   - Check required fields are present
   - Verify data types match expectations
   - Ensure arrays have correct structure

3. **Generate Final JSON Output**:
   - Follow the JSON Schema structure
   - Include all required fields
   - Handle optional fields appropriately
   - Provide validation status to user

**Example Claude Output:**
```json
{
  "title": "Quarterly Sales Report",
  "project_info": "Analysis of Q1 2026 performance...",
  "data_items": [
    {"name": "Region A", "value": 125000},
    {"name": "Region B", "value": 98000}
  ],
  "chart_image": {"path": "/materials/chart.png"}
}
```

---

### Phase 4: Document Generation (Runtime)

**This phase requires an external runtime tool.**

**Runtime Tool's Task**: Execute template rendering.

1. Load template using `docxtpl`
2. Parse the Claude-generated context JSON
3. Render template with Jinja2
4. Handle image embedding
5. Save the generated .docx file

**See Runtime Reference section for implementation details.**

## Supported Placeholder Syntax

### Simple Variables
```
Dear {{name}}:
Your order {{order_id}} has been confirmed.
```

### List Loops
```
{% for item in items %}
- {{item.name}}: {{item.price}}
{% endfor %}
```

### Conditional Logic
```
{% if is_vip %}
VIP Member Exclusive Offer
{% endif %}
```

### Table Row Loops
```
| Product | Quantity | Unit Price |
|---------|----------|------------|
{%tr for product in products %}
| {{product.name}} | {{product.qty}} | {{product.price}} |
{%tr endfor %}
```

---

## Runtime Reference Code

**IMPORTANT**: The following code is for **runtime environment execution only**.
Claude cannot execute this code directly. It should be used by an external tool.

### Read Template and Extract Placeholders
```python
import re
from docx import Document

def extract_placeholders(template_path):
    """Extract placeholders from template - RUNTIME CODE"""
    doc = Document(template_path)
    text = '\n'.join([p.text for p in doc.paragraphs])
    # Extract text from tables
    for table in doc.tables:
        for row in table.rows:
            for cell in row.cells:
                text += cell.text + '\n'

    # Find {{...}} placeholders
    placeholders = re.findall(r'\{\{([^}]+)\}\}', text)
    return list(set([p.strip() for p in placeholders]))
```

### Fill Template and Generate Document
```python
from docxtpl import DocxTemplate

def generate_document(template_path, output_path, context):
    """Fill template with data and generate new document - RUNTIME CODE"""
    doc = DocxTemplate(template_path)
    doc.render(context)
    doc.save(output_path)
```

### Complete Workflow (with Materials Folder Support)
```python
from docx import Document
from docxtpl import DocxTemplate
from pathlib import Path
import re
import pandas as pd

def process_template_with_materials(template_path, materials_folder, output_path):
    """Fill template using data from materials folder - RUNTIME CODE"""

    # 1. Extract template placeholders
    doc = Document(template_path)
    full_text = get_full_text(doc)
    placeholders = extract_placeholders(full_text)

    # 2. Scan materials folder
    materials = scan_materials_folder(materials_folder)

    # 3. Smart data extraction
    context = {}
    for placeholder in placeholders:
        # Try to match by filename
        matched_data = find_data_for_placeholder(placeholder, materials)
        if matched_data is not None:
            context[placeholder] = matched_data

    # 4. Check for missing data
    missing = [p for p in placeholders if p not in context]
    if missing:
        print(f"Missing data for placeholders: {', '.join(missing)}")
        print("Please provide these data manually")

    return context

def scan_materials_folder(folder_path):
    """Scan materials folder - RUNTIME CODE"""
    materials = {}
    folder = Path(folder_path)

    for file in folder.iterdir():
        if file.is_file():
            # Use filename (without extension) as key
            key = file.stem
            materials[key] = {
                'path': str(file),
                'type': file.suffix.lower(),
                'file': file
            }
    return materials

def find_data_for_placeholder(placeholder, materials):
    """Find and extract data based on placeholder name - RUNTIME CODE"""
    # Direct filename match
    if placeholder in materials:
        mat = materials[placeholder]
        return extract_data_from_file(mat['path'], mat['type'])

    # Fuzzy match (e.g., contract_info matches contract_info_data.txt)
    for key, mat in materials.items():
        if placeholder.lower() in key.lower() or key.lower() in placeholder.lower():
            return extract_data_from_file(mat['path'], mat['type'])

    return None

def extract_data_from_file(file_path, file_type):
    """Extract data from file - RUNTIME CODE"""
    if file_type in ['.txt', '.md']:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()

    elif file_type == '.docx':
        doc = Document(file_path)
        return '\n'.join([p.text for p in doc.paragraphs])

    elif file_type in ['.xlsx', '.csv']:
        # Read Excel/CSV, return list of dictionaries
        df = pd.read_excel(file_path) if file_type == '.xlsx' else pd.read_csv(file_path)
        return df.to_dict('records')

    elif file_type in ['.png', '.jpg', '.jpeg']:
        # Return image path for template use
        return file_path

    return None

def generate_document(template_path, context, output_path):
    """Generate final document - RUNTIME CODE"""
    tpl = DocxTemplate(template_path)
    tpl.render(context)
    tpl.save(output_path)
    print(f"Document generated: {output_path}")
```

---

## Usage Examples

### Example 1: Simple Contract Generation

**Template (contract_template.docx)**:
```
Contract No: {{contract_no}}

Party A: {{party_a}}
Party B: {{party_b}}

Date: {{date}}
```

**User Input**:
```
Generate a contract using this template:
/Users/user/contract_template.docx

Party A: Zhang San Company
Party B: Li Si Enterprise
Date: 2026-02-22
Contract No: HT-2026-001
```

**Claude Generates (Context JSON)**:
```json
{
  "contract_no": "HT-2026-001",
  "party_a": "Zhang San Company",
  "party_b": "Li Si Enterprise",
  "date": "2026-02-22"
}
```

**Runtime Tool Output**:
`/Users/user/contract_20260222.docx`

---

### Example 2: Invoice Generation (with Tables)

**Template (invoice_template.docx)**:
```
Invoice No: {{invoice_no}}

| Product | Quantity | Unit Price | Total |
|---------|----------|------------|-------|
{%tr for item in items %}
| {{item.name}} | {{item.qty}} | {{item.price}} | {{item.total}} |
{%tr endfor %}

Total: {{total_amount}}
```

**User Input**:
```
Generate invoice:
Template: /Users/user/invoice_template.docx
Invoice No: INV-001
Product List:
- Product A x 2 @ 100 yuan
- Product B x 3 @ 50 yuan
```

**Claude Generates (Context JSON)**:
```json
{
  "invoice_no": "INV-001",
  "items": [
    {"name": "Product A", "qty": 2, "price": 100, "total": 200},
    {"name": "Product B", "qty": 3, "price": 50, "total": 150}
  ],
  "total_amount": 350
}
```

---

### Example 3: Auto-Generate with Materials Folder (Recommended)

**Template (report_template.docx)**:
```
# {{title}}

## Project Information
{{project_info}}

## Data Analysis
{% for item in data_items %}
- {{item.name}}: {{item.value}}
{% endfor %}

## Chart
{{chart_image}}
```

**Materials Folder Structure**:
```
/Users/user/materials/
├── title.txt           # Content: Quarterly Sales Report
├── project_info.txt    # Content: Project details...
├── data_items.xlsx     # Table: name, value columns
└── chart.png           # Image file
```

**User Input**:
```
Generate document using this template and materials:
Template: /Users/user/report_template.docx
Materials: /Users/user/materials/
```

**Claude's Processing**:
1. Analyze template placeholders: `{{title}}`, `{{project_info}}`, `{{data_items}}`, `{{chart_image}}`
2. Map materials to placeholders:
   - `title.txt` → `{{title}}`
   - `project_info.txt` → `{{project_info}}`
   - `data_items.xlsx` → `{{data_items}}` (parse as array)
   - `chart.png` → `{{chart_image}}` (image path object)
3. Validate structure against JSON Schema

**Claude Generates (Context JSON)**:
```json
{
  "title": "Quarterly Sales Report",
  "project_info": "Analysis of Q1 2026 sales performance across all regions showing 15% growth...",
  "data_items": [
    {"name": "Region A", "value": 125000},
    {"name": "Region B", "value": 98000},
    {"name": "Region C", "value": 156000}
  ],
  "chart_image": {
    "path": "/Users/user/materials/chart.png"
  }
}
```

**Runtime Tool Output**:
`/Users/user/report_output.docx`

## Limitations

### Claude (This Skill)
- Cannot directly execute Python code or manipulate .docx binaries
- Cannot read binary file contents directly
- Relies on user-provided file descriptions or structured inputs
- JSON generation depends on clear user input

### Runtime Tool Requirements
- Only supports .docx format (not .doc)
- Complex formatting may require manual adjustment
- Limited support for nested tables
- Images require special handling (path reference or InlineImage)
- File naming in materials folder should have clear correspondence with placeholders
- Excel files need standardized table structure

---

## Validation Criteria

### Claude's Responsibilities (Validated by This Skill)
1. ✅ Analyzes template structure and identifies placeholders
2. ✅ Generates context JSON conforming to JSON Schema
3. ✅ Validates data types (string, number, boolean, array, object)
4. ✅ Maps materials to placeholders intelligently
5. ✅ Handles user input and converts to structured data
6. ✅ Provides clear validation status and error messages
7. ✅ Separates concerns between data generation and rendering

### Runtime Tool's Responsibilities (External)
1. ✅ Reads Word template files using `python-docx`
2. ✅ Extracts placeholders from .docx content
3. ✅ Scans and reads files from materials folder
4. ✅ Renders templates using `docxtpl` with Jinja2
5. ✅ Handles image embedding and formatting
6. ✅ Generates formatted Word documents
7. ✅ Processes complex syntax (loops, conditions, tables)

---

## Installation of Dependencies

**For Runtime Environment Only** - Claude cannot execute these commands.

To run the reference code in an actual Python environment:

```bash
pip install python-docx docxtpl openpyxl pandas pillow
```

**Dependency Overview**:
- `python-docx`: Reading .docx files
- `docxtpl`: Jinja2 template rendering for Word
- `openpyxl`: Excel file support
- `pandas`: Data manipulation and Excel/CSV parsing
- `pillow`: Image processing

---

## Summary

This skill provides:
- ✅ Clear separation between Claude (data generation) and runtime tools (document rendering)
- ✅ JSON Schema definitions for validated context output
- ✅ Reference implementations for runtime environments
- ✅ Complete workflow guidance from template to generated document

**Claude's Output**: Validated JSON context conforming to the defined schema
**Runtime Tool's Role**: Execute template rendering with the provided context
