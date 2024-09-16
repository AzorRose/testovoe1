import os
import requests
from dotenv import load_dotenv

load_dotenv()

GITHUB_API_URL = "https://api.github.com"
GITHUB_USER = os.getenv("GITHUB_USER")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
REPO_NAME = os.getenv("REPO_NAME")

headers = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github.v3+json"
}

def create_repo(repo_name):
    url = f"{GITHUB_API_URL}/user/repos"
    payload = {
        "name": repo_name,
        "auto_init": True,
        "private": False
    }
    
    response = requests.post(url, headers=headers, json=payload)
    
    if response.status_code == 201:
        print(f"Repository '{repo_name}' created successfully.")
    else:
        print(f"Error creating repository: {response.json()}")
        
    return response.status_code

def list_repos():
    url = f"{GITHUB_API_URL}/user/repos"
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        repos = [repo['name'] for repo in response.json()]
        print(f"Repository list: {repos}")
        return repos
    else:
        print(f"Error fetching repositories: {response.json()}")
        
    return []

def delete_repo(repo_name):
    url = f"{GITHUB_API_URL}/repos/{GITHUB_USER}/{repo_name}"
    
    response = requests.delete(url, headers=headers)
    
    if response.status_code == 204:
        print(f"Repository '{repo_name}' deleted successfully.")
    else:
        print(f"Error deleting repository: {response.json()}")
        
    return response.status_code

def test_github_api():
    create_status = create_repo(REPO_NAME)
    assert create_status == 201, "Failed to create repository"

    repos = list_repos()
    assert REPO_NAME in repos, f"Repository {REPO_NAME} not found"

    delete_status = delete_repo(REPO_NAME)
    assert delete_status == 204, "Failed to delete repository"

    repos = list_repos()
    assert REPO_NAME not in repos, f"Repository {REPO_NAME} still exists"

if __name__ == "__main__":
    test_github_api()
