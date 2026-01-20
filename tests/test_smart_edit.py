from itak.tools.smart_edit import SmartEditor, SmartEditTool
import os

def test_smart_edit():
    editor = SmartEditor()
    test_file = "test_smart_edit_sample.py"
    
    # 1. Setup Test File
    content = """def hello():
    print("Hello World")
    return True
"""
    with open(test_file, 'w') as f:
        f.write(content)
        
    print(f"Created {test_file}")

    # 2. Test Flexible Match (Multi-line Indentation Mismatch)
    # File has 4 spaces indent. Search has 0 spaces.
    # Standard replace() fails because it won't match "\n    " with "\n".
    old_str = 'print("Hello World")\nreturn True' 
    new_str = 'print("Hello Universe")\nreturn False'
    
    print("\n--- Test 1: Flexible Match (Indentation Ignored) ---")
    result = editor.apply_edit(test_file, old_str, new_str)
    
    if result["success"]:
        print(f"[PASS] Strategy Used: {result['strategy']}")
        print(f"New Content:\n{result['content']}")
        # Verify it preserved the indentation
        if '    print("Hello Universe")' in result['content']:
            print("[PASS] Indentation Preserved!")
        else:
            print("[FAIL] Indentation Lost!")
    else:
        print(f"[FAIL] Edit Failed: {result['error']}")

    # 3. Test Regex Match (Variable Whitespace)
    # File now has "Hello Universe"
    # Search string has weird spacing: "return    True" vs "return True"
    print("\n--- Test 2: Regex Match (Whitespace Ignored) ---")
    
    # RESET file content for Test 2
    content_2 = """def hello():
    print("Hello World")
    return True
"""
    with open(test_file, 'w') as f:
        f.write(content_2)
        
    old_str_regex = "return      True" # Excessive spaces
    new_str_regex = "return False"
    
    result = editor.apply_edit(test_file, old_str_regex, new_str_regex)
    
    if result["success"]:
        print(f"[PASS] Strategy Used: {result['strategy']}")
        print(f"New Content:\n{result['content']}")
        if '    return False' in result['content']:
             print("[PASS] Regex replacement worked!")
    else:
        print(f"[FAIL] Edit Failed: {result['error']}")


    # 4. Test SmartEditTool Wrapper
    print("\n--- Test 3: Tool Wrapper ---")
    tool = SmartEditTool()
    # Reset file again
    with open(test_file, 'w') as f:
        f.write('def foo():\n    return True')
        
    result_msg = tool._run(test_file, 'return True', 'return False')
    print(f"Tool Output: {result_msg}")
    
    if "Successfully edited" in result_msg:
        print("[PASS] Tool Wrapper works!")
    else:
        print("[FAIL] Tool Wrapper failed!")

    # Cleanup
    if os.path.exists(test_file):
        os.remove(test_file)

if __name__ == "__main__":
    test_smart_edit()
