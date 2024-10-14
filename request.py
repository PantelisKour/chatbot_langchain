import os
import base64
import requests

# GitHub user and token (Replace these with your actual values)
GITHUB_USER = "<user>"
GITHUB_TOKEN = "<api_key>"

# The name of the repository you want to create
REPO_NAME = "chatbot-langchain"

# The local folder you want to upload
FOLDER_PATH = ''

# Step 1: Create a new repository on GitHub
def create_github_repo(repo_name):
    url = "https://api.github.com/user/repos"
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}
    data = {
        "name": repo_name,
        "private": False,  # Set to True if you want a private repo
        "description": "Repository for Folder Upload"
    }

    response = requests.post(url, json=data, headers=headers)

    if response.status_code == 201:
        print(f"Repository '{repo_name}' created successfully!")
        return True
    else:
        print(f"Failed to create repository: {response.json()}")
        return False

# Step 2: Upload a file to the repository
def upload_file_to_repo(repo_name, file_path, file_content):
    # Convert the local Windows file path to GitHub-friendly path (Unix-style)
    github_path = file_path.replace(FOLDER_PATH, '').lstrip('\\').replace('\\', '/')
    github_path = github_path.lstrip('/')  # Remove any leading slash for the correct URL
    url = f"https://api.github.com/repos/{GITHUB_USER}/{repo_name}/contents/{github_path}"

    headers = {"Authorization": f"token {GITHUB_TOKEN}"}

    # Encode file content in base64
    content = base64.b64encode(file_content).decode("utf-8")

    # Create the data payload
    data = {
        "message": f"Add {os.path.basename(file_path)}",
        "content": content
    }

    # Make the PUT request to upload the file
    response = requests.put(url, json=data, headers=headers)

    if response.status_code == 201:
        print(f"File '{file_path}' uploaded successfully!")
    else:
        print(f"Failed to upload file: {response.json()}")

# Step 3: Iterate over the files in the folder and upload them
def upload_folder_to_repo(repo_name, folder_path):
    for root, dirs, files in os.walk(folder_path):
        for file_name in files:
            # Create the full path of the file
            file_path = os.path.join(root, file_name)
            # Read the file content
            with open(file_path, "rb") as file:
                file_content = file.read()
                # Upload the file to the GitHub repository
                upload_file_to_repo(repo_name, file_path, file_content)

# Step 4: Execute the script
if create_github_repo(REPO_NAME):
    upload_folder_to_repo(REPO_NAME, FOLDER_PATH)
