import anthropic

client = anthropic.Anthropic()

response = client.messages.create(
    model="claude-3-7-sonnet-20250219",
    max_tokens=1024,
    tools=[
        {
            "name": "get_all_keys",
            "description": "Get all the keys in the data",
            "parameters": {
                "type": "object",
                "properties": {
                    "dbId": {"type": "string", "description": "The unique identifier for the database entry."},
                    "external_id": {"type": "string", "description": "The external identifier for the database entry."},
                    "ElementId": {"type": "string", "description": "The element identifier for the database entry."},
                    # Add other properties as needed
                },
                "required": ["dbId", "external_id", "ElementId"],
            },
        }
    ],
    messages=[
        {"role": "tool", "content": "Get all the columns in the data."},
    ],
)
print(response)