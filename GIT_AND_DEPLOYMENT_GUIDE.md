# Git, GitHub, and Streamlit Deployment Guide

This guide provides step-by-step instructions for managing your web application (e.g., `weather-vibe-dash`), deploying it to Streamlit, and collaborating with a team.

---

## 1. Create a Git Repository & Push to GitHub

**Goal:** Turn your local folder into a tracked Git repository and upload it to GitHub.

### Prerequisites
- You have created a folder for your project (e.g., `weather-vibe-dash`) with your code files.
- You have a GitHub account.
- You have Git installed on your computer.

### Step 1: Initialize Git Locally
1.  **Open Terminal** (or Command Prompt).
2.  **Navigate** to your project folder:
    ```bash
    cd path/to/your/weather-vibe-dash
    ```
3.  **Initialize** the repository:
    ```bash
    git init
    ```
    *(This creates a hidden `.git` folder that tracks changes.)*

### Step 2: Prepare Files
1.  **Create a `.gitignore` file** (if you don't have one) to exclude unnecessary files:
    ```bash
    touch .gitignore
    ```
2.  **Edit `.gitignore`** and add common exclusions:
    ```text
    .DS_Store
    __pycache__/
    *.pyc
    .venv/
    env/
    .env
    ```
3.  **Create `requirements.txt`** (Crucial for Streamlit):
    ```bash
    pip freeze > requirements.txt
    ```
    *Or manually list your libraries, e.g.:*
    ```text
    streamlit
    pandas
    plotly
    ```

### Step 3: Commit Code Locally
1.  **Check status**:
    ```bash
    git status
    ```
    *(You will see red, untracked files.)*
2.  **Add files** to staging:
    ```bash
    git add .
    ```
3.  **Commit** the changes:
    ```bash
    git commit -m "Initial commit: basic app structure"
    ```

### Step 4: Create Repo on GitHub & Push
1.  Go to [GitHub.com](https://github.com) and sign in.
2.  Click the **+** icon (top right) -> **New repository**.
3.  **Repository name**: `weather-vibe-dash` (or match your folder name).
4.  **Privacy**: Public (easier for Streamlit Cloud) or Private.
5.  **Do NOT** check "Add a README", ".gitignore", or "License" (since you have local code).
6.  Click **Create repository**.
7.  Copy the commands under **"…or push an existing repository from the command line"**:
    ```bash
    git remote add origin https://github.com/YOUR_USERNAME/weather-vibe-dash.git
    git branch -M main
    git push -u origin main
    ```
    *(Run these commands in your terminal inside your project folder.)*

---

## 2. Deploy Web App to Streamlit

**Goal:** Make your app live on the web.

### Step 1: Login to Streamlit
1.  Go to [share.streamlit.io](https://share.streamlit.io/).
2.  Click **"Continue with GitHub"**.

### Step 2: Create New App
1.  Click **"New app"** (top right).
2.  **Repository**: Select your repo (`YOUR_USERNAME/weather-vibe-dash`).
3.  **Branch**: `main`.
4.  **Main file path**: `app.py` (or whatever your main python file is named, e.g., `streamlit_app.py`, `dashboard.py`).
5.  Click **"Deploy!"**.

### Step 3: Wait & Verify
- Streamlit will install dependencies from your `requirements.txt`.
- Once done, you will see your app live.
- **Copy the URL** to share it.

---

## 3. Regular Workflow (Code, Commit, Push)

**Goal:** Update your code and see changes reflected online.

When you modify files on your computer:

1.  **Check which files changed**:
    ```bash
    git status
    ```
2.  **View detailed changes** (optional):
    ```bash
    git diff
    ```
3.  **Add changes** to staging:
    ```bash
    git add app.py
    # OR to add all changed files:
    git add .
    ```
4.  **Commit** with a clear message:
    ```bash
    git commit -m "Fixed chart colors"
    ```
5.  **Push** to GitHub:
    ```bash
    git push
    ```

**Result:**
- GitHub repo is updated immediately.
- Streamlit Cloud detects the push and **automatically redeploys** your app (usually takes 1-2 minutes).

---

## 4. Team Collaboration Guide

**Goal:** Work on the same project without overwriting each other's work.

### Principles
- **Never push directly to `main`** if working in a team.
- **Start Every Session** with a Pull: Before you start coding, always run `git checkout main` and `git pull` to ensure you have the latest code.
- Use **Branches** for features.
- Use **Pull Requests (PRs)** to merge code.

### The Workflow

#### A. Starting a New Feature (Developer A)
1.  **Get latest code**:
    ```bash
    git checkout main
    git pull
    ```
2.  **Create a new branch**:
    ```bash
    git checkout -b feature/new-sidebar
    ```
3.  **Code, Add, and Commit** as usual (see Section 3).
4.  **Push the branch** (first time only):
    ```bash
    git push -u origin feature/new-sidebar
    ```

#### B. Merging Changes (GitHub)
1.  Go to the repo on GitHub.
2.  You will see a yellow banner: **"feature/new-sidebar had recent pushes"** -> Click **Compare & pull request**.
3.  Write a title/description.
4.  Click **Create Pull Request**.
5.  **Review**: Teammates can review the code files.
6.  **Merge**: Click **"Merge pull request"**.

#### C. syncing Local (Developer B)
1.  Developer B wants the new sidebar code:
    ```bash
    git checkout main
    git pull
    ```

### Handling Conflicts
If two people edited the same line:
1.  Git will warn you about a "Merge Conflict" when you pull or merge.
2.  Open the file in your editor (VS Code).
3.  Look for `<<<<<<<`, `=======`, `>>>>>>>`.
4.  Delete the markers and keep the code you want.
5.  Save, `git add .`, `git commit`, and `git push`.
