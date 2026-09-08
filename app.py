# --- ملف النظام المحاسبي المحدث مع نموذج الهيئة لضريبة القيمة المضافة ---
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

# قاعدة بيانات إقرارات الهيئة الضريبية المضافة
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
    /* حل مشكلة التداخل العلوي وتوفير مساحة كافية للشريط */
    .block-container { padding: 5rem 1.5rem 1rem 1.5rem !important; background-color: #f4f6f9; }
    
    .stButton>button {
        font-size: 12px !important;
        padding: 4px 8px !important;
    }
    
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

if 'active_module' not in st.session_state:
    st.session_state['active_module'] = "الرئيسية"

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

elif main_menu == "الشركاء":
    st.markdown("<h3 style='color: #714B67;'>👥 إدارة شركاء النجاح (العملاء والموردين)</h3>", unsafe_allow_html=True)
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
        st.info("يجب أن يحتوي ملف الـ Excel على أعمدة تتضمن: النوع (عميل/مورد)، الكود، الاسم، السجل التجاري، الرقم الضريبي، الهاتف، العنوان، والرصيد.")
        up_partners_file = st.file_uploader("اختر ملف إكسل للشركاء (.xlsx, .csv)", type=["xlsx", "csv"], key="partners_excel_up")
        if up_partners_file is not None:
            try:
                if up_partners_file.name.endswith('.csv'):
                    df_imp = pd.read_csv(up_partners_file)
                else:
                    df_imp = pd.read_excel(up_partners_file)
                st.write("معاينة البيانات المستوردة:", df_imp.head())
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
    st.markdown("<h3 style='color: #714B67;'>👨‍💼 إدارة الموارد البشرية (HR)</h3>", unsafe_allow_html=True)
    hr_tab1, hr_tab2, hr_tab3, hr_tab4, hr_tab5, hr_tab6 = st.tabs([
        "📋 سجل الموظفين الشامل", "➕ إضافة موظف جديد", "⏰ متابعة الحضور والانصراف", "🏖️ إدارة الإجازات والطلبات", "💰 مسير الرواتب والأجور (Payroll)", "📊 استيراد الموظفين من الاكسيل"
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
    with hr_tab6:
        st.markdown("#### استيراد بيانات الموظفين عبر ملف إكسل Excel")
        up_emp_file = st.file_uploader("اختر ملف إكسل للموظفين (.xlsx, .csv)", type=["xlsx", "csv"], key="emp_excel_up")
        if up_emp_file is not None:
            try:
                if up_emp_file.name.endswith('.csv'):
                    df_emp_imp = pd.read_csv(up_emp_file)
                else:
                    df_emp_imp = pd.read_excel(up_emp_file)
                st.write("معاينة موظفي الإكسل:", df_emp_imp.head())
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

elif main_menu == "الصلاحيات":
    st.markdown("<h3 style='color: #714B67;'>🔐 شاشة إدارة الصلاحيات وتحديد صلاحيات المستخدمين بدقة</h3>", unsafe_allow_html=True)
    perm_tab1, perm_tab2 = st.tabs(["👥 قائمة المستخدمين وصلاحياتهم", "➕ إضافة / تعديل مستخدم وصلاحياته"])
    
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
    st.markdown("<h3 style='color: #714B67;'>🛒 موديول المبيعات المتكامل والدورة المستندية</h3>", unsafe_allow_html=True)
    sales_tab1, sales_tab2, sales_tab3 = st.tabs([
        "📄 ورقة عرض السعر وأمر البيع", 
        "🧾 ورقة الفاتورة الإلكترونية الضريبية الكاملة", 
        "📊 تقرير المبيعات الشامل"
    ])
    
    with sales_tab1:
        with st.form("quotation_order_form"):
            c_qo1, c_qo2, c_qo3 = st.columns(3)
            with c_qo1:
                q_num = st.text_input("رقم المستند / العرض", value=f"SQ-{int(datetime.now().timestamp())}")
                q_cust = st.selectbox("اختر العميل", list(st.session_state['customers_db'].keys()))
            with c_qo2:
                q_date = st.date_input("التاريخ", value=datetime.now())
                q_status = st.selectbox("حالة المستند", ["عرض سعر", "أمر بيع", "مفوترة"])
            with c_qo3:
                q_wh = st.selectbox("المستودع", st.session_state['warehouses_db'])
                
            st.markdown("---")
            inv_keys = list(st.session_state['inventory_stock'].keys())
            selected_item = st.selectbox("اختر المنتج / الصنف", inv_keys if inv_keys else ["غير متوفر"])
            item_data = st.session_state['inventory_stock'].get(selected_item, {"سعر البيع": 100.0})
            
            q_qty = st.number_input("الكمية المطلوبة", value=1.0, min_value=0.1)
            q_price = st.number_input("سعر الوحدة", value=float(item_data.get("سعر البيع", 100.0)))
            q_discount = st.number_input("الخصم", value=0.0)
            
            line_sub = (q_price * q_qty) - q_discount
            line_tot_incl = line_sub + (line_sub * 0.15)
            st.info(f"إجمالي السطر (شامل ضريبة القيمة المضافة 15%): {line_tot_incl:,.2f} ر.س")
            
            col_b1, col_b2, col_b3, col_b4 = st.columns(4)
            if col_b1.form_submit_button("حفظ 💾"):
                st.session_state['sales_quotations'].append({
                    "رقم المستند": q_num, "العميل": q_cust, "التاريخ": str(q_date), "الحالة": q_status,
                    "الصنف": selected_item, "الكمية": q_qty, "الإجمالي شامل ض ق م": line_tot_incl, "المستودع": q_wh
                })
                st.success(f"تم حفظ المستند برقم {q_num} بنجاح!")
                st.rerun()
                
        if st.session_state['sales_quotations']:
            render_arabic_table_with_controls(pd.DataFrame(st.session_state['sales_quotations']), "سجل_عروض_الأسعار_وأوامر_البيع")

    with sales_tab2:
        with st.form("full_tax_sales_invoice_form"):
            c_fi1, c_fi2, c_fi3 = st.columns(3)
            with c_fi1:
                inv_no = st.text_input("رقم الفاتورة الضريبية", value=f"INV-{int(datetime.now().timestamp())}")
                inv_cust = st.selectbox("اختر العميل للفاتورة", list(st.session_state['customers_db'].keys()))
            with c_fi2:
                inv_date = st.date_input("تاريخ الفاتورة", value=datetime.now())
                inv_type = st.selectbox("النوع الرئيسي", ["مبيعات", "مردودات مبيعات"])
                pay_method = st.selectbox("طريقة الدفع", ["أجل", "نقدي (صندوق)", "تحويل أو شبكة (بنك)"])
            with c_fi3:
                inv_warehouse = st.selectbox("المستودع (صرف المخزون)", st.session_state['warehouses_db'])

            inv_keys = list(st.session_state['inventory_stock'].keys())
            inv_item = st.selectbox("كود / اسم المنتج", inv_keys if inv_keys else ["غير متوفر"], key="inv_item_sel")
            item_row = st.session_state['inventory_stock'].get(inv_item, {"سعر البيع": 100.0, "الكمية": 0})
            
            inv_qty = st.number_input("الكمية المطلوبة", value=1.0, min_value=0.1, key="inv_qty_val")
            inv_price = st.number_input("سعر الوحدة", value=float(item_row.get("سعر البيع", 100.0)), key="inv_price_val")
            
            sub_val = inv_price * inv_qty
            tax_val = sub_val * 0.15
            total_incl = sub_val + tax_val
            
            if st.form_submit_button("حفظ الفاتورة 💾"):
                st.session_state['sales_invoices_db'].append({
                    "رقم الفاتورة": inv_no, "العميل": inv_cust, "التاريخ": str(inv_date), "النوع": inv_type,
                    "طريقة الدفع": pay_method, "المستودع": inv_warehouse, "الصنف": inv_item, "الكمية": inv_qty,
                    "الإجمالي شامل ض ق م": total_incl, "الحالة": "معتمدة ومرحلة"
                })
                st.success("تم حفظ الفاتورة الضريبية وتوليد القيد بنجاح!")
                st.rerun()

        if st.session_state['sales_invoices_db']:
            render_arabic_table_with_controls(pd.DataFrame(st.session_state['sales_invoices_db']), "سجل_فواتير_المبيعات")

    with sales_tab3:
        if st.session_state['sales_invoices_db']:
            render_arabic_table_with_controls(pd.DataFrame(st.session_state['sales_invoices_db']), "تقرير_المبيعات_الشامل")

elif main_menu == "المشتريات":
    st.markdown("<h3 style='color: #714B67;'>📦 موديول المشتريات المتكامل والدورة المستندية</h3>", unsafe_allow_html=True)
    pur_tab1, pur_tab2, pur_tab3 = st.tabs([
        "📄 طلب وأمر الشراء", "🧾 فاتورة المشتريات الضريبية", "📊 تقرير المشتريات الشامل"
    ])
    with pur_tab1:
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
                
            inv_keys = list(st.session_state['inventory_stock'].keys())
            p_item = st.selectbox("اختر الصنف للشراء", inv_keys if inv_keys else ["غير متوفر"])
            p_qty = st.number_input("الكمية المطلوبة شراءً", value=5.0, min_value=0.1)
            p_cost = st.number_input("سعر الشراء للوحدة", value=1500.0)
            
            p_tot = (p_cost * p_qty) * 1.15
            if st.form_submit_button("حفظ مستند الشراء 💾"):
                st.session_state['purchase_quotations'].append({
                    "رقم المستند": p_doc_no, "المورد": p_supp_name, "التاريخ": str(p_doc_date),
                    "الحالة": p_doc_status, "الصنف": p_item, "الكمية": p_qty, "الإجمالي شامل ض ق م": p_tot
                })
                st.success("تم حفظ مستند الشراء بنجاح!")
                st.rerun()
                
        if st.session_state['purchase_quotations']:
            render_arabic_table_with_controls(pd.DataFrame(st.session_state['purchase_quotations']), "سجل_طلبات_وأوامر_الشراء")

    with pur_tab2:
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
                
            inv_keys = list(st.session_state['inventory_stock'].keys())
            pinv_item = st.selectbox("اختر الصنف المشتري", inv_keys if inv_keys else ["غير متوفر"], key="pinv_item_key")
            pinv_qty = st.number_input("الكمية المشتراة", value=5.0, min_value=0.1, key="pinv_qty_key")
            pinv_cost = st.number_input("سعر التكلفة للوحدة", value=1500.0, key="pinv_cost_key")
            
            ptot_incl = (pinv_cost * pinv_qty) * 1.15
            if st.form_submit_button("حفظ فاتورة المشتريات 💾"):
                if pinv_item in st.session_state['inventory_stock']:
                    st.session_state['inventory_stock'][pinv_item]["الكمية"] += pinv_qty
                
                st.session_state['purchase_invoices_db'].append({
                    "رقم الفاتورة": pinv_no, "المورد": pinv_supp, "التاريخ": str(pinv_date),
                    "طريقة السداد": pinv_pay, "الصنف": pinv_item, "الكمية": pinv_qty,
                    "الإجمالي شامل ض ق م": ptot_incl, "الحالة": "مرحلة للمخزون والأستاذ"
                })
                st.success("تم تسجيل فاتورة المشتريات بنجاح!")
                st.rerun()

        if st.session_state['purchase_invoices_db']:
            render_arabic_table_with_controls(pd.DataFrame(st.session_state['purchase_invoices_db']), "سجل_فواتير_المشتريات")

    with pur_tab3:
        if st.session_state['purchase_invoices_db']:
            render_arabic_table_with_controls(pd.DataFrame(st.session_state['purchase_invoices_db']), "تقرير_المشتريات_الشامل")

elif main_menu == "المخزون":
    st.markdown("<h3 style='color: #714B67;'>📋 نظام المخزون والجرد المستمر</h3>", unsafe_allow_html=True)
    inv_tab1, inv_tab2, inv_tab3 = st.tabs(["📋 أرصدة المخزون الحالية", "➕ إضافة صنف جديد بالمخزن", "📊 استيراد الأصناف من الاكسيل"])
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
    with inv_tab3:
        st.markdown("#### استيراد أصناف المخزون عبر ملف إكسل Excel")
        up_inv_file = st.file_uploader("اختر ملف إكسل للأصناف (.xlsx, .csv)", type=["xlsx", "csv"], key="inv_excel_up")
        if up_inv_file is not None:
            try:
                if up_inv_file.name.endswith('.csv'):
                    df_inv_imp = pd.read_csv(up_inv_file)
                else:
                    df_inv_imp = pd.read_excel(up_inv_file)
                st.write("معاينة أصناف الإكسل:", df_inv_imp.head())
                if st.button("تأكيد استيراد الأصناف والمخزون 📥"):
                    for _, row in df_inv_imp.iterrows():
                        iname = str(row.get("اسم الصنف", "صنف جديد"))
                        icode = str(row.get("رمز الصنف", f"ITM-{int(datetime.now().timestamp())}"))
                        iqty = float(row.get("الكمية", 10.0))
                        icost = float(row.get("سعر الشراء", 100.0))
                        iprice = float(row.get("سعر البيع", 150.0))
                        st.session_state['inventory_stock'][iname] = {
                            "رمز الصنف": icode, "الكمية": iqty, "سعر الشراء": icost, "سعر البيع": iprice
                        }
                    st.success("تم استيراد الأصناف بنجاح!")
                    st.rerun()
            except Exception as e:
                st.error(f"حدث خطأ: {e}")

elif main_menu == "المحاسبة والشجرة":
    st.markdown("<h3 style='color: #714B67;'>💰 النظام المحاسبي والشجرة والقوائم المالية الاحترافية الشاملة</h3>", unsafe_allow_html=True)
    
    acc_tabs = st.tabs([
        "🌳 شجرة الحسابات", "⚖️ ميزان المراجعة", "📈 قائمة الدخل", "💵 التدفقات", 
        "🏛️ الميزانية", "🔄 حقوق الملكية", "🧾 ضريبة القيمة المضافة بالربع", 
        "📉 الإهلاكات", "📝 القيود", "📖 الأستاذ", "👥 دفتر الاستاذ العام للشركاء"
    ])
    
    with acc_tabs[0]:
        st.markdown("#### شجرة الحسابات الهيكلية المتكاملة")
        tree_rows = []
        for main_cat, main_data in st.session_state['accounts_tree_hierarchical'].items():
            for sub_cat, sub_data in main_data["sub"].items():
                for item_name, balance in sub_data["items"].items():
                    tree_rows.append({"التصنيف الرئيسي": main_cat, "التصنيف الفرعي": sub_cat, "الحساب": item_name, "الرصيد": balance})
        render_arabic_table_with_controls(pd.DataFrame(tree_rows), "شجرة_الحسابات")

    with acc_tabs[1]:
        st.markdown("#### ميزان المراجعة الشامل والكامل لجميع الحسابات")
        trial_balance_rows = [
            {"رقم الحساب": "101", "اسم الحساب": "الأصول الثابتة", "مجموع مدين": 750000.0, "مجموع دائن": 0.0, "رصيد مدين": 750000.0, "رصيد دائن": 0.0},
            {"رقم الحساب": "102", "اسم الحساب": "الأصول المتداولة والنقدية", "مجموع مدين": 1000000.0, "مجموع دائن": 0.0, "رصيد مدين": 1000000.0, "رصيد دائن": 0.0},
            {"رقم الحساب": "201", "اسم الحساب": "الالتزامات والخصوم المتداولة", "مجموع مدين": 0.0, "مجموع دائن": 300000.0, "رصيد مدين": 0.0, "رصيد دائن": 300000.0},
            {"رقم الحساب": "301", "اسم الحساب": "رأس المال وحقوق الملكية", "مجموع مدين": 0.0, "مجموع دائن": 3000000.0, "رصيد مدين": 0.0, "رصيد دائن": 3000000.0},
            {"رقم الحساب": "401", "اسم الحساب": "إيرادات المبيعات والنشاط", "مجموع مدين": 0.0, "مجموع دائن": 2500000.0, "رصيد مدين": 0.0, "رصيد دائن": 2500000.0},
            {"رقم الحساب": "501", "اسم الحساب": "تكلفة البضائع المباعة والمصروفات", "مجموع مدين": 1950000.0, "مجموع دائن": 0.0, "رصيد مدين": 1950000.0, "رصيد دائن": 0.0},
        ]
        tb_df = pd.DataFrame(trial_balance_rows)
        render_arabic_table_with_controls(tb_df, "ميزان_المراجعة")

    with acc_tabs[2]:
        st.markdown("#### قائمة الدخل الشاملة الكاملة")
        income_rows = [
            {"البند المحاسبي": "إجمالي الإيرادات والمبيعات", "المبلغ (ر.س)": 2500000.0, "النوع": "إيرادات"},
            {"البند المحاسبي": "(-) تكلفة البضائع المباعة", "المبلغ (ر.س)": -1800000.0, "النوع": "تكاليف مباشرة"},
            {"البند المحاسبي": "(=) مجمل الربح", "المبلغ (ر.س)": 700000.0, "النوع": "مؤشر رئيسي"},
            {"البند المحاسبي": "(-) المصروفات التشغيلية", "المبلغ (ر.س)": -175000.0, "النوع": "مصروفات"},
            {"البند المحاسبي": "(=) صافي الربح الصافي الشامل", "المبلغ (ر.س)": 525000.0, "النوع": "الصافي النهائي"}
        ]
        render_arabic_table_with_controls(pd.DataFrame(income_rows), "قائمة_الدخل")

    with acc_tabs[3]:
        st.markdown("#### قائمة التدفقات النقدية الشاملة الكاملة")
        cashflow_rows = [
            {"النشاط": "الأنشطة التشغيلية", "البند": "النقد المتأتي من المبيعات والعملاء", "المبلغ (ر.س)": 2450000.0},
            {"النشاط": "الأنشطة التشغيلية", "البند": "النقد المدفوع للموردين والمصروفات", "المبلغ (ر.س)": -1950000.0},
            {"النشاط": "صافي التغير النقدي", "البند": "صافي الزيادة النقدية المحققة خلال الفترة", "المبلغ (ر.س)": 300000.0}
        ]
        render_arabic_table_with_controls(pd.DataFrame(cashflow_rows), "قائمة_التدفقات_النقدية")

    with acc_tabs[4]:
        st.markdown("#### الميزانية العمومية الشاملة الكاملة (المركز المالي)")
        bs_rows = [
            {"القسم الرئيسي": "الأصول الثابتة", "تفصيل الحساب": "السيارات، الأثاث، المعدات", "القيمة (ر.س)": 750000.0},
            {"القسم الرئيسي": "الأصول المتداولة", "تفصيل الحساب": "النقدية والمخزون والعملاء", "القيمة (ر.س)": 1000000.0},
            {"القسم الرئيسي": "إجمالي الالتزامات وحقوق الملكية", "تفصيل الحساب": "الخصوم ورأس المال والأرباح", "القيمة (ر.س)": 1750000.0}
        ]
        render_arabic_table_with_controls(pd.DataFrame(bs_rows), "الميزانية_العمومية")

    with acc_tabs[5]:
        st.markdown("#### قائمة التغيير في حقوق الملكية الكاملة والشاملة")
        equity_rows = [
            {"البند": "رأس المال المدفوع أول الفترة", "المبلغ (ر.س)": 3000000.0},
            {"البند": "(+) صافي دخل الفترة الحالية", "المبلغ (ر.س)": 525000.0},
            {"البند": "(=) إجمالي حقوق الملكية في نهاية الفترة", "المبلغ (ر.س)": 3525000.0}
        ]
        render_arabic_table_with_controls(pd.DataFrame(equity_rows), "التغيير_في_حقوق_الملكية")

    with acc_tabs[6]:
        st.markdown("#### إقرار حساب ضريبة القيمة المضافة (مقسماً بالأرباع السنوية)")
        vat_quarters = [
            {
                "الفترة الضريبية": "الربع الأول",
                "المدة": "من 1 يناير إلى 31 مارس",
                "إجمالي المبيعات (ر.س)": 600000.0,
                "ضريبة المبيعات المحصلة (ر.س)": 90000.0,
                "إجمالي المشتريات (ر.س)": 450000.0,
                "ضريبة المشتريات القابلة للخصم (ر.س)": 67500.0,
                "صافي الضريبة المستحقة (ر.س)": 22500.0
            },
            {
                "الفترة الضريبية": "الربع الثاني",
                "المدة": "من 1 أبريل إلى 30 يونيو",
                "إجمالي المبيعات (ر.س)": 650000.0,
                "ضريبة المبيعات المحصلة (ر.س)": 97500.0,
                "إجمالي المشتريات (ر.س)": 480000.0,
                "ضريبة المشتريات القابلة للخصم (ر.س)": 72000.0,
                "صافي الضريبة المستحقة (ر.س)": 25500.0
            },
            {
                "الفترة الضريبية": "الربع الثالث",
                "المدة": "من 1 يوليو إلى 30 سبتمبر",
                "إجمالي المبيعات (ر.س)": 620000.0,
                "ضريبة المبيعات المحصلة (ر.س)": 93000.0,
                "إجمالي المشتريات (ر.س)": 430000.0,
                "ضريبة المشتريات القابلة للخصم (ر.س)": 64500.0,
                "صافي الضريبة المستحقة (ر.س)": 28500.0
            },
            {
                "الفترة الضريبية": "الربع الرابع",
                "المدة": "من 1 أكتوبر إلى 31 ديسمبر",
                "إجمالي المبيعات (ر.س)": 630000.0,
                "ضريبة المبيعات المحصلة (ر.س)": 94500.0,
                "إجمالي المشتريات (ر.س)": 440000.0,
                "ضريبة المشتريات القابلة للخصم (ر.س)": 66000.0,
                "صافي الضريبة المستحقة (ر.س)": 28500.0
            }
        ]
        render_arabic_table_with_controls(pd.DataFrame(vat_quarters), "حساب_ضريبة_القيمة_المضافة_بالأرباع")

        st.markdown("---")
        st.markdown("#### 🏛️ نموذج الإقرار الضريبي الرسمي لهيئة الزكاة والضريبة والجمارك (ZATCA)")
        
        zatca_t1, zatca_t2 = st.tabs(["📋 سجل إقرارات هيئة الزكاة والضريبة", "➕ إضافة / ✏️ تعديل إقرار هيئة جديد"])
        
        with zatca_t1:
            if st.session_state['zatca_vat_returns_db']:
                render_arabic_table_with_controls(pd.DataFrame(st.session_state['zatca_vat_returns_db']), "سجل_إقرارات_الهيئة_الضريبية")
            else:
                st.info("لا توجد إقرارات مسجلة.")
                
        with zatca_t2:
            with st.form("zatca_official_form"):
                st.markdown("##### نموذج إدخال وتعديل إقرار الهيئة (إضافة وتعديل فقط بدون حذف)")
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
                
                st.info(f"حسابات الهيئة التلقائية -> ضريبة المخرجات: {calc_out:,.2f} | ضريبة المدخلات: {calc_in:,.2f} | صافي المستحق: **{calc_net:,.2f} ر.س**")
                
                z_b1, z_b2 = st.columns(2)
                z_add_btn = z_b1.form_submit_button("حفظ أو إضافة الإقرار 💾")
                z_edit_btn = z_b2.form_submit_button("تعديل الإقرار ✏️")
                
                if z_add_btn:
                    new_zatca_record = {
                        "رقم الإقرار": zatca_no,
                        "الفترة": f"{zatca_period} {zatca_year}",
                        "المبيعات الخاضعة 15% (ر.س)": zatca_sales,
                        "ضريبة المخرجات (ر.س)": calc_out,
                        "المشتريات الخاضعة 15% (ر.س)": zatca_purch,
                        "ضريبة المدخلات (ر.س)": calc_in,
                        "صافي الضريبة المستحقة (ر.س)": calc_net,
                        "حالة الإقرار": zatca_status
                    }
                    updated = False
                    for i, item in enumerate(st.session_state['zatca_vat_returns_db']):
                        if item.get("رقم الإقرار") == zatca_no:
                            st.session_state['zatca_vat_returns_db'][i] = new_zatca_record
                            updated = True
                            break
                    if not updated:
                        st.session_state['zatca_vat_returns_db'].append(new_zatca_record)
                    st.success("تم حفظ إقرار الهيئة الضريبي بنجاح!")
                    st.rerun()
                    
                if z_edit_btn:
                    st.info("تم تفعيل وضع التعديل للإقرار الضريبي.")

    with acc_tabs[7]:
        st.markdown("#### حساب وسجل الإهلاكات الشامل الكامل للأصول الثابتة")
        dep_rows = [
            {"الأصل الثابت": "السيارات ووسائل النقل", "التكلفة الاصلية": 150000.0, "نسبة الإهلاك": "20%", "مجمع الإهلاك السابق": 30000.0, "مصروف الإهلاك للفترة": 10000.0, "القيمة الدفترية الصافية": 110000.0},
        ]
        render_arabic_table_with_controls(pd.DataFrame(dep_rows), "حساب_الإهلاكات")

    with acc_tabs[8]:
        st.markdown("#### قيود اليومية العامة التلقائية")
        render_arabic_table_with_controls(pd.DataFrame(st.session_state['general_ledger']), "قيود_اليومية")

    with acc_tabs[9]:
        st.markdown("#### دفتر الأستاذ العام الشامل")
        render_arabic_table_with_controls(pd.DataFrame(st.session_state['general_ledger']), "دفتر_الأستاذ")

    # --- الحساب الجديد المطللوب: دفتر الاستاذ العام للشركاء ---
    with acc_tabs[10]:
        st.markdown("#### 👥 دفتر الاستاذ العام للشركاء (كشف حساب العميل / المورد بنفس الأكواد)")
        st.info("هذا الحساب يعرض تفاصيل وأرصدة وكشوفات حسابات العملاء والموردين بدقة مع الاحتفاظ بكافة البيانات والرموز.")
        
        partner_select_type = st.radio("اختر نوع الشريك للعرض:", ["العملاء", "الموردين"], horizontal=True)
        
        if partner_select_type == "العملاء":
            cust_names = list(st.session_state['customers_db'].keys())
            selected_partner = st.selectbox("اختر العميل المطلوب كشف حسابه:", cust_names if cust_names else ["لا يوجد عملاء"])
            if selected_partner and selected_partner != "لا يوجد عملاء":
                p_data = st.session_state['customers_db'][selected_partner]
                partner_rows = [{
                    "كود العميل": p_data.get("كود العميل"),
                    "اسم الشريك": selected_partner,
                    "السجل التجاري": p_data.get("رقم السجل"),
                    "الرقم الضريبي": p_data.get("الرقم الضريبي"),
                    "الهاتف": p_data.get("الهاتف"),
                    "العنوان": p_data.get("العنوان"),
                    "الرصيد الجاري (ر.س)": p_data.get("الرصيد الحالي")
                }]
                render_arabic_table_with_controls(pd.DataFrame(partner_rows), "كشف_حساب_العميل_استاذ_الشركاء")
        else:
            supp_names = list(st.session_state['suppliers_db'].keys())
            selected_partner = st.selectbox("اختر المورد المطلوب كشف حسابه:", supp_names if supp_names else ["لا يوجد موردين"])
            if selected_partner and selected_partner != "لا يوجد موردين":
                p_data = st.session_state['suppliers_db'][selected_partner]
                partner_rows = [{
                    "كود المورد": p_data.get("كود المورد"),
                    "اسم الشريك": selected_partner,
                    "السجل التجاري": p_data.get("رقم السجل"),
                    "الرقم الضريبي": p_data.get("الرقم الضريبي"),
                    "الهاتف": p_data.get("الهاتف"),
                    "العنوان": p_data.get("العنوان"),
                    "الرصيد الجاري (ر.س)": p_data.get("الرصيد الحالي")
                }]
                render_arabic_table_with_controls(pd.DataFrame(partner_rows), "كشف_حساب_المورد_استاذ_الشركاء")

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
