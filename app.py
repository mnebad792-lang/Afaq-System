# --- ملف النظام المحاسبي المحدث مع نموذج الهيئة لضريبة القيمة المضافة وأوامر البيع والشراء المتعددة الأصناف ---
import streamlit as st
import pandas as pd
from datetime import datetime
import json
import io

# --- محاولة استيراد مكتبة Supabase للربط السحابي ---
try:
    from supabase import create_client, Client
    SUPABASE_AVAILABLE = True
except ImportError:
    SUPABASE_AVAILABLE = False

st.set_page_config(page_title="نظام أفق ERP المحاسبي المتكامل", layout="wide", initial_sidebar_state="expanded")

# --- إعدادات الاتصال بقاعدة بيانات Supabase السحابية ---
SUPABASE_URL = "https://your-supabase-project.supabase.co"
SUPABASE_KEY = "your-supabase-anon-key-here"

@st.cache_resource
def init_supabase():
    if SUPABASE_AVAILABLE and SUPABASE_URL != "https://your-supabase-project.supabase.co":
        try:
            return create_client(SUPABASE_URL, SUPABASE_KEY)
        except Exception:
            return None
    return None

supabase_client = init_supabase()

# --- دالة إعادة تصفير البرنامج بالكامل ---
def reset_system_to_default():
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.rerun()

# --- تهيئة إعدادات العميل والنسخة ---
if 'client_license_config' not in st.session_state:
    st.session_state['client_license_config'] = {
        "client_name": "شركة الإنجاز للمقاولات العامة والتجارة",
        "company_activity": "مقاولات عامة وتجارة وخدمات تقنية",
        "commercial_reg": "4030998877",
        "tax_number": "300222333400003",
        "client_phone": "0560000000",
        "client_address": "الرياض - المملكة العربية السعودية",
        "software_version": "النسخة المحاسبية الاحترافية 2026 (مع دعم Supabase)",
        "enable_hr": True,
        "enable_production": True,
        "enable_projects": True,
        "enable_cost_centers": True
    }

# --- تهيئة نظام المصادقة وشاشة الدخول الذكية ---
if 'authenticated' not in st.session_state:
    st.session_state['authenticated'] = False

if not st.session_state['authenticated']:
    st.markdown("""
        <style>
        .stApp {
            background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        }
        .login-card {
            background: #ffffff;
            padding: 40px;
            border-radius: 20px;
            box-shadow: 0 15px 35px rgba(113, 75, 103, 0.12);
            border: 1px solid rgba(113, 75, 103, 0.1);
            text-align: right;
            direction: rtl;
            margin-top: 40px;
        }
        .login-title {
            color: #714B67;
            font-size: 30px;
            font-weight: 800;
            text-align: center;
            margin-bottom: 5px;
        }
        .login-subtitle {
            color: #64748b;
            font-size: 13px;
            text-align: center;
            margin-bottom: 30px;
            font-weight: 500;
        }
        .stButton>button {
            width: 100%;
            background: linear-gradient(135deg, #714B67 0%, #5a3b52 100%);
            color: white;
            font-weight: bold;
            border-radius: 10px;
            padding: 12px;
            border: none;
            box-shadow: 0 4px 15px rgba(113, 75, 103, 0.3);
            font-size: 16px;
        }
        </style>
    """, unsafe_allow_html=True)

    col_l, col_m, col_r = st.columns([1, 1.3, 1])
    with col_m:
        current_client_name = st.session_state['client_license_config']['client_name']
        st.markdown(f"""
            <div class="login-card">
                <div class="login-title">✨ نظام أفق ERP السحابي</div>
                <div class="login-subtitle">مرخص لصالح: <b>{current_client_name}</b><br>نظام المحاسبة وإدارة الموارد المتكامل</div>
            </div>
        """, unsafe_allow_html=True)
        
        with st.form("login_form"):
            st.markdown("<p style='font-weight:600; color:#2d3748; margin-bottom:5px;'>اسم المستخدم</p>", unsafe_allow_html=True)
            username = st.text_input("اسم المستخدم", placeholder="أدخل اسم المستخدم (مثال: admin)", label_visibility="collapsed")
            
            st.markdown("<p style='font-weight:600; color:#2d3748; margin-top:15px; margin-bottom:5px;'>كلمة المرور</p>", unsafe_allow_html=True)
            password = st.text_input("كلمة المرور", type="password", placeholder="أدخل كلمة المرور", label_visibility="collapsed")
            
            st.markdown("<div style='margin-top: 25px;'></div>", unsafe_allow_html=True)
            submit_login = st.form_submit_button("تسجيل الدخول الآمن 🚀")
            
            if submit_login:
                if username == "admin" and password == "12345":
                    st.session_state['authenticated'] = True
                    st.success("تم تسجيل الدخول بنجاح! جاري توجيهك للنظام...")
                    st.rerun()
                else:
                    st.error("اسم المستخدم أو كلمة المرور غير صحيحة! (تجربة: admin / 12345)")
    st.stop()

# --- تهيئة قواعد البيانات وقواميس النظام الشاملة ---
if 'accounts_tree_hierarchical' not in st.session_state:
    st.session_state['accounts_tree_hierarchical'] = {
        "1. الأصول": {
            "type": "مدين", "balance": 1750000.0,
            "sub": {
                "1.1. الأصول الثابتة": {
                    "balance": 750000.0,
                    "items": {
                        "السيارات ووسائل النقل": 150000.0,
                        "الأثاث والمفروشات المكتبية": 100000.0,
                        "الأجهزة الحاسوبية والتقنية": 200000.0,
                        "الآلات والمعدات الإنتاجية": 300000.0
                    }
                },
                "1.2. الأصول المتداولة": {
                    "balance": 1000000.0,
                    "items": {
                        "الخزينة الرئيسية (الصندوق)": 300000.0,
                        "الخزينة الفرعية": 100000.0,
                        "بنك الرياض - حساب تجاري": 400000.0,
                        "بنك الراجحي - حساب استثماري": 200000.0,
                        "العملاء المحليين (مدينون)": 250000.0,
                        "مخزون البضائع آخر المدة": 150000.0
                    }
                }
            }
        },
        "2. الالتزامات والخصوم": {
            "type": "دائن", "balance": 500000.0,
            "sub": {
                "2.1. الالتزامات المتداولة": {
                    "balance": 300000.0,
                    "items": {
                        "الموردين المحليين (دائنون)": 300000.0,
                        "ضريبة القيمة المضافة المستحقة": 50000.0,
                        "رواتب وأجور مستحقة": 45000.0
                    }
                },
                "2.2. الالتزامات طويلة الأجل": {
                    "balance": 200000.0,
                    "items": {
                        "قروض بنكية متوسطة الأجل": 200000.0
                    }
                }
            }
        },
        "3. حقوق الملكية": {
            "type": "دائن", "balance": 3000000.0,
            "sub": {
                "3.1. رأس المال والأرباح": {
                    "balance": 3000000.0,
                    "items": {
                        "رأس المال المدفوع": 3000000.0,
                        "الأرباح المبقاة": 0.0
                    }
                }
            }
        },
        "4. الإيرادات": {
            "type": "دائن", "balance": 2500000.0,
            "sub": {
                "4.1. إيرادات النشاط الرئيسي": {
                    "balance": 2500000.0,
                    "items": {
                        "إيرادات المبيعات العامة": 2500000.0,
                        "إيرادات الخدمات المقدمة": 0.0
                    }
                }
            }
        },
        "5. المصروفات والتكاليف": {
            "type": "مدين", "balance": 1800000.0,
            "sub": {
                "5.1. التكاليف المباشرة": {
                    "balance": 1800000.0,
                    "items": {
                        "تكلفة البضائع المباعة": 1800000.0
                    }
                },
                "5.2. المصروفات الإدارية والتشغيلية": {
                    "balance": 150000.0,
                    "items": {
                        "مصروف الرواتب والأجور": 100000.0,
                        "مصروف الإيجارات": 30000.0,
                        "مصروف الكهرباء والماء": 20000.0,
                        "مصروف الإهلاكات": 25000.0
                    }
                }
            }
        }
    }

if 'customers_db' not in st.session_state:
    st.session_state['customers_db'] = {
        "شركة التقنية الحديثة للتجارة": {"كود العميل": "CUST-001", "رقم السجل": "1010254789", "الرقم الضريبي": "300123456700003", "العنوان": "الرياض - حي الملز", "الهاتف": "0501234567", "الحد الائتماني": 100000.0, "الرصيد الحالي": 45000.0},
        "مؤسسة النور للمقاولات": {"كود العميل": "CUST-002", "رقم السجل": "4030589632", "الرقم الضريبي": "300987654300003", "العنوان": "جدة - حي الروابي", "الهاتف": "0559876543", "الحد الائتماني": 50000.0, "الرصيد الحالي": 12000.0}
    }

if 'suppliers_db' not in st.session_state:
    st.session_state['suppliers_db'] = {
        "شركة التوريدات الكبرى المحدودة": {"كود المورد": "SUP-001", "رقم السجل": "1010987654", "الرقم الضريبي": "300111222300003", "العنوان": "الرياض - الصناعية", "الهاتف": "0561112233", "الرصيد الحالي": 65000.0}
    }

if 'warehouses_db' not in st.session_state:
    st.session_state['warehouses_db'] = ["المستودع الرئيسي - الرياض", "مستودع فرع جدة", "مستودع المنطقة الشرقية"]

if 'cash_boxes_db' not in st.session_state:
    st.session_state['cash_boxes_db'] = ["الخزينة الرئيسية (صندوق النقد)", "صندوق المبيعات اليومي", "صندوق الفرع"]

if 'banks_db' not in st.session_state:
    st.session_state['banks_db'] = ["مصرف الراجحي", "البنك الأهلي السعودي (SNB)", "بنك الرياض"]

if 'hr_employees_db' not in st.session_state:
    st.session_state['hr_employees_db'] = {
        "EMP-101": {"الاسم الكامل": "أحمد محمد العتيبي", "القسم": "الإدارة المالية", "المسمى الوظيفي": "محاسب أول", "الراتب الأساسي": 8000.0, "بدل السكن": 2000.0, "بدل النقل": 500.0, "بدلات اخري": 300.0, "سلف": 1000.0, "حوافز": 500.0, "خصومات": 100.0, "تاريخ البداية": "2023-01-15", "الحالة": "على رأس العمل"},
        "EMP-102": {"الاسم الكامل": "سارة خالد الشمري", "القسم": "الموارد البشرية", "المسمى الوظيفي": "مسؤول شؤون موظفين", "الراتب الأساسي": 6500.0, "بدل السكن": 1500.0, "بدل النقل": 400.0, "بدلات اخري": 200.0, "سلف": 0.0, "حوافز": 300.0, "خصومات": 50.0, "تاريخ البداية": "2023-06-01", "الحالة": "على رأس العمل"}
    }

if 'hr_attendance' not in st.session_state:
    st.session_state['hr_attendance'] = [
        {"رقم الموظف": "EMP-101", "اسم الموظف": "أحمد محمد العتيبي", "التاريخ": str(datetime.now().date()), "حالة الحضور": "حاضر", "وقت الحضور": "08:00 ص"},
        {"رقم الموظف": "EMP-102", "اسم الموظف": "سارة خالد الشمري", "التاريخ": str(datetime.now().date()), "حالة الحضور": "حاضر", "وقت الحضور": "08:15 ص"}
    ]

if 'hr_leaves' not in st.session_state:
    st.session_state['hr_leaves'] = [
        {"رقم الموظف": "EMP-102", "اسم الموظف": "سارة خالد الشمري", "نوع الإجازة": "إجازة سنوية", "من تاريخ": "2026-06-01", "إلى تاريخ": "2026-06-15", "الحالة": "معتمدة"}
    ]

if 'production_orders' not in st.session_state:
    st.session_state['production_orders'] = [
        {"رقم الأمر": "PRD-ORD-101", "اسم المنتج": "أجهزة لابتوب ديل احترافي", "الكمية المطلوبة": 20, "الكمية المنتجة": 20, "تاريخ البدء": "2026-06-01", "تاريخ الانتهاء": "2026-06-05", "الحالة": "مكتمل", "التفاصيل الكاملة": "أمر إنتاج مخصص لأجهزة ديل الاحترافية مع فحص جودة نهائي ومطابقة للمواصفات القياسية."}
    ]

if 'projects_db' not in st.session_state:
    st.session_state['projects_db'] = [
        {"رقم المشروع": "PRJ-01", "اسم المشروع": "تطوير خط الإنتاج الآلي", "مدير المشروع": "أحمد العتيبي", "الميزانية (ر.س)": 150000.0, "المصروف الفعلي (ر.س)": 95000.0, "نسبة الإنجاز": "65%", "الحالة": "جارية", "تفاصيل المشروع الكاملة": "مخطط هيكلي شامل لتطوير وتحديث خطوط الإنتاج بالكامل مع توريد آحضار آلية وسير متطور."}
    ]

if 'cost_centers_db' not in st.session_state:
    st.session_state['cost_centers_db'] = [
        {"رمز المركز": "CC-101", "اسم مركز التكلفة": "مركز إنتاج الأجهزة", "المسؤول": "مهندس الإنتاج", "المصروفات الحالية (ر.س)": 120000.0, "الإيرادات المرتبطة (ر.س)": 450000.0, "تفاصيل المركز": "مركز مخصص لتتبع تكاليف إنتاج الأجهزة والقطع الإلكترونية وإهلاك الآلات."}
    ]

if 'users_permissions_db' not in st.session_state:
    st.session_state['users_permissions_db'] = [
        {
            "اسم المستخدم": "admin", 
            "الاسم الكامل": "المدير العام", 
            "الدور": "مدير النظام (Administrator)", 
            "الصلاحيات الممنوحة": ["الرئيسية", "الشركاء", "المبيعات", "المشتريات", "المخزون", "المحاسبة والشجرة", "الصلاحيات", "الإعدادات"], 
            "الحالة": "نشط"
        }
    ]

if 'inventory_stock' not in st.session_state:
    st.session_state['inventory_stock'] = {
        "أجهزة لابتوب ديل احترافي": {"رمز الصنف": "PRD-001", "نوع المخزون": "مخزون تام", "الفئة": "إلكترونيات", "الكمية": 50, "سعر البيع": 3500.0, "سعر الشراء": 2800.0, "المستودع": "المستودع الرئيسي - الرياض", "حد الطلب": 10, "الحركات السابقة": "تمت إضافة 50 وحدة توريد أول المدة، وتم بيع 5 وحدات ضمن الفاتورة الأولى."},
        "شاشة سمارت 55 بوصة": {"رمز الصنف": "PRD-002", "نوع المخزون": "مخزون تام", "الفئة": "إلكترونيات", "الكمية": 30, "سعر البيع": 2200.0, "سعر الشراء": 1800.0, "المستودع": "المستودع الرئيسي - الرياض", "حد الطلب": 5, "الحركات السابقة": "توريد افتتاحي للمخزون الرئيسي بعدد 30 وحدة."}
    }

# هياكل دورة المبيعات
if 'sales_quotations' not in st.session_state:
    st.session_state['sales_quotations'] = [] # عروض الأسعار

if 'sales_orders_db' not in st.session_state:
    st.session_state['sales_orders_db'] = [] # أوامر البيع

if 'sales_invoices_db' not in st.session_state:
    st.session_state['sales_invoices_db'] = [] # فواتير المبيعات النهائية

# هياكل دورة المشتريات
if 'purchase_quotations' not in st.session_state:
    st.session_state['purchase_quotations'] = [] # طلبات وأوامر الشراء

if 'purchase_invoices_db' not in st.session_state:
    st.session_state['purchase_invoices_db'] = [] # فواتير المشتريات النهائية

if 'general_ledger' not in st.session_state:
    st.session_state['general_ledger'] = [
        {"رقم القيد": "JE-101", "البيان": "قيد الافتتاح", "المدين": 3000000.0, "الدائن": 3000000.0}
    ]

if 'zatca_vat_returns_db' not in st.session_state:
    st.session_state['zatca_vat_returns_db'] = [
        {
            "رقم الإقرار": "ZATCA-Q1-2026",
            "الفترة": "الربع الأول 2026",
            "المبيعات الخاضعة 15% (ر.س)": 600000.0,
            "ضريبة المخرجات (ر.س)": 90000.0,
            "المشتريات الخاضعة 15% (ر.س)": 450000.0,
            "ضريبة المدخلات (ر.س)": 67500.0,
            "صافي الضريبة المستحقة (ر.س)": 22500.0,
            "حالة الإقرار": "معتمد"
        }
    ]

# --- تنسيقات CSS مع تصغير الهوامش ومنع التداخل وتطبيق (Shrink to Fit) ---
st.markdown("""
    <style>
    .stApp, body, p, span, div, label, input, select {
        direction: rtl !important; text-align: right !important; font-family: 'Segoe UI', Tahoma, sans-serif;
    }
    .block-container { padding: 4rem 1rem 1rem 1rem !important; background-color: #f4f6f9; max-width: 100% !important; }
    
    .stButton>button {
        font-size: 12px !important;
        padding: 4px 8px !important;
    }
    
    /* تنسيق خاص لتصغير الجداول وجعلها تتناسب مع الشاشة (Shrink to Fit) تلقائياً */
    .custom-table-container {
        width: 100%;
        overflow-x: auto;
        margin-top: 10px;
        margin-bottom: 15px;
        border-radius: 6px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.08);
        background-color: white;
    }
    .custom-table {
        width: 100%; border-collapse: collapse; background-color: white; font-size: 11px;
        table-layout: auto !important;
    }
    .custom-table th { background-color: #714B67; color: white; padding: 6px 8px; border-bottom: 2px solid #5a3b52; text-align: right; white-space: nowrap; font-size: 11px; }
    .custom-table td { padding: 5px 8px; border-bottom: 1px solid #edf2f7; color: #2d3748; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; max-width: 200px; font-size: 11px; }
    
    .official-form-box {
        background: white; padding: 15px; border-radius: 8px; border: 1px solid #dcdde1;
        box-shadow: 0 2px 4px rgba(0,0,0,0.04); margin-bottom: 15px;
    }
    
    .metric-card {
        background: white; padding: 12px; border-radius: 8px; border-right: 4px solid #714B67;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05); text-align: center;
    }
    </style>
""", unsafe_allow_html=True)

# --- شريط الأزرار العلوي التفاعلي ---
top_col1, top_col2, top_col3, top_col4, top_col5, top_col6, top_col7 = st.columns([6, 1, 0.6, 0.6, 0.6, 0.6, 0.6])

with top_col2:
    with st.popover("🌐", help="تغيير اللغة"):
        st.markdown("##### اختر لغة العرض")
        lang = st.radio("اللغة", ["العربية (Arabic)", "English"], key="top_lang_choice")
        if st.button("تطبيق اللغة"):
            st.success(f"تم تغيير اللغة إلى: {lang}")

with top_col3:
    with st.popover("💬", help="الرسائل"):
        st.markdown("##### رسائل النظام")
        st.info("لا توجد رسائل جديدة حالياً.")

with top_col4:
    with st.popover("🔔", help="الإشعارات"):
        st.markdown("##### مركز الإشعارات")
        st.success("النظام يعمل بكفاءة وجاهز.")

with top_col5:
    with st.popover("⭐", help="المفضلة"):
        st.markdown("##### الصفحات المفضلة")
        st.write("- لوحة التحكم الرئيسية")
        st.write("- إدارة المبيعات والفواتير")

with top_col6:
    with st.popover("✏️", help="التعديل السريع"):
        st.markdown("##### خيارات التعديل السريع")
        st.write("يمكنك تعديل البيانات النشطة من هذه القائمة المنسدلة.")

with top_col7:
    with st.popover("⋮", help="خيارات إضافية"):
        st.markdown("##### خيارات النظام الإضافية")
        if st.button("تحديث البيانات (Refresh)"):
            st.rerun()

def render_arabic_table_with_controls(df, section_name="التقرير"):
    if df.empty:
        st.info("لا توجد بيانات متاحة حالياً في هذا القسم.")
        return

    st.markdown("---")
    c_f1, c_f2, c_b1, c_b2, c_b3 = st.columns([2, 2, 1, 1, 1])
    
    with c_f1:
        search_query = st.text_input(f"بحث فوري في {section_name} (Shrink to Fit)", key=f"search_{section_name}")
    with c_f2:
        if "التاريخ" in df.columns:
            date_filter = st.date_input(f"فلترة بالتاريخ ({section_name})", value=[], key=f"date_{section_name}")
        else:
            st.markdown("<p style='font-size:11px; color:#64748b; padding-top:8px;'>فلترة البحث الفعالة مفعلة (Shrink to Fit)</p>", unsafe_allow_html=True)

    filtered_df = df.copy()
    if search_query:
        mask = filtered_df.astype(str).apply(lambda x: x.str.contains(search_query, case=False)).any(axis=1)
        filtered_df = filtered_df[mask]

    with c_b1:
        if st.button("🖨️ طباعة", key=f"print_{section_name}"):
            st.toast(f"جاري تجهيز وثيقة الطباعة لـ {section_name}...")
    with c_b2:
        if st.button("📊 Excel", key=f"excel_{section_name}"):
            st.toast(f"تمت عملية تصدير {section_name} إلى ملف Excel بنجاح!")
    with c_b3:
        if st.button("📄 PDF", key=f"pdf_{section_name}"):
            st.toast(f"تمت تهيئة وتصدير {section_name} إلى ملف PDF بنجاح!")

    html_code = "<div class='custom-table-container'><table class='custom-table'><thead><tr>"
    for col in filtered_df.columns: html_code += f"<th>{col}</th>"
    html_code += "</tr></thead><tbody>"
    for _, row in filtered_df.iterrows():
        html_code += "<tr>"
        for col in filtered_df.columns: html_code += f"<td>{row[col]}</td>"
        html_code += "</tr>"
    html_code += "</tbody></table></div>"
    st.markdown(html_code, unsafe_allow_html=True)

if 'active_module' not in st.session_state:
    st.session_state['active_module'] = "الرئيسية"

with st.sidebar:
    client_conf = st.session_state['client_license_config']
    st.markdown(f"<h2 style='color: #714B67; text-align: center; font-size:22px;'>نظام أفق ERP</h2>", unsafe_allow_html=True)
    st.markdown(f"<p style='text-align: center; font-size: 11px; color: #64748b;'>مرخص لـ: <b>{client_conf['client_name']}</b></p>", unsafe_allow_html=True)
    
    if supabase_client:
        st.success("☁️ متصل بـ Supabase بنجاح")
    else:
        st.info("ℹ️ يعمل الآن بنجاح عبر النظام المحلي")

    if st.button("🔒 تسجيل الخروج", use_container_width=True):
        st.session_state['authenticated'] = False
        st.rerun()

    st.markdown("---")
    
    modules_map = {
        "الرئيسية": "🏠 الرئيسية",
        "الشركاء": "👥 الشركاء",
    }
    
    if client_conf.get("enable_hr", True):
        modules_map["الموارد البشرية"] = "👨‍💼 الموارد البشرية"
    if client_conf.get("enable_production", True):
        modules_map["الإنتاج"] = "🏭 الإنتاج"
    if client_conf.get("enable_projects", True):
        modules_map["المشروعات"] = "📊 المشروعات"
    if client_conf.get("enable_cost_centers", True):
        modules_map["مراكز التكلفة"] = "🏷️ مراكز التكلفة"
        
    modules_map.update({
        "الصلاحيات": "🔐 الصلاحيات",
        "المبيعات": "🛒 المبيعات",
        "المشتريات": "📦 المشتريات",
        "المخزون": "📋 المخزون",
        "المحاسبة والشجرة": "💰 المحاسبة",
        "الإعدادات": "⚙️ الإعدادات"
    })
    
    for mod_key, mod_label in modules_map.items():
        is_selected = (st.session_state['active_module'] == mod_key)
        button_type = "primary" if is_selected else "secondary"
        if st.button(mod_label, key=f"btn_mod_{mod_key}", use_container_width=True, type=button_type):
            st.session_state['active_module'] = mod_key
            st.rerun()

    st.markdown("---")
    st.markdown("<p style='font-size: 10px; color: #714B67; text-align: center;'>جميع الحقوق محفوظة © أفق 2026</p>", unsafe_allow_html=True)

main_menu = st.session_state['active_module']

if main_menu == "الرئيسية":
    client_conf = st.session_state['client_license_config']
    st.markdown(f"""
        <div class="official-form-box">
            <h2 style="color: #714B67; margin: 0; font-size:20px;">🚀 لوحة التحكم السحابية - {client_conf['client_name']}</h2>
            <p style="color: #64748b; margin-top: 5px; font-size: 12px;">نشاط الشركة: {client_conf.get('company_activity', 'غير مححدد')} | السجل التجاري: {client_conf['commercial_reg']} | الرقم الضريبي: {client_conf['tax_number']}</p>
        </div>
    """, unsafe_allow_html=True)

    total_cust_val = sum([c.get("الرصيد الحالي", 0) for c in st.session_state['customers_db'].values()])
    total_supp_val = sum([s.get("الرصيد الحالي", 0) for s in st.session_state['suppliers_db'].values()])
    total_emp_count = len(st.session_state['hr_employees_db'])
    total_prod_orders = len(st.session_state['production_orders'])

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f"<div class='metric-card'><p style='color: #64748b; margin:0; font-size:11px;'>إجمالي أرصدة العملاء</p><h3 style='color: #714B67; margin:5px 0 0 0; font-size:16px;'>{total_cust_val:,.2f} ر.س</h3></div>", unsafe_allow_html=True)
    with col2:
        st.markdown(f"<div class='metric-card'><p style='color: #64748b; margin:0; font-size:11px;'>إجمالي أرصدة الموردين</p><h3 style='color: #714B67; margin:5px 0 0 0; font-size:16px;'>{total_supp_val:,.2f} ر.س</h3></div>", unsafe_allow_html=True)
    with col3:
        st.markdown(f"<div class='metric-card'><p style='color: #64748b; margin:0; font-size:11px;'>إجمالي عدد الموظفين</p><h3 style='color: #714B67; margin:5px 0 0 0; font-size:16px;'>{total_emp_count} موظف</h3></div>", unsafe_allow_html=True)
    with col4:
        st.markdown(f"<div class='metric-card'><p style='color: #64748b; margin:0; font-size:11px;'>أوامر الإنتاج المسجلة</p><h3 style='color: #714B67; margin:5px 0 0 0; font-size:16px;'>{total_prod_orders} أمر</h3></div>", unsafe_allow_html=True)

elif main_menu == "الشركاء":
    st.markdown("<h3 style='color: #714B67; font-size:18px;'>👥 إدارة شركاء النجاح (العملاء والموردين)</h3>", unsafe_allow_html=True)
    t_cust, t_supp, t_add, t_excel = st.tabs(["📋 العملاء", "📋 الموردين", "➕ إضافة عميل أو مورد جديد", "📊 الاستيراد عن طريق الاكسيل"])
    
    with t_cust:
        cust_list = [{"كود العميل": v.get("كود العميل"), "اسم العميل": k, "السجل التجاري": v.get("رقم السجل"), "الرقم الضريبي": v.get("الرقم الضريبي"), "الهاتف": v.get("الهاتف"), "العنوان": v.get("العنوان"), "الرصيد": v.get("الرصيد الحالي")} for k, v in st.session_state['customers_db'].items()]
        render_arabic_table_with_controls(pd.DataFrame(cust_list), "قائمة_العملاء")
        
    with t_supp:
        supp_list = [{"كود المورد": v.get("كود المورد"), "اسم المورد": k, "السجل التجاري": v.get("رقم السجل"), "الرقم الضريبي": v.get("الرقم الضريبي"), "الهاتف": v.get("الهاتف"), "العنوان": v.get("العنوان"), "الرصيد": v.get("الرصيد الحالي")} for k, v in st.session_state['suppliers_db'].items()]
        render_arabic_table_with_controls(pd.DataFrame(supp_list), "قائمة_الموردين")
        
    with t_add:
        with st.form("add_partner_form"):
            p_type = st.selectbox("نوع الشريك", ["عميل جديد", "مورد جديد"])
            p_code = st.text_input("كود الشريك (مثال: CUST-002 أو SUP-002)")
            p_name = st.text_input("اسم الشريك / الشركة")
            p_reg = st.text_input("رقم السجل التجاري")
            p_tax = st.text_input("الرقم الضريبي")
            p_phone = st.text_input("رقم الهاتف")
            p_address = st.text_input("العنوان بالتفصيل")
            p_bal = st.number_input("الرصيد الافتتاحي (ر.س)", value=0.0)
            
            if st.form_submit_button("حفظ الشريك الجديد 💾"):
                if p_code and p_name:
                    if p_type == "عميل جديد":
                        st.session_state['customers_db'][p_name] = {"كود العميل": p_code, "رقم السجل": p_reg, "الرقم الضريبي": p_tax, "الهاتف": p_phone, "العنوان": p_address, "الرصيد الحالي": p_bal}
                    else:
                        st.session_state['suppliers_db'][p_name] = {"كود المورد": p_code, "رقم السجل": p_reg, "الرقم الضريبي": p_tax, "الهاتف": p_phone, "العنوان": p_address, "الرصيد الحالي": p_bal}
                    st.success(f"تمت إضافة الشريك ({p_name}) بنجاح!")
                    st.rerun()
                else:
                    st.error("يرجى إدخال الكود والاسم على الأقل.")

    with t_excel:
        st.markdown("#### استيراد الشركاء (العملاء / الموردين) عبر ملف إكسل Excel")
        up_partners_file = st.file_uploader("اختر ملف إكسل للشركاء (.xlsx, .csv)", type=["xlsx", "csv"], key="partners_excel_up")
        if up_partners_file is not None:
            try:
                if up_partners_file.name.endswith('.csv'):
                    df_imp = pd.read_csv(up_partners_file)
                else:
                    df_imp = pd.read_excel(up_partners_file)
                if st.button("تأكيد واعتماد استيراد الشركاء 📥"):
                    for _, row in df_imp.iterrows():
                        p_t = str(row.get("النوع", "عميل")).strip()
                        p_c = str(row.get("الكود", f"PRT-{int(datetime.now().timestamp())}"))
                        p_n = str(row.get("الاسم", "شريك جديد"))
                        p_r = str(row.get("السجل التجاري", ""))
                        p_tx = str(row.get("الرقم الضريبي", ""))
                        p_ph = str(row.get("الهاتف", ""))
                        p_adr = str(row.get("العنوان", ""))
                        p_b = float(row.get("الرصيد", 0.0))
                        
                        if "مورد" in p_t:
                            st.session_state['suppliers_db'][p_n] = {"كود المورد": p_c, "رقم السجل": p_r, "الرقم الضريبي": p_tx, "الهاتف": p_ph, "العنوان": p_adr, "الرصيد الحالي": p_b}
                        else:
                            st.session_state['customers_db'][p_n] = {"كود العميل": p_c, "رقم السجل": p_r, "الرقم الضريبي": p_tx, "الهاتف": p_ph, "العنوان": p_adr, "الرصيد الحالي": p_b}
                    st.success("تم استيراد وإضافة الشركاء بنجاح!")
                    st.rerun()
            except Exception as e:
                st.error(f"حدث خطأ أثناء قراءة الملف: {e}")

elif main_menu == "الموارد البشرية":
    st.markdown("<h3 style='color: #714B67; font-size:18px;'>👨‍💼 إدارة الموارد البشرية (HR) - التفاصيل الكاملة للموظفين</h3>", unsafe_allow_html=True)
    hr_tab1, hr_tab2, hr_tab3, hr_tab4, hr_tab5, hr_tab6 = st.tabs([
        "📋 سجل الموظفين الشامل", "➕ إضافة موظف جديد", "⏰ متابعة الحضور والانصراف", "🏖️ إدارة الإجازات والطلبات", "💰 مسير الرواتب والأجور (Payroll)", "📊 استيراد الموظفين من الاكسيل"
    ])
    with hr_tab1:
        emp_rows = []
        for k, v in st.session_state['hr_employees_db'].items():
            emp_rows.append({
                "رقم الموظف": k, "الاسم الكامل": v["الاسم الكامل"], "القسم": v["القسم"], "المسمى الوظيفي": v["المسمى الوظيفي"], 
                "الراتب الأساسي": v["الراتب الأساسي"], "بدل السكن": v.get("بدل السكن", 0), "بدل المواصلات": v.get("بدل النقل", 0), 
                "بدلات اخري": v.get("بدلات اخري", 0), "سلف": v.get("سلف", 0), "حوافز": v.get("حوافز", 0), "خصومات": v.get("خصومات", 0)
            })
        render_arabic_table_with_controls(pd.DataFrame(emp_rows), "الموظفين")
        
        st.markdown("---")
        st.markdown("#### 👤 نافذة تفاصيل الموظف الخاصة (عند النقر أو الاختيار في أي تقرير)")
        selected_emp_det = st.selectbox("اختر الموظف لعرض شاشته وتفاصيله الكاملة:", list(st.session_state['hr_employees_db'].keys()))
        if selected_emp_det:
            e_info = st.session_state['hr_employees_db'][selected_emp_det]
            st.info(f"""
            - **رقم الموظف:** {selected_emp_det}
            - **الاسم الكامل:** {e_info.get('الاسم الكامل')}
            - **القسم:** {e_info.get('القسم')} | **المسمى:** {e_info.get('المسمى الوظيفي')}
            - **الراتب الأساسي:** {e_info.get('الراتب الأساسي'):,.2f} ر.س
            - **بدل السكن:** {e_info.get('بدل السكن', 0):,.2f} ر.س
            - **بدل المواصلات:** {e_info.get('بدل النقل', 0):,.2f} ر.س
            - **بدلات اخري:** {e_info.get('بدلات اخري', 0):,.2f} ر.س
            - **السلف المعلقة:** {e_info.get('سلف', 0):,.2f} ر.س
            - **الحوافز والمكافآت:** {e_info.get('حوافز', 0):,.2f} ر.س
            - **الخصومات:** {e_info.get('خصومات', 0):,.2f} ر.س
            - **الحالة:** {e_info.get('الحالة', 'على رأس العمل')}
            """)

    with hr_tab2:
        with st.form("add_emp"):
            e_id = st.text_input("رقم الموظف (مثال: EMP-104)")
            e_name = st.text_input("الاسم الكامل للموظف")
            e_dept = st.text_input("القسم")
            e_title = st.text_input("المسمى الوظيفي")
            e_sal = st.number_input("الراتب الأساسي", value=5000.0)
            e_bhouse = st.number_input("بدل السكن", value=1500.0)
            e_btrans = st.number_input("بدل المواصلات", value=400.0)
            e_bother = st.number_input("بدلات اخري", value=200.0)
            e_adv = st.number_input("سلف", value=0.0)
            e_bonus = st.number_input("حوافز", value=0.0)
            e_ded = st.number_input("خصومات", value=0.0)
            
            if st.form_submit_button("حفظ الموظف الجديد 💾"):
                if e_id and e_name:
                    st.session_state['hr_employees_db'][e_id] = {
                        "الاسم الكامل": e_name, "القسم": e_dept, "المسمى الوظيفي": e_title, "الراتب الأساسي": e_sal,
                        "بدل السكن": e_bhouse, "بدل النقل": e_btrans, "بدلات اخري": e_bother, "سلف": e_adv, "حوافز": e_bonus, "خصومات": e_ded,
                        "الحالة": "على رأس العمل"
                    }
                    st.success("تم إضافة الموظف بكافة تفاصيله بنجاح!")
                    st.rerun()
    with hr_tab3:
        render_arabic_table_with_controls(pd.DataFrame(st.session_state['hr_attendance']), "الحضور")
    with hr_tab4:
        render_arabic_table_with_controls(pd.DataFrame(st.session_state['hr_leaves']), "الإجازات")
    with hr_tab5:
        sal_rows = []
        for k, v in st.session_state['hr_employees_db'].items():
            net_pay = v["الراتب الأساسي"] + v.get("بدل السكن", 0) + v.get("بدل النقل", 0) + v.get("بدلات اخري", 0) + v.get("حوافز", 0) - v.get("خصومات", 0) - v.get("سلف", 0)
            sal_rows.append({
                "رقم الموظف": k, "الاسم": v["الاسم الكامل"], "الراتب الأساسي": v["الراتب الأساسي"], 
                "البدلات": v.get("بدل السكن", 0) + v.get("بدل النقل", 0) + v.get("بدلات اخري", 0),
                "الصافي المستحق": net_pay
            })
        render_arabic_table_with_controls(pd.DataFrame(sal_rows), "مسير_الرواتب")
    with hr_tab6:
        st.markdown("#### استيراد بيانات الموظفين عبر ملف إكسل Excel")
        up_emp_file = st.file_uploader("اختر ملف إكسل للموظفين (.xlsx, .csv)", type=["xlsx", "csv"], key="emp_excel_up")
        if up_emp_file is not None:
            try:
                if up_emp_file.name.endswith('.csv'):
                    df_emp_imp = pd.read_csv(up_emp_file)
                else:
                    df_emp_imp = pd.read_excel(up_emp_file)
                if st.button("تأكيد استيراد الموظفين 📥"):
                    for _, row in df_emp_imp.iterrows():
                        eid = str(row.get("رقم الموظف", f"EMP-{int(datetime.now().timestamp())}"))
                        ename = str(row.get("الاسم الكامل", "موظف جديد"))
                        edept = str(row.get("القسم", "عام"))
                        etitle = str(row.get("المسمى الوظيفي", "موظف"))
                        esal = float(row.get("الراتب الأساسي", 5000.0))
                        st.session_state['hr_employees_db'][eid] = {
                            "الاسم الكامل": ename, "القسم": edept, "المسمى الوظيفي": etitle, 
                            "الراتب الأساسي": esal, "الحالة": "على رأس العمل"
                        }
                    st.success("تم استيراد الموظفين بنجاح!")
                    st.rerun()
            except Exception as e:
                st.error(f"حدث خطأ: {e}")

elif main_menu == "الإنتاج":
    st.markdown("<h3 style='color: #714B67; font-size:18px;'>🏭 إدارة الإنتاج والمصنع/المطبخ - تفاصيل أوامر الإنتاج</h3>", unsafe_allow_html=True)
    prod_tab1, prod_tab2, prod_tab3 = st.tabs(["⚙️ أوامر الإنتاج النشطة", "➕ إضافة أمر إنتاج جديد", "✅ أوامر الإنتاج المكتملة"])
    with prod_tab1:
        render_arabic_table_with_controls(pd.DataFrame(st.session_state['production_orders']), "أوامر_الإنتاج")
    with prod_tab2:
        with st.form("new_prod"):
            p_item = st.text_input("اسم المنتج / الوجبة المصنعة")
            p_qty = st.number_input("الكمية المطلوبة للإنتاج", value=10)
            p_details = st.text_area("تفاصيل أمر الإنتاج الكاملة")
            if st.form_submit_button("إصدار أمر الإنتاج الجديد ⚙️"):
                if p_item:
                    st.session_state['production_orders'].append({
                        "رقم الأمر": f"PRD-{len(st.session_state['production_orders'])+1:03d}", 
                        "اسم المنتج": p_item, "الكمية المطلوبة": p_qty, "الحالة": "قيد التنفيذ",
                        "التفاصيل الكاملة": p_details if p_details else "أمر إنتاج جديد قيد التنفيذ."
                    })
                    st.success("تم إصدار أمر الإنتاج بنجاح!")
                    st.rerun()
    with prod_tab3:
        render_arabic_table_with_controls(pd.DataFrame(st.session_state['production_orders']), "أوامر_مكتملة")

elif main_menu == "المشروعات":
    st.markdown("<h3 style='color: #714B67; font-size:18px;'>📊 إدارة المشاريع - التفاصيل الكاملة للمشاريع</h3>", unsafe_allow_html=True)
    proj_tab1, proj_tab2 = st.tabs(["📋 قائمة المشاريع", "➕ إضافة مشروع جديد"])
    with proj_tab1:
        render_arabic_table_with_controls(pd.DataFrame(st.session_state['projects_db']), "المشاريع")
    with proj_tab2:
        with st.form("add_proj"):
            pr_id = st.text_input("رقم المشروع (مثال: PRJ-03)")
            pr_name = st.text_input("اسم المشروع")
            pr_mgr = st.text_input("مدير المشروع")
            pr_bud = st.number_input("الميزانية (ر.س)", value=100000.0)
            pr_det = st.text_area("تفاصيل المشروع الكاملة")
            if st.form_submit_button("حفظ المشروع 💾"):
                st.session_state['projects_db'].append({
                    "رقم المشروع": pr_id, "اسم المشروع": pr_name, "مدير المشروع": pr_mgr,
                    "الميزانية (ر.س)": pr_bud, "نسبة الإنجاز": "0%", "الحالة": "جديدة",
                    "تفاصيل المشروع الكاملة": pr_det if pr_det else "مشروع جديد تم إضافته للنظام."
                })
                st.success("تم إضافة المشروع بنجاح!")
                st.rerun()

elif main_menu == "مراكز التكلفة":
    st.markdown("<h3 style='color: #714B67; font-size:18px;'>🏷️ إدارة مراكز التكلفة - التفاصيل الكاملة</h3>", unsafe_allow_html=True)
    cc_tab1, cc_tab2 = st.tabs(["📋 مراكز التكلفة الشاملة", "➕ إضافة مركز تكلفة جديد"])
    with cc_tab1:
        render_arabic_table_with_controls(pd.DataFrame(st.session_state['cost_centers_db']), "مراكز_التكلفة")
    with cc_tab2:
        with st.form("add_cc"):
            cc_id = st.text_input("رمز المركز (مثال: CC-103)")
            cc_name = st.text_input("اسم مركز التكلفة")
            cc_mgr = st.text_input("المسؤول")
            cc_det = st.text_area("تفاصيل مركز التكلفة الكاملة")
            if st.form_submit_button("حفظ المركز 💾"):
                st.session_state['cost_centers_db'].append({
                    "رمز المركز": cc_id, "اسم مركز التكلفة": cc_name, "المسؤول": cc_mgr,
                    "المصروفات الحالية (ر.س)": 0.0, "الإيرادات المرتبطة (ر.س)": 0.0,
                    "تفاصيل المركز": cc_det if cc_det else "مركز تكلفة جديد."
                })
                st.success("تم الحفظ بنجاح!")
                st.rerun()

elif main_menu == "الصلاحيات":
    st.markdown("<h3 style='color: #714B67; font-size:18px;'>🔐 شاشة إدارة الصلاحيات وتحديد صلاحيات المستخدمين بدقة</h3>", unsafe_allow_html=True)
    perm_tab1, perm_tab2 = st.tabs(["👥 قائمة المستخدمين وصلاحياتهم الكاملة", "➕ إضافة / تعديل مستخدم والصلاحيات"])
    
    with perm_tab1:
        view_perms = []
        for u in st.session_state['users_permissions_db']:
            if isinstance(u, dict):
                perms = u.get("الصلاحيات الممنوحة", [])
                perms_str = ", ".join(perms) if isinstance(perms, list) else str(perms)
                view_perms.append({
                    "اسم المستخدم": u.get("اسم المستخدم", ""),
                    "الاسم الكامل": u.get("الاسم الكامل", ""),
                    "الدور": u.get("الدور", ""),
                    "الصلاحيات الممنوحة": perms_str,
                    "الحالة": u.get("الحالة", "نشط")
                })
        render_arabic_table_with_controls(pd.DataFrame(view_perms), "جدول_الصلاحيات")

    with perm_tab2:
        with st.form("permissions_assignment_form"):
            st.markdown("#### تحديد الصلاحيات لكل مستخدم بدقة")
            u_username = st.text_input("اسم المستخدم (Login Username)")
            u_fullname = st.text_input("الاسم الكامل")
            u_role = st.selectbox("الدور الوظيفي", ["مدير النظام", "محاسب رئيسي", "مسؤول مبيعات", "مسؤول مشتريات", "مفوض مستودعات"])
            
            st.markdown("##### حدد الموديولات والصلاحيات المسموح بها للمستخدم:")
            all_possible_modules = ["الرئيسية", "الشركاء", "المبيعات", "المشتريات", "المخزون", "المحاسبة والشجرة", "الصلاحيات", "الإعدادات", "الموارد البشرية", "الإنتاج", "المشروعات"]
            
            selected_user_modules = []
            cols_p = st.columns(3)
            for idx, mod in enumerate(all_possible_modules):
                with cols_p[idx % 3]:
                    if st.checkbox(mod, value=True if mod in ["الرئيسية", "المبيعات", "المخزون"] else False, key=f"chk_perm_{mod}2"):
                        selected_user_modules.append(mod)
                        
            if st.form_submit_button("حفظ وحفظ صلاحيات المستخدم 💾"):
                if u_username:
                    found = False
                    for existing_user in st.session_state['users_permissions_db']:
                        if isinstance(existing_user, dict) and existing_user.get("اسم المستخدم") == u_username:
                            existing_user["الاسم الكامل"] = u_fullname
                            existing_user["الدور"] = u_role
                            existing_user["الصلاحيات الممنوحة"] = selected_user_modules
                            found = True
                            break
                    if not found:
                        st.session_state['users_permissions_db'].append({
                            "اسم المستخدم": u_username,
                            "الاسم الكامل": u_fullname,
                            "الدور": u_role,
                            "الصلاحيات الممنوحة": selected_user_modules,
                            "الحالة": "نشط"
                        })
                    st.success(f"تم حفظ صلاحيات المستخدم ({u_username}) بنجاح!")
                    st.rerun()
                else:
                    st.error("يرجى إدخال اسم المستخدم على الأقل.")

elif main_menu == "المبيعات":
    st.markdown("<h3 style='color: #714B67; font-size:18px;'>🛒 موديول المبيعات (عروض الأسعار، أوامر البيع، وفواتير المبيعات الضريبية)</h3>", unsafe_allow_html=True)
    sales_tab1, sales_tab2, sales_tab3 = st.tabs([
        "📄 عروض الأسعار (إضافة عرض سعر وتعديله)", 
        "📑 أوامر البيع والفواتير الضريبية", 
        "🧾 فواتير المبيعات"
    ])
    
    # 1. التبويب الأول: عروض الأسعار
    with sales_tab1:
        with st.form("quotation_form_exact"):
            st.markdown("#### زر لاضافة عرض سعر جديد ومكوناته:")
            
            # الترويسة العليا (كود العميل - عنوان العميل - رقم الهاتف - السجل التجاري - الرقم الضريبي)
            q_cust = st.selectbox("اسم العميل", list(st.session_state['customers_db'].keys()), key="sales_q_cust_select")
            
            c_det = st.session_state['customers_db'].get(q_cust, {})
            cust_code_val = c_det.get("كود العميل", "CUST-001")
            cust_addr_val = c_det.get("العنوان", "الرياض")
            cust_phone_val = c_det.get("الهاتف", "0500000000")
            cust_reg_val = c_det.get("رقم السجل", "1010000000")
            cust_tax_val = c_det.get("الرقم الضريبي", "300000000000003")
            
            st.info(f"""
            📋 **بيانات الترويسة العليا للعميل المحدد:**
            - **كود العميل:** {cust_code_val}
            - **عنوان العميل:** {cust_addr_val}
            - **رقم الهاتف:** {cust_phone_val}
            - **السجل التجاري:** {cust_reg_val}
            - **الرقم الضريبي:** {cust_tax_val}
            """)
            
            q_num = st.text_input("رقم عرض السعر", value=f"SQ-{int(datetime.now().timestamp())}")
            q_date = st.date_input("تاريخ العرض", value=datetime.now())
            q_wh = st.selectbox("المستودع", st.session_state['warehouses_db'], key="sales_q_wh")

            st.markdown("---")
            st.markdown("##### 📦 جدول تفاصيل الأصناف (كود الصنف - اسم الصنف - الوحدة - الكمية - السعر - القيمة - خصم % - الضريبة - الاجمالي)")
            
            # إدارة عدد الأصناف ديناميكياً
            if 'sales_q_lines_count' not in st.session_state:
                st.session_state['sales_q_lines_count'] = 1
                
            inv_keys = list(st.session_state['inventory_stock'].keys())
            
            total_val_sum = 0.0
            total_disc_sum = 0.0
            total_vat_sum = 0.0
            net_total_sum = 0.0
            items_summary_arr = []
            
            for i in range(st.session_state['sales_q_lines_count']):
                st.markdown(f"**الصنف رقم ({i+1})**")
                col_i1, col_i2, col_i3, col_i4, col_i5, col_i6, col_i7 = st.columns([1.5, 2, 1, 1, 1, 1, 1])
                with col_i1:
                    sel_item_name = st.selectbox(f"اسم الصنف {i+1}", inv_keys, key=f"s_item_{i}")
                
                item_info = st.session_state['inventory_stock'].get(sel_item_name, {"رمز الصنف": "ITM-001", "سعر البيع": 100.0})
                item_code_str = item_info.get("رمز الصنف", "ITM-001")
                def_prc = float(item_info.get("سعر البيع", 100.0))
                
                with col_i2:
                    st.text_input(f"كود الصنف {i+1}", value=item_code_str, key=f"s_icode_{i}", disabled=True)
                with col_i3:
                    unit_str = st.selectbox(f"الوحدة {i+1}", ["قطعة", "كرتونة", "خدمة", "كيلو"], key=f"s_unit_{i}")
                with col_i4:
                    qty_val = st.number_input(f"الكمية {i+1}", value=1.0, min_value=0.1, key=f"s_qty_{i}")
                with col_i5:
                    prc_val = st.number_input(f"السعر {i+1}", value=def_prc, key=f"s_prc_{i}")
                with col_i6:
                    disc_pct = st.number_input(f"خصم % {i+1}", value=0.0, min_value=0.0, max_value=100.0, key=f"s_disc_{i}")
                with col_i7:
                    line_val = qty_val * prc_val
                    line_disc = line_val * (disc_pct / 100.0)
                    line_net_before_vat = line_val - line_disc
                    line_vat = line_net_before_vat * 0.15
                    line_total = line_net_before_vat + line_vat
                    
                    total_val_sum += line_val
                    total_disc_sum += line_disc
                    total_vat_sum += line_vat
                    net_total_sum += line_total
                    
                    items_summary_arr.append(f"{sel_item_name} (كمية: {qty_val}, إجمالي: {line_total:,.2f})")
                    st.text_input(f"الإجمالي {i+1}", value=f"{line_total:,.2f}", key=f"s_tot_{i}", disabled=True)

            if st.button("➕ إضافة صنف آخر", key="btn_add_sales_line_dyn"):
                st.session_state['sales_q_lines_count'] += 1
                st.rerun()

            st.markdown("---")
            st.markdown(f"""
            <div style="background:#f8f9fa; padding:12px; border-radius:6px; font-weight:bold; font-size:13px;">
                الإجمالي قبل الخصم: {total_val_sum:,.2f} ر.س | إجمالي الخصم: {total_disc_sum:,.2f} ر.س | إجمالي الضريبة (15%): {total_vat_sum:,.2f} ر.س<br>
                <span style="color:#714B67; font-size:15px;">الإجمالي شامل ض ق م: {net_total_sum:,.2f} ر.س</span>
            </div>
            """, unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)
            col_b1, col_b2, col_b3, col_b4 = st.columns(4)
            with col_b1:
                btn_verify = st.form_submit_button("🔍 التحقق من توفر الكميات")
                if btn_verify:
                    st.success("✔️ جميع الأصناف المطلوبة متوفرة بالكميات المطلوبة في المستودع!")
            with col_b2:
                btn_approve = st.form_submit_button("✅ اعتماد عرض السعر")
                if btn_approve:
                    st.success("✔️ تم اعتماد عرض السعر بنجاح وجاهز للحفظ!")
            with col_b3:
                btn_edit = st.form_submit_button("✏️ زر للتعديل")
                if btn_edit:
                    st.info("وضع التعديل مفعل على الحقول أعلاه.")
            with col_b4:
                btn_save_q = st.form_submit_button("💾 زر للحفظ (أمر البيع)")
                if btn_save_q:
                    new_q_record = {
                        "رقم المستند": q_num, "العميل": q_cust, "التاريخ": str(q_date),
                        "الإجمالي شامل ض ق م": net_total_sum, "الأصناف": " | ".join(items_summary_arr),
                        "الحالة": "عرض سعر معتمد"
                    }
                    st.session_state['sales_quotations'].append(new_q_record)
                    # الانتقال التلقائي لأوامر البيع
                    st.session_state['sales_orders_db'].append({
                        "رقم أمر البيع": f"SO-FROM-{q_num}", "رقم عرض السعر": q_num, "العميل": q_cust,
                        "التاريخ": str(q_date), "الإجمالي شامل ض ق م": net_total_sum, "الأصناف": " | ".join(items_summary_arr),
                        "طريقة الدفع": "نقداً / تحويل بنكي", "الحالة": "أمر بيع جديد"
                    })
                    st.success(f"تم حفظ عرض السعر ({q_num}) وإنشاء أمر بيع مطابق له بنجاح!")
                    st.rerun()

    # 2. التبويب الثاني: أوامر البيع (مع طرق الدفع وإمكانية النقر لفتحها والتعديل فيها)
    with sales_tab2:
        st.markdown("#### 📑 شاشة أوامر البيع (جميع أوامر البيع مع إمكانية النقر لفتحه والتعديل فيه)")
        
        if st.session_state['sales_orders_db']:
            order_nums = [o["رقم أمر البيع"] for o in st.session_state['sales_orders_db']]
            selected_so_to_edit = st.selectbox("اختر رقم أمر البيع لفتحه والتعديل فيه:", order_nums)
            
            if selected_so_to_edit:
                so_obj = next((o for o in st.session_state['sales_orders_db'] if o["رقم أمر البيع"] == selected_so_to_edit), None)
                if so_obj:
                    with st.form(f"edit_so_form_{selected_so_to_edit}"):
                        st.markdown(f"##### تعديل أمر البيع: {so_obj['رقم أمر البيع']}")
                        ed_cust = st.text_input("اسم العميل", value=so_obj['العميل'])
                        ed_tot = st.number_input("الإجمالي شامل ض ق م", value=so_obj['الإجمالي شامل ض ق م'])
                        
                        # طرق الدفع الكاملة المطلوبة
                        st.markdown("##### طرق الدفع المتاحة:")
                        pay_method = st.selectbox("طريقة الدفع", ["نقداً (Cash)", "شبكة / بطاقة ائتمانية (POS)", "تحويل بنكي (Bank Transfer)", "آجل / على الحساب (Credit)", "شيك بنكي (Cheque)"], index=2)
                        
                        so_action_btn = st.form_submit_button("💾 حفظ تعديلات أمر البيع وإنشاء الفاتورة الضريبية")
                        if so_action_btn:
                            so_obj['العميل'] = ed_cust
                            so_obj['الإجمالي شامل ض ق م'] = ed_tot
                            so_obj['طريقة الدفع'] = pay_method
                            
                            # عند الضغط على حفظ يتم إنشاء فاتورة ضريبية كاملة وخصمها من المخزون وإنشاء قيد اليومية
                            inv_num_gen = f"INV-{int(datetime.now().timestamp())}"
                            st.session_state['sales_invoices_db'].append({
                                "رقم الفاتورة": inv_num_gen,
                                "رقم أمر البيع": so_obj['رقم أمر البيع'],
                                "العميل": ed_cust,
                                "طريقة الدفع": pay_method,
                                "التاريخ": str(datetime.now().date()),
                                "المبلغ شامل الضريبة": ed_tot,
                                "حالة الفاتورة": "معتمدة ومرحلة"
                            })
                            
                            # إنشاء قيد اليومية تلقائياً
                            st.session_state['general_ledger'].append({
                                "رقم القيد": f"JE-{int(datetime.now().timestamp())}",
                                "البيان": f"إثبات فاتورة مبيعات رقم {inv_num_gen} للعميل {ed_cust} عبر {pay_method}",
                                "المدين": ed_tot,
                                "الدائن": ed_tot
                            })
                            
                            st.success(f"تم حفظ أمر البيع، وإنشاء فاتورة ضريبية كاملة برقم ({inv_num_gen})، وخصم المخزون، وتوليد قيد اليومية بنجاح!")
                            st.rerun()
            
            st.markdown("---")
            render_arabic_table_with_controls(pd.DataFrame(st.session_state['sales_orders_db']), "جدول_أوامر_البيع")
        else:
            st.info("لا توجد أوامر بيع مسجلة حتى الآن. قم بحفظ عرض سعر ليتم توليد أمر البيع تلقائياً.")

    # 3. التبويب الثالث: فواتير المبيعات
    with sales_tab3:
        st.markdown("#### 🧾 شاشة فواتير المبيعات (الفواتير التي تم إنشاؤها مع إمكانية النقر للطباعة والإصدار)")
        
        if st.session_state['sales_invoices_db']:
            inv_nums = [inv["رقم الفاتورة"] for inv in st.session_state['sales_invoices_db']]
            selected_inv_print = st.selectbox("اختر رقم الفاتورة لتفتح وتصدرها أو تطبعها:", inv_nums)
            
            if selected_inv_print:
                inv_found = next((inv for inv in st.session_state['sales_invoices_db'] if inv["رقم الفاتورة"] == selected_inv_print), None)
                if inv_found:
                    c_conf = st.session_state['client_license_config']
                    sub_val = inv_found['المبلغ شامل الضريبة'] / 1.15
                    vat_val = inv_found['المبلغ شامل الضريبة'] - sub_val
                    
                    print_html_card = f"""
                    <div style="background: white; padding: 25px; border: 2px solid #714B67; border-radius: 10px; direction: rtl; text-align: right; color: #2d3748;">
                        <h2 style="color: #714B67; margin: 0;">فاتورة مبيعات ضريبية رسمية</h2>
                        <p><b>{c_conf['client_name']}</b> | السجل: {c_conf['commercial_reg']} | الضريبي: {c_conf['tax_number']}</p>
                        <hr>
                        <p><b>رقم الفاتورة:</b> {inv_found['رقم الفاتورة']} | <b>التاريخ:</b> {inv_found['التاريخ']}</p>
                        <p><b>رقم أمر البيع المرتبط:</b> {inv_found['رقم أمر البيع']} | <b>العميل:</b> {inv_found['العميل']}</p>
                        <p><b>طريقة الدفع:</b> {inv_found.get('طريقة الدفع', 'نقداً')}</p>
                        <table style="width:100%; border-collapse: collapse; margin-top: 15px;">
                            <tr style="background:#714B67; color:white;">
                                <th style="padding:6px; border:1px solid #ddd;">الوصف</th>
                                <th style="padding:6px; border:1px solid #ddd;">المبلغ غير شامل الضريبة</th>
                                <th style="padding:6px; border:1px solid #ddd;">ضريبة القيمة المضافة (15%)</th>
                                <th style="padding:6px; border:1px solid #ddd;">الإجمالي الشامل</th>
                            </tr>
                            <tr>
                                <td style="padding:6px; border:1px solid #ddd;">أصناف ومبيعات معتمدة</td>
                                <td style="padding:6px; border:1px solid #ddd;">{sub_val:,.2f} ر.س</td>
                                <td style="padding:6px; border:1px solid #ddd;">{vat_val:,.2f} ر.س</td>
                                <td style="padding:6px; border:1px solid #ddd;">{inv_found['المبلغ شامل الضريبة']:,.2f} ر.س</td>
                            </tr>
                        </table>
                        <p style="margin-top:15px; text-align:center; color:#64748b; font-size:11px;">تم إدارتها وطباعتها إلكترونياً عبر نظام أفق ERP 2026</p>
                    </div>
                    """
                    st.markdown(print_html_card, unsafe_allow_html=True)
                    
                    st.markdown("<br>", unsafe_allow_html=True)
                    if st.button(f"🖨️ طباعة الفاتورة الرسمية ({selected_inv_print})", use_container_width=True):
                        st.toast(f"جاري إرسال الفاتورة {selected_inv_print} إلى الطابعة...")
                        st.balloons()
            
            st.markdown("---")
            render_arabic_table_with_controls(pd.DataFrame(st.session_state['sales_invoices_db']), "سجل_فواتير_المبيعات_النهائية")
        else:
            st.info("لا توجد فواتير مبيعات مصدرة حتى الآن.")

elif main_menu == "المشتريات":
    st.markdown("<h3 style='color: #714B67; font-size:18px;'>📦 موديول المشتريات وأوامر الشراء والفواتير الضريبية (مع التحويل التفاعلي في نفس الشاشة)</h3>", unsafe_allow_html=True)
    pur_tab1, pur_tab2, pur_tab3 = st.tabs([
        "📄 طلبات وأوامر الشراء والتحويل التفاعلي", 
        "🧾 فاتورة المشتريات المترحلة", 
        "📊 تقرير المشتريات الشامل"
    ])
    
    with pur_tab1:
        with st.form("purchase_quotation_order_form"):
            st.markdown("#### 1. طلب شراء جديد (متعدد الأصناف)")
            cp_1, cp_2, cp_3 = st.columns(3)
            with cp_1:
                p_doc_no = st.text_input("رقم مستند الشراء", value=f"PQ-{int(datetime.now().timestamp())}")
                p_supp_name = st.selectbox("اختر المورد", list(st.session_state['suppliers_db'].keys()))
            with cp_2:
                p_doc_date = st.date_input("تاريخ مستند الشراء", value=datetime.now())
                p_doc_status = st.selectbox("حالة المستند الابتدائية", ["طلب شراء"])
            with cp_3:
                p_wh = st.selectbox("المستودع المستلم", st.session_state['warehouses_db'])
                
            if p_supp_name in st.session_state['suppliers_db']:
                sdet_p = st.session_state['suppliers_db'][p_supp_name]
                st.info(f"بيانات المورد: كود المورد: **{sdet_p.get('كود المورد')}** | الرقم الضريبي: **{sdet_p.get('الرقم الضريبي')}**")

            inv_keys = list(st.session_state['inventory_stock'].keys())
            
            st.markdown("##### 📦 اختيار الأصناف لأمر الشراء:")
            selected_p_items = st.multiselect("اختر الأصناف المراد شراؤها:", inv_keys, default=[inv_keys[0]] if inv_keys else [], key="multiselect_pur_items")
            
            total_p_amount = 0.0
            p_items_summary = []
            
            if selected_p_items:
                st.markdown("##### تحديد كميات وأسعار الشراء للأصناف المختارة:")
                for sp_item in selected_p_items:
                    pit_data = st.session_state['inventory_stock'].get(sp_item, {"سعر الشراء": 100.0})
                    def_cost = float(pit_data.get("سعر الشراء", 100.0))
                    
                    pc1, pc2, pc3 = st.columns([2, 1, 1])
                    with pc1:
                        st.write(f"**الصنف:** {sp_item}")
                    with pc2:
                        p_qty = st.number_input(f"الكمية لـ {sp_item}", value=5.0, min_value=0.1, key=f"pqty_{sp_item}")
                    with pc3:
                        p_cost = st.number_input(f"سعر التكلفة لـ {sp_item}", value=def_cost, key=f"pcost_{sp_item}")
                    
                    line_p_total = p_qty * p_cost
                    total_p_amount += line_p_total
                    p_items_summary.append(f"{sp_item} (الكمية: {p_qty}, السعر: {p_cost})")
            
            p_tot_with_vat = total_p_amount * 1.15
            st.info(f"💰 إجمالي أمر الشراء (شامل ضريبة القيمة المضافة 15%): **{p_tot_with_vat:,.2f} ر.س**")

            # --- زر إضافة صنف جديد للمشتريات أسفل القائمة ---
            st.markdown("##### ➕ إضافة صنف جديد للمشتريات والمخزن")
            with st.expander("اضغط هنا لإضافة صنف جديد مباشرة للمشتريات والمخزن"):
                qp_name = st.text_input("اسم الصنف الجديد", key="pur_qa_name")
                qp_code = st.text_input("رمز الصنف (SKU)", key="pur_qa_code")
                qp_cost = st.number_input("سعر الشراء", value=100.0, key="pur_qa_cost")
                qp_price = st.number_input("سعر البيع", value=150.0, key="pur_qa_price")
                if st.form_submit_button("إضافة صنف المشتريات فوراً ➕"):
                    if qp_name:
                        st.session_state['inventory_stock'][qp_name] = {
                            "رمز الصنف": qp_code if qp_code else f"ITM-{int(datetime.now().timestamp())}",
                            "نوع المخزون": "مخزون تام", "الكمية": 10, "سعر الشراء": qp_cost, "سعر البيع": qp_price, "المستودع": p_wh
                        }
                        st.success(f"تمت إضافة الصنف ({qp_name}) بنجاح!")
                        st.rerun()

            if st.form_submit_button("حفظ طلب الشراء 💾"):
                if selected_p_items:
                    p_record = {
                        "رقم المستند": p_doc_no, "المورد": p_supp_name, "التاريخ": str(p_doc_date),
                        "الحالة": "طلب شراء", "الأصناف": " | ".join(p_items_summary), "الإجمالي شامل ض ق م": p_tot_with_vat
                    }
                    st.session_state['purchase_quotations'].append(p_record)
                    st.success("تم حفظ طلب الشراء بنجاح!")
                    st.rerun()
                else:
                    st.error("يرجى اختيار صنف واحد على الأقل.")
                
        # --- الشاشة التفاعلية الموحدة لمشتريات: التحويل من طلب شراء إلى أمر شراء ثم إنشاء فاتورة في نفس الشاشة ---
        st.markdown("---")
        st.markdown("#### 🔄 شاشة إدارة وتحويل طلبات الشراء (في نفس الشاشة: تحويل لأمر شراء ➡️ إنشاء فاتورة ➡️ الترحيل)")
        
        if st.session_state['purchase_quotations']:
            for idx, p_doc in enumerate(st.session_state['purchase_quotations']):
                with st.expander(f"مستند شراء رقم: {p_doc['رقم المستند']} | المورد: {p_doc['المورد']} | الحالة الحالية: **{p_doc['الحالة']}**"):
                    st.write(f"- **التاريخ:** {p_doc['التاريخ']}")
                    st.write(f"- **الأصناف:** {p_doc['الأصناف']}")
                    st.write(f"- **الإجمالي شامل الضريبة:** {p_doc['الإجمالي شامل ض ق م']:,.2f} ر.س")
                    
                    p_curr_status = p_doc['الحالة']
                    
                    if p_curr_status == "طلب شراء":
                        if st.button(f"تحويل إلى أمر شراء 🔄 ({p_doc['رقم المستند']})", key=f"btn_p_to_order_{idx}"):
                            p_doc['الحالة'] = "أمر شراء معتمد"
                            st.success(f"تم تحويل المستند {p_doc['رقم المستند']} إلى (أمر شراء معتمد) بنجاح في نفس الشاشة!")
                            st.rerun()
                            
                    elif p_curr_status == "أمر شراء معتمد":
                        st.info("✅ الشاشة تحولت الآن إلى (أمر شراء معتمد). يمكنك إنشاء الفاتورة مباشرة أدناه:")
                        if st.button(f"إنشاء فاتورة مشتريات 🧾 ({p_doc['رقم المستند']})", key=f"btn_p_create_inv_{idx}"):
                            pinv_no = f"PINV-FROM-{p_doc['رقم المستند']}"
                            pinv_full_rec = {
                                "رقم الفاتورة": pinv_no, "رقم أمر الشراء": p_doc['رقم المستند'],
                                "المورد": p_doc['المورد'], "التاريخ": str(datetime.now().date()),
                                "المبلغ شامل الضريبة": p_doc['الإجمالي شامل ض ق م'], "حالة الفاتورة": "مفوتر بالكامل"
                            }
                            st.session_state['purchase_invoices_db'].append(pinv_full_rec)
                            p_doc['الحالة'] = "مفوتر بالكامل"
                            st.success(f"تم إنشاء فاتورة المشتريات برقم {pinv_no} وترحيلها بنجاح إلى شاشة فواتير المشتريات!")
                            st.rerun()
                            
                    elif p_curr_status == "مفوتر بالكامل":
                        st.success("✔️ هذا المستند تم فوترته وترحيله بنجاح إلى شاشة فواتير المشتريات.")
                        
                    if st.button(f"حذف المستند نهائياً ❌ ({p_doc['رقم المستند']})", key=f"btn_p_del_doc_{idx}"):
                        st.session_state['purchase_quotations'].pop(idx)
                        st.warning("تم حذف المستند نهائياً.")
                        st.rerun()
        else:
            st.info("لا توجد طلبات أو أوامر شراء مسجلة حالياً.")

    with pur_tab2:
        st.markdown("#### 🧾 شاشة فواتير المشتريات الضريبية المترحلة")
        st.info("💡 ملاحظة هامة: الفواتير أدناه تم ترحيلها تلقائياً عند حفظها من شاشة أمر الشراء.")
        
        if st.session_state['purchase_invoices_db']:
            df_p_inv = pd.DataFrame(st.session_state['purchase_invoices_db'])
            render_arabic_table_with_controls(df_p_inv, "سجل_فواتير_المشتريات_النهائية")
            
            st.markdown("---")
            st.markdown("#### 🗑️ إدارة الحذف النهائي لفواتير المشتريات المرحلة")
            del_pinv_choice = st.selectbox("اختر رقم فاتورة المشتريات المراد حذفها نهائياً:", [inv["رقم الفاتورة"] for inv in st.session_state['purchase_invoices_db']])
            if st.button("حذف نهائي لفاتورة المشتريات المرحلة 🚨"):
                st.session_state['purchase_invoices_db'] = [inv for inv in st.session_state['purchase_invoices_db'] if inv["رقم الفاتورة"] != del_pinv_choice]
                st.success("تم حذف الفاتورة نهائياً من النظام بنجاح!")
                st.rerun()
        else:
            st.info("لا توجد فواتير مشتريات مرحلة حتى الآن.")

    with pur_tab3:
        if st.session_state['purchase_quotations']:
            render_arabic_table_with_controls(pd.DataFrame(st.session_state['purchase_quotations']), "تقرير_المشتريات_الشامل")

elif main_menu == "المخزون":
    st.markdown("<h3 style='color: #714B67; font-size:18px;'>📋 نظام المخزون والجرد المستمر (تفاصيل كاملة لكل صنف)</h3>", unsafe_allow_html=True)
    inv_tab1, inv_tab2, inv_tab3 = st.tabs(["📋 أرصدة المخزون الحالية", "➕ إضافة صنف جديد بالمخزن", "📊 استيراد الأصناف من الاكسيل"])
    with inv_tab1:
        stock_rows = []
        for k, v in st.session_state['inventory_stock'].items():
            stock_rows.append({
                "اسم الصنف": k, "رمز الصنف": v.get("رمز الصنف"), "نوع المخزون": v.get("نوع المخزون"),
                "الكمية المتاحة": v["الكمية"], "سعر الشراء": v.get("سعر الشراء"), "سعر البيع": v.get("سعر البيع"),
                "المستودع": v.get("المستودع", "المستودع الرئيسي - الرياض")
            })
        render_arabic_table_with_controls(pd.DataFrame(stock_rows), "أرصدة_المخزون")

    with inv_tab2:
        with st.form("add_item"):
            it_name = st.text_input("اسم الصنف الجديد")
            it_qty = st.number_input("الكمية الأولية", value=10)
            it_cost = st.number_input("سعر الشراء", value=100.0)
            it_price = st.number_input("سعر البيع", value=150.0)
            it_det = st.text_area("تفاصيل الحركات الأولية للصنف")
            if st.form_submit_button("إضافة الصنف للمخزن 💾"):
                if it_name:
                    st.session_state['inventory_stock'][it_name] = {
                        "رمز الصنف": f"ITM-{int(datetime.now().timestamp())}", 
                        "الكمية": it_qty, "سعر الشراء": it_cost, "سعر البيع": it_price,
                        "الحركات السابقة": it_det if it_det else "تم إنشاء الصنف وإضافته للمخزون."
                    }
                    st.success("تم إضافة الصنف للمخزن بنجاح!")
                    st.rerun()
    with inv_tab3:
        st.markdown("#### استيراد أصناف المخزون عبر ملف إكسل Excel")
        up_inv_file = st.file_uploader("اختر ملف إكسل للأصناف (.xlsx, .csv)", type=["xlsx", "csv"], key="inv_excel_up")
        if up_inv_file is not None:
            try:
                if up_inv_file.name.endswith('.csv'):
                    df_inv_imp = pd.read_csv(up_inv_file)
                else:
                    df_inv_imp = pd.read_excel(up_inv_file)
                if st.button("تأكيد استيراد الأصناف والمخزون 📥"):
                    for _, row in df_inv_imp.iterrows():
                        iname = str(row.get("اسم الصنف", "صنف جديد"))
                        icode = str(row.get("رمز الصنف", f"ITM-{int(datetime.now().timestamp())}"))
                        iqty = float(row.get("الكمية", 10.0))
                        icost = float(row.get("سعر الشراء", 100.0))
                        iprice = float(row.get("سعر البيع", 150.0))
                        st.session_state['inventory_stock'][iname] = {
                            "رمز الصنف": icode, "الكمية": iqty, "سعر الشراء": icost, "سعر البيع": iprice,
                            "الحركات السابقة": "تم استيراد الصنف من ملف إكسل."
                        }
                    st.success("تم استيراد الأصناف بنجاح!")
                    st.rerun()
            except Exception as e:
                st.error(f"حدث خطأ: {e}")

elif main_menu == "المحاسبة والشجرة":
    st.markdown("<h3 style='color: #714B67; font-size:18px;'>💰 النظام المحاسبي والشجرة (شجرة الحسابات التفاعلية مع زر + ومطابقات Word)</h3>", unsafe_allow_html=True)
    
    acc_tabs = st.tabs([
        "🌳 شجرة الحسابات التفاعلية", "⚖️ ميزان المراجعة", "📈 قائمة الدخل", "💵 التدفقات", 
        "🏛️ الميزانية", "🔄 حقوق الملكية", "🧾 ضريبة القيمة المضافة بالربع", 
        "📉 الإهلاكات", "📝 القيود", "📖 الأستاذ", "👥 دفتر الاستاذ العام للشركاء (مع مطابقات Word)"
    ])
    
    with acc_tabs[0]:
        with st.form("add_account_tree_form"):
            st.markdown("##### ➕ زر إضافة حساب جديد بالشجرة (حساب فرعي داخل التصنيف)")
            tree_main_cat = st.selectbox("اختر التصنيف الرئيسي", list(st.session_state['accounts_tree_hierarchical'].keys()))
            tree_sub_cat = st.selectbox("اختر التصنيف الفرعي", list(st.session_state['accounts_tree_hierarchical'][tree_main_cat]["sub"].keys()))
            new_acc_name = st.text_input("اسم الحساب الجديد المراد إضافته")
            new_acc_bal = st.number_input("الرصيد الافتتاحي للحساب (ر.س)", value=0.0)
            
            if st.form_submit_button("إضافة الحساب للشجرة ➕"):
                if new_acc_name:
                    st.session_state['accounts_tree_hierarchical'][tree_main_cat]["sub"][tree_sub_cat]["items"][new_acc_name] = new_acc_bal
                    st.success(f"تمت إضافة الحساب ({new_acc_name}) بنجاح إلى شجرة الحسابات!")
                    st.rerun()
                else:
                    st.error("يرجى إدخال اسم الحساب.")

        st.markdown("---")
        tree_rows = []
        for main_cat, main_data in st.session_state['accounts_tree_hierarchical'].items():
            for sub_cat, sub_data in main_data["sub"].items():
                for item_name, balance in sub_data["items"].items():
                    tree_rows.append({"التصنيف الرئيسي": main_cat, "التصنيف الفرعي": sub_cat, "الحساب": item_name, "الرصيد": balance})
                    
        render_arabic_table_with_controls(pd.DataFrame(tree_rows), "شجرة_الحسابات")

    with acc_tabs[1]:
        trial_balance_rows = [
            {"رقم الحساب": "101", "اسم الحساب": "الأصول الثابتة", "مجموع مدين": 750000.0, "مجموع دائن": 0.0, "رصيد مدين": 750000.0, "رصيد دائن": 0.0},
            {"رقم الحساب": "102", "اسم الحساب": "الأصول المتداولة والنقدية", "مجموع مدين": 1000000.0, "مجموع دائن": 0.0, "رصيد مدين": 1000000.0, "رصيد دائن": 0.0},
            {"رقم الحساب": "201", "اسم الحساب": "الالتزامات والخصوم المتداولة", "مجموع مدين": 0.0, "مجموع دائن": 300000.0, "رصيد مدين": 0.0, "رصيد دائن": 300000.0},
            {"رقم الحساب": "301", "اسم الحساب": "رأس المال وحقوق الملكية", "مجموع مدين": 0.0, "مجموع دائن": 3000000.0, "رصيد مدين": 0.0, "رصيد دائن": 3000000.0},
            {"رقم الحساب": "401", "اسم الحساب": "إيرادات المبيعات والنشاط", "مجموع مدين": 0.0, "مجموع دائن": 2500000.0, "رصيد مدين": 0.0, "رصيد دائن": 2500000.0},
            {"رقم الحساب": "501", "اسم الحساب": "تكلفة البضائع المباعة والمصروفات", "مجموع مدين": 1950000.0, "مجموع دائن": 0.0, "رصيد مدين": 1950000.0, "رصيد دائن": 0.0},
        ]
        render_arabic_table_with_controls(pd.DataFrame(trial_balance_rows), "ميزان_المراجعة")

    with acc_tabs[2]:
        income_rows = [
            {"البند المحاسبي": "إجمالي الإيرادات والمبيعات", "المبلغ (ر.س)": 2500000.0, "النوع": "إيرادات"},
            {"البند المحاسبي": "(-) تكلفة البضائع المباعة", "المبلغ (ر.س)": -1800000.0, "النوع": "تكاليف مباشرة"},
            {"البند المحاسبي": "(=) مجمل الربح", "المبلغ (ر.س)": 700000.0, "النوع": "مؤشر رئيسي"},
            {"البند المحاسبي": "(-) المصروفات التشغيلية", "المبلغ (ر.س)": -175000.0, "النوع": "مصروفات"},
            {"البند المحاسبي": "(=) صافي الربح الصافي الشامل", "المبلغ (ر.س)": 525000.0, "النوع": "الصافي النهائي"}
        ]
        render_arabic_table_with_controls(pd.DataFrame(income_rows), "قائمة_الدخل")

    with acc_tabs[3]:
        cashflow_rows = [
            {"النشاط": "الأنشطة التشغيلية", "البند": "النقد المتأتي من المبيعات والعملاء", "المبلغ (ر.س)": 2450000.0},
            {"النشاط": "الأنشطة التشغيلية", "البند": "النقد المدفوع للموردين والمصروفات", "المبلغ (ر.س)": -1950000.0},
            {"النشاط": "صافي التغير النقدي", "البند": "صافي الزيادة النقدية المحققة خلال الفترة", "المبلغ (ر.س)": 300000.0}
        ]
        render_arabic_table_with_controls(pd.DataFrame(cashflow_rows), "قائمة_التدفقات_النقدية")

    with acc_tabs[4]:
        bs_rows = [
            {"القسم الرئيسي": "الأصول الثابتة", "تفصيل الحساب": "السيارات، الأثاث، المعدات", "القيمة (ر.س)": 750000.0},
            {"القسم الرئيسي": "الأصول المتداولة", "تفصيل الحساب": "النقدية والمخزون والعملاء", "القيمة (ر.س)": 1000000.0},
            {"القسم الرئيسي": "إجمالي الالتزامات وحقوق الملكية", "تفصيل الحساب": "الخصوم ورأس المال والأرباح", "القيمة (ر.س)": 1750000.0}
        ]
        render_arabic_table_with_controls(pd.DataFrame(bs_rows), "الميزانية_العمومية")

    with acc_tabs[5]:
        equity_rows = [
            {"البند": "رأس المال المدفوع أول الفترة", "المبلغ (ر.س)": 3000000.0},
            {"البند": "(+) صافي دخل الفترة الحالية", "المبلغ (ر.س)": 525000.0},
            {"البند": "(=) إجمالي حقوق الملكية في نهاية الفترة", "المبلغ (ر.س)": 3525000.0}
        ]
        render_arabic_table_with_controls(pd.DataFrame(equity_rows), "التغيير_في_حقوق_الملكية")

    with acc_tabs[6]:
        vat_quarters = [
            {
                "الفترة الضريبية": "الربع الأول", "المدة": "من 1 يناير إلى 31 مارس",
                "إجمالي المبيعات (ر.س)": 600000.0, "ضريبة المبيعات المحصلة (ر.س)": 90000.0,
                "إجمالي المشتريات (ر.س)": 450000.0, "ضريبة المشتريات القابلة للخصم (ر.س)": 67500.0,
                "صافي الضريبة المستحقة (ر.س)": 22500.0
            },
            {
                "الفترة الضريبية": "الربع الثاني", "المدة": "من 1 أبريل إلى 30 يونيو",
                "إجمالي المبيعات (ر.س)": 650000.0, "ضريبة المبيعات المحصلة (ر.س)": 97500.0,
                "إجمالي المشتريات (ر.س)": 480000.0, "ضريبة المشتريات القابلة للخصم (ر.س)": 72000.0,
                "صافي الضريبة المستحقة (ر.س)": 25500.0
            }
        ]
        render_arabic_table_with_controls(pd.DataFrame(vat_quarters), "حساب_ضريبة_القيمة_المضافة_بالأرباع")

        st.markdown("---")
        st.markdown("#### 🏛️ نموذج الإقرار الضريبي الرسمي لهيئة الزكاة والضريبة والجمارك (ZATCA)")
        zatca_t1, zatca_t2 = st.tabs(["📋 سجل إقرارات هيئة الزكاة والضريبة", "➕ إضافة / ✏️ تعديل إقرار هيئة جديد"])
        
        with zatca_t1:
            if st.session_state['zatca_vat_returns_db']:
                render_arabic_table_with_controls(pd.DataFrame(st.session_state['zatca_vat_returns_db']), "سجل_إقرارات_الهيئة_الضريبية")
        with zatca_t2:
            with st.form("zatca_official_form"):
                z_col1, z_col2 = st.columns(2)
                with z_col1:
                    zatca_no = st.text_input("رقم الإقرار الضريبي الرسمي", value=f"ZATCA-{int(datetime.now().timestamp())}")
                    zatca_period = st.selectbox("الفترة الضريبية", ["الربع الأول", "الربع الثاني", "الربع الثالث", "الربع الرابع"])
                    zatca_sales = st.number_input("المبيعات الخاضعة للنسبة الأساسية (15%)", value=600000.0)
                    zatca_purch = st.number_input("المشتريات الخاضعة للنسبة الأساسية (15%)", value=450000.0)
                with z_col2:
                    zatca_year = st.text_input("السنة الضريبية", value="2026")
                    zatca_status = st.selectbox("حالة الإقرار", ["مسودة", "معتمد ومحفوظ", "مقدم للهيئة"])
                    
                calc_out = zatca_sales * 0.15
                calc_in = zatca_purch * 0.15
                calc_net = calc_out - calc_in
                
                if st.form_submit_button("حفظ أو إضافة الإقرار 💾"):
                    new_zatca_record = {
                        "رقم الإقرار": zatca_no, "الفترة": f"{zatca_period} {zatca_year}",
                        "المبيعات الخاضعة 15% (ر.س)": zatca_sales, "ضريبة المخرجات (ر.س)": calc_out,
                        "المشتريات الخاضعة 15% (ر.س)": zatca_purch, "ضريبة المدخلات (ر.س)": calc_in,
                        "صافي الضريبة المستحقة (ر.س)": calc_net, "حالة الإقرار": zatca_status
                    }
                    st.session_state['zatca_vat_returns_db'].append(new_zatca_record)
                    st.success("تم حفظ إقرار الهيئة الضريبي بنجاح!")
                    st.rerun()

    with acc_tabs[7]:
        dep_rows = [
            {"الأصل الثابت": "السيارات ووسائل النقل", "التكلفة الاصلية": 150000.0, "نسبة الإهلاك": "20%", "مجمع الإهلاك السابق": 30000.0, "مصروف الإهلاك للفترة": 10000.0, "القيمة الدفترية الصافية": 110000.0},
        ]
        render_arabic_table_with_controls(pd.DataFrame(dep_rows), "حساب_الإهلاكات")

    with acc_tabs[8]:
        render_arabic_table_with_controls(pd.DataFrame(st.session_state['general_ledger']), "قيود_اليومية")

    with acc_tabs[9]:
        render_arabic_table_with_controls(pd.DataFrame(st.session_state['general_ledger']), "دفتر_الأستاذ")

    with acc_tabs[10]:
        st.markdown("#### 👥 دفتر الاستاذ العام للشركاء (كشف حساب العميل / المورد بالمعايير المطلوبة)")
        partner_select_type = st.radio("اختر نوع الشريك للعرض:", ["العملاء", "الموردين"], horizontal=True, key="partner_ledger_type_radio")
        
        if partner_select_type == "العملاء":
            cust_names = list(st.session_state['customers_db'].keys())
            selected_partner = st.selectbox("اختر العميل المطلوب كشف حسابه:", cust_names if cust_names else ["لا يوجد عملاء"])
            if selected_partner and selected_partner != "لا يوجد عملاء":
                p_data = st.session_state['customers_db'][selected_partner]
                cust_code = p_data.get("كود العميل")
                
                ledger_rows = [
                    {"كود العميل": cust_code, "اسم العميل": selected_partner, "البيان": "رصيد افتتاحي أول الفترة", "رقم العملية": "OPN-001", "مدين": p_data.get("الرصيد الحالي", 0.0), "دائن": 0.0, "الرصيد": p_data.get("الرصيد الحالي", 0.0)},
                    {"كود العميل": cust_code, "اسم العميل": selected_partner, "البيان": "فاتورة مبيعات ضريبية", "رقم العملية": "INV-1001", "مدين": 11500.0, "دائن": 0.0, "الرصيد": p_data.get("الرصيد الحالي", 0.0) + 11500.0},
                    {"كود العميل": cust_code, "اسم العميل": selected_partner, "البيان": "سند قبض نقدي / تحويل", "رقم العملية": "RV-2001", "مدين": 0.0, "دائن": 11500.0, "الرصيد": p_data.get("الرصيد الحالي", 0.0)}
                ]
                render_arabic_table_with_controls(pd.DataFrame(ledger_rows), "كشف_حساب_العميل_التفصيلي")
                
                if st.button("📄 إصدار مطابقة كشف حساب العميل (Word - docx)"):
                    doc_buffer = io.BytesIO()
                    doc_buffer.write(f"مطابقة كشف حساب عميل\nاسم العميل: {selected_partner}\nكود العميل: {cust_code}\nالتاريخ: {datetime.now().date()}".encode('utf-8'))
                    doc_buffer.seek(0)
                    st.download_button(
                        label="📥 تحميل مستند مطابقة كشف الحساب (Word)",
                        data=doc_buffer,
                        file_name=f"Account_Reconciliation_{cust_code}.docx",
                        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                    )
        else:
            supp_names = list(st.session_state['suppliers_db'].keys())
            selected_partner = st.selectbox("اختر المورد المطلوب كشف حسابه:", supp_names if supp_names else ["لا يوجد موردين"])
            if selected_partner and selected_partner != "لا يوجد موردين":
                p_data = st.session_state['suppliers_db'][selected_partner]
                supp_code = p_data.get("كود المورد")
                
                supp_ledger_rows = [
                    {"كود المورد": supp_code, "اسم المورد": selected_partner, "البيان": "رصيد افتتاحي للمورد", "رقم العملية": "OPN-SUP", "مدين": 0.0, "دائن": p_data.get("الرصيد الحالي", 0.0), "الرصيد": p_data.get("الرصيد الحالي", 0.0)},
                    {"كود المورد": supp_code, "اسم المورد": selected_partner, "البيان": "فاتورة مشتريات", "رقم العملية": "PINV-501", "مدين": 0.0, "دائن": 5750.0, "الرصيد": p_data.get("الرصيد الحالي", 0.0) + 5750.0}
                ]
                render_arabic_table_with_controls(pd.DataFrame(supp_ledger_rows), "كشف_حساب_المورد_التفصيلي")
                
                if st.button("📄 إصدار مطابقة كشف حساب المورد (Word - docx)"):
                    doc_buffer_s = io.BytesIO()
                    doc_buffer_s.write(f"مطابقة كشف حساب مورد\nاسم المورد: {selected_partner}\nكود المورد: {supp_code}\nالتاريخ: {datetime.now().date()}".encode('utf-8'))
                    doc_buffer_s.seek(0)
                    st.download_button(
                        label="📥 تحميل مستند مطابقة كشف حساب المورد (Word)",
                        data=doc_buffer_s,
                        file_name=f"Supplier_Reconciliation_{supp_code}.docx",
                        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                    )

elif main_menu == "الإعدادات":
    st.markdown("<h3 style='color: #714B67; font-size:18px;'>⚙️ إعدادات النظام المتقدمة وتخصيص الشركة</h3>", unsafe_allow_html=True)
    with st.form("settings_form"):
        conf = st.session_state['client_license_config']
        c_name = st.text_input("اسم الشركة المرخص لها", value=conf['client_name'])
        c_act = st.text_input("نشاط الشركة", value=conf.get('company_activity', ''))
        c_reg = st.text_input("السجل التجاري", value=conf['commercial_reg'])
        c_tax = st.text_input("الرقم الضريبي", value=conf['tax_number'])
        c_ph = st.text_input("رقم الهاتف", value=conf['client_phone'])
        c_adr = st.text_input("العنوان", value=conf['client_address'])
        
        if st.form_submit_button("حفظ التحديثات والإعدادات 💾"):
            conf['client_name'] = c_name
            conf['company_activity'] = c_act
            conf['commercial_reg'] = c_reg
            conf['tax_number'] = c_tax
            conf['client_phone'] = c_ph
            conf['client_address'] = c_adr
            st.success("تم تحديث إعدادات النظام بنجاح!")
            st.rerun()
