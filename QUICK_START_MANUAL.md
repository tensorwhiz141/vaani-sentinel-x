# 🚀 Quick Start Guide - Manual Setup

## 🔧 **Step-by-Step Manual Setup**

### **Step 1: Install Backend Dependencies**
```cmd
cd agents_api
pip install fastapi uvicorn pydantic python-multipart aiofiles httpx python-dateutil pytz structlog langdetect orjson python-dotenv
```

### **Step 2: Test Backend**
```cmd
# From the root directory
python test_backend.py
```

### **Step 3: Start Backend (Manual)**
```cmd
cd agents_api
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### **Step 4: Install Frontend Dependencies**
```cmd
cd frontend
npm install
```

### **Step 5: Start Frontend (Manual)**
```cmd
cd frontend
npm start
```

## 🌐 **Access Points**
- **Frontend:** http://localhost:3000
- **Backend API:** http://localhost:8000
- **API Docs:** http://localhost:8000/docs

## 🧪 **Test API Endpoints**

### **Test Translation API:**
```bash
curl -X POST "http://localhost:8000/api/agents/translate" \
  -H "Content-Type: application/json" \
  -d '{
    "original_text": "Hello, how are you?",
    "source_language": "en",
    "target_languages": ["hi"],
    "tone": "formal"
  }'
```

### **Test Health Check:**
```bash
curl http://localhost:8000/health
```

### **Test System Info:**
```bash
curl http://localhost:8000/
```

## 🔧 **Troubleshooting**

### **Backend Issues:**
1. **Import Errors:** Make sure you're in the `agents_api` directory
2. **Port Issues:** Change port if 8000 is busy: `--port 8001`
3. **Dependencies:** Install missing packages with pip

### **Frontend Issues:**
1. **Node.js:** Make sure Node.js 16+ is installed
2. **Dependencies:** Run `npm install` in frontend directory
3. **Port Issues:** React will auto-select available port

### **Common Solutions:**
- Use Command Prompt instead of PowerShell
- Run as Administrator if needed
- Check firewall settings
- Ensure all dependencies are installed

## 🎯 **Success Indicators**

### **Backend Running Successfully:**
```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

### **Frontend Running Successfully:**
```
Compiled successfully!

You can now view vaani-sentinel-x-frontend in the browser.

  Local:            http://localhost:3000
  On Your Network:  http://192.168.x.x:3000
```

## 🎉 **You're Ready!**

Once both servers are running:
1. Open http://localhost:3000 in your browser
2. Navigate through the agent interfaces
3. Test the translation agent with your own text
4. Explore the API documentation at http://localhost:8000/docs

**Your dynamic Vaani Sentinel-X system is now running!** 🚀
