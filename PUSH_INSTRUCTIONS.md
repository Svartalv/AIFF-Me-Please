# How to Push to GitHub

## Option 1: Using SSH Key (Recommended)

### Step 1: Add Your SSH Key to GitHub

**A new SSH key has been generated for you. Follow these steps:**

1. **Copy the new public key** (shown below after generation)

2. Go to: https://github.com/settings/keys

3. Click "New SSH key"

4. Title: "MacBook GitHub" (or any name you prefer)

5. Paste the NEW key (the one that will be shown below)

6. Click "Add SSH key"

**After adding the key to GitHub, we'll configure git to use it and push.**

### Step 2: Switch to SSH and Push

```bash
cd "/Users/pamelagarcia/Coding/AIFF Me Please"
git remote set-url origin git@github.com:Svartalv/AIFF-Me-Please.git
git push -u origin main
```

## Option 2: Using Personal Access Token (Faster Setup)

### Step 1: Create a Personal Access Token

1. Go to: https://github.com/settings/tokens

2. Click "Generate new token" → "Generate new token (classic)"

3. Name it: "AIFF Me Please"

4. Select scopes: Check "repo" (full control of private repositories)

5. Click "Generate token"

6. **COPY THE TOKEN** (you won't see it again!)

### Step 2: Push Using Token

```bash
cd "/Users/pamelagarcia/Coding/AIFF Me Please"
git push https://YOUR_TOKEN@github.com/Svartalv/AIFF-Me-Please.git main
```

Replace `YOUR_TOKEN` with the token you copied.

Or set it as the remote URL:
```bash
git remote set-url origin https://YOUR_TOKEN@github.com/Svartalv/AIFF-Me-Please.git
git push -u origin main
```

## Option 3: Use GitHub CLI (If Installed)

```bash
gh auth login
git push -u origin main
```

## Troubleshooting

**"Permission denied (publickey)"**
- Make sure you added your SSH key to GitHub
- Try: `ssh -T git@github.com` to test

**"HTTP 400" error**
- Use Personal Access Token instead
- Make sure token has "repo" scope

**"Repository not found"**
- Make sure the repository exists at: https://github.com/Svartalv/AIFF-Me-Please
- Check you have write access to the repository

