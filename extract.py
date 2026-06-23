import json
import os

log_path = r'C:\Users\Harsh\.gemini\antigravity-ide\brain\2fed6cc9-763f-4702-b90f-4ca919d5ab87\.system_generated\logs\transcript.jsonl'
replacements = []

with open(log_path, 'r', encoding='utf-8') as f:
    for line in f:
        try:
            obj = json.loads(line)
            if 'tool_calls' in obj:
                for tc in obj['tool_calls']:
                    if tc.get('name') in ['default_api:multi_replace_file_content', 'default_api:replace_file_content']:
                        args = tc.get('arguments', {})
                        if 'views.py' in args.get('TargetFile', ''):
                            replacements.append(args)
        except Exception:
            pass

with open('recovered_views_replacements.json', 'w', encoding='utf-8') as f:
    json.dump(replacements, f, indent=2)
