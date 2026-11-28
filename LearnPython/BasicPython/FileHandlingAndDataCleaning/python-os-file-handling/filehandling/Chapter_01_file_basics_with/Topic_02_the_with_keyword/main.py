# --- STEP 1: Let's create a file to test with ---
with open("proof_diary.txt", "w", encoding="utf-8") as setup:
    setup.write("Line 1: Learning Python context managers.\n")
    setup.write("Line 2: The with statement auto-closes files!\n")


# --- STEP 2: Prove that 'with' closes the file automatically ---
print("--- STARTING THE PROOF ---")

# We open the file using 'with'. Notice we NEVER type f.close() anywhere.
with open("proof_diary.txt", "r", encoding="utf-8") as f:
    # Read a line from the file
    content = f.readline().strip()
    print(f"📄 File Content Read: '{content}'")
    
    # 🔍 Check if the file is closed right now
    print(f"🔒 Inside the 'with' block -> Is the file closed? {f.closed}")

# 🚨 WE ARE NOW OUTSIDE THE INDENTATION 🚨
# The 'with' block has ended. Let's inspect the file state now:

print(f"🔓 Outside the 'with' block -> Is the file closed? {f.closed}")


# --- STEP 3: Prove it works even if an error happens mid-way ---
print("\n--- ERROR RESILIENCE PROOF ---")

try:
    with open("proof_diary.txt", "r", encoding="utf-8") as f:
        print("💥 About to cause a manual error inside the block...")
        raise ValueError("Simulated crash!")
        
except ValueError:
    print("⚠️ The program encountered an error and jumped to this fallback code.")

# Even though a crash happened inside the block, look what happened to the file:
print(f"🔒 After an error occurred -> Is the file closed? {f.closed}")


# --- CLEANUP ---
import os
if os.path.exists("proof_diary.txt"):
    os.remove("proof_diary.txt")
