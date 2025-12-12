# 🌐 Linear Programming Web App

An interactive web application for solving product-mix linear programming problems. Perfect for Operations Management and Supply Chain Management students!

![Version](https://img.shields.io/badge/version-1.0.0-blue)
![Python](https://img.shields.io/badge/python-3.8+-green)
![Streamlit](https://img.shields.io/badge/streamlit-1.28+-red)

---

## ✨ Features

### 🎯 For Students
- **Zero coding required** - Just input your problem data
- **Instant solutions** - Get optimal results in seconds
- **Visual insights** - Interactive charts and graphs
- **Export functionality** - Download results for homework
- **Built-in examples** - Learn from pre-loaded problems
- **Mobile-friendly** - Works on phones and tablets

### 👨‍🏫 For Instructors
- **Team-Based Learning ready** - Perfect for in-class exercises
- **Multiple scenarios** - Students can experiment quickly
- **Educational content** - Built-in explanations and help
- **Professional output** - Results ready for grading
- **Easy deployment** - Share via URL or run locally

### 🔧 Technical Features
- Supports maximization and minimization problems
- Handles continuous and integer variables
- Shows resource utilization and slack
- Calculates shadow prices (dual values)
- Interactive data tables
- Beautiful Plotly visualizations

---

## 🚀 Quick Start

### Method 1: Double-Click Launch (Easiest!)

**Windows:**
1. Double-click `launch_app.bat`
2. Wait for browser to open
3. Start solving!

**Mac/Linux:**
1. Double-click `launch_app.sh` (or run `./launch_app.sh` in terminal)
2. Wait for browser to open
3. Start solving!

**All Platforms (Python script):**
```bash
python launch_app.py
```

### Method 2: Manual Launch

```bash
# Install dependencies (first time only)
pip install -r requirements_webapp.txt

# Run the app
streamlit run lp_web_app.py
```

### Method 3: Access Online

Your instructor may provide a URL to access the app online without any installation.

---

## 📦 What's Included

### Core Files
- **`lp_web_app.py`** - Main web application
- **`requirements_webapp.txt`** - Python dependencies

### Launcher Scripts
- **`launch_app.py`** - Universal Python launcher
- **`launch_app.bat`** - Windows batch file
- **`launch_app.sh`** - Mac/Linux shell script

### Documentation
- **`STUDENT_GUIDE.md`** - Complete student reference
- **`DEPLOYMENT_GUIDE.md`** - Instructor deployment guide
- **`README_WEBAPP.md`** - This file

---

## 📖 How to Use

### Step-by-Step for Students

1. **Configure Problem (Sidebar)**
   - Enter number of products and resources
   - Choose maximize or minimize
   - Select continuous or integer variables

2. **Input Data (Main Area)**
   - Name your products and enter profits/costs
   - Name your resources and enter available amounts
   - Fill in the usage matrix (how much of each resource each product uses)

3. **Solve**
   - Click the "Solve Problem" button
   - Results appear automatically

4. **Analyze Results**
   - View optimal production quantities
   - Check resource utilization
   - Understand shadow prices
   - Download report

### Example Problem

**Wyndor Glass Co.**
- **Products**: Doors ($300 profit), Windows ($500 profit)
- **Resources**: 
  - Plant 1: 4 hours (1 hr/door)
  - Plant 2: 12 hours (2 hrs/window)
  - Plant 3: 18 hours (3 hrs/door, 2 hrs/window)
- **Solution**: Make 2 doors and 6 windows for $3,600 profit

Load this example directly in the app to see how it works!

---

## 💡 Key Concepts

### Decision Variables
What you're deciding (usually production quantities)

### Objective Function
What you're trying to optimize (maximize profit or minimize cost)

### Constraints
Limitations on your decision (resource availability)

### Optimal Solution
The best feasible solution that satisfies all constraints

### Shadow Price
The value of obtaining one more unit of a resource
- High shadow price = valuable resource
- Zero shadow price = resource has slack (not fully utilized)

### Binding Constraint
A constraint that is fully utilized (slack = 0)

---

## 🎓 Educational Use

### Perfect For:
- Operations Management courses (SCM 361, 461, 478)
- Supply Chain Management courses
- Operations Research courses
- Management Science courses

### Learning Objectives:
Students will be able to:
1. ✅ Formulate LP problems from word problems
2. ✅ Identify decision variables and constraints
3. ✅ Interpret optimal solutions
4. ✅ Understand shadow prices and sensitivity
5. ✅ Make data-driven business decisions

### Classroom Activities:

**Individual Practice:**
- Homework verification
- What-if analysis
- Sensitivity exploration

**Team-Based Learning:**
- Collaborative problem solving
- Compare different scenarios
- Discuss business implications

**In-Class Demonstration:**
- Project app on screen
- Build problem together
- Analyze results as a class

---

## 🔧 Technical Requirements

### Minimum Requirements:
- Python 3.8 or higher
- 2GB RAM
- Modern web browser (Chrome, Firefox, Safari, Edge)
- Internet connection (for initial setup)

### Dependencies:
```
streamlit >= 1.28.0
pulp >= 2.7.0
pandas >= 2.0.0
numpy >= 1.24.0
plotly >= 5.17.0
```

All dependencies install automatically with the launcher scripts!

---

## 🌐 Deployment Options

### 1. Local Use (Computer Lab)
Run on individual computers or lab machines
- **Pros**: Complete privacy, works offline
- **Cons**: Each machine needs setup

### 2. Streamlit Cloud (Recommended)
Free hosting for public apps
- **Pros**: Share via URL, no maintenance
- **Cons**: Public by default
- **Setup**: Push to GitHub, deploy at share.streamlit.io

### 3. Department Server
Host on BYU-Idaho servers
- **Pros**: Private, integrated with systems
- **Cons**: Requires IT support

See **DEPLOYMENT_GUIDE.md** for detailed instructions!

---

## 📊 Screenshots

### Main Interface
Students input problem data in a clean, intuitive interface with:
- Sidebar for configuration
- Tabs for data entry, solving, and results
- Built-in help and examples

### Results Dashboard
Professional results display with:
- Optimal production plan
- Resource utilization charts
- Shadow price analysis
- Export functionality

---

## 🚨 Troubleshooting

### Common Issues

**App won't start:**
- Make sure Python 3.8+ is installed
- Run: `python --version` to check
- Reinstall dependencies: `pip install -r requirements_webapp.txt`

**Port already in use:**
- Another app is using port 8501
- Use different port: `streamlit run lp_web_app.py --server.port 8502`

**"Infeasible" result:**
- Constraints too restrictive
- Double-check all data entry
- Verify problem is correctly specified

**Changes not showing:**
- Click "Rerun" button at top
- Or press 'R' in terminal

**Browser doesn't open:**
- Manually navigate to: http://localhost:8501

See **STUDENT_GUIDE.md** for complete troubleshooting!

---

## 🎨 Customization

### For Instructors

Want to customize for your course?

1. **Change Branding**
   - Edit header in `lp_web_app.py`
   - Add institution logo
   - Update color scheme

2. **Add Custom Examples**
   - Create new example problems
   - Add to sidebar buttons
   - Include course-specific scenarios

3. **Modify Interface**
   - Adjust input fields
   - Add validation rules
   - Include additional help text

4. **Track Usage** (Optional)
   - Add simple logging
   - Monitor which problems students solve
   - Gather analytics (respect FERPA!)

---

## 📚 Additional Resources

### Documentation
- **STUDENT_GUIDE.md** - Complete student reference with examples
- **DEPLOYMENT_GUIDE.md** - Deployment and customization guide
- **Streamlit Docs**: [docs.streamlit.io](https://docs.streamlit.io)
- **PuLP Docs**: [coin-or.github.io/pulp](https://coin-or.github.io/pulp/)

### Related Files
This web app is part of a larger LP toolkit that includes:
- Command-line Python solvers
- Generic templates for custom problems
- Interactive problem builders
- Step-by-step conversion guides

---

## 🤝 Contributing

### Found a Bug?
- Check if it's a data entry issue first
- Document the problem clearly
- Include screenshots if possible

### Have a Feature Request?
- What would make the app more useful?
- How would students benefit?
- Submit detailed suggestions

### Want to Customize?
- Fork the code
- Make your modifications
- Share improvements with others!

---

## 📜 License

This educational tool is provided for academic use in Operations Management and Supply Chain Management courses.

---

## 🙏 Acknowledgments

Built for:
- BYU-Idaho Operations Management courses
- Students learning linear programming
- Instructors teaching optimization

Powered by:
- [Streamlit](https://streamlit.io) - Web app framework
- [PuLP](https://github.com/coin-or/pulp) - Linear programming library
- [Plotly](https://plotly.com) - Interactive visualizations

---

## 📞 Support

### For Students:
1. Check the **Help** tab in the app
2. Review **STUDENT_GUIDE.md**
3. Try example problems
4. Ask your instructor

### For Instructors:
1. Review **DEPLOYMENT_GUIDE.md**
2. Check Streamlit documentation
3. Test locally before deploying
4. Contact IT for server deployment

---

## 🎯 Quick Reference

| Task | Command |
|------|---------|
| Launch app (Windows) | Double-click `launch_app.bat` |
| Launch app (Mac/Linux) | `./launch_app.sh` |
| Launch app (Universal) | `python launch_app.py` |
| Manual launch | `streamlit run lp_web_app.py` |
| Install dependencies | `pip install -r requirements_webapp.txt` |
| Access app | http://localhost:8501 |
| Stop server | Ctrl+C |

---

## 📈 Version History

**v1.0.0** - Initial Release
- Core functionality for product-mix problems
- Interactive data input
- Visual results dashboard
- Shadow price analysis
- Export functionality
- Example problems
- Comprehensive help system

---

## 🚀 Getting Started Checklist

- [ ] Python 3.8+ installed
- [ ] Download all files to same folder
- [ ] Run launcher script
- [ ] Try example problem
- [ ] Read STUDENT_GUIDE.md
- [ ] Solve your first homework problem
- [ ] Share with classmates!

---

**Ready to optimize? Let's go! 📊🎓**

For questions or feedback, contact your course instructor.

---

**Made with ❤️ for Operations Management students**
