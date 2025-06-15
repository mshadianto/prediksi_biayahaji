#!/usr/bin/env python3
"""
Diagnostic script to check project setup and fix common issues
"""

import os
import sys
from pathlib import Path

def check_and_create_init_files():
    """Ensure __init__.py files exist in all Python packages"""
    python_dirs = [
        "src",
        "src/core", 
        "src/components",
        "src/utils",
        "src/models"
    ]
    
    print("🔍 Checking __init__.py files...")
    
    for dir_path in python_dirs:
        if os.path.exists(dir_path):
            init_file = os.path.join(dir_path, "__init__.py")
            if not os.path.exists(init_file):
                print(f"➕ Creating {init_file}")
                with open(init_file, "w") as f:
                    f.write(f'"""Package: {dir_path}"""\n')
            else:
                print(f"✅ {init_file} exists")
        else:
            print(f"❌ Directory {dir_path} not found")
    
    print("✅ __init__.py check completed!\n")

def check_critical_files():
    """Check if all critical files exist"""
    critical_files = {
        "src/core/config.py": "Configuration management",
        "src/core/data_collector.py": "Data collection from APIs",
        "src/core/rag_system.py": "RAG system implementation", 
        "src/core/agentic_ai.py": "Agentic AI implementation",
        "src/core/predictor.py": "Hajj cost predictor",
        "src/components/sidebar.py": "Sidebar component",
        "src/components/dashboard.py": "Dashboard component",
        "src/components/ai_chat.py": "AI chat component",
        "src/utils/visualizations.py": "Visualization utilities",
        "requirements.txt": "Python dependencies",
        "app.py": "Main Streamlit application"
    }
    
    print("🔍 Checking critical files...")
    
    missing_files = []
    
    for file_path, description in critical_files.items():
        if os.path.exists(file_path):
            print(f"✅ {file_path} - {description}")
        else:
            print(f"❌ {file_path} - {description}")
            missing_files.append(file_path)
    
    if missing_files:
        print(f"\n⚠️ Found {len(missing_files)} missing files!")
        return False
    else:
        print("\n✅ All critical files found!")
        return True

def test_imports():
    """Test if imports work correctly"""
    print("🔍 Testing imports...")
    
    # Add src to path
    src_path = os.path.join(os.getcwd(), "src")
    if src_path not in sys.path:
        sys.path.insert(0, src_path)
    
    import_tests = [
        ("core.config", "Config"),
        ("core.data_collector", "DataCollector"),
        ("core.rag_system", "RAGSystem"),
        ("core.agentic_ai", "AgenticAI"),
        ("core.predictor", "HajjCostPredictor"),
        ("components.sidebar", "render_sidebar"),
        ("components.dashboard", "render_dashboard"),
        ("components.ai_chat", "render_ai_chat"),
        ("utils.visualizations", "create_prediction_chart")
    ]
    
    all_imports_successful = True
    
    for module_name, class_name in import_tests:
        try:
            module = __import__(module_name, fromlist=[class_name])
            getattr(module, class_name)
            print(f"✅ {module_name}.{class_name}")
        except ImportError as e:
            print(f"❌ {module_name}.{class_name} - {e}")
            all_imports_successful = False
        except AttributeError as e:
            print(f"⚠️ {module_name}.{class_name} - {e}")
            all_imports_successful = False
    
    if all_imports_successful:
        print("\n✅ All imports successful!")
    else:
        print("\n❌ Some imports failed!")
    
    return all_imports_successful

def check_dependencies():
    """Check if required dependencies are installed"""
    print("🔍 Checking dependencies...")
    
    required_packages = [
        "streamlit",
        "requests", 
        "pandas",
        "numpy",
        "plotly"
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package}")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n⚠️ Missing packages: {', '.join(missing_packages)}")
        print("Run: pip install -r requirements.txt")
        return False
    else:
        print("\n✅ All dependencies installed!")
        return True

def fix_common_issues():
    """Fix common setup issues"""
    print("🔧 Fixing common issues...")
    
    # 1. Ensure __init__.py files exist
    check_and_create_init_files()
    
    # 2. Create minimal requirements.txt if missing
    if not os.path.exists("requirements.txt"):
        print("➕ Creating requirements.txt")
        with open("requirements.txt", "w") as f:
            f.write("""streamlit==1.29.0
requests==2.31.0
pandas==2.1.3
numpy==1.24.3
plotly==5.17.0
scikit-learn==1.3.2
python-dotenv==1.0.0
""")
    
    # 3. Create .env.example if missing
    if not os.path.exists(".env.example"):
        print("➕ Creating .env.example")
        with open(".env.example", "w") as f:
            f.write("""# API Keys
OPENROUTER_API_KEY=your_openrouter_key_here
FINNHUB_API_KEY=your_finnhub_key_here
FIXER_API_KEY=your_fixer_key_here
""")
    
    print("✅ Common issues fixed!")

def create_minimal_working_app():
    """Create a minimal working version if main files are missing"""
    print("🔧 Creating minimal working app...")
    
    minimal_app = '''import streamlit as st
import requests
import pandas as pd
from datetime import datetime

st.set_page_config(
    page_title="🕌 Prediksi Biaya Haji - Minimal Version",
    page_icon="🕌",
    layout="wide"
)

st.title("🕌 Prediksi Biaya Haji Indonesia (Minimal Version)")
st.markdown("*Versi minimal - sedang dalam pengembangan*")

# Demo data
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Harga Emas (Demo)", "$2,000.50", "+15.25")

with col2:
    st.metric("USD/IDR (Demo)", "Rp 15,000", "+50")

with col3:
    st.metric("Prediksi Biaya Haji", "Rp 75,000,000", "+5%")

st.success("✅ Aplikasi minimal berjalan! Jalankan setup_project.py untuk versi lengkap.")

# Component breakdown
st.header("💰 Komponen Biaya Haji")

demo_costs = {
    "Biaya Pendaftaran": 500000,
    "Transportasi Udara": 25000000,
    "Akomodasi Makkah": 15000000,
    "Akomodasi Madinah": 10000000,
    "Makan & Konsumsi": 8000000,
    "Perlengkapan": 5000000,
    "Lain-lain": 10500000
}

df = pd.DataFrame([
    {"Komponen": k, "Biaya (IDR)": f"Rp {v:,}"}
    for k, v in demo_costs.items()
])

st.dataframe(df, use_container_width=True)

total = sum(demo_costs.values())
st.success(f"**Total Estimasi**: Rp {total:,}")

# Setup instructions
with st.expander("🛠️ Setup Aplikasi Lengkap"):
    st.markdown("""
    **Untuk fitur lengkap, jalankan:**
    
    ```bash
    # 1. Setup project structure
    python setup_project.py
    
    # 2. Install dependencies  
    pip install -r requirements.txt
    
    # 3. Restart aplikasi
    streamlit run app.py
    ```
    
    **Atau download file setup dari artifacts di atas.**
    """)
'''
    
    with open("app_minimal.py", "w") as f:
        f.write(minimal_app)
    
    print("✅ Created app_minimal.py as backup!")

def main():
    """Main diagnostic function"""
    print("🚀 Starting project diagnostic...\n")
    
    # Check current directory
    print(f"📁 Current directory: {os.getcwd()}")
    print(f"🐍 Python version: {sys.version}")
    print(f"📦 Python executable: {sys.executable}\n")
    
    # Run checks
    files_ok = check_critical_files()
    deps_ok = check_dependencies() 
    
    if not files_ok:
        print("\n🔧 Attempting to fix file issues...")
        fix_common_issues()
        
        if not os.path.exists("src/core/config.py"):
            print("\n⚠️ Critical files still missing!")
            print("📥 Please run setup_project.py first:")
            print("   python setup_project.py")
            
            # Create minimal working app as fallback
            create_minimal_working_app()
            print("\n🎯 Created app_minimal.py as fallback!")
            print("   Run: streamlit run app_minimal.py")
    
    if not deps_ok:
        print("\n📦 Please install dependencies:")
        print("   pip install -r requirements.txt")
    
    # Test imports if files exist
    if files_ok:
        print("\n🧪 Testing imports...")
        imports_ok = test_imports()
        
        if imports_ok:
            print("\n🎉 All checks passed! Your app should work now.")
            print("🚀 Run: streamlit run app.py")
        else:
            print("\n⚠️ Import issues detected. Check file contents.")
    
    print("\n✅ Diagnostic completed!")

if __name__ == "__main__":
    main()
'''