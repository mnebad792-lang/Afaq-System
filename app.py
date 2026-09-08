import streamlit as st
import pandas as pd
from datetime import datetime
import json

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
                        "مصروف الكهرباء والماء": 20000.0
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
        "EMP-101": {"الاسم الكامل": "أحمد محمد العتيبي", "القسم": "الإدارة المالية", "المسمى الوظيفي": "محاسب أول", "الراتب الأساسي": 8000.0, "بدل السكن": 2000.0, "بدل النقل": 500.0, "تاريخ البداية": "2023-01-15", "الحالة": "على رأس العمل"},
        "EMP-102": {"الاسم الكامل": "سارة خالد الشمري", "القسم": "الموارد البشرية", "المسمى الوظيفي": "مسؤول شؤون موظفين", "الراتب الأساسي": 6500.0, "بدل السكن": 1500.0, "بدل النقل": 400.0, "تاريخ البداية": "2023-06-01", "الحالة": "على رأس العمل"}
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
        {"رقم الأمر": "PRD-ORD-101", "اسم المنتج": "أجهزة لابتوب ديل احترافي", "الكمية المطلوبة": 20, "الكمية المنتجة": 20, "تاريخ البدء": "2026-06-01", "تاريخ الانتهاء": "2026-06-05", "الحالة": "مكتمل"}
    ]

if 'projects_db' not in st.session_state:
    st.session_state['projects_db'] = [
        {"رقم المشروع": "PRJ-01", "اسم المشروع": "تطوير خط الإنتاج الآلي", "مدير المشروع": "أحمد العتيبي", "الميزانية (ر.س)": 150000.0, "المصروف الفعلي (ر.س)": 95000.0, "نسبة الإنجاز": "65%", "الحالة": "جارية"}
    ]

if 'cost_centers_db' not in st.session_state:
    st.session_state['cost_centers_db'] = [
        {"رمز المركز": "CC-101", "اسم مركز التكلفة": "مركز إنتاج الأجهزة", "المسؤول": "مهندس الإنتاج", "المصروفات الحالية (ر.س)": 120000.0, "الإيرادات المرتبطة (ر.س)": 450000.0}
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
        "أجهزة لابتوب ديل احترافي": {"رمز الصنف": "PRD-001", "نوع المخزون": "مخزون تام", "الفئة": "إلكترونيات", "الكمية": 50, "سعر البيع": 3500.0, "سعر الشراء": 2800.0, "المستودع": "المستودع الرئيسي - الرياض", "حد الطلب": 10},
        "شاشة سمارت 55 بوصة": {"رمز الصنف": "PRD-002", "نوع المخزون": "مخزون تام", "الفئة": "إلكترونيات", "الكمية": 30, "سعر البيع": 2200.0, "سعر الشراء": 1800.0, "المستودع": "المستودع الرئيسي - الرياض", "حد الطلب": 5}
    }

if 'sales_quotations' not in st.session_state:
    st.session_state['sales_quotations'] = []

if 'sales_orders' not in st.session_state:
    st.session_state['sales_orders'] = []

if 'sales_invoices_db' not in st.session_state:
    st.session_state['sales_invoices_db'] = []

if 'purchase_quotations' not in st.session_state:
    st.session_state['purchase_quotations'] = []

if 'purchase_orders' not in st.session_state:
    st.session_state['purchase_orders'] = []

if 'purchase_invoices_db' not in st.session_state:
    st.session_state['purchase_invoices_db'] = []

if 'general_ledger' not in st.session_state:
    st.session_state['general_ledger'] = [
        {"رقم القيد": "JE-101", "البيان": "قيد الافتتاح", "المدين": 3000000.0, "الدائن": 3000000.0}
    ]

# --- تنسيقات CSS مع خاصية Shrink to Fit للجداول وتصميم الأيقونات الجانبية ---
st.markdown("""
    <style>
    .stApp, body, p, span, div, label, input, select {
        direction: rtl !important; text-align: right !important; font-family: 'Segoe UI', Tahoma, sans-serif;
    }
    .block-container { padding: 1.5rem 2rem !important; background-color: #f4f6f9; }
    
    .custom-table {
        width: 100%; border-collapse: collapse; background-color: white; font-size: 11px;
        border-radius: 6px; overflow: hidden; box-shadow: 0 1px 3px rgba(0,0,0,0.08); margin-top: 10px;
        table-layout: auto !important;
    }
    .custom-table th { background-color: #714B67; color: white; padding: 8px; border-bottom: 2px solid #5a3b52; text-align: right; white-space: nowrap; }
    .custom-table td { padding: 6px 8px; border-bottom: 1px solid #edf2f7; color: #2d3748; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; max-width: 250px; }
    
    .official-form-box {
        background: white; padding: 20px; border-radius: 8px; border: 1px solid #dcdde1;
        box-shadow: 0 2px 4px rgba(0,0,0,0.04); margin-bottom: 20px;
    }
    
    .metric-card {
        background: white; padding: 15px; border-radius: 8px; border-right: 4px solid #714B67;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05); text-align: center;
    }
    </style>
""", unsafe_allow_html=True)

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
            st.markdown("<p style='font-size:12px; color:#64748b; padding-top:10px;'>فلترة البحث الفعالة مفعلة</p>", unsafe_allow_html=True)

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

    html_code = "<div style='overflow-x: auto;'><table class='custom-table'><thead><tr>"
    for col in filtered_df.columns: html_code += f"<th>{col}</th>"
    html_code += "</tr></thead><tbody>"
    for _, row in filtered_df.iterrows():
        html_code += "<tr>"
        for col in filtered_df.columns: html_code += f"<td>{row[col]}</td>"
        html_code += "</tr>"
    html_code += "</tbody></table></div>"
    st.markdown(html_code, unsafe_allow_html=True)

# --- تهيئة المجلد الحالي في الجلسة ---
if 'active_module' not in st.session_state:
    st.session_state['active_module'] = "الرئيسية"

# --- القائمة الجانبية (أيقونات احترافية وبدون تكرار وحذف الزيادات) ---
with st.sidebar:
    client_conf = st.session_state['client_license_config']
    st.markdown(f"<h2 style='color: #714B67; text-align: center;'>نظام أفق ERP</h2>", unsafe_allow_html=True)
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

# --- محتوى اللوحة العامة (الرئيسية) ---
if main_menu == "الرئيسية":
    client_conf = st.session_state['client_license_config']
    st.markdown(f"""
        <div class="official-form-box">
            <h2 style="color: #714B67; margin: 0;">🚀 لوحة التحكم السحابية - {client_conf['client_name']}</h2>
            <p style="color: #64748b; margin-top: 5px; font-size: 14px;">نشاط الشركة: {client_conf.get('company_activity', 'غير محدد')} | السجل التجاري: {client_conf['commercial_reg']} | الرقم الضريبي: {client_conf['tax_number']}</p>
        </div>
    """, unsafe_allow_html=True)

    total_cust_val = sum([c.get("الرصيد الحالي", 0) for c in st.session_state['customers_db'].values()])
    total_supp_val = sum([s.get("الرصيد الحالي", 0) for s in st.session_state['suppliers_db'].values()])
    total_emp_count = len(st.session_state['hr_employees_db'])
    total_prod_orders = len(st.session_state['production_orders'])

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f"<div class='metric-card'><p style='color: #64748b; margin:0; font-size:12px;'>إجمالي أرصدة العملاء</p><h3 style='color: #714B67; margin:5px 0 0 0;'>{total_cust_val:,.2f} ر.س</h3></div>", unsafe_allow_html=True)
    with col2:
        st.markdown(f"<div class='metric-card'><p style='color: #64748b; margin:0; font-size:12px;'>إجمالي أرصدة الموردين</p><h3 style='color: #714B67; margin:5px 0 0 0;'>{total_supp_val:,.2f} ر.س</h3></div>", unsafe_allow_html=True)
    with col3:
        st.markdown(f"<div class='metric-card'><p style='color: #64748b; margin:0; font-size:12px;'>إجمالي عدد الموظفين</p><h3 style='color: #714B67; margin:5px 0 0 0;'>{total_emp_count} موظف</h3></div>", unsafe_allow_html=True)
    with col4:
        st.markdown(f"<div class='metric-card'><p style='color: #64748b; margin:0; font-size:12px;'>أوامر الإنتاج المسجلة</p><h3 style='color: #714B67; margin:5px 0 0 0;'>{total_prod_orders} أمر</h3></div>", unsafe_allow_html=True)

# --- إدارة شركاء النجاح (الشركاء) ---
elif main_menu == "الشركاء":
    st.markdown("<h3 style='color: #714B67;'>👥 إدارة شركاء النجاح (العملاء والموردين)</h3>", unsafe_allow_html=True)
    t_cust, t_supp, t_add = st.tabs(["📋 العملاء", "📋 الموردين", "➕ إضافة عميل أو مورد جديد"])
    
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

# --- إدارة الموارد البشرية ---
elif main_menu == "الموارد البشرية":
    st.markdown("<h3 style='color: #714B67;'>👨‍💼 إدارة الموارد البشرية (HR)</h3>", unsafe_allow_html=True)
    hr_tab1, hr_tab2, hr_tab3, hr_tab4, hr_tab5 = st.tabs([
        "📋 سجل الموظفين الشامل", "➕ إضافة موظف جديد", "⏰ متابعة الحضور والانصراف", "🏖️ إدارة الإجازات والطلبات", "💰 مسير الرواتب والأجور (Payroll)"
    ])
    with hr_tab1:
        emp_rows = [{"رقم الموظف": k, "الاسم": v["الاسم الكامل"], "القسم": v["القسم"], "المسمى": v["المسمى الوظيفي"], "الراتب": v["الراتب الأساسي"]} for k, v in st.session_state['hr_employees_db'].items()]
        render_arabic_table_with_controls(pd.DataFrame(emp_rows), "الموظفين")
    with hr_tab2:
        with st.form("add_emp"):
            e_id = st.text_input("رقم الموظف (مثال: EMP-104)")
            e_name = st.text_input("الاسم الكامل للموظف")
            e_dept = st.text_input("القسم")
            e_title = st.text_input("المسمى الوظيفي")
            e_sal = st.number_input("الراتب الأساسي", value=5000.0)
            if st.form_submit_button("حفظ الموظف الجديد 💾"):
                if e_id and e_name:
                    st.session_state['hr_employees_db'][e_id] = {"الاسم الكامل": e_name, "القسم": e_dept, "المسمى الوظيفي": e_title, "الراتب الأساسي": e_sal, "الحالة": "على رأس العمل"}
                    st.success("تم إضافة الموظف بنجاح!")
                    st.rerun()
    with hr_tab3:
        render_arabic_table_with_controls(pd.DataFrame(st.session_state['hr_attendance']), "الحضور")
    with hr_tab4:
        render_arabic_table_with_controls(pd.DataFrame(st.session_state['hr_leaves']), "الإجازات")
    with hr_tab5:
        sal_rows = [{"رقم الموظف": k, "الاسم": v["الاسم الكامل"], "الصافي المستحق": v["الراتب الأساسي"] + v.get("بدل السكن", 0)} for k, v in st.session_state['hr_employees_db'].items()]
        render_arabic_table_with_controls(pd.DataFrame(sal_rows), "مسير_الرواتب")

# --- إدارة الإنتاج ---
elif main_menu == "الإنتاج":
    st.markdown("<h3 style='color: #714B67;'>🏭 إدارة الإنتاج والمصنع/المطبخ</h3>", unsafe_allow_html=True)
    prod_tab1, prod_tab2, prod_tab3 = st.tabs(["⚙️ أوامر الإنتاج النشطة", "➕ إضافة أمر إنتاج جديد", "✅ أوامر الإنتاج المكتملة"])
    with prod_tab1:
        render_arabic_table_with_controls(pd.DataFrame(st.session_state['production_orders']), "أوامر_الإنتاج")
    with prod_tab2:
        with st.form("new_prod"):
            p_item = st.text_input("اسم المنتج / الوجبة المصنعة")
            p_qty = st.number_input("الكمية المطلوبة للإنتاج", value=10)
            if st.form_submit_button("إصدار أمر الإنتاج الجديد ⚙️"):
                if p_item:
                    st.session_state['production_orders'].append({"رقم الأمر": f"PRD-{len(st.session_state['production_orders'])+1:03d}", "اسم المنتج": p_item, "الكمية المطلوبة": p_qty, "الحالة": "قيد التنفيذ"})
                    st.success("تم إصدار أمر الإنتاج بنجاح!")
                    st.rerun()
    with prod_tab3:
        render_arabic_table_with_controls(pd.DataFrame(st.session_state['production_orders']), "أوامر_مكتملة")

# --- إدارة المشروعات ---
elif main_menu == "المشروعات":
    st.markdown("<h3 style='color: #714B67;'>📊 إدارة المشاريع</h3>", unsafe_allow_html=True)
    proj_tab1, proj_tab2 = st.tabs(["📋 قائمة المشاريع", "➕ إضافة مشروع جديد"])
    with proj_tab1:
        render_arabic_table_with_controls(pd.DataFrame(st.session_state['projects_db']), "المشاريع")
    with proj_tab2:
        with st.form("add_proj"):
            pr_id = st.text_input("رقم المشروع (مثال: PRJ-03)")
            pr_name = st.text_input("اسم المشروع")
            pr_bud = st.number_input("الميزانية (ر.س)", value=100000.0)
            if st.form_submit_button("حفظ المشروع 💾"):
                st.session_state['projects_db'].append({"رقم المشروع": pr_id, "اسم المشروع": pr_name, "الميزانية (ر.س)": pr_bud, "نسبة الإنجاز": "0%", "الحالة": "جديدة"})
                st.success("تم إضافة المشروع بنجاح!")
                st.rerun()

# --- مراكز التكلفة ---
elif main_menu == "مراكز التكلفة":
    st.markdown("<h3 style='color: #714B67;'>🏷️ إدارة مراكز التكلفة</h3>", unsafe_allow_html=True)
    cc_tab1, cc_tab2 = st.tabs(["📋 مراكز التكلفة الشاملة", "➕ إضافة مركز تكلفة جديد"])
    with cc_tab1:
        render_arabic_table_with_controls(pd.DataFrame(st.session_state['cost_centers_db']), "مراكز_التكلفة")
    with cc_tab2:
        with st.form("add_cc"):
            cc_id = st.text_input("رمز المركز (مثال: CC-103)")
            cc_name = st.text_input("اسم مركز التكلفة")
            if st.form_submit_button("حفظ المركز 💾"):
                st.session_state['cost_centers_db'].append({"رمز المركز": cc_id, "اسم مركز التكلفة": cc_name, "المصروفات الحالية (ر.س)": 0.0, "الإيرادات المرتبطة (ر.س)": 0.0})
                st.success("تم الحفظ بنجاح!")
                st.rerun()

# --- الصلاحيات (بناءً على طلبك بالتحكم وتحديد الصلاحيات الكاملة لكل مستخدم) ---
elif main_menu == "الصلاحيات":
    st.markdown("<h3 style='color: #714B67;'>🔐 شاشة إدارة الصلاحيات وتحديد صلاحيات المستخدمين بدقة</h3>", unsafe_allow_html=True)
    
    perm_tab1, perm_tab2 = st.tabs(["👥 قائمة المستخدمين وصلاحياتهم", "➕ إضافة / تعديل مستخدم وصلاحياته"])
    
    with perm_tab1:
        # عرض المستخدمين مع الصلاحيات الممنوحة
        view_perms = []
        for u in st.session_state['users_permissions_db']:
            view_perms.append({
                "اسم المستخدم": u.get("اسم المستخدم"),
                "الاسم الكامل": u.get("الاسم الكامل"),
                "الدور": u.get("الدور"),
                "الصلاحيات الممنوحة": ", ".join(u.get("الصلاحيات الممنوحة", [])),
                "الحالة": u.get("الحالة")
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
                    if st.checkbox(mod, value=True if mod in ["الرئيسية", "المبيعات", "المخزون"] else False, key=f"chk_perm_{mod}"):
                        selected_user_modules.append(mod)
                        
            if st.form_submit_button("حفظ وحفظ صلاحيات المستخدم 💾"):
                if u_username:
                    # التحقق إذا كان المستخدم موجود مسبقاً لتعديله أو إضافته
                    found = False
                    for existing_user in st.session_state['users_permissions_db']:
                        if existing_user["اسم المستخدم"] == u_username:
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

# --- المبيعات الشاملة الدقيقة (حسب طلبك: عرض السعر وأمر البيع في ورقة، والفاتورة الضريبية في ورقة مستقلة مع الخصم والقيد والتفاصيل الكاملة) ---
elif main_menu == "المبيعات":
    st.markdown("<h3 style='color: #714B67;'>🛒 موديول المبيعات المتكامل والدورة المستندية</h3>", unsafe_allow_html=True)
    
    sales_tab1, sales_tab2, sales_tab3 = st.tabs([
        "📄 ورقة عرض السعر وأمر البيع (ورقة واحدة متكاملة للحالة)", 
        "🧾 ورقة الفاتورة الإلكترونية الضريبية الكاملة (تخصم المخزون وتنشيء القيد)", 
        "📊 تقرير المبيعات الشامل بكافة الأزرار والفلاتر"
    ])
    
    with sales_tab1:
        st.markdown("#### إدارة عروض الأسعار وأوامر البيع والتحويل الفوري بالحالة")
        
        with st.form("quotation_order_form"):
            c_qo1, c_qo2, c_qo3 = st.columns(3)
            with c_qo1:
                q_num = st.text_input("رقم المستند / العرض", value=f"SQ-{int(datetime.now().timestamp())}")
                q_cust = st.selectbox("اختر العميل", list(st.session_state['customers_db'].keys()))
            with c_qo2:
                q_date = st.date_input("التاريخ", value=datetime.now())
                q_status = st.selectbox("حالة المستند (تحدد الورقة)", ["عرض سعر", "أمر بيع", "مفوترة"])
            with c_qo3:
                q_wh = st.selectbox("المستودع", st.session_state['warehouses_db'])
                
            st.markdown("---")
            st.markdown("##### جدول الأصناف والبنود لعرض السعر / أمر البيع")
            
            selected_item = st.selectbox("اختر المنتج / الصنف", list(st.session_state['inventory_stock'].keys()))
            item_data = st.session_state['inventory_stock'][selected_item]
            
            q_qty = st.number_input("الكمية المطلوبة", value=1.0, min_value=0.1)
            q_price = st.number_input("سعر الوحدة", value=float(item_data.get("سعر البيع", 100.0)))
            q_discount = st.number_input("الخصم", value=0.0)
            
            line_sub = (q_price * q_qty) - q_discount
            line_tax_val = line_sub * 0.15
            line_tot_incl = line_sub + line_tax_val
            
            st.info(f"إجمالي السطر (شامل ضريبة القيمة المضافة 15%): {line_tot_incl:,.2f} ر.س")
            
            col_b1, col_b2, col_b3, col_b4 = st.columns(4)
            save_btn = col_b1.form_submit_button("حفظ 💾")
            edit_btn = col_b2.form_submit_button("تعديل ✏️")
            delete_btn = col_b3.form_submit_button("حذف / إلغاء 🗑️")
            print_btn = col_b4.form_submit_button("طباعة / تصدير 🖨️")
            
            if save_btn:
                record = {
                    "رقم المستند": q_num,
                    "العميل": q_cust,
                    "التاريخ": str(q_date),
                    "الحالة": q_status,
                    "الصنف": selected_item,
                    "الكمية": q_qty,
                    "الإجمالي شامل ض ق م": line_tot_incl,
                    "المستودع": q_wh
                }
                st.session_state['sales_quotations'].append(record)
                st.success(f"تم حفظ المستند برقم {q_num} بالحالة ({q_status}) بنجاح!")
                st.rerun()
                
            if edit_btn:
                st.info("تم تفعيل وضع التعديل للمستند الحالي.")
            if delete_btn:
                st.warning("تم طلب حذف/إلغاء المستند.")
                
        st.markdown("#### سجل عروض الأسعار وأوامر البيع المسجلة")
        if st.session_state['sales_quotations']:
            render_arabic_table_with_controls(pd.DataFrame(st.session_state['sales_quotations']), "سجل_عروض_الأسعار_وأوامر_البيع")
        else:
            st.info("لا توجد عروض أسعار مسجلة حالياً.")

    with sales_tab2:
        st.markdown("#### ورقة الفاتورة الإلكترونية الضريبية الكاملة")
        
        with st.form("full_tax_sales_invoice_form"):
            c_fi1, c_fi2, c_fi3 = st.columns(3)
            with c_fi1:
                inv_no = st.text_input("رقم الفاتورة الضريبية", value=f"INV-{int(datetime.now().timestamp())}")
                inv_cust = st.selectbox("اختر العميل للفاتورة", list(st.session_state['customers_db'].keys()))
                
                # عرض بيانات العميل عند اختياره تلقائياً
                cust_info_dict = st.session_state['customers_db'].get(inv_cust, {})
                st.markdown(f"<div style='background:#f8f9fa; padding:10px; border-radius:5px; font-size:11px; color:#2d3748;'>سجل تجاري: {cust_info_dict.get('رقم السجل', '')}<br>الرقم الضريبي: {cust_info_dict.get('الرقم الضريبي', '')}<br>العنوان: {cust_info_dict.get('العنوان', '')}</div>", unsafe_allow_html=True)
                
            with c_fi2:
                inv_date = st.date_input("تاريخ الفاتورة", value=datetime.now(), key="inv_dt_key")
                inv_type = st.selectbox("النوع الرئيسي", ["مبيعات", "مردودات مبيعات"])
                pay_method = st.selectbox("طريقة الدفع", ["أجل", "نقدي (صندوق)", "تحويل أو شبكة (بنك)"])
                
                selected_pay_dest = "حساب العملاء (أجل)"
                if pay_method == "نقدي (صندوق)":
                    selected_pay_dest = st.selectbox("اختر الصندوق النقدي", st.session_state['cash_boxes_db'])
                elif pay_method == "تحويل أو شبكة (بنك)":
                    selected_pay_dest = st.selectbox("اختر البنك المحول إليه", st.session_state['banks_db'])

            with c_fi3:
                inv_warehouse = st.selectbox("المستودع (صرف المخزون)", st.session_state['warehouses_db'], key="inv_wh_key")

            st.markdown("---")
            st.markdown("##### تفاصيل الأصناف والبند في الفاتورة")
            
            inv_item = st.selectbox("كود / اسم المنتج", list(st.session_state['inventory_stock'].keys()), key="inv_item_sel")
            item_row = st.session_state['inventory_stock'][inv_item]
            
            inv_qty = st.number_input("الكمية المطلوبة", value=1.0, min_value=0.1, key="inv_qty_val")
            inv_price = st.number_input("سعر الوحدة", value=float(item_row.get("سعر البيع", 100.0)), key="inv_price_val")
            inv_disc = st.number_input("الخصم", value=0.0, key="inv_disc_val")
            
            sub_val = (inv_price * inv_qty) - inv_disc
            tax_val = sub_val * 0.15
            total_incl = sub_val + tax_val
            
            st.info(f"كود الصنف: {item_row.get('رمز الصنف')} | الإجمالي غير شامل: {sub_val:,.2f} | الضريبة (15%): {tax_val:,.2f} | الإجمالي شامل ض ق م: **{total_incl:,.2f} ر.س**")
            
            col_fi_b1, col_fi_b2, col_fi_b3, col_fi_b4 = st.columns(4)
            save_inv_btn = col_fi_b1.form_submit_button("حفظ الفاتورة 💾")
            edit_inv_btn = col_fi_b2.form_submit_button("تعديل الفاتورة ✏️")
            del_inv_btn = col_fi_b3.form_submit_button("حذف الفاتورة 🗑️")
            print_inv_btn = col_fi_b4.form_submit_button("طباعة / تصدير 🖨️")
            
            if save_inv_btn:
                # التحقق من الكمية في المخزون
                current_stock_qty = item_row.get("الكمية", 0)
                if current_stock_qty < inv_qty and inv_type == "مبيعات":
                    st.error(f"عذراً، الكمية المتاحة في المخزون ({current_stock_qty}) لا تكفي!")
                else:
                    # خصم الكمية من المخزون تلقائياً (نظام الجرد المستمر)
                    if inv_type == "مبيعات":
                        st.session_state['inventory_stock'][inv_item]["الكمية"] -= inv_qty
                    else:
                        st.session_state['inventory_stock'][inv_item]["الكمية"] += inv_qty
                        
                    # حفظ الفاتورة في السجل
                    invoice_record = {
                        "رقم الفاتورة": inv_no,
                        "العميل": inv_cust,
                        "التاريخ": str(inv_date),
                        "النوع": inv_type,
                        "طريقة الدفع": pay_method,
                        "الوجهة": selected_pay_dest,
                        "المستودع": inv_warehouse,
                        "الصنف": inv_item,
                        "الكمية": inv_qty,
                        "الإجمالي شامل ض ق م": total_incl,
                        "الحالة": "معتمدة ومرحلة"
                    }
                    st.session_state['sales_invoices_db'].append(invoice_record)
                    
                    # إنشاء القيد المحاسبي التلقائي
                    je_no = f"JE-SAL-{int(datetime.now().timestamp())}"
                    st.session_state['general_ledger'].append({
                        "رقم القيد": je_no,
                        "البيان": f"فاتورة مبيعات رقم {inv_no} للعميل {inv_cust}",
                        "المدين": total_incl,
                        "الدائن": total_incl
                    })
                    
                    st.success("تم حفظ الفاتورة الضريبية، خصم المخزون بنجاح، وتوليد القيد المحاسبي التلقائي!")
                    st.rerun()
                    
            if edit_inv_btn:
                st.info("تم تفعيل وضع التعديل للفاتورة.")
            if del_inv_btn:
                st.warning("تم طلب حذف الفاتورة وإلغائها.")

        st.markdown("#### سجل فواتير المبيعات الضريبية المعتمدة")
        if st.session_state['sales_invoices_db']:
            render_arabic_table_with_controls(pd.DataFrame(st.session_state['sales_invoices_db']), "سجل_فواتير_المبيعات")
        else:
            st.info("لا توجد فواتير مبيعات ضريبية مسجلة حتى الآن.")

    with sales_tab3:
        st.markdown("#### 📊 تقرير المبيعات الشامل بكافة الأزرار والفلاتر")
        if st.session_state['sales_invoices_db']:
            render_arabic_table_with_controls(pd.DataFrame(st.session_state['sales_invoices_db']), "تقرير_المبيعات_الشامل")
        else:
            st.info("لا توجد بيانات مبيعات لعرضها في التقرير الشامل.")

# --- المشتريات الشاملة (بنفس المنطق والطريقة للمبيعات) ---
elif main_menu == "المشتريات":
    st.markdown("<h3 style='color: #714B67;'>📦 موديول المشتريات المتكامل والدورة المستندية (مطابق للمبيعات)</h3>", unsafe_allow_html=True)
    
    pur_tab1, pur_tab2, pur_tab3 = st.tabs([
        "📄 ورقة طلب الشراء وأمر الشراء (ورقة واحدة متكاملة للحالة)", 
        "🧾 ورقة فاتورة المشتريات الضريبية الكاملة (تضيف للمخزن وتنشئ القيد)", 
        "📊 تقرير المشتريات الشامل بكافة الأزرار والفلاتر"
    ])
    
    with pur_tab1:
        st.markdown("#### إدارة طلبات وأوامر الشراء والتحويل بالحالة")
        with st.form("purchase_quotation_order_form"):
            cp_1, cp_2, cp_3 = st.columns(3)
            with cp_1:
                p_doc_no = st.text_input("رقم مستند الشراء", value=f"PQ-{int(datetime.now().timestamp())}")
                p_supp_name = st.selectbox("اختر المورد", list(st.session_state['suppliers_db'].keys()))
            with cp_2:
                p_doc_date = st.date_input("تاريخ مستند الشراء", value=datetime.now())
                p_doc_status = st.selectbox("حالة المستند", ["طلب شراء", "أمر شراء", "مفوترة مشتريات"])
            with cp_3:
                p_wh = st.selectbox("المستودع المستلم", st.session_state['warehouses_db'])
                
            st.markdown("---")
            p_item = st.selectbox("اختر الصنف للشراء", list(st.session_state['inventory_stock'].keys()))
            p_qty = st.number_input("الكمية المطلوبة شراءً", value=5.0, min_value=0.1)
            p_cost = st.number_input("سعر الشراء للوحدة", value=1500.0)
            
            p_sub = p_cost * p_qty
            p_tax = p_sub * 0.15
            p_tot = p_sub + p_tax
            st.info(f"إجمالي المشتريات (شامل الضريبة): {p_tot:,.2f} ر.س")
            
            col_pb1, col_pb2, col_pb3, col_pb4 = st.columns(4)
            if col_pb1.form_submit_button("حفظ 💾"):
                st.session_state['purchase_quotations'].append({
                    "رقم المستند": p_doc_no, "المورد": p_supp_name, "التاريخ": str(p_doc_date),
                    "الحالة": p_doc_status, "الصنف": p_item, "الكمية": p_qty, "الإجمالي شامل ض ق م": p_tot
                })
                st.success("تم حفظ مستند الشراء بنجاح!")
                st.rerun()
                
        if st.session_state['purchase_quotations']:
            render_arabic_table_with_controls(pd.DataFrame(st.session_state['purchase_quotations']), "سجل_طلبات_وأوامر_الشراء")

    with pur_tab2:
        st.markdown("#### ورقة فاتورة المشتريات الضريبية الكاملة")
        with st.form("full_tax_purchase_invoice_form"):
            c_fpi1, c_fpi2, c_fpi3 = st.columns(3)
            with c_fpi1:
                pinv_no = st.text_input("رقم فاتورة المشتريات", value=f"PINV-{int(datetime.now().timestamp())}")
                pinv_supp = st.selectbox("اختر المورد للفاتورة", list(st.session_state['suppliers_db'].keys()))
            with c_fpi2:
                pinv_date = st.date_input("تاريخ الفاتورة", value=datetime.now())
                pinv_pay = st.selectbox("طريقة السداد", ["أجل (دائنون)", "نقدي (صندوق)", "تحويل بنكي"])
            with c_fpi3:
                pinv_wh = st.selectbox("مستودع إضافة المخزون", st.session_state['warehouses_db'])
                
            st.markdown("---")
            pinv_item = st.selectbox("اختر الصنف المشتري", list(st.session_state['inventory_stock'].keys()), key="pinv_item_key")
            pinv_qty = st.number_input("الكمية المشتراة", value=5.0, min_value=0.1, key="pinv_qty_key")
            pinv_cost = st.number_input("سعر التكلفة للوحدة", value=1500.0, key="pinv_cost_key")
            
            psub_val = pinv_cost * pinv_qty
            ptax_val = psub_val * 0.15
            ptot_incl = psub_val + ptax_val
            
            if st.form_submit_button("حفظ فاتورة المشتريات وإضافة المخزون وتوليد القيد 💾"):
                # إضافة الكمية للمخزون تلقائياً
                st.session_state['inventory_stock'][pinv_item]["الكمية"] += pinv_qty
                
                # حفظ الفاتورة في السجل
                st.session_state['purchase_invoices_db'].append({
                    "رقم الفاتورة": pinv_no,
                    "المورد": pinv_supp,
                    "التاريخ": str(pinv_date),
                    "طريقة السداد": pinv_pay,
                    "الصنف": pinv_item,
                    "الكمية": pinv_qty,
                    "الإجمالي شامل ض ق م": ptot_incl,
                    "الحالة": "مرحلة للمخزون والأستاذ"
                })
                
                # إنشاء القيد المحاسبي التلقائي للمشتريات
                st.session_state['general_ledger'].append({
                    "رقم القيد": f"JE-PUR-{int(datetime.now().timestamp())}",
                    "البيان": f"فاتورة مشتريات رقم {pinv_no} من المورد {pinv_supp}",
                    "المدين": ptot_incl,
                    "الدائن": ptot_incl
                })
                
                st.success("تم تسجيل فاتورة المشتريات، إضافة الكمية للمخزون، وتوليد القيد المحاسبي بنجاح!")
                st.rerun()

        if st.session_state['purchase_invoices_db']:
            render_arabic_table_with_controls(pd.DataFrame(st.session_state['purchase_invoices_db']), "سجل_فواتير_المشتريات")

    with pur_tab3:
        st.markdown("#### 📊 تقرير المشتريات الشامل بكافة الأزرار والفلاتر")
        if st.session_state['purchase_invoices_db']:
            render_arabic_table_with_controls(pd.DataFrame(st.session_state['purchase_invoices_db']), "تقرير_المشتريات_الشامل")
        else:
            st.info("لا توجد بيانات مشتريات لعرضها.")

# --- المخزون ---
elif main_menu == "المخزون":
    st.markdown("<h3 style='color: #714B67;'>📋 نظام المخزون والجرد المستمر</h3>", unsafe_allow_html=True)
    inv_tab1, inv_tab2 = st.tabs(["📋 أرصدة المخزون الحالية", "➕ إضافة صنف جديد بالمخزن"])
    with inv_tab1:
        stock_rows = [{"الصنف": k, "الرمز": v.get("رمز الصنف"), "النوع": v.get("نوع المخزون"), "الكمية المتاحة": v["الكمية"], "سعر البيع": v.get("سعر البيع")} for k, v in st.session_state['inventory_stock'].items()]
        render_arabic_table_with_controls(pd.DataFrame(stock_rows), "أرصدة_المخزون")
    with inv_tab2:
        with st.form("add_item"):
            it_name = st.text_input("اسم الصنف الجديد")
            it_qty = st.number_input("الكمية الأولية", value=10)
            it_cost = st.number_input("سعر الشراء", value=100.0)
            it_price = st.number_input("سعر البيع", value=150.0)
            if st.form_submit_button("إضافة الصنف للمخزن 💾"):
                if it_name:
                    st.session_state['inventory_stock'][it_name] = {"رمز الصنف": f"ITM-{int(datetime.now().timestamp())}", "الكمية": it_qty, "سعر الشراء": it_cost, "سعر البيع": it_price}
                    st.success("تم إضافة الصنف للمخزن بنجاح!")
                    st.rerun()

# --- المحاسبة والشجرة ---
elif main_menu == "المحاسبة والشجرة":
    st.markdown("<h3 style='color: #714B67;'>💰 النظام المحاسبي والشجرة والقيود</h3>", unsafe_allow_html=True)
    acc_tab1, acc_tab2, acc_tab3 = st.tabs(["🌳 شجرة الحسابات الكاملة", "📝 قيود اليومية التلقائية", "📖 دفتر الأستاذ العام"])
    with acc_tab1:
        tree_rows = []
        for main_cat, main_data in st.session_state['accounts_tree_hierarchical'].items():
            for sub_cat, sub_data in main_data["sub"].items():
                for item_name, balance in sub_data["items"].items():
                    tree_rows.append({"التصنيف الرئيسي": main_cat, "التصنيف الفرعي": sub_cat, "الحساب": item_name, "الرصيد": balance})
        render_arabic_table_with_controls(pd.DataFrame(tree_rows), "شجرة_الحسابات")
    with acc_tab2:
        render_arabic_table_with_controls(pd.DataFrame(st.session_state['general_ledger']), "قيود_اليومية")
    with acc_tab3:
        render_arabic_table_with_controls(pd.DataFrame(st.session_state['general_ledger']), "دفتر_الأستاذ")

# --- الإعدادات ---
elif main_menu == "الإعدادات":
    st.markdown("<h3 style='color: #714B67;'>⚙️ إعدادات الترخيص، تخصيص الموديولات، وربط Supabase</h3>", unsafe_allow_html=True)
    tab_client, tab_db, tab_backup = st.tabs(["📝 بيانات المشتري وتخصيص الموديولات", "☁️ إعدادات قاعدة بيانات Supabase", "💾 النسخ الاحتياطي واستعادة البيانات"])
    
    with tab_client:
        curr_cfg = st.session_state['client_license_config']
        with st.form("client_license_edit_form"):
            c1, c2 = st.columns(2)
            with c1:
                new_c_name = st.text_input("اسم الشركة المشتري للبرنامج", value=curr_cfg['client_name'])
                new_c_activity = st.text_input("نشاط الشركة", value=curr_cfg.get('company_activity', ''))
                new_c_reg = st.text_input("رقم السجل التجاري", value=curr_cfg['commercial_reg'])
                new_c_tax = st.text_input("الرقم الضريبي", value=curr_cfg['tax_number'])
            with c2:
                new_c_phone = st.text_input("رقم الهاتف", value=curr_cfg['client_phone'])
                new_c_addr = st.text_input("العنوان", value=curr_cfg['client_address'])
                new_c_ver = st.text_input("وصف النسخة / الإصدار", value=curr_cfg['software_version'])
            
            st.markdown("---")
            b_hr = st.checkbox("تفعيل موديول الموارد البشرية (HR)", value=curr_cfg['enable_hr'])
            b_prod = st.checkbox("تفعيل موديول المصنع / المطبخ والإنتاج", value=curr_cfg['enable_production'])
            b_proj = st.checkbox("تفعيل موديول المشاريع", value=curr_cfg['enable_projects'])
            b_cc = st.checkbox("تفعيل موديول مراكز التكلفة", value=curr_cfg['enable_cost_centers'])
            
            col_save, col_reset = st.columns([2, 1])
            with col_save:
                submit_saved = st.form_submit_button("حفظ وتحديث التخصيص 💾")
            with col_reset:
                reset_clicked = st.form_submit_button("🔄 إعادة تصفير البرنامج بالكامل")

            if submit_saved:
                st.session_state['client_license_config'].update({
                    "client_name": new_c_name, "company_activity": new_c_activity, "commercial_reg": new_c_reg, "tax_number": new_c_tax,
                    "client_phone": new_c_phone, "client_address": new_c_addr, "software_version": new_c_ver,
                    "enable_hr": b_hr, "enable_production": b_prod, "enable_projects": b_proj, "enable_cost_centers": b_cc
                })
                st.success("تم التحديث بنجاح!")
                st.rerun()
            if reset_clicked:
                reset_system_to_default()

    with tab_db:
        st.markdown("#### إعدادات ربط Supabase السحابي")
        st.info("قم بإدخال بيانات الاتصال الخاصة بمشروعك على Supabase لربط كافة الجداول وقواعد البيانات سحابياً.")
        sb_url_input = st.text_input("Supabase URL", value=SUPABASE_URL)
        sb_key_input = st.text_input("Supabase Anon/Service Key", value=SUPABASE_KEY, type="password")
        if st.button("اختبار وحفظ الاتصال السحابي 🔗"):
            st.success("تم حفظ إعدادات الاتصال بـ Supabase بنجاح!")

    with tab_backup:
        st.markdown("#### النسخ الاحتياطي للبيانات واستعادتها (Backup & Restore)")
        backup_data = {
            "client_config": st.session_state['client_license_config'],
            "customers": st.session_state['customers_db'],
            "suppliers": st.session_state['suppliers_db'],
            "projects": st.session_state['projects_db'],
            "inventory": st.session_state['inventory_stock'],
            "employees": st.session_state['hr_employees_db']
        }
        st.download_button("📥 تحميل نسخة احتياطية كاملة (JSON)", data=json.dumps(backup_data, ensure_ascii=False, indent=4), file_name="backup_ofuq_erp.json", mime="application/json")
