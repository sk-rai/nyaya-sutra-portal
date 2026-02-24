# Migration Guide - Moving Project to New Laptop

**Project:** Nyaya Sutra Legal Portal  
**Date:** February 23, 2026  
**Purpose:** Migrate project and Kiro license to new laptop

---

## 📋 Table of Contents

1. [Pre-Migration Checklist](#pre-migration-checklist)
2. [Kiro License Migration](#kiro-license-migration)
3. [Project Migration Steps](#project-migration-steps)
4. [Post-Migration Verification](#post-migration-verification)
5. [Cleanup Old Machine](#cleanup-old-machine)

---

## ✅ Pre-Migration Checklist

### Current Machine Status:

**Untracked Files Found:**
- `IMG-20260222-WA0010.jpg` - Client mockup image
- `IMG-20260222-WA0011.jpg` - Client mockup image
- `IMG-20260222-WA0015.jpg` - Client mockup image
- `IMG-20260222-WA0016.jpg` - Client mockup image
- `VISUAL_CHANGES_DIAGRAM.txt` - Visual changes documentation
- `.vscode/settings.json` - Modified VSCode settings

**Decision Required:**
Do you want to commit these files to git?

### Recommendation:

**YES - Commit mockup images:**
- These are client reference materials
- Useful for future reference
- Should be version controlled

**MAYBE - Commit visual diagram:**
- If it contains useful documentation, commit it
- If it's just temporary notes, skip it

**NO - Don't commit .vscode/settings.json:**
- This is machine-specific
- Already in .gitignore (should be)
- Will be recreated on new machine

---

## 🔑 Kiro License Migration

### Understanding Kiro Licensing:

Kiro licenses are typically tied to:
1. **User account** (not machine-specific)
2. **Activation limit** (number of concurrent machines)

### Migration Process:

#### Option 1: Deactivate on Old Machine (Recommended)

**On Current Machine (CIPL1114):**

1. **Deactivate Kiro License:**
   ```
   - Open Kiro
   - Go to: Settings → Account → License
   - Click "Deactivate License" or "Sign Out"
   - Confirm deactivation
   ```

2. **This frees up the license slot for new machine**

**On New Machine:**

1. **Install Kiro**
2. **Sign in with your account**
3. **License will activate automatically**

#### Option 2: Use Multiple Activations (If Available)

If your Kiro license allows multiple machines:

1. **Keep license active on current machine**
2. **Simply sign in on new machine**
3. **Both will work simultaneously**

#### Option 3: Contact Kiro Support

If you encounter issues:

1. **Email:** support@kiro.ai (or check Kiro documentation)
2. **Explain:** Moving to new machine
3. **Request:** License transfer assistance
4. **Provide:** Your account email and license key

### Important Notes:

- **Personal licenses** are usually transferable
- **You can use on one machine at a time** (typically)
- **Deactivating is cleaner** than just deleting
- **Your work/settings are cloud-synced** (if enabled)

---

## 🚀 Project Migration Steps

### Step 1: Commit Remaining Files (Current Machine)

**Decision: Commit mockup images for reference**

```bash
# Add mockup images
git add IMG-20260222-WA0010.jpg
git add IMG-20260222-WA0011.jpg
git add IMG-20260222-WA0015.jpg
git add IMG-20260222-WA0016.jpg

# Optional: Add visual diagram if useful
git add VISUAL_CHANGES_DIAGRAM.txt

# Commit
git commit -m "Add client mockup images and visual documentation for reference"

# Push to GitHub
git push origin main
```

**Skip .vscode/settings.json:**
```bash
# Discard changes (machine-specific)
git restore .vscode/settings.json
```

### Step 2: Verify Everything is Pushed

```bash
# Check status
git status
# Should show: "nothing to commit, working tree clean"

# Verify remote is up to date
git log origin/main..HEAD
# Should show: nothing (all commits pushed)

# List all branches
git branch -a
# Should show: main and gh-pages

# Verify gh-pages is also up to date
git checkout gh-pages
git status
git push origin gh-pages  # If needed
git checkout main
```

### Step 3: Document Important Information

**Save these details somewhere safe:**

1. **Repository URL:**
   ```
   https://github.com/sk-rai/nyaya-sutra-portal.git
   ```

2. **SSH Key Location (if using SSH):**
   ```
   ~/.ssh/id_rsa
   ~/.ssh/id_rsa.pub
   ```

3. **Git Configuration:**
   ```bash
   git config user.name
   git config user.email
   ```

4. **Live URLs:**
   - GitHub Pages: https://sk-rai.github.io/nyaya-sutra-portal/
   - Netlify: https://prismatic-halva-095761.netlify.app

5. **Important Credentials:**
   - GitHub username/token
   - Netlify account details
   - Any API keys (if added later)

### Step 4: Setup New Machine

**On New Laptop:**

#### A. Install Prerequisites

```bash
# Install Git
sudo apt update
sudo apt install git

# Install Node.js (if needed for future backend)
# Download from: https://nodejs.org/

# Install Kiro
# Download from: https://kiro.ai/download
```

#### B. Configure Git

```bash
# Set your identity
git config --global user.name "Santosh Rai"
git config --global user.email "santoshrai@crimsoni.com"

# Verify
git config --list
```

#### C. Setup SSH Key (Recommended)

```bash
# Generate new SSH key
ssh-keygen -t rsa -b 4096 -C "santoshrai@crimsoni.com"

# Start SSH agent
eval "$(ssh-agent -s)"

# Add key
ssh-add ~/.ssh/id_rsa

# Copy public key
cat ~/.ssh/id_rsa.pub
# Copy output and add to GitHub: Settings → SSH Keys → New SSH Key
```

#### D. Clone Repository

```bash
# Navigate to desired location
cd ~/Documents/POC/

# Clone using SSH (recommended)
git clone git@github.com:sk-rai/nyaya-sutra-portal.git

# OR clone using HTTPS
git clone https://github.com/sk-rai/nyaya-sutra-portal.git

# Enter directory
cd nyaya-sutra-portal

# Verify
git status
git branch -a
```

#### E. Setup Kiro

```bash
# Open Kiro
# Sign in with your account
# License should activate automatically

# Open the cloned project folder in Kiro
# File → Open Folder → Select nyaya-sutra-portal
```

### Step 5: Verify Everything Works

**On New Machine:**

```bash
# Check all files are present
ls -la

# Check git status
git status

# Check branches
git branch -a

# Pull latest (should be up to date)
git pull origin main

# Check gh-pages branch
git checkout gh-pages
git pull origin gh-pages
git checkout main

# Test if you can make changes
echo "# Test" >> TEST.md
git add TEST.md
git commit -m "Test commit from new machine"
git push origin main

# If successful, remove test file
git rm TEST.md
git commit -m "Remove test file"
git push origin main
```

---

## 🧪 Post-Migration Verification

### Checklist for New Machine:

- [ ] Git installed and configured
- [ ] SSH key setup and added to GitHub
- [ ] Repository cloned successfully
- [ ] All files present (check file count)
- [ ] All branches available (main, gh-pages)
- [ ] Can pull from remote
- [ ] Can push to remote
- [ ] Kiro installed and activated
- [ ] Kiro can open project folder
- [ ] Kiro license shows as active
- [ ] Can edit files in Kiro
- [ ] Can run git commands from Kiro terminal

### Test Workflow:

1. **Make a small change:**
   ```bash
   echo "Migration successful - $(date)" >> MIGRATION_LOG.md
   ```

2. **Commit and push:**
   ```bash
   git add MIGRATION_LOG.md
   git commit -m "Test: Verify new machine setup"
   git push origin main
   ```

3. **Check GitHub:**
   - Go to: https://github.com/sk-rai/nyaya-sutra-portal
   - Verify commit appears
   - Check file is updated

4. **Deploy to gh-pages (optional test):**
   ```bash
   git checkout gh-pages
   git checkout main -- MIGRATION_LOG.md
   cp MIGRATION_LOG.md .
   git add MIGRATION_LOG.md
   git commit -m "Test: Deploy from new machine"
   git push origin gh-pages
   git checkout main
   ```

---

## 🧹 Cleanup Old Machine

### After Successful Migration:

**IMPORTANT: Only do this AFTER verifying new machine works!**

#### Step 1: Deactivate Kiro License

```
- Open Kiro
- Settings → Account → License
- Click "Deactivate" or "Sign Out"
- Confirm
```

#### Step 2: Verify No Uncommitted Work

```bash
cd ~/Documents/POC/nyaya-sutra-portal
git status
# Should show: "nothing to commit, working tree clean"

# Double-check with git log
git log --oneline -5
# Verify latest commits are pushed
```

#### Step 3: Backup (Optional but Recommended)

```bash
# Create a backup archive just in case
cd ~/Documents/POC/
tar -czf nyaya-sutra-portal-backup-$(date +%Y%m%d).tar.gz nyaya-sutra-portal/

# Move backup to safe location
mv nyaya-sutra-portal-backup-*.tar.gz ~/Backups/
```

#### Step 4: Delete Project Folder

```bash
# Navigate to parent directory
cd ~/Documents/POC/

# Delete project folder
rm -rf nyaya-sutra-portal/

# Verify deletion
ls -la
```

#### Step 5: Uninstall Kiro (Optional)

If you're not using this machine anymore:

```bash
# Uninstall Kiro (method depends on installation)
# Check Kiro documentation for uninstall instructions
```

---

## 📝 Quick Reference Commands

### On Current Machine (Before Migration):

```bash
# 1. Commit remaining files
git add IMG-*.jpg VISUAL_CHANGES_DIAGRAM.txt
git commit -m "Add reference materials"
git push origin main

# 2. Verify everything is pushed
git status
git log origin/main..HEAD

# 3. Deactivate Kiro license
# (Do this in Kiro UI)
```

### On New Machine (After Migration):

```bash
# 1. Setup Git
git config --global user.name "Santosh Rai"
git config --global user.email "santoshrai@crimsoni.com"

# 2. Setup SSH (optional but recommended)
ssh-keygen -t rsa -b 4096 -C "santoshrai@crimsoni.com"
ssh-add ~/.ssh/id_rsa
cat ~/.ssh/id_rsa.pub  # Add to GitHub

# 3. Clone repository
cd ~/Documents/POC/
git clone git@github.com:sk-rai/nyaya-sutra-portal.git
cd nyaya-sutra-portal

# 4. Verify
git status
git branch -a
git pull origin main

# 5. Open in Kiro
# File → Open Folder → Select nyaya-sutra-portal
```

---

## ⚠️ Important Warnings

### DO NOT:

1. **Delete old machine files before verifying new machine works**
2. **Forget to deactivate Kiro license on old machine**
3. **Commit sensitive information** (API keys, passwords)
4. **Delete .git folder** (you'll lose all history)
5. **Force push** unless absolutely necessary

### DO:

1. **Verify everything is pushed to GitHub**
2. **Test new machine setup thoroughly**
3. **Keep a backup** (at least temporarily)
4. **Document any custom configurations**
5. **Update SSH keys on GitHub**

---

## 🆘 Troubleshooting

### Issue: Can't push to GitHub from new machine

**Solution:**
```bash
# Check remote URL
git remote -v

# If using HTTPS, you may need personal access token
# Go to: GitHub → Settings → Developer settings → Personal access tokens
# Generate new token with 'repo' scope
# Use token as password when pushing

# Or switch to SSH
git remote set-url origin git@github.com:sk-rai/nyaya-sutra-portal.git
```

### Issue: Kiro license won't activate on new machine

**Solution:**
1. Verify you deactivated on old machine
2. Check internet connection
3. Sign out and sign in again
4. Contact Kiro support if issue persists

### Issue: Missing files after cloning

**Solution:**
```bash
# Check if files were committed
git log --stat

# Check if files are in .gitignore
cat .gitignore

# Pull all branches
git fetch --all
git pull origin main
```

### Issue: Permission denied (SSH)

**Solution:**
```bash
# Verify SSH key is added to GitHub
cat ~/.ssh/id_rsa.pub

# Test SSH connection
ssh -T git@github.com

# Should see: "Hi sk-rai! You've successfully authenticated..."
```

---

## 📞 Support Resources

### Kiro Support:
- Documentation: https://docs.kiro.ai
- Support: Check Kiro app for support options
- Community: Kiro Discord/Forum (if available)

### Git/GitHub:
- Git Documentation: https://git-scm.com/doc
- GitHub Docs: https://docs.github.com
- SSH Setup: https://docs.github.com/en/authentication/connecting-to-github-with-ssh

### Project Repository:
- GitHub: https://github.com/sk-rai/nyaya-sutra-portal
- Issues: https://github.com/sk-rai/nyaya-sutra-portal/issues

---

## ✅ Migration Checklist Summary

### Before Migration (Current Machine):
- [ ] Commit all important files
- [ ] Push everything to GitHub
- [ ] Verify git status is clean
- [ ] Document important information
- [ ] Deactivate Kiro license

### During Migration (New Machine):
- [ ] Install Git
- [ ] Configure Git identity
- [ ] Setup SSH key
- [ ] Clone repository
- [ ] Install Kiro
- [ ] Activate Kiro license
- [ ] Open project in Kiro

### After Migration (Verification):
- [ ] All files present
- [ ] Can pull from GitHub
- [ ] Can push to GitHub
- [ ] Kiro works properly
- [ ] Test workflow successful
- [ ] GitHub Pages still works

### Cleanup (Old Machine):
- [ ] Verify new machine works
- [ ] Create backup (optional)
- [ ] Delete project folder
- [ ] Uninstall Kiro (optional)

---

## 📊 Summary

**Migration is straightforward:**

1. **Commit and push everything** from current machine
2. **Deactivate Kiro license** on current machine
3. **Clone repository** on new machine
4. **Activate Kiro license** on new machine
5. **Verify everything works**
6. **Delete old files** (after verification)

**Key Point:** Since everything is in Git, you can safely delete the local folder and clone fresh on any machine. Your Kiro license is account-based, so you can move it between machines.

---

**Document Created:** February 23, 2026  
**Status:** Ready for Migration  
**Estimated Time:** 30-60 minutes
