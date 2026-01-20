from itak.tools.ripgrep import RipGrepSearch, RipGrepTool
import os

def test_ripgrep_wrapper():
    # 1. Initialize
    rg = RipGrepSearch()
    print(f"Binary found: {rg.rg_path}")
    
    # 2. Run Search (Expected to fail if no binary)
    result = rg.search("def helper", ".")
    
    if result["success"]:
        print(f"[PASS] Search successful! Found {result['count']} matches.")
        for match in result['matches'][:3]:
            print(f"  - {match['file']}:{match['line_number']}")
    else:
        print(f"[EXPECTED FAIL] Search Check: {result['error']}")
        if "binary not found" in result["error"]:
            print("[PASS] Correctly identified missing binary.")
        else:
            print("[FAIL] Unexpected error message.")

    # 3. Test Tool Wrapper
    print("\n--- Test 2: Tool Wrapper ---")
    tool = RipGrepTool()
    tool_out = tool._run("def helper", ".")
    print(f"Tool Output: {tool_out}")
    
    if "Search Error" in tool_out or "No matches" in tool_out:
         print("[PASS] Tool Wrapper handled missing binary/empty result correctly.")

if __name__ == "__main__":
    test_ripgrep_wrapper()
