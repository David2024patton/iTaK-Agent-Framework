"""
Minimal test to see where guild system fails
"""
import sys
sys.path.insert(0, r'd:\test\testing\src')

# Test 1: Can we import everything?
print("Test 1: Imports...")
try:
    from itak.cli.guild_auto import run_guild_build, get_or_create_guild_for_project
    from itak.cli.agent_manager import initialize_default_wizards
    print("✅ Imports work")
except Exception as e:
    print(f"❌ Import failed: {e}")
    sys.exit(1)

# Test 2: Can we initialize wizards?
print("\nTest 2: Initialize wizards...")
try:
    initialize_default_wizards()
    from pathlib import Path
    AGENTS_DIR = Path.home() / '.itak' / 'agents'
    wizards = list(AGENTS_DIR.glob('*.yaml'))
    print(f"✅ Created {len(wizards)} wizards: {[w.stem for w in wizards]}")
except Exception as e:
    print(f"❌ Wizard init failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Test 3: Can we create a guild?
print("\nTest 3: Create guild...")
try:
    guild_name = get_or_create_guild_for_project('web', 'test')
    print(f"✅ Guild created: {guild_name}")
except Exception as e:
    print(f"❌ Guild creation failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Test 4: Can we run the guild? (This is where it likely fails)
print("\nTest 4: Run guild build...")
print("This will show if agents actually execute or just hang/fail")
try:
    run_guild_build(guild_name, "Build a simple test.html file", "./test_output")
    print("✅ Guild build completed")
except Exception as e:
    print(f"❌ Guild build failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\n✅ ALL TESTS PASSED!")
