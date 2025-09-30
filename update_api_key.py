#!/usr/bin/env python3
"""
Simple script to update your Anthropic API key in the .env file
"""

import os
from pathlib import Path

def update_anthropic_key():
    """Update the Anthropic API key in .env file"""
    
    # Find .env file
    env_file = Path(".env")
    if not env_file.exists():
        print("❌ .env file not found in current directory")
        return False
    
    print("🔑 Anthropic API Key Updater")
    print("=" * 40)
    print("Please enter your NEW Anthropic API key:")
    print("(It should start with 'sk-ant-api03-')")
    print()
    
    # Get new API key from user
    new_key = input("New API key: ").strip()
    
    if not new_key:
        print("❌ No API key provided")
        return False
    
    # Validate format
    if not new_key.startswith("sk-ant-api03-"):
        print("⚠️  Warning: API key doesn't start with 'sk-ant-api03-'")
        confirm = input("Continue anyway? (y/N): ").strip().lower()
        if confirm != 'y':
            print("❌ Cancelled")
            return False
    
    # Read current .env file
    with open(env_file, 'r') as f:
        lines = f.readlines()
    
    # Update ANTHROPIC_API_KEY line
    updated = False
    new_lines = []
    for line in lines:
        if line.startswith('ANTHROPIC_API_KEY='):
            new_lines.append(f'ANTHROPIC_API_KEY={new_key}\n')
            updated = True
            print(f"✅ Updated ANTHROPIC_API_KEY")
        else:
            new_lines.append(line)
    
    if not updated:
        # Add new line if not found
        new_lines.append(f'ANTHROPIC_API_KEY={new_key}\n')
        print(f"✅ Added ANTHROPIC_API_KEY")
    
    # Write back to file
    with open(env_file, 'w') as f:
        f.writelines(new_lines)
    
    print(f"✅ API key updated in {env_file}")
    print(f"📝 Key prefix: {new_key[:20]}...")
    print(f"📏 Key length: {len(new_key)} characters")
    
    # Test the new key
    print("\n🧪 Testing new API key...")
    try:
        from dotenv import load_dotenv
        import anthropic
        
        load_dotenv()
        test_key = os.getenv('ANTHROPIC_API_KEY')
        
        if test_key == new_key:
            print("✅ Key loaded correctly from .env")
            
            # Test API call
            client = anthropic.Anthropic(api_key=test_key)
            response = client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=10,
                messages=[{"role": "user", "content": "Hi"}]
            )
            print(f"✅ API test successful: {response.content[0].text}")
            return True
        else:
            print("❌ Key mismatch - something went wrong")
            return False
            
    except Exception as e:
        print(f"❌ API test failed: {e}")
        print("Please check:")
        print("1. Your API key is valid and active")
        print("2. Your Anthropic account has billing set up")
        print("3. You have access to the models")
        return False

if __name__ == "__main__":
    update_anthropic_key()
