import os
import requests
from dotenv import load_dotenv

# Load the token from your hidden .env file
load_dotenv()
TOKEN = os.getenv("GITHUB_TOKEN")

headers = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json"
}

# GraphQL Query to find your username and project details
query = """
query {
  viewer {
    login
    projectsV2(first: 5) {
      nodes {
        id
        title
      }
    }
  }
}
"""

response = requests.post("https://api.github.com/graphql", json={"query": query}, headers=headers)

if response.status_code == 200:
    data = response.json()
    viewer = data['data']['viewer']
    print(f"Authenticated as User: {viewer['login']}\n")
    print("Found the following Projects:")
    for project in viewer['projectsV2']['nodes']:
        print(f"- Title: {project['title']}")
        print(f"  ID: {project['id']}\n")
else:
    print(f"Failed! Status code: {response.status_code}")
    print(response.text)


