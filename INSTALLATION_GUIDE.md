# 📦 Complete Installation Guide - AI Digital Call Center

## 🔧 System Requirements

### Required Software:
1. **Python 3.10 or higher** (3.11 recommended)
2. **pip** (Python package manager - comes with Python)
3. **Internet Connection** (for downloading packages)

### Optional:
- **Git** (for version control)
- **VS Code** or any code editor
- **Web Browser** (Chrome, Firefox, Edge)

---

## 📥 Step-by-Step Installation

### Step 1: Install Python

#### Windows:
1. **Download Python:**
   - Go to: https://www.python.org/downloads/
   - Click "Download Python 3.11.x" (latest version)
   - Or direct link: https://www.python.org/downloads/windows/

2. **Install Python:**
   - Run the downloaded `.exe` file
   - ✅ **IMPORTANT:** Check "Add Python to PATH" checkbox
   - Click "Install Now"
   - Wait for installation to complete

3. **Verify Installation:**
   ```bash
   python --version
   ```
   Should show: `Python 3.11.x` or higher

4. **Verify pip:**
   ```bash
   pip --version
   ```
   Should show: `pip 23.x.x` or higher

#### Mac/Linux:
```bash
# Check if Python is installed
python3 --version

# If not installed:
# Mac: brew install python3
# Linux (Ubuntu/Debian): sudo apt-get install python3 python3-pip
```

---

### Step 2: Download Project Files

#### Option A: If you have the project folder already:
- Just navigate to the project folder in terminal/command prompt

#### Option B: If using Git:
```bash
git clone <repository-url>
cd DECODE
```

---

### Step 3: Install All Dependencies (Automatic)

#### 🚀 EASIEST METHOD - One Command:

**Windows:**
```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

**Mac/Linux:**
```bash
python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt
```

#### What gets installed:
- ✅ **FastAPI** - Backend web framework
- ✅ **Uvicorn** - ASGI server
- ✅ **SQLAlchemy** - Database ORM
- ✅ **Streamlit** - Frontend framework
- ✅ **Plotly** - Data visualization
- ✅ **Requests** - HTTP client
- ✅ **Pydantic** - Data validation
- ✅ All other dependencies automatically

**Installation time:** 2-5 minutes (depending on internet speed)

---

### Step 4: Verify Installation

Check if all packages are installed:

```bash
python -c "import fastapi, streamlit, sqlalchemy; print('✅ All packages installed!')"
```

If no error, you're good to go!

---

## 🎯 Quick Start After Installation

### Method 1: Automatic (Recommended)
Just run:
```bash
# Windows
START.bat

# Or
RUN_EVERYTHING.bat
```

This will:
- Check dependencies
- Initialize database
- Start all services

### Method 2: Manual Start
```bash
# Terminal 1 - Backend
cd backend
python -m uvicorn main:app --reload

# Terminal 2 - Chat Interface
streamlit run ../frontend/chat_interface.py

# Terminal 3 - Dashboard (optional)
streamlit run ../frontend/dashboard.py
```

---

## 🔍 Troubleshooting Installation

### Problem 1: "Python is not recognized"

**Solution:**
1. Python was not added to PATH during installation
2. Reinstall Python and **check "Add Python to PATH"**
3. Or manually add Python to PATH:
   - Search "Environment Variables" in Windows
   - Add Python installation folder to PATH
   - Restart terminal

### Problem 2: "pip is not recognized"

**Solution:**
```bash
# Try using:
python -m pip install -r requirements.txt

# Instead of:
pip install -r requirements.txt
```

### Problem 3: "Permission denied" or "Access denied"

**Solution (Windows):**
```bash
# Run Command Prompt as Administrator
# Right-click Command Prompt > Run as Administrator
# Then try installation again
```

**Solution (Mac/Linux):**
```bash
# Use sudo (if needed)
sudo pip3 install -r requirements.txt

# Or better: use --user flag
pip3 install --user -r requirements.txt
```

### Problem 4: "No module named '...'"

**Solution:**
```bash
# Reinstall all dependencies
pip install --upgrade -r requirements.txt

# Or install specific package
pip install <package-name>
```

### Problem 5: Slow Download / Connection Error

**Solution:**
```bash
# Use timeout flag
pip install --default-timeout=100 -r requirements.txt

# Or use mirror (China/India):
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt
```

### Problem 6: Python Version Too Old

**Check Python version:**
```bash
python --version
```

**If less than 3.10:**
- Download and install Python 3.11+ from python.org
- Make sure to add to PATH

---

## 📋 Dependencies List (for reference)

All these are in `requirements.txt` and install automatically:

| Package | Purpose | Version |
|---------|---------|---------|
| fastapi | Backend API framework | 0.104+ |
| uvicorn | ASGI web server | 0.24+ |
| sqlalchemy | Database ORM | 2.0+ |
| streamlit | Frontend UI | 1.28+ |
| plotly | Charts/graphs | 5.17+ |
| requests | HTTP client | 2.31+ |
| pydantic | Data validation | 2.5+ |

---

## ✅ Installation Checklist

After installation, verify:

- [ ] Python installed (`python --version`)
- [ ] pip installed (`pip --version`)
- [ ] All dependencies installed (`pip list`)
- [ ] Database directory created (automatic)
- [ ] Can run `START.bat` successfully

---

## 🎓 First Time Setup Summary

**Complete Command Sequence:**

```bash
# 1. Check Python
python --version

# 2. Upgrade pip
python -m pip install --upgrade pip

# 3. Install all dependencies
python -m pip install -r requirements.txt

# 4. Verify installation
python -c "import fastapi, streamlit; print('✅ Ready!')"

# 5. Run the application
START.bat
```

**That's it!** 🎉

---

## 🌐 Internet Requirements

- **Initial Setup:** Required (to download packages ~50-100 MB)
- **Runtime:** Not required (all packages installed locally)
- **Updates:** Required (if updating packages)

---

## 💾 Disk Space

- **Python Installation:** ~100 MB
- **Dependencies:** ~200-300 MB
- **Project Files:** ~5 MB
- **Total:** ~400 MB

---

## 📞 Need Help?

If you face any issues:

1. Check Python version: `python --version` (must be 3.10+)
2. Check pip: `pip --version`
3. Try reinstalling: `pip install --upgrade -r requirements.txt`
4. Check error messages carefully
5. Ensure internet connection is stable

---

## 🚀 Next Steps After Installation

1. **Run Setup:** `START.bat` or `RUN_EVERYTHING.bat`
2. **Test Chat:** Open http://localhost:8501
3. **Test Dashboard:** Open http://localhost:8502
4. **View API Docs:** Open http://localhost:8000/docs

---

**Happy Coding! 🎉**


