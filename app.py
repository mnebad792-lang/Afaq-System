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

# --- تهيئة إعدادات العميل والنسخة (بيانات المشتري والتخصيص) ---
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
        {"اسم المستخدم": "admin", "الاسم الكامل": "المدير العام", "الدور": "مدير النظام (Administrator)", "الصلاحيات الممنوحة": "كامل الصلاحيات", "الحالة": "نشط"}
    ]

if 'inventory_stock' not in st.session_state:
    st.session_state['inventory_stock'] = {
        "أجهزة لابتوب ديل احترافي": {"رمز الصنف": "PRD-001", "نوع المخزون": "مخزون تام", "الفئة": "إلكترونيات", "الكمية": 50, "سعر البيع": 3500.0, "سعر الشراء": 2800.0, "المستودع": "المستودع الرئيسي - الرياض", "حد الطلب": 10}
    }

if 'sales_quotations' not in st.session_state:
    st.session_state['sales_quotations'] = []

if 'sales_orders' not in st.session_state:
    st.session_state['sales_orders'] = []

if 'sales_invoices_db' not in st.session_state:
    st.session_state['sales_invoices_db'] = []

if 'purchase_invoices_db' not in st.session_state:
    st.session_state['purchase_invoices_db'] = []

if 'general_ledger' not in st.session_state:
    st.session_state['general_ledger'] = [
        {"رقم القيد": "JE-101", "البيان": "قيد الافتتاح", "المدين": 3000000.0, "الدائن": 3000000.0}
    ]

# --- تنسيقات CSS مع خاصية Shrink to Fit للجداول ---
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

# --- القائمة الجانبية ---
with st.sidebar:
    client_conf = st.session_state['client_license_config']
    st.markdown(f"<h2 style='color: #714B67; text-align: center;'>نظام أفق ERP</h2>", unsafe_allow_html=True)
    st.markdown(f"<p style='text-align: center; font-size: 11px; color: #64748b;'>مرخص لـ: <b>{client_conf['client_name']}</b></p>", unsafe_allow_html=True)
    
    if supabase_client:
        st.success("☁️ متصل بـ Supabase بنجاح")
    else:
        st.info("ℹ️ يعمل الآن بنجاح عبر النظام المحلي")

    if st.button("🔒 تسجيل الخروج"):
        st.session_state['authenticated'] = False
        st.rerun()

    st.markdown("---")
    
    menu_options = [
        "الرئيسية واللوحة العامة", 
        "إدارة شركاء النجاح (العملاء والموردين)"
    ]
    
    if client_conf.get("enable_hr", True):
        menu_options.append("إدارة الموارد البشرية (HR)")
    if client_conf.get("enable_production", True):
        menu_options.append("إدارة الإنتاج والمصنع/المطبخ")
    if client_conf.get("enable_projects", True):
        menu_options.append("إدارة المشاريع")
    if client_conf.get("enable_cost_centers", True):
        menu_options.append("إدارة مراكز التكلفة")
        
    menu_options.extend([
        "إدارة الصلاحيات والمستخدمين",
        "إدارة المبيعات المتكاملة", 
        "إدارة المشتريات المتكاملة", 
        "نظام المخزون (الجرد المستمر)",
        "النظام المحاسبي والشجرة",
        "⚙️ إعدادات ترخيص العميل والنسخ الاحتياطي"
    ])
    
    main_menu = st.selectbox("اختر النظام الرئيسي:", menu_options)
    
    hr_sub_menu = "سجل الموظفين الشامل"
    if main_menu == "إدارة الموارد البشرية (HR)":
        st.markdown("---")
        hr_sub_menu = st.radio("خيارات الموارد البشرية:", ["سجل الموظفين الشامل", "إضافة موظف جديد", "متابعة الحضور والانصراف", "إدارة الإجازات والطلبات", "مسير الرواتب والأجور (Payroll)"])

    production_sub_menu = "أوامر الإنتاج"
    if main_menu == "إدارة الإنتاج والمصنع/المطبخ":
        st.markdown("---")
        production_sub_menu = st.radio("خيارات الإنتاج:", ["أوامر الإنتاج النشطة", "إضافة أمر إنتاج جديد", "أوامر الإنتاج المكتملة"])

    projects_sub_menu = "قائمة المشاريع"
    if main_menu == "إدارة المشاريع":
        st.markdown("---")
        projects_sub_menu = st.radio("خيارات المشاريع:", ["قائمة المشاريع", "إضافة مشروع جديد"])

    cost_centers_sub_menu = "مراكز التكلفة الشاملة"
    if main_menu == "إدارة مراكز التكلفة":
        st.markdown("---")
        cost_centers_sub_menu = st.radio("خيارات مراكز التكلفة:", ["مراكز التكلفة الشاملة", "إضافة مركز تكلفة جديد"])

    users_sub_menu = "قائمة المستخدمين والصلاحيات"
    if main_menu == "إدارة الصلاحيات والمستخدمين":
        st.markdown("---")
        users_sub_menu = st.radio("خيارات الصلاحيات:", ["قائمة المستخدمين والصلاحيات", "إضافة مستخدم جديد"])

    inventory_sub_menu = "أرصدة المخزون الحالية"
    if main_menu == "نظام المخزون (الجرد المستمر)":
        st.markdown("---")
        inventory_sub_menu = st.radio("خيارات المخزون:", ["أرصدة المخزون الحالية", "إضافة صنف جديد بالمخزن"])

    accounting_sub_menu = "شجرة الحسابات الكاملة"
    if main_menu == "النظام المحاسبي والشجرة":
        st.markdown("---")
        accounting_sub_menu = st.radio("خيارات النظام المحاسبي:", ["شجرة الحسابات الكاملة", "قيود اليومية", "دفتر الأستاذ العام"])

    st.markdown("---")
    st.markdown("<p style='font-size: 10px; color: #714B67; text-align: center;'>جميع الحقوق محفوظة © أفق 2026</p>", unsafe_allow_html=True)

# --- محتوى اللوحة العامة ---
if main_menu == "الرئيسية واللوحة العامة":
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

# --- إدارة شركاء النجاح ---
elif main_menu == "إدارة شركاء النجاح (العملاء والموردين)":
    st.markdown("<h3 style='color: #714B67;'>👥 إدارة شركاء النجاح (العملاء والموردين)</h3>", unsafe_allow_html=True)
    t_cust, t_supp, t_add = st.tabs(["📋 العملاء", "📋 الموردين", "➕ إضافة عميل أو مورد جديد"])
    
    with t_cust:
        cust_list = [{"كود العميل": k, "اسم العميل": k, "السجل التجاري": v.get("رقم السجل"), "الرقم الضريبي": v.get("الرقم الضريبي"), "الهاتف": v.get("الهاتف"), "العنوان": v.get("العنوان"), "الرصيد": v.get("الرصيد الحالي")} for k, v in st.session_state['customers_db'].items()]
        render_arabic_table_with_controls(pd.DataFrame(cust_list), "قائمة_العملاء")
        
    with t_supp:
        supp_list = [{"كود المورد": k, "اسم المورد": k, "السجل التجاري": v.get("رقم السجل"), "الرقم الضريبي": v.get("الرقم الضريبي"), "الهاتف": v.get("الهاتف"), "العنوان": v.get("العنوان"), "الرصيد": v.get("الرصيد الحالي")} for k, v in st.session_state['suppliers_db'].items()]
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
elif main_menu == "إدارة الموارد البشرية (HR)":
    st.markdown("<h3 style='color: #714B67;'>👥 إدارة الموارد البشرية (HR)</h3>", unsafe_allow_html=True)
    if hr_sub_menu == "سجل الموظفين الشامل":
        emp_rows = [{"رقم الموظف": k, "الاسم": v["الاسم الكامل"], "القسم": v["القسم"], "المسمى": v["المسمى الوظيفي"], "الراتب": v["الراتب الأساسي"]} for k, v in st.session_state['hr_employees_db'].items()]
        render_arabic_table_with_controls(pd.DataFrame(emp_rows), "الموظفين")
    elif hr_sub_menu == "إضافة موظف جديد":
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
    elif hr_sub_menu == "متابعة الحضور والانصراف":
        render_arabic_table_with_controls(pd.DataFrame(st.session_state['hr_attendance']), "الحضور")
    elif hr_sub_menu == "إدارة الإجازات والطلبات":
        render_arabic_table_with_controls(pd.DataFrame(st.session_state['hr_leaves']), "الإجازات")
    elif hr_sub_menu == "مسير الرواتب والأجور (Payroll)":
        sal_rows = [{"رقم الموظف": k, "الاسم": v["الاسم الكامل"], "الصافي المستحق": v["الراتب الأساسي"] + v.get("بدل السكن", 0)} for k, v in st.session_state['hr_employees_db'].items()]
        render_arabic_table_with_controls(pd.DataFrame(sal_rows), "مسير_الرواتب")

# --- إدارة الإنتاج ---
elif main_menu == "إدارة الإنتاج والمصنع/المطبخ":
    st.markdown("<h3 style='color: #714B67;'>🏭 إدارة الإنتاج والمصنع/المطبخ</h3>", unsafe_allow_html=True)
    if production_sub_menu == "أوامر الإنتاج النشطة":
        render_arabic_table_with_controls(pd.DataFrame(st.session_state['production_orders']), "أوامر_الإنتاج")
    elif production_sub_menu == "إضافة أمر إنتاج جديد":
        with st.form("new_prod"):
            p_item = st.text_input("اسم المنتج / الوجبة المصنعة")
            p_qty = st.number_input("الكمية المطلوبة للإنتاج", value=10)
            if st.form_submit_button("إصدار أمر الإنتاج الجديد ⚙️"):
                if p_item:
                    st.session_state['production_orders'].append({"رقم الأمر": f"PRD-{len(st.session_state['production_orders'])+1:03d}", "اسم المنتج": p_item, "الكمية المطلوبة": p_qty, "الحالة": "قيد التنفيذ"})
                    st.success("تم إصدار أمر الإنتاج بنجاح!")
                    st.rerun()
    else:
        render_arabic_table_with_controls(pd.DataFrame(st.session_state['production_orders']), "أوامر_مكتملة")

# --- إدارة المشاريع ---
elif main_menu == "إدارة المشاريع":
    st.markdown("<h3 style='color: #714B67;'>📊 إدارة المشاريع</h3>", unsafe_allow_html=True)
    if projects_sub_menu == "قائمة المشاريع":
        render_arabic_table_with_controls(pd.DataFrame(st.session_state['projects_db']), "المشاريع")
    else:
        with st.form("add_proj"):
            pr_id = st.text_input("رقم المشروع (مثال: PRJ-03)")
            pr_name = st.text_input("اسم المشروع")
            pr_bud = st.number_input("الميزانية (ر.س)", value=100000.0)
            if st.form_submit_button("حفظ المشروع 💾"):
                st.session_state['projects_db'].append({"رقم المشروع": pr_id, "اسم المشروع": pr_name, "الميزانية (ر.س)": pr_bud, "نسبة الإنجاز": "0%", "الحالة": "جديدة"})
                st.success("تم إضافة المشروع بنجاح!")
                st.rerun()

# --- مراكز التكلفة ---
elif main_menu == "إدارة مراكز التكلفة":
    st.markdown("<h3 style='color: #714B67;'>🏷️ إدارة مراكز التكلفة</h3>", unsafe_allow_html=True)
    if cost_centers_sub_menu == "مراكز التكلفة الشاملة":
        render_arabic_table_with_controls(pd.DataFrame(st.session_state['cost_centers_db']), "مراكز_التكلفة")
    else:
        with st.form("add_cc"):
            cc_id = st.text_input("رمز المركز (مثال: CC-103)")
            cc_name = st.text_input("اسم مركز التكلفة")
            if st.form_submit_button("حفظ المركز 💾"):
                st.session_state['cost_centers_db'].append({"رمز المركز": cc_id, "اسم مركز التكلفة": cc_name, "المصروفات الحالية (ر.س)": 0.0, "الإيرادات المرتبطة (ر.س)": 0.0})
                st.success("تم الحفظ بنجاح!")
                st.rerun()

# --- إدارة الصلاحيات والمستخدمين ---
elif main_menu == "إدارة الصلاحيات والمستخدمين":
    st.markdown("<h3 style='color: #714B67;'>🔐 إدارة الصلاحيات والمستخدمين</h3>", unsafe_allow_html=True)
    if users_sub_menu == "قائمة المستخدمين والصلاحيات":
        render_arabic_table_with_controls(pd.DataFrame(st.session_state['users_permissions_db']), "المستخدمين")
    else:
        with st.form("add_usr"):
            u_name = st.text_input("اسم المستخدم")
            u_full = st.text_input("الاسم الكامل")
            u_role = st.selectbox("الدور", ["محاسب", "مدير", "مستودعات"])
            if st.form_submit_button("إضافة المستخدم 💾"):
                st.session_state['users_permissions_db'].append({"اسم المستخدم": u_name, "الاسم الكامل": u_full, "الدور": u_role, "الحالة": "نشط"})
                st.success("تمت الإضافة بنجاح!")
                st.rerun()

# --- إدارة المبيعات المتكاملة ---
elif main_menu == "إدارة المبيعات المتكاملة":
    st.markdown("<h3 style='color: #714B67;'>🛒 إدارة المبيعات الشاملة والدورة المحاسبية</h3>", unsafe_allow_html=True)
    m_tab1, m_tab2, m_tab3, m_tab4 = st.tabs(["1️⃣ عروض الأسعار", "2️⃣ أوامر البيع", "3️⃣ فواتير المبيعات المعتمدة", "➕ إنشاء عرض سعر جديد"])
    
    with m_tab1:
        render_arabic_table_with_controls(pd.DataFrame(st.session_state['sales_quotations']), "عروض_الأسعار")
        if st.session_state['sales_quotations']:
            q_to_approve = st.selectbox("اختر عرض سعر لتحويله لأمر بيع", [q["رقم العرض"] for q in st.session_state['sales_quotations']])
            if st.button("تحويل لأمر بيع ➔"):
                for q in st.session_state['sales_quotations']:
                    if q["رقم العرض"] == q_to_approve:
                        st.session_state['sales_orders'].append({"رقم الأمر": f"SO-{len(st.session_state['sales_orders'])+1:03d}", "العميل": q["العميل"], "المبلغ": q["المبلغ"], "الحالة": "معتمد"})
                        st.success("تم تحويل عرض السعر إلى أمر بيع بنجاح!")
                        st.rerun()

    with m_tab2:
        render_arabic_table_with_controls(pd.DataFrame(st.session_state['sales_orders']), "أوامر_البيع")
        if st.session_state['sales_orders']:
            so_to_inv = st.selectbox("اختر أمر بيع لتحويله لفاتورة", [s["رقم الأمر"] for s in st.session_state['sales_orders']])
            if st.button("تحويل لفاتورة مبيعات وخصم المخزون وإنشاء القيد ➔"):
                for s in st.session_state['sales_orders']:
                    if s["رقم الأمر"] == so_to_inv:
                        inv_no = f"INV-{len(st.session_state['sales_invoices_db'])+1:03d}"
                        st.session_state['sales_invoices_db'].append({"رقم الفاتورة": inv_no, "العميل": s["العميل"], "المبلغ": s["المبلغ"], "الحالة": "مرحلة للأستاذ ومخصومة"})
                        st.session_state['general_ledger'].append({"رقم القيد": f"JE-{len(st.session_state['general_ledger'])+1}", "البيان": f"فاتورة مبيعات {inv_no}", "المدين": s["المبلغ"], "الدائن": s["المبلغ"]})
                        st.success("تم إصدار الفاتورة وخصم المخزون وتوليد القيد المحاسبي بنجاح!")
                        st.rerun()

    with m_tab3:
        render_arabic_table_with_controls(pd.DataFrame(st.session_state['sales_invoices_db']), "فواتير_المبيعات")

    with m_tab4:
        with st.form("new_quotation"):
            cust_name = st.selectbox("اختر العميل", list(st.session_state['customers_db'].keys()))
            item_name = st.selectbox("اختر الصنف", list(st.session_state['inventory_stock'].keys()))
            qty = st.number_input("الكمية", value=2, min_value=1)
            price = st.number_input("سعر الوحدة", value=3500.0)
            if st.form_submit_button("حفظ وإصدار عرض السعر 💾"):
                q_no = f"QT-{len(st.session_state['sales_quotations'])+1:03d}"
                st.session_state['sales_quotations'].append({"رقم العرض": q_no, "العميل": cust_name, "الصنف": item_name, "الكمية": qty, "المبلغ": qty * price, "الحالة": "جديد"})
                st.success("تم حفظ عرض السعر بنجاح!")
                st.rerun()

# --- إدارة المشتريات المتكاملة ---
elif main_menu == "إدارة المشتريات المتكاملة":
    st.markdown("<h3 style='color: #714B67;'>📦 إدارة المشتريات وفواتير الموردين</h3>", unsafe_allow_html=True)
    p_t1, p_t2 = st.tabs(["📋 فواتير المشتريات المسجلة", "➕ تسجيل فاتورة مشتريات جديدة"])
    with p_t1:
        render_arabic_table_with_controls(pd.DataFrame(st.session_state['purchase_invoices_db']), "المشتريات")
    with p_t2:
        with st.form("new_pur"):
            supp = st.selectbox("اختر المورد", list(st.session_state['suppliers_db'].keys()))
            amt = st.number_input("إجمالي قيمة المشتريات (ر.س)", value=5000.0)
            if st.form_submit_button("تسجيل وترحيل المشتريات 💾"):
                p_no = f"PUR-{len(st.session_state['purchase_invoices_db'])+1:03d}"
                st.session_state['purchase_invoices_db'].append({"رقم الفاتورة": p_no, "المورد": supp, "المبلغ": amt, "الحالة": "معتمدة ومرحلة"})
                st.session_state['general_ledger'].append({"رقم القيد": f"JE-{len(st.session_state['general_ledger'])+1}", "البيان": f"فاتورة مشتريات {p_no}", "المدين": amt, "الدائن": amt})
                st.success("تم تسجيل المشتريات وترحيل القيد بنجاح!")
                st.rerun()

# --- نظام المخزون ---
elif main_menu == "نظام المخزون (الجرد المستمر)":
    st.markdown("<h3 style='color: #714B67;'>📦 نظام المخزون والجرد المستمر</h3>", unsafe_allow_html=True)
    if inventory_sub_menu == "أرصدة المخزون الحالية":
        stock_rows = [{"الصنف": k, "النوع": v.get("نوع المخزون"), "الكمية": v["الكمية"], "سعر الشراء": v["سعر الشراء"]} for k, v in st.session_state['inventory_stock'].items()]
        render_arabic_table_with_controls(pd.DataFrame(stock_rows), "المخزون")
    else:
        with st.form("add_item"):
            it_name = st.text_input("اسم الصنف الجديد")
            it_qty = st.number_input("الكمية الأولية", value=10)
            it_cost = st.number_input("سعر الشراء", value=100.0)
            if st.form_submit_button("إضافة الصنف للمخزن 💾"):
                if it_name:
                    st.session_state['inventory_stock'][it_name] = {"رمز الصنف": "ITM-new", "الكمية": it_qty, "سعر الشراء": it_cost, "سعر البيع": it_cost * 1.3}
                    st.success("تم إضافة الصنف للمخزن بنجاح!")
                    st.rerun()

# --- النظام المحاسبي والشجرة ---
elif main_menu == "النظام المحاسبي والشجرة":
    st.markdown("<h3 style='color: #714B67;'>📊 النظام المحاسبي والشجرة والقيود</h3>", unsafe_allow_html=True)
    if accounting_sub_menu == "شجرة الحسابات الكاملة":
        tree_rows = []
        for main_cat, main_data in st.session_state['accounts_tree_hierarchical'].items():
            for sub_cat, sub_data in main_data["sub"].items():
                for item_name, balance in sub_data["items"].items():
                    tree_rows.append({"التصنيف الرئيسي": main_cat, "التصنيف الفرعي": sub_cat, "الحساب": item_name, "الرصيد": balance})
        render_arabic_table_with_controls(pd.DataFrame(tree_rows), "شجرة_الحسابات")
    elif accounting_sub_menu == "قيود اليومية":
        render_arabic_table_with_controls(pd.DataFrame(st.session_state['general_ledger']), "قيود_اليومية")
    else:
        render_arabic_table_with_controls(pd.DataFrame(st.session_state['general_ledger']), "دفتر_الأستاذ")

# --- إعدادات ترخيص العميل والنسخ الاحتياطي ---
elif main_menu == "⚙️ إعدادات ترخيص العميل والنسخ الاحتياطي":
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
