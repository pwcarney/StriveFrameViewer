import sys
import os

def replace_in_file(file_path):
    # Read the content of the file
    with open(file_path, 'r') as file:
        content = file.read()
    
    # Perform the replacement
    modified_content = content.replace(r"\defaultlib:msvcrt.obj", r"msvcrt.lib")
    modified_content = content.replace(r"\defaultlib:msvcrt", r"msvcrt.lib")
    
    # Write the modified content back to the file
    with open(file_path, 'w') as file:
        file.write(modified_content)
    print(f"Replacements made in {file_path}")

def process_directory(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.vcxproj'):
                file_path = os.path.join(root, file)
                replace_in_file(file_path)

if __name__ == "__main__":
    directory_path = "build"
    
    if not os.path.exists(directory_path):
        print(f"Error: Directory '{directory_path}' does not exist.")
        sys.exit(1)

    if not os.path.isdir(directory_path):
        print(f"Error: '{directory_path}' is not a directory.")
        sys.exit(1)

    process_directory(directory_path)
    print("Operation completed successfully.")