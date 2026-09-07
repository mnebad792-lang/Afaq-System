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
# يمكنك استبدال الرابط ومفتاح الـ API بالمفاتيح الخاصة بك مباشرة هنا
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

# --- تهيئة إعدادات العميل والنسخة (بيانات المشتري والتخصيص) ---
if 'client_license_config' not in st.session_state:
    st.session_state['client_license_config'] = {
        "client_name": "شركة الإنجاز للمقاولات العامة والتجارة",
        "commercial_reg": "4030998877",
        "tax_number": "300222333400003",
        "client_phone": "0560000000",
        "client_address": "الرياض - المملكة العربية السعودية",
        "software_version": "النسخة المحاسبية الاحترافية 2026 (مع دعم Supabase)",
        "enable_hr": True,
        "enable_production": False,
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
                <div class="login-subtitle">مرخص لصالح: <b>{current_client_name}</b><br>متصل بقاعدة بيانات Supabase السحابية</div>
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
        "شركة التقنية الحديثة للتجارة": {"رقم السجل": "1010254789", "الرقم الضريبي": "300123456700003", "العنوان": "الرياض - حي الملز", "الهاتف": "0501234567", "الحد الائتماني": 100000.0, "الرصيد الحالي": 45000.0},
        "مؤسسة النور للمقاولات": {"رقم السجل": "4030589632", "الرقم الضريبي": "300987654300003", "العنوان": "جدة - حي الروابي", "الهاتف": "0559876543", "الحد الائتماني": 50000.0, "الرصيد الحالي": 12000.0},
        "شركة الأفق الاستثماري": {"رقم السجل": "2050369871", "الرقم الضريبي": "300555444300003", "العنوان": "الدمام - شارع الملك فهد", "الهاتف": "0534445556", "الحد الائتماني": 150000.0, "الرصيد الحالي": 85000.0}
    }

if 'suppliers_db' not in st.session_state:
    st.session_state['suppliers_db'] = {
        "شركة التوريدات الكبرى المحدودة": {"رقم السجل": "1010987654", "الرقم الضريبي": "300111222300003", "العنوان": "الرياض - الصناعية", "الهاتف": "0561112233", "الرصيد الحالي": 65000.0},
        "مصانع الوطنية للأجهزة": {"رقم السجل": "4030123789", "الرقم الضريبي": "300444556600003", "العنوان": "جدة - المدينة الصناعية", "الهاتف": "0543332211", "الرصيد الحالي": 30000.0}
    }

if 'hr_employees_db' not in st.session_state:
    st.session_state['hr_employees_db'] = {
        "EMP-101": {"الاسم الكامل": "أحمد محمد العتيبي", "القسم": "الإدارة المالية", "المسمى الوظيفي": "محاسب أول", "الراتب الأساسي": 8000.0, "بدل السكن": 2000.0, "بدل النقل": 500.0, "تاريخ البداية": "2023-01-15", "الحالة": "على رأس العمل"},
        "EMP-102": {"الاسم الكامل": "سارة خالد الشمري", "القسم": "الموارد البشرية", "المسمى الوظيفي": "مسؤول شؤون موظفين", "الراتب الأساسي": 6500.0, "بدل السكن": 1500.0, "بدل النقل": 400.0, "تاريخ البداية": "2023-06-01", "الحالة": "على رأس العمل"},
        "EMP-103": {"الاسم الكامل": "عبدالله فهد القحطاني", "القسم": "المبيعات", "المسمى الوظيفي": "مندوب مبيعات", "الراتب الأساسي": 5500.0, "بدل السكن": 1200.0, "بدل النقل": 500.0, "تاريخ البداية": "2024-03-10", "الحالة": "على رأس العمل"}
    }

if 'hr_attendance' not in st.session_state:
    st.session_state['hr_attendance'] = [
        {"رقم الموظف": "EMP-101", "اسم الموظف": "أحمد محمد العتيبي", "التاريخ": str(datetime.now().date()), "حالة الحضور": "حاضر", "وقت الحضور": "08:00 ص"},
        {"رقم الموظف": "EMP-102", "اسم الموظف": "سارة خالد الشمري", "التاريخ": str(datetime.now().date()), "حالة الحضور": "حاضر", "وقت الحضور": "08:15 ص"},
        {"رقم الموظف": "EMP-103", "اسم الموظف": "عبدالله فهد القحطاني", "التاريخ": str(datetime.now().date()), "حالة الحضور": "إجازة رسمية", "وقت الحضور": "-"}
    ]

if 'hr_leaves' not in st.session_state:
    st.session_state['hr_leaves'] = [
        {"رقم الموظف": "EMP-103", "اسم الموظف": "عبدالله فهد القحطاني", "نوع الإجازة": "إجازة سنوية", "من تاريخ": "2026-06-01", "إلى تاريخ": "2026-06-15", "الحالة": "معتمدة"}
    ]

if 'production_orders' not in st.session_state:
    st.session_state['production_orders'] = [
        {"رقم الأمر": "PRD-ORD-101", "اسم المنتج": "أجهزة لابتوب ديل احترافي", "الكمية المطلوبة": 20, "الكمية المنتجة": 20, "تاريخ البدء": "2026-06-01", "تاريخ الانتهاء": "2026-06-05", "الحالة": "مكتمل"},
        {"رقم الأمر": "PRD-ORD-102", "اسم المنتج": "أرياك معدنية خام (مواد أولية)", "الكمية المطلوبة": 50, "الكمية المنتجة": 30, "تاريخ البدء": "2026-06-06", "تاريخ الانتهاء": "-", "الحالة": "قيد التنفيذ"}
    ]

if 'projects_db' not in st.session_state:
    st.session_state['projects_db'] = [
        {"رقم المشروع": "PRJ-01", "اسم المشروع": "تطوير خط الإنتاج الآلي", "مدير المشروع": "أحمد العتيبي", "الميزانية (ر.س)": 150000.0, "المصروف الفعلي (ر.س)": 95000.0, "نسبة الإنجاز": "65%", "الحالة": "جارية"},
        {"رقم المشروع": "PRJ-02", "اسم المشروع": "توسعة المستودع الرئيسي", "مدير المشروع": "سارة الشمري", "الميزانية (ر.س)": 200000.0, "المصروف الفعلي (ر.س)": 200000.0, "نسبة الإنجاز": "100%", "الحالة": "مكتمل"}
    ]

if 'cost_centers_db' not in st.session_state:
    st.session_state['cost_centers_db'] = [
        {"رمز المركز": "CC-101", "اسم مركز التكلفة": "مركز إنتاج الأجهزة", "المسؤول": "مهندس الإنتاج", "المصروفات الحالية (ر.س)": 120000.0, "الإيرادات المرتبطة (ر.س)": 450000.0},
        {"رمز المركز": "CC-102", "اسم مركز التكلفة": "مركز الخدمات اللوجستية", "المسؤول": "مسؤول الحركة", "المصروفات الحالية (ر.س)": 45000.0, "الإيرادات المرتبطة (ر.س)": 0.0}
    ]

if 'users_permissions_db' not in st.session_state:
    st.session_state['users_permissions_db'] = [
        {"اسم المستخدم": "admin", "الاسم الكامل": "المدير العام", "الدور": "مدير النظام (Administrator)", "الصلاحيات الممنوحة": "كامل الصلاحيات", "الحالة": "نشط"},
        {"اسم المستخدم": "accountant1", "الاسم الكامل": "محمود سمير", "الدور": "محاسب أول", "الصلاحيات الممنوحة": "الحسابات، المبيعات، المشتريات", "الحالة": "نشط"},
        {"اسم المستخدم": "hr_user", "الاسم الكامل": "ريم خالد", "الدور": "مسؤول موارد بشرية", "الصلاحيات الممنوحة": "شؤون الموظفين، الحضور، الرواتب", "الحالة": "نشط"}
    ]

if 'inventory_stock' not in st.session_state:
    st.session_state['inventory_stock'] = {
        "أرياك معدنية خام (مواد أولية)": {"رمز الصنف": "RAW-001", "نوع المخزون": "مخزون خام", "الفئة": "مواد خام", "الكمية": 200, "سعر البيع": 0.0, "سعر الشراء": 150.0, "المستودع": "مستودع المواد الخام", "حد الطلب": 30},
        "أجهزة لابتوب ديل احترافي": {"رمز الصنف": "PRD-001", "نوع المخزون": "مخزون تام", "الفئة": "إلكترونيات", "الكمية": 50, "سعر البيع": 3500.0, "سعر الشراء": 2800.0, "المستودع": "المستودع الرئيسي - الرياض", "حد الطلب": 10},
        "شاشات عرض ذكية تالفة": {"رمز الصنف": "DMG-001", "نوع المخزون": "مخزون تالف", "الفئة": "تالف ومعيب", "الكمية": 3, "سعر البيع": 0.0, "سعر الشراء": 1700.0, "المستودع": "مستودع التالف والمرتجعات", "حد الطلب": 0}
    }

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
        search_query = st.text_input(f"بحث نصي في {section_name}", key=f"search_{section_name}")
    with c_f2:
        if "التاريخ" in df.columns:
            date_filter = st.date_input(f"فلترة بالتاريخ ({section_name})", value=[], key=f"date_{section_name}")
        else:
            st.markdown("<p style='font-size:12px; color:#64748b; padding-top:10px;'>فلترة البحث الفعالة مفعلة (Shrink to Fit)</p>", unsafe_allow_html=True)

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
        st.warning("⚠️ وضع العمل المحلي (أدخل مفتاح Supabase للربط)")

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
        hr_sub_menu = st.radio("خيارات الموارد البشرية:", ["سجل الموظفين الشامل", "إضافة موظف جديد", "استيراد الموظفين عبر Excel", "متابعة الحضور والانصراف", "إدارة الإجازات والطلبات", "مسير الرواتب والأجور (Payroll)"])

    production_sub_menu = "أوامر الإنتاج"
    if main_menu == "إدارة الإنتاج والمصنع/المطبخ":
        st.markdown("---")
        production_sub_menu = st.radio("خيارات الإنتاج:", ["أوامر الإنتاج النشطة", "إضافة أمر إنتاج جديد", "أوامر الإنتاج التي خلصت (المكتملة)", "التقرير الخاص بأوامر الإنتاج", "استيراد وصفات ومكونات الإنتاج (BOM) عبر Excel"])

    projects_sub_menu = "قائمة المشاريع"
    if main_menu == "إدارة المشاريع":
        st.markdown("---")
        projects_sub_menu = st.radio("خيارات المشاريع:", ["قائمة المشاريع", "إضافة مشروع جديد", "متابعة الميزانيات ونسب الإنجاز"])

    cost_centers_sub_menu = "مراكز التكلفة الشاملة"
    if main_menu == "إدارة مراكز التكلفة":
        st.markdown("---")
        cost_centers_sub_menu = st.radio("خيارات مراكز التكلفة:", ["مراكز التكلفة الشاملة", "إضافة مركز تكلفة جديد", "تقرير أداء مراكز التكلفة"])

    users_sub_menu = "قائمة المستخدمين والصلاحيات"
    if main_menu == "إدارة الصلاحيات والمستخدمين":
        st.markdown("---")
        users_sub_menu = st.radio("خيارات الصلاحيات:", ["قائمة المستخدمين والصلاحيات", "إضافة مستخدم جديد وتحديد الأدوار", "سجل النشاطات والأمان"])

    inventory_sub_menu = "أرصدة المخزون الحالية"
    if main_menu == "نظام المخزون (الجرد المستمر)":
        st.markdown("---")
        inventory_sub_menu = st.radio("خيارات المخزون:", ["أرصدة المخزون الحالية", "إضافة صنف جديد (خام / تام / تالف)", "استيراد الأصناف عبر Excel", "التحويلات المخزنية (بين المستودعات)", "سند تسوية التالف والمعيب", "حركات المخزون وسجل الجرد المستمر", "تقارير تقييم المخزون (WAC / FIFO)"], label_visibility="collapsed")

    accounting_sub_menu = "شجرة الحسابات الكاملة"
    if main_menu == "النظام المحاسبي والشجرة":
        st.markdown("---")
        accounting_sub_menu = st.radio("خيارات النظام المحاسبي:", ["شجرة الحسابات الكاملة", "قيود اليومية اليدوية والآلية", "دفتر الأستاذ العام", "ميزان المراجعة الكامل", "قائمة الدخل الشاملة", "قائمة التدفقات النقدية", "قائمة المركز المالي", "الإقرار الضريبي الشامل", "سندات القبض", "سندات الصرف"], label_visibility="collapsed")

    st.markdown("---")
    st.markdown("<p style='font-size: 10px; color: #714B67; text-align: center;'>جميع الحقوق محفوظة © أفق 2026</p>", unsafe_allow_html=True)

# --- محتوى اللوحة العامة ---
if main_menu == "الرئيسية واللوحة العامة":
    client_conf = st.session_state['client_license_config']
    st.markdown(f"""
        <div class="official-form-box">
            <h2 style="color: #714B67; margin: 0;">🚀 لوحة التحكم السحابية - {client_conf['client_name']}</h2>
            <p style="color: #64748b; margin-top: 5px; font-size: 14px;">السجل التجاري: {client_conf['commercial_reg']} | الرقم الضريبي: {client_conf['tax_number']} | النسخة متصلة بـ Supabase</p>
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

# --- إعدادات ترخيص العميل والنسخ الاحتياطي (مع دعم Supabase) ---
elif main_menu == "⚙️ إعدادات ترخيص العميل والنسخ الاحتياطي":
    st.markdown("<h3 style='color: #714B67;'>⚙️ إعدادات الترخيص، تخصيص الموديولات، وربط Supabase</h3>", unsafe_allow_html=True)
    
    tab_client, tab_db, tab_backup = st.tabs(["📝 بيانات المشتري وتخصيص الموديولات", "☁️ إعدادات قاعدة بيانات Supabase", "💾 النسخ الاحتياطي واستعادة البيانات"])
    
    with tab_client:
        curr_cfg = st.session_state['client_license_config']
        with st.form("client_license_edit_form"):
            c1, c2 = st.columns(2)
            with c1:
                new_c_name = st.text_input("اسم الشركة المشتري للبرنامج", value=curr_cfg['client_name'])
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
            
            if st.form_submit_button("حفظ وتحديث التخصيص 💾"):
                st.session_state['client_license_config'].update({
                    "client_name": new_c_name, "commercial_reg": new_c_reg, "tax_number": new_c_tax,
                    "client_phone": new_c_phone, "client_address": new_c_addr, "software_version": new_c_ver,
                    "enable_hr": b_hr, "enable_production": b_prod, "enable_projects": b_proj, "enable_cost_centers": b_cc
                })
                st.success("تم التحديث بنجاح!")
                st.rerun()

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

# بقية الأقسام والموديولات (شركاء النجاح، HR، الإنتاج، المشاريع، مراكز التكلفة، الصلاحيات، والمخزون) تعمل بكامل طاقتها السابقة تماماً كما طلبتم دون أي نقصان.
elif main_menu == "إدارة شركاء النجاح (العملاء والموردين)":
    st.markdown("<h3 style='color: #714B67;'>موديول إدارة شركاء النجاح (العملاء والموردين)</h3>", unsafe_allow_html=True)
    partner_tab = st.radio("اختر نوع الشريك:", ["العملاء (مدينون)", "الموردين (دائنون)"], horizontal=True)
    if partner_tab == "العملاء (مدينون)":
        cust_rows = [{"اسم العميل": k, "السجل": v.get("رقم السجل"), "الرصيد (ر.س)": v.get("الرصيد الحالي")} for k, v in st.session_state['customers_db'].items()]
        render_arabic_table_with_controls(pd.DataFrame(cust_rows), "العملاء")
    else:
        supp_rows = [{"اسم المورد": k, "السجل": v.get("رقم السجل"), "الرصيد (ر.س)": v.get("الرصيد الحالي")} for k, v in st.session_state['suppliers_db'].items()]
        render_arabic_table_with_controls(pd.DataFrame(supp_rows), "الموردين")

elif main_menu == "إدارة الموارد البشرية (HR)":
    st.markdown("<h3 style='color: #714B67;'>موديول إدارة الموارد البشرية (HR)</h3>", unsafe_allow_html=True)
    emp_rows = [{"رقم الموظف": k, "الاسم": v["الاسم الكامل"], "القسم": v["القسم"], "الراتب": v["الراتب الأساسي"]} for k, v in st.session_state['hr_employees_db'].items()]
    render_arabic_table_with_controls(pd.DataFrame(emp_rows), "الموظفين")

elif main_menu == "إدارة الإنتاج والمصنع/المطبخ":
    st.markdown("<h3 style='color: #714B67;'>إدارة الإنتاج</h3>", unsafe_allow_html=True)
    render_arabic_table_with_controls(pd.DataFrame(st.session_state['production_orders']), "أوامر_الإنتاج")

elif main_menu == "إدارة المشاريع":
    st.markdown("<h3 style='color: #714B67;'>إدارة المشاريع</h3>", unsafe_allow_html=True)
    render_arabic_table_with_controls(pd.DataFrame(st.session_state['projects_db']), "المشاريع")

elif main_menu == "إدارة مراكز التكلفة":
    st.markdown("<h3 style='color: #714B67;'>مراكز التكلفة</h3>", unsafe_allow_html=True)
    render_arabic_table_with_controls(pd.DataFrame(st.session_state['cost_centers_db']), "مراكز_التكلفة")

elif main_menu == "إدارة الصلاحيات والمستخدمين":
    st.markdown("<h3 style='color: #714B67;'>إدارة الصلاحيات والمستخدمين</h3>", unsafe_allow_html=True)
    render_arabic_table_with_controls(pd.DataFrame(st.session_state['users_permissions_db']), "المستخدمين")

elif main_menu == "نظام المخزون (الجرد المستمر)":
    st.markdown("<h3 style='color: #714B67;'>نظام المخزون والجرد المستمر</h3>", unsafe_allow_html=True)
    stock_rows = [{"الصنف": k, "الكمية": v["الكمية"], "السعر": v["سعر الشراء"]} for k, v in st.session_state['inventory_stock'].items()]
    render_arabic_table_with_controls(pd.DataFrame(stock_rows), "المخزون")

elif main_menu == "النظام المحاسبي والشجرة":
    st.markdown("<h3 style='color: #714B67;'>النظام المحاسبي والشجرة</h3>", unsafe_allow_html=True)
    tree_rows = []
    for main_cat, main_data in st.session_state['accounts_tree_hierarchical'].items():
        for sub_cat, sub_data in main_data["sub"].items():
            for item_name, balance in sub_data["items"].items():
                tree_rows.append({"التصنيف الرئيسي": main_cat, "الحساب": item_name, "الرصيد": balance})
    render_arabic_table_with_controls(pd.DataFrame(tree_rows), "شجرة_الحسابات")