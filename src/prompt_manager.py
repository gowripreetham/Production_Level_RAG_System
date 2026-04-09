import yaml

def load_prompt(version=None):
    with open("prompts.yaml", "r") as f:
        prompts = yaml.load(f, Loader=yaml.SafeLoader)
    
    # Use specified version or fall back to active
    version = version or prompts["active"]
    
    prompt = prompts[version]
    print(f"Using prompt: {version} — {prompt['name']}")
    return prompt["system"]