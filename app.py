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

# --- تهيئة قاعدة بيانات المستخدمين والصلاحيات المفصلة (لمنع أي خطأ مفقود) ---
if 'users_permissions_db' not in st.session_state:
    st.session_state['users_permissions_db'] = {
        "admin": {
            "اسم المستخدم": "admin",
            "الاسم الكامل": "المدير العام",
            "الدور": "مدير النظام (Administrator)",
            "الحالة": "نشط",
            "صلاحيات الموديولات": {
                "الرئيسية": True, "الشركاء": True, "الموارد البشرية": True, "الإنتاج": True, 
                "المشروعات": True, "مراكز التكلفة": True, "الصلاحيات": True, "المبيعات": True, 
                "المشتريات": True, "المخزون": True, "المحاسبة والشجرة": True, "الإعدادات": True
            }
        },
        "accountant1": {
            "اسم المستخدم": "accountant1",
            "الاسم الكامل": "محمد خالد المحاسب",
            "الدور": "محاسب أول",
            "الحالة": "نشط",
            "صلاحيات الموديولات": {
                "الرئيسية": True, "الشركاء": True, "الموارد البشرية": False, "الإنتاج": False, 
                "المشروعات": False, "مراكز التكلفة": True, "الصلاحيات": False, "المبيعات": True, 
                "المشتريات": True, "المخزون": True, "المحاسبة والشجرة": True, "الإعدادات": False
            }
        }
    }

# --- تهيئة نظام المصادقة وشاشة الدخول الذكية ---
if 'authenticated' not in st.session_state:
    st.session_state['authenticated'] = False

if not st.session_state['authenticated']:
    st.markdown("""
        <style>
        .stApp { background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%); }
        .login-card { background: #ffffff; padding: 40px; border-radius: 20px; box-shadow: 0 15px 35px rgba(113, 75, 103, 0.12); border: 1px solid rgba(113, 75, 103, 0.1); text-align: right; direction: rtl; margin-top: 40px; }
        .login-title { color: #714B67; font-size: 30px; font-weight: 800; text-align: center; margin-bottom: 5px; }
        .login-subtitle { color: #64748b; font-size: 13px; text-align: center; margin-bottom: 30px; font-weight: 500; }
        .stButton>button { width: 100%; background: linear-gradient(135deg, #714B67 0%, #5a3b52 100%); color: white; font-weight: bold; border-radius: 10px; padding: 12px; border: none; box-shadow: 0 4px 15px rgba(113, 75, 103, 0.3); font-size: 16px; }
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

# --- تهيئة قواعد البيانات وباقي القواميس الشاملة ---
if 'customers_db' not in st.session_state:
    st.session_state['customers_db'] = {
        "شركة التقنية الحديثة للتجارة": {"كود العميل": "CUST-001", "رقم السجل": "1010254789", "الرقم الضريبي": "300123456700003", "العنوان": "الرياض - حي الملز", "الهاتف": "0501234567", "الحد الائتماني": 100000.0, "الرصيد الحالي": 45000.0}
    }

if 'suppliers_db' not in st.session_state:
    st.session_state['suppliers_db'] = {
        "شركة التوريدات الكبرى المحدودة": {"كود المورد": "SUP-001", "رقم السجل": "1010987654", "الرقم الضريبي": "300111222300003", "العنوان": "الرياض - الصناعية", "الهاتف": "0561112233", "الرصيد الحالي": 65000.0}
    }

if 'hr_employees_db' not in st.session_state:
    st.session_state['hr_employees_db'] = {
        "EMP-101": {"الاسم الكامل": "أحمد محمد العتيبي", "القسم": "الإدارة المالية", "المسمى الوظيفي": "محاسب أول", "الراتب الأساسي": 8000.0, "الحالة": "على رأس العمل"}
    }

if 'production_orders' not in st.session_state:
    st.session_state['production_orders'] = []

if 'projects_db' not in st.session_state:
    st.session_state['projects_db'] = []

if 'cost_centers_db' not in st.session_state:
    st.session_state['cost_centers_db'] = []

if 'inventory_stock' not in st.session_state:
    st.session_state['inventory_stock'] = {}

if 'sales_quotations' not in st.session_state:
    st.session_state['sales_quotations'] = []

if 'sales_orders' not in st.session_state:
    st.session_state['sales_orders'] = []

if 'sales_invoices_db' not in st.session_state:
    st.session_state['sales_invoices_db'] = []

if 'purchase_invoices_db' not in st.session_state:
    st.session_state['purchase_invoices_db'] = []

if 'general_ledger' not in st.session_state:
    st.session_state['general_ledger'] = []

# --- تنسيقات CSS ---
st.markdown("""
    <style>
    .stApp, body, p, span, div, label, input, select {
        direction: rtl !important; text-align: right !important; font-family: 'Segoe UI', Tahoma, sans-serif;
    }
    .block-container { padding: 1.5rem 2rem !important; background-color: #f4f6f9; }
    .custom-table {
        width: 100%; border-collapse: collapse; background-color: white; font-size: 11px;
        border-radius: 6px; overflow: hidden; box-shadow: 0 1px 3px rgba(0,0,0,0.08); margin-top: 10px;
    }
    .custom-table th { background-color: #714B67; color: white; padding: 8px; text-align: right; white-space: nowrap; }
    .custom-table td { padding: 6px 8px; border-bottom: 1px solid #edf2f7; color: #2d3748; white-space: nowrap; }
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
    c_f1, c_f2, c_b1, c_b2, c_b3 = st.columns([2, 2, 1, 1, 1])
    with c_f1:
        search_query = st.text_input(f"بحث فوري في {section_name}", key=f"search_{section_name}")
    with c_f2:
        st.markdown("<p style='font-size:12px; color:#64748b; padding-top:10px;'>فلترة البحث الفعالة مفعلة</p>", unsafe_allow_html=True)

    filtered_df = df.copy()
    if search_query:
        mask = filtered_df.astype(str).apply(lambda x: x.str.contains(search_query, case=False)).any(axis=1)
        filtered_df = filtered_df[mask]

    with c_b1:
        if st.button("🖨️ طباعة", key=f"print_{section_name}"): st.toast("جاري الطباعة...")
    with c_b2:
        if st.button("📊 Excel", key=f"excel_{section_name}"): st.toast("تم التصدير لـ Excel!")
    with c_b3:
        if st.button("📄 PDF", key=f"pdf_{section_name}"): st.toast("تم التصدير لـ PDF!")

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

# --- القائمة الجانبية ---
with st.sidebar:
    client_conf = st.session_state['client_license_config']
    st.markdown(f"<h2 style='color: #714B67; text-align: center;'>نظام أفق ERP</h2>", unsafe_allow_html=True)
    st.markdown(f"<p style='text-align: center; font-size: 11px; color: #64748b;'>مرخص لـ: <b>{client_conf['client_name']}</b></p>", unsafe_allow_html=True)
    
    if st.button("🔒 تسجيل الخروج", use_container_width=True):
        st.session_state['authenticated'] = False
        st.rerun()

    st.markdown("---")
    modules_map = {
        "الرئيسية": "🏠 الرئيسية",
        "الشركاء": "👥 الشركاء",
        "الموارد البشرية": "👨‍💼 الموارد البشرية",
        "الإنتاج": "🏭 الإنتاج",
        "المشروعات": "📊 المشروعات",
        "مراكز التكلفة": "🏷️ مراكز التكلفة",
        "الصلاحيات": "🔐 الصلاحيات",
        "المبيعات": "🛒 المبيعات",
        "المشتريات": "📦 المشتريات",
        "المخزون": "📋 المخزون",
        "المحاسبة والشجرة": "💰 المحاسبة",
        "الإعدادات": "⚙️ الإعدادات"
    }
    
    for mod_key, mod_label in modules_map.items():
        is_selected = (st.session_state['active_module'] == mod_key)
        if st.button(mod_label, key=f"btn_mod_{mod_key}", use_container_width=True, type="primary" if is_selected else "secondary"):
            st.session_state['active_module'] = mod_key
            st.rerun()

main_menu = st.session_state['active_module']

# --- لوحة التحكم ---
if main_menu == "الرئيسية":
    st.markdown("<h3>🚀 لوحة التحكم السحابية</h3>", unsafe_allow_html=True)

# --- الصلاحيات (مع شاشة التخصيص التفاعلية) ---
elif main_menu == "الصلاحيات":
    st.markdown("<h3 style='color: #714B67;'>🔐 إدارة الصلاحيات والمستخدمين وتخصيص الموديولات</h3>", unsafe_allow_html=True)
    
    perm_tab1, perm_tab2 = st.tabs(["👥 قائمة المستخدمين وصلاحياتهم التفاعلية", "➕ إضافة مستخدم جديد للنظام"])
    
    with perm_tab1:
        st.markdown("<p style='color:#64748b;'>قم باختيار المستخدم من القائمة أدناه لفتح شاشة الصلاحيات الخاصة به وتعديل صلاحياته بكل سهولة:</p>", unsafe_allow_html=True)
        
        # التأكد التام من وجود القاموس لمنع أي خطأ
        if 'users_permissions_db' not in st.session_state:
            st.session_state['users_permissions_db'] = {}

        user_keys = list(st.session_state['users_permissions_db'].keys())
        
        if not user_keys:
            st.warning("لا توجد حسابات مستخدمين مسجلة. يجدر إضافة مستخدم جديد.")
        else:
            selected_user_key = st.selectbox("اختر المستخدم للتعديل والتخصيص:", user_keys, format_func=lambda x: f"{x} - {st.session_state['users_permissions_db'][x]['الاسم الكامل']}")
            
            if selected_user_key:
                user_obj = st.session_state['users_permissions_db'][selected_user_key]
                
                st.markdown(f"""
                    <div class="official-form-box" style="border-right: 5px solid #714B67;">
                        <h4>تعديل صلاحيات المستخدم: <span style="color: #714B67;">{user_obj['الاسم الكامل']} ({selected_user_key})</span></h4>
                        <p style="margin:0; font-size:13px; color:#64748b;">الدور الحالي: {user_obj['الدور']} | الحالة: {user_obj['الحالة']}</p>
                    </div>
                """, unsafe_allow_html=True)
                
                with st.form(f"form_perms_{selected_user_key}"):
                    st.markdown("##### حدد الصلاحيات والموديولات المتاحة لهذا المستخدم:")
                    
                    current_perms = user_obj.get("صلاحيات الموديولات", {})
                    all_modules_list = [
                        "الرئيسية", "الشركاء", "الموارد البشرية", "الإنتاج", 
                        "المشروعات", "مراكز التكلفة", "الصلاحيات", "المبيعات", 
                        "المشتريات", "المخزون", "المحاسبة والشجرة", "الإعدادات"
                    ]
                    
                    new_assigned_perms = {}
                    col_a, col_b, col_c = st.columns(3)
                    
                    for idx, mod in enumerate(all_modules_list):
                        default_val = current_perms.get(mod, True)
                        if idx % 3 == 0:
                            with col_a:
                                new_assigned_perms[mod] = st.checkbox(f"موديول {mod}", value=default_val, key=f"p_{selected_user_key}_{mod}")
                        elif idx % 3 == 1:
                            with col_b:
                                new_assigned_perms[mod] = st.checkbox(f"موديول {mod}", value=default_val, key=f"p_{selected_user_key}_{mod}")
                        else:
                            with col_c:
                                new_assigned_perms[mod] = st.checkbox(f"موديول {mod}", value=default_val, key=f"p_{selected_user_key}_{mod}")
                    
                    st.markdown("<div style='margin-top:15px;'></div>", unsafe_allow_html=True)
                    save_perms_btn = st.form_submit_button("حفظ وتطبيق الصلاحيات الجديدة 💾")
                    
                    if save_perms_btn:
                        st.session_state['users_permissions_db'][selected_user_key]["صلاحيات الموديولات"] = new_assigned_perms
                        st.success(f"تم حفظ الصلاحيات المخصصة للمستخدم ({user_obj['الاسم الكامل']}) بنجاح!")
                        st.rerun()

        st.markdown("---")
        st.markdown("#### جدول ملخص المستخدمين والصلاحيات العامة")
        summary_rows = []
        for uk, uv in st.session_state['users_permissions_db'].items():
            active_count = sum(1 for v in uv.get("صلاحيات الموديولات", {}).values() if v)
            summary_rows.append({
                "اسم المستخدم": uk,
                "الاسم الكامل": uv["الاسم الكامل"],
                "الدور": uv["الدور"],
                "عدد الموديولات المتاحة": f"{active_count} موديول",
                "الحالة": uv["الحالة"]
            })
        render_arabic_table_with_controls(pd.DataFrame(summary_rows), "المستخدمين_والصلاحيات")

    with perm_tab2:
        with st.form("add_new_user_perms"):
            st.markdown("#### إضافة مستخدم جديد للنظام وتحديد بياناته")
            u_id = st.text_input("اسم المستخدم (Username - إنجليزي بدون مسافات)")
            u_full = st.text_input("الاسم الكامل للموظف/المستخدم")
            u_role = st.selectbox("الدور الوظيفي", ["مدير النظام (Administrator)", "محاسب أول", "مستودعات", "مدير مبيعات", "مشرف عام"])
            
            if st.form_submit_button("إضافة المستخدم الجديد 🚀"):
                if u_id and u_full:
                    if u_id in st.session_state['users_permissions_db']:
                        st.error("اسم المستخدم موجود مسبقاً، اختر اسم آخر.")
                    else:
                        st.session_state['users_permissions_db'][u_id] = {
                            "اسم المستخدم": u_id,
                            "الاسم الكامل": u_full,
                            "الدور": u_role,
                            "الحالة": "نشط",
                            "صلاحيات الموديولات": {m: True for m in ["الرئيسية", "الشركاء", "الموارد البشرية", "الإنتاج", "المشروعات", "مراكز التكلفة", "الصلاحيات", "المبيعات", "المشتريات", "المخزون", "المحاسبة والشجرة", "الإعدادات"]}
                        }
                        st.success(f"تم إضافة المستخدم ({u_full}) وتفعيل صلاحياته بنجاح!")
                        st.rerun()
                else:
                    st.error("يرجى ملء الحقول الأساسية.")

# بقية الأقسام (الشركاء، الموارد البشرية، المبيعات، إلخ...)
elif main_menu == "الشركاء":
    st.markdown("<h3 style='color: #714B67;'>👥 إدارة شركاء النجاح</h3>", unsafe_allow_html=True)
    cust_list = [{"كود العميل": k, "اسم العميل": k} for k in st.session_state['customers_db'].keys()]
    render_arabic_table_with_controls(pd.DataFrame(cust_list), "العملاء")

elif main_menu == "الإعدادات":
    st.markdown("<h3 style='color: #714B67;'>⚙️ الإعدادات العامة</h3>", unsafe_allow_html=True)
    if st.button("🔄 إعادة تصفير البرنامج بالكامل"):
        reset_system_to_default()
