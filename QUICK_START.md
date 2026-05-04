# 🚀 Quick Start Guide - Run the Project in 5 Minutes

## ✅ Prerequisites Check

Before starting, make sure you have:
- ✅ Python 3.8 or higher installed
- ✅ Node.js 16 or higher installed
- ✅ Git installed (optional)

**Check your versions:**
```bash
python --version    # Should show 3.8+
node --version      # Should show 16+
npm --version       # Should show 8+
```

---

## 🎯 Step-by-Step Instructions

### **STEP 1: Navigate to Project Directory**

Open your terminal/command prompt and go to the project folder:

```bash
cd review-insight-system
```

---

### **STEP 2: Install Python Dependencies**

Install required Python packages:

```bash
pip install -r requirements.txt
```

**Wait for installation to complete** (takes 1-2 minutes)

---

### **STEP 3: Generate Sample Data**

Run the main script to process reviews:

```bash
python main.py --no-dashboard
```

**What this does:**
- Generates 300 sample reviews
- Analyzes sentiment
- Detects aspects
- Creates insights
- Saves `processed_reviews.csv` and `report.json`

**Expected output:**
```
Generating 300 sample reviews...
[1/5] Preprocessing text...
[2/5] Running sentiment analysis...
[3/5] Classifying aspects...
[4/5] Generating insights...
[5/5] Evaluating model...
Saved: processed_reviews.csv, report.json
```

⏱️ **Takes about 30 seconds**

---

### **STEP 4: Start the Backend API**

Open a **NEW terminal window** (keep the first one open) and run:

```bash
cd review-insight-system
python api.py
```

**Expected output:**
```
API running at http://localhost:5000
 * Running on http://127.0.0.1:5000
```

✅ **Backend is now running!** (Don't close this terminal)

---

### **STEP 5: Install Frontend Dependencies**

Open a **THIRD terminal window** and run:

```bash
cd review-insight-system/frontend
npm install
```

**Wait for installation to complete** (takes 2-3 minutes)

---

### **STEP 6: Start the Frontend**

In the same terminal (frontend folder), run:

```bash
npm run dev
```

**Expected output:**
```
  VITE v8.0.10  ready in 500 ms

  ➜  Local:   http://localhost:5173/
  ➜  Network: use --host to expose
```

✅ **Frontend is now running!**

---

### **STEP 7: Open in Browser**

Open your web browser and go to:

```
http://localhost:5173
```

🎉 **You should see the Review Insight System dashboard!**

---

## 🖥️ What You Should See

### Terminal Windows (3 total):

**Terminal 1:** Closed (data generation complete)
**Terminal 2:** Backend API running on port 5000
**Terminal 3:** Frontend dev server running on port 5173

### Browser:
- Beautiful dashboard with charts
- Sidebar with 5 navigation items
- Data showing 300 reviews analyzed

---

## 🎮 Quick Tour

### 1. **Dashboard Page** (Default)
- See overall statistics
- View sentiment distribution
- Check top problems and features

### 2. **Aspects Page** (Click "Aspects" in sidebar)
- See sentiment by aspect
- View aspect health radar
- Check detailed metrics

### 3. **Reviews Page** (Click "Reviews" in sidebar)
- Browse all reviews
- Filter by sentiment
- See keyword clouds

### 4. **Analyzer Page** (Click "Analyzer" in sidebar)
- Type any review text
- Click "Analyze" button
- See instant results

### 5. **Metrics Page** (Click "Evaluation" in sidebar)
- View model accuracy
- Check confusion matrix
- See performance metrics

---

## 🛑 How to Stop

When you're done:

1. **Stop Frontend:** Press `Ctrl + C` in Terminal 3
2. **Stop Backend:** Press `Ctrl + C` in Terminal 2
3. **Close terminals**

---

## 🔄 How to Restart

Next time you want to run it:

**Terminal 1:**
```bash
cd review-insight-system
python api.py
```

**Terminal 2:**
```bash
cd review-insight-system/frontend
npm run dev
```

**Browser:**
```
http://localhost:5173
```

---

## ❌ Troubleshooting

### Problem: "Module not found" error

**Solution:**
```bash
pip install -r requirements.txt
```

---

### Problem: "Port 5000 already in use"

**Solution:**
```bash
# Windows
netstat -ano | findstr :5000
taskkill /PID <PID_NUMBER> /F

# Mac/Linux
lsof -ti:5000 | xargs kill -9
```

---

### Problem: "Port 5173 already in use"

**Solution:**
```bash
# Windows
netstat -ano | findstr :5173
taskkill /PID <PID_NUMBER> /F

# Mac/Linux
lsof -ti:5173 | xargs kill -9
```

---

### Problem: Frontend shows "Failed to fetch"

**Solution:**
- Make sure backend is running (Terminal 2)
- Check `http://localhost:5000/api/summary` in browser
- If it shows JSON data, backend is working

---

### Problem: NLTK data not found

**Solution:**
```bash
python -c "import nltk; nltk.download('vader_lexicon'); nltk.download('stopwords'); nltk.download('wordnet')"
```

---

### Problem: Python command not found

**Solution:**
Try using `python3` instead:
```bash
python3 --version
python3 main.py --no-dashboard
python3 api.py
```

---

## 📝 Using Your Own Data

Want to analyze your own reviews?

### Step 1: Prepare CSV file
Create a CSV file with these columns:
- `text` (required): The review text
- `label` (optional): positive/negative/neutral for evaluation

**Example CSV:**
```csv
text,label
"Great product, love it!",positive
"Terrible quality, broke immediately",negative
"It's okay, nothing special",neutral
```

### Step 2: Run with your CSV
```bash
python main.py --csv your_reviews.csv --no-dashboard
```

### Step 3: Start API and Frontend
```bash
# Terminal 1
python api.py

# Terminal 2
cd frontend
npm run dev
```

---

## 🎯 Quick Command Reference

### Generate Data
```bash
python main.py --no-dashboard
```

### Start Backend
```bash
python api.py
```

### Start Frontend
```bash
cd frontend
npm run dev
```

### Install Dependencies
```bash
# Python
pip install -r requirements.txt

# Frontend
cd frontend
npm install
```

### Check if Running
```bash
# Backend
curl http://localhost:5000/api/summary

# Frontend
# Open http://localhost:5173 in browser
```

---

## 🎨 Customization Options

### Change Number of Sample Reviews
```bash
python main.py --samples 500 --no-dashboard
```

### Change API Port
```bash
# Edit api.py, change last line:
app.run(debug=False, port=8000)
```

### Change Frontend Port
```bash
# Edit frontend/vite.config.js, add:
server: { port: 3000 }
```

---

## 📊 Expected Results

After running successfully, you should have:

### Files Created:
- ✅ `processed_reviews.csv` (300 rows with sentiment, aspects, etc.)
- ✅ `report.json` (complete analysis report)

### Services Running:
- ✅ Backend API on `http://localhost:5000`
- ✅ Frontend on `http://localhost:5173`

### Data Visible:
- ✅ ~130 positive reviews
- ✅ ~90 neutral reviews
- ✅ ~80 negative reviews
- ✅ 12 aspects analyzed
- ✅ Keywords extracted
- ✅ Recommendations generated

---

## 🚀 For Presentation/Demo

### Before Your Demo:

**1 Day Before:**
```bash
# Test everything works
python main.py --no-dashboard
python api.py  # In separate terminal
cd frontend && npm run dev  # In another terminal
```

**1 Hour Before:**
```bash
# Start services
python api.py  # Terminal 1
cd frontend && npm run dev  # Terminal 2
```

**5 Minutes Before:**
- Open browser to `http://localhost:5173`
- Test all 5 pages
- Prepare sample text for Live Analyzer
- Have backup screenshots ready

---

## 💡 Pro Tips

### Tip 1: Keep Terminals Organized
- Label Terminal 1: "BACKEND"
- Label Terminal 2: "FRONTEND"
- Use different colors if possible

### Tip 2: Bookmark URLs
- Backend: `http://localhost:5000/api/summary`
- Frontend: `http://localhost:5173`

### Tip 3: Prepare Sample Reviews
Have these ready for Live Analyzer demo:
```
"Amazing camera quality but battery dies too fast"
"Terrible customer service, very disappointed"
"The design is beautiful and feels premium"
```

### Tip 4: Check Logs
If something breaks, check terminal outputs for error messages

### Tip 5: Have Backup
Take screenshots of all pages in case of technical issues

---

## 📞 Need Help?

### Check These First:
1. Are all dependencies installed?
2. Are both terminals running?
3. Is the browser on the correct URL?
4. Are there any error messages in terminals?

### Common Issues:
- **Blank page**: Check browser console (F12)
- **No data**: Make sure you ran `python main.py` first
- **Connection error**: Backend might not be running
- **Slow loading**: First load takes longer, be patient

---

## ✅ Success Checklist

Before your presentation, verify:

- [ ] Python dependencies installed
- [ ] Frontend dependencies installed
- [ ] Sample data generated (processed_reviews.csv exists)
- [ ] Backend running (Terminal 1)
- [ ] Frontend running (Terminal 2)
- [ ] Browser shows dashboard
- [ ] All 5 pages load correctly
- [ ] Live Analyzer works
- [ ] Charts display data
- [ ] No error messages in terminals

---

## 🎉 You're Ready!

If you can see the dashboard with data, **you're all set!**

Enjoy exploring the Review Insight System! 🚀

---

**Last Updated:** 2025
**Questions?** Check FEATURES_DOCUMENTATION.md for detailed explanations
