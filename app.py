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

# --- تهيئة قاعدة بيانات المستخدمين والصلاحيات المفصلة ---
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

# --- تهيئة قواعد البيانات والباقي ---
if 'customers_db' not in st.session_state:
    st.session_state['customers_db'] = {
        "شركة التقنية الحديثة للتجارة": {"كود العميل": "CUST-001", "رقم السجل": "1010254789", "الرقم الضريبي": "300123456700003", "العنوان": "الرياض - حي الملز", "الهاتف": "0501234567", "الحد الائتماني": 100000.0, "الرصيد الحالي": 45000.0}
    }

if 'suppliers_db' not in st.session_state:
    st.session_state['suppliers_db'] = {
        "شركة التوريدات الكبرى المحدودة": {"كود المورد": "SUP-001", "رقم السجل": "1010987654", "الرقم الضريبي": "300111222300003", "العنوان": "الرياض - الصناعية", "الهاتف": "0561112233", "الرصيد الحالي": 65000.0}
    }

if 'warehouses_db' not in st.session_state:
    st.session_state['warehouses_db'] = ["المستودع الرئيسي - الرياض", "مستودع فرع جدة", "مستودع المنطقة الشرقية"]

if 'cash_boxes_db' not in st.session_state:
    st.session_state['cash_boxes_db'] = ["الخزينة الرئيسية (صندوق النقد)", "صندوق المبيعات اليومي"]

if 'banks_db' not in st.session_state:
    st.session_state['banks_db'] = ["مصرف الراجحي", "البنك الأهلي السعودي (SNB)", "بنك الرياض"]

if 'inventory_stock' not in st.session_state:
    st.session_state['inventory_stock'] = {
        "PROD-001": {"اسم المنتج": "شاشة سمارت 55 بوصة 4K", "السعر": 1500.0, "الكمية المتاحة": 50},
        "PROD-002": {"اسم المنتج": "جهاز حاسب آلي محمول Core i7", "السعر": 3500.0, "الكمية المتاحة": 30},
        "PROD-003": {"اسم المنتج": "طابعة ليزر متعددة الوظائف", "السعر": 850.0, "الكمية المتاحة": 20}
    }

if 'sales_workflow_db' not in st.session_state:
    st.session_state['sales_workflow_db'] = []

if 'sales_invoices_full_db' not in st.session_state:
    st.session_state['sales_invoices_full_db'] = []

if 'purchases_workflow_db' not in st.session_state:
    st.session_state['purchases_workflow_db'] = []

if 'purchases_invoices_full_db' not in st.session_state:
    st.session_state['purchases_invoices_full_db'] = []

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
        "المبيعات": "🛒 المبيعات الشاملة",
        "المشتريات": "📦 المشتريات الشاملة",
        "المخزون": "📋 المخزون",
        "المحاسبة والشجرة": "💰 المحاسبة والقيد التلقائي",
        "الصلاحيات": "🔐 الصلاحيات",
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
    st.markdown("<h3>🚀 لوحة التحكم السحابية - نظام أفق ERP</h3>", unsafe_allow_html=True)
    st.info("مرحباً بك في النظام. تم تفعيل دورة مستندات المبيعات والمشتريات المتكاملة (عرض سعر -> أمر بيع -> فاتورة ضريبية مع خصم المخزون والقيود التلقائية).")

# --- الشركاء ---
elif main_menu == "الشركاء":
    st.markdown("<h3 style='color: #714B67;'>👥 إدارة شركاء النجاح (العملاء والموردين)</h3>", unsafe_allow_html=True)
    tab_c1, tab_c2 = st.tabs(["العملاء", "الموردين"])
    with tab_c1:
        cust_list = [{"كود العميل": v["كود العميل"], "اسم العميل": k, "السجل التجاري": v["رقم السجل"], "الرقم الضريبي": v["الرقم الضريبي"], "الرصيد": v["الرصيد الحالي"]} for k, v in st.session_state['customers_db'].items()]
        render_arabic_table_with_controls(pd.DataFrame(cust_list), "العملاء")
    with tab_c2:
        supp_list = [{"كود المورد": v["كود المورد"], "اسم المورد": k, "السجل التجاري": v["رقم السجل"], "الرقم الضريبي": v["الرقم الضريبي"], "الرصيد": v["الرصيد الحالي"]} for k, v in st.session_state['suppliers_db'].items()]
        render_arabic_table_with_controls(pd.DataFrame(supp_list), "الموردين")

# ==================== موديول المبيعات (عرض سعر / أمر بيع / ورقة واحدة بالحالة / الفاتورة الضريبية الكاملة / التقارير) ====================
elif main_menu == "المبيعات":
    st.markdown("<h3 style='color: #714B67;'>🛒 موديول المبيعات المتكامل (عروض الأسعار، أوامر البيع، والفواتير الضريبية)</h3>", unsafe_allow_html=True)
    
    sales_tab1, sales_tab2, sales_tab3 = st.tabs([
        "📄 ورقة عرض السعر وأمر البيع (ورقة واحدة بالحالة)", 
        "🧾 الفاتورة الضريبية الكاملة (تخصم المخزون وتنشئ قيد تلقائي)", 
        "📊 تقرير المبيعات الشامل والفلاتر"
    ])
    
    # --- التبويب الأول: ورقة عرض السعر وتحولها لأمر بيع ومفوترة ---
    with sales_tab1:
        st.markdown("#### إدارة عروض الأسعار وأوامر البيع (ورقة عمل ديناميكية واحدة)")
        
        with st.form("sales_workflow_form"):
            col_w1, col_w2, col_w3 = st.columns(3)
            with col_w1:
                doc_number = st.text_input("رقم المستند / العرض", value=f"SQ-{int(datetime.now().timestamp())}")
                selected_customer = st.selectbox("اختر العميل", list(st.session_state['customers_db'].keys()))
            with col_w2:
                doc_date = st.date_input("التاريخ", value=datetime.now())
                doc_type = st.selectbox("النوع الرئيسي", ["مبيعات", "مردودات مبيعات"])
            with col_w3:
                workflow_status = st.selectbox("حالة المستند (تتحول ديناميكياً)", ["عرض سعر", "أمر بيع", "مفوترة"])
                warehouse_choice = st.selectbox("المستودع", st.session_state['warehouses_db'])
            
            st.markdown("---")
            st.markdown("##### جدول الأصناف والبنود")
            
            item_code_input = st.selectbox("كود المنتج / البند", list(st.session_state['inventory_stock'].keys()), format_func=lambda x: f"{x} - {st.session_state['inventory_stock'][x]['اسم المنتج']}")
            item_qty = st.number_input("الكمية المطلوبة", min_value=1.0, value=1.0)
            
            prod_details = st.session_state['inventory_stock'][item_code_input]
            unit_price = st.number_input("سعر الوحدة", value=float(prod_details["السعر"]))
            discount_val = st.number_input("الخصم", value=0.0)
            tax_rate = 0.15 # 15% ضريبة القيمة المضافة
            
            line_subtotal = (unit_price * item_qty) - discount_val
            line_tax = line_subtotal * tax_rate
            line_total_incl = line_subtotal + line_tax
            
            st.info(f"إجمالي السطر (شامل الضريبة): {line_total_incl:,.2f} ر.س")
            
            col_b_act1, col_b_act2, col_b_act3, col_b_act4 = st.columns(4)
            save_wf = col_b_act1.form_submit_button("حفظ 💾")
            edit_wf = col_b_act2.form_submit_button("تعديل ✏️")
            cancel_wf = col_b_act3.form_submit_button("إلغاء / حذف 🗑️")
            
            if save_wf:
                new_record = {
                    "رقم المستند": doc_number,
                    "العميل": selected_customer,
                    "التاريخ": str(doc_date),
                    "النوع": doc_type,
                    "الحالة": workflow_status,
                    "كود المنتج": item_code_input,
                    "اسم المنتج": prod_details["اسم المنتج"],
                    "الكمية": item_qty,
                    "السعر": unit_price,
                    "الإجمالي شامل ض ق م": line_total_incl,
                    "المستودع": warehouse_choice
                }
                st.session_state['sales_workflow_db'].append(new_record)
                st.success(f"تم حفظ المستند برقم {doc_number} والحالة الحالية: {workflow_status} بنجاح!")
        
        st.markdown("#### سجل عروض الأسعار وأوامر البيع المسجلة")
        if st.session_state['sales_workflow_db']:
            df_wf = pd.DataFrame(st.session_state['sales_workflow_db'])
            render_arabic_table_with_controls(df_wf, "عروض_الأسعار_وأوامر_البيع")
        else:
            st.info("لا توجد عروض أسعار أو أوامر بيع مسجلة حتى الآن.")

    # --- التبويب الثاني: الفاتورة الضريبية الكاملة (تخصم المخزون وتنشئ قيد محاسبي تلقائي) ---
    with sales_tab2:
        st.markdown("#### الفاتورة الإلكترونية الضريبية الكاملة (نظام جرد مستمر)")
        
        with st.form("full_tax_invoice_form"):
            col_inv1, col_inv2, col_inv3 = st.columns(3)
            with col_inv1:
                inv_number = st.text_input("رقم الفاتورة الضريبية", value=f"INV-{int(datetime.now().timestamp())}")
                inv_customer = st.selectbox("اختر العميل للفاتورة", list(st.session_state['customers_db'].keys()))
                
                cust_data = st.session_state['customers_db'][inv_customer]
                st.markdown(f"""
                    <div style='background:#f8f9fa; padding:10px; border-radius:5px; font-size:12px; color:#2d3748;'>
                        <b>السجل التجاري:</b> {cust_data['رقم السجل']}<br>
                        <b>الرقم الضريبي:</b> {cust_data['الرقم الضريبي']}<br>
                        <b>العنوان:</b> {cust_data['العنوان']}<br>
                        <b>الهاتف:</b> {cust_data['الهاتف']}
                    </div>
                """, unsafe_allow_html=True)
                
            with col_inv2:
                inv_date = st.date_input("تاريخ الفاتورة", value=datetime.now())
                inv_type = st.selectbox("نوع الفاتورة", ["مبيعات", "مردودات مبيعات"])
                payment_method = st.selectbox("طريقة الدفع", ["أجل (تحول إلى حساب العميل)", "نقدي (صندوق)", "تحويل أو شبكة (بنك)"])
                
                selected_payment_destination = ""
                if payment_method == "نقدي (صندوق)":
                    selected_payment_destination = st.selectbox("اختر الصندوق", st.session_state['cash_boxes_db'])
                elif payment_method == "تحويل أو شبكة (بنك)":
                    selected_payment_destination = st.selectbox("اختر البنك", st.session_state['banks_db'])
                else:
                    selected_payment_destination = "حساب العملاء (أجل)"

            with col_inv3:
                inv_warehouse = st.selectbox("مستودع الصرف", st.session_state['warehouses_db'])
                st.markdown("<p style='font-size:12px; color:#64748b; margin-top:10px;'>عند حفظ الفاتورة سيتم تلقائياً:</p>", unsafe_allow_html=True)
                st.markdown("<ul style='font-size:11px; color:#64748b; padding-right:15px;'><li>خصم الكميات من المخزون</li><li>توليد قيد يومية مزدوج (جرد مستمر)</li><li>ترحيل الرصيد لحساب العميل</li></ul>", unsafe_allow_html=True)

            st.markdown("---")
            st.markdown("##### تفاصيل أصناف الفاتورة")
            inv_prod_code = st.selectbox("المنتج المراد بيعه", list(st.session_state['inventory_stock'].keys()), format_func=lambda x: f"{x} - {st.session_state['inventory_stock'][x]['اسم المنتج']}")
            inv_qty = st.number_input("الكمية المباعة", min_value=1.0, value=1.0, key="inv_qty_input")
            
            prod_row = st.session_state['inventory_stock'][inv_prod_code]
            inv_price = st.number_input("سعر البيع للوحدة", value=float(prod_row["السعر"]), key="inv_price_input")
            inv_discount = st.number_input("قيمة الخصم", value=0.0, key="inv_disc_input")
            
            sub_total_val = (inv_price * inv_qty) - inv_discount
            tax_val = sub_total_val * 0.15
            total_incl_tax = sub_total_val + tax_val
            
            st.markdown(f"**إجمالي السطر شامل ضريبة القيمة المضافة (15%):** {total_incl_tax:,.2f} ر.س")
            
            col_ib1, col_ib2, col_ib3 = st.columns(3)
            save_inv = col_ib1.form_submit_button("حفظ الفاتورة الضريبية 💾")
            edit_inv = col_ib2.form_submit_button("تعديل الفاتورة ✏️")
            cancel_inv = col_ib3.form_submit_button("إلغاء أو حذف الفاتورة 🗑️")
            
            if save_inv:
                if prod_row["الكمية المتاحة"] < inv_qty:
                    st.error(f"عذراً، الكمية المتاحة في المستودع ({prod_row['الكمية المتاحة']}) لا تكفي للكمية المطلوبة!")
                else:
                    st.session_state['inventory_stock'][inv_prod_code]["الكمية المتاحة"] -= inv_qty
                    
                    journal_entry = {
                        "رقم المستند": inv_number,
                        "الالتزام/النوع": "فاتورة ضريبية مبيعات",
                        "التاريخ": str(inv_date),
                        "البيان": f"فاتورة مبيعات رقم {inv_number} للعميل {inv_customer} عبر {payment_method} ({selected_payment_destination})",
                        "المدين": total_incl_tax,
                        "الدائن": total_incl_tax,
                        "الحساب الطرف": selected_payment_destination
                    }
                    st.session_state['general_ledger'].append(journal_entry)
                    
                    invoice_record = {
                        "رقم الفاتورة": inv_number,
                        "العميل": inv_customer,
                        "التاريخ": str(inv_date),
                        "النوع": inv_type,
                        "طريقة الدفع": payment_method,
                        "جهة الدفع": selected_payment_destination,
                        "المستودع": inv_warehouse,
                        "الإجمالي شامل ض ق م": total_incl_tax
                    }
                    st.session_state['sales_invoices_full_db'].append(invoice_record)
                    st.success("تم حفظ الفاتورة الضريبية الكاملة بنجاح، وتم خصم الكمية من المستودع وإنشاء القيد المحاسبي التلقائي!")

        st.markdown("#### سجل الفواتير الضريبية المسجلة")
        if st.session_state['sales_invoices_full_db']:
            render_arabic_table_with_controls(pd.DataFrame(st.session_state['sales_invoices_full_db']), "الفواتير_الضريبية")
        else:
            st.info("لا توجد فواتير ضريبية مسجلة بعد.")

    # --- التبويب الثالث: تقرير المبيعات الشامل والفلاتر والأزرار ---
    with sales_tab3:
        st.markdown("#### 📊 تقرير المبيعات الشامل (جميع الفلاتر والأزرار)")
        if st.session_state['sales_invoices_full_db']:
            df_sales_rep = pd.DataFrame(st.session_state['sales_invoices_full_db'])
            render_arabic_table_with_controls(df_sales_rep, "تقرير_المبيعات_الشامل")
        else:
            st.info("لا توجد بيانات مبيعات كافية لعرض التقرير الشامل.")


# ==================== موديول المشتريات (بنفس المنطق والطريقة) ====================
elif main_menu == "المشتريات":
    st.markdown("<h3 style='color: #714B67;'>📦 موديول المشتريات المتكامل (نفس المنطق والطريقة للمبيعات)</h3>", unsafe_allow_html=True)
    
    pur_tab1, pur_tab2, pur_tab3 = st.tabs([
        "📄 طلب شراء / عرض سعر مورد (ورقة واحدة بالحالة)", 
        "🧾 فاتورة المشتريات الضريبية (تزيد المخزون وتنشئ قيد تلقائي)", 
        "📊 تقرير المشتريات الشامل والفلاتر"
    ])
    
    with pur_tab1:
        st.markdown("#### إدارة طلبات الشراء وعروض أسعار الموردين")
        with st.form("pur_workflow_form"):
            c_pw1, c_pw2, c_pw3 = st.columns(3)
            with c_pw1:
                p_doc_num = st.text_input("رقم مستند الشراء", value=f"PO-{int(datetime.now().timestamp())}")
                p_supplier = st.selectbox("اختر المورد", list(st.session_state['suppliers_db'].keys()))
            with c_pw2:
                p_date = st.date_input("تاريخ الطلب", value=datetime.now())
                p_type = st.selectbox("نوع الحركة", ["مشتريات", "مردودات مشريات"])
            with c_pw3:
                p_status = st.selectbox("حالة المستند", ["طلب شراء", "معتمد", "مففوترة مشتريات"])
                p_warehouse = st.selectbox("مستودع الاستلام", st.session_state['warehouses_db'])
            
            st.markdown("---")
            p_item_code = st.selectbox("المنتج المطلوب شراؤه", list(st.session_state['inventory_stock'].keys()), format_func=lambda x: f"{x} - {st.session_state['inventory_stock'][x]['اسم المنتج']}")
            p_qty = st.number_input("الكمية", min_value=1.0, value=1.0, key="p_qty_in")
            p_price = st.number_input("سعر الشراء للوحدة", value=100.0, key="p_price_in")
            
            p_sub = (p_price * p_qty)
            p_tax = p_sub * 0.15
            p_total = p_sub + p_tax
            
            st.info(f"إجمالي سطر المشتريات شامل الضريبة: {p_total:,.2f} ر.س")
            
            col_pb1, col_pb2, col_pb3 = st.columns(3)
            if col_pb1.form_submit_button("حفظ طلب الشراء 💾"):
                st.session_state['purchases_workflow_db'].append({
                    "رقم المستند": p_doc_num,
                    "المورد": p_supplier,
                    "التاريخ": str(p_date),
                    "الحالة": p_status,
                    "الإجمالي شامل ض ق م": p_total
                })
                st.success("تم حفظ طلب الشراء بنجاح!")
        
        if st.session_state['purchases_workflow_db']:
            render_arabic_table_with_controls(pd.DataFrame(st.session_state['purchases_workflow_db']), "طلبات_الشراء")

    with pur_tab2:
        st.markdown("#### فاتورة المشتريات الضريبية الكاملة (تزيد المخزون وتنشئ قيد تلقائي)")
        with st.form("pur_invoice_form"):
            cp_i1, cp_i2, cp_i3 = st.columns(3)
            with cp_i1:
                pin_num = st.text_input("رقم فاتورة المشتريات", value=f"PINV-{int(datetime.now().timestamp())}")
                pin_supp = st.selectbox("المورد للفاتورة", list(st.session_state['suppliers_db'].keys()))
                
                supp_data = st.session_state['suppliers_db'][pin_supp]
                st.markdown(f"""
                    <div style='background:#f8f9fa; padding:10px; border-radius:5px; font-size:12px; color:#2d3748;'>
                        <b>السجل التجاري:</b> {supp_data['رقم السجل']}<br>
                        <b>الرقم الضريبي:</b> {supp_data['الرقم الضريبي']}<br>
                        <b>العنوان:</b> {supp_data['العنوان']}
                    </div>
                """, unsafe_allow_html=True)
                
            with cp_i2:
                pin_date = st.date_input("تاريخ الفاتورة", value=datetime.now(), key="pin_date_k")
                pin_pay = st.selectbox("طريقة السداد", ["أجل (إلى حساب المورد)", "نقدي (صندوق)", "تحويل بنكي"])
                
                pin_dest = ""
                if pin_pay == "نقدي (صندوق)":
                    pin_dest = st.selectbox("اختر الصندوق للصرف", st.session_state['cash_boxes_db'], key="pin_box_k")
                elif pin_pay == "تحويل بنكي":
                    pin_dest = st.selectbox("اختر البنك للتحويل", st.session_state['banks_db'], key="pin_bank_k")
                else:
                    pin_dest = "حساب الموردين (أجل)"

            with cp_i3:
                pin_warehouse = st.selectbox("المستودع المضاف إليه", st.session_state['warehouses_db'], key="pin_wh_k")
            
            st.markdown("---")
            pin_item = st.selectbox("المنتج المشتري", list(st.session_state['inventory_stock'].keys()), format_func=lambda x: f"{x} - {st.session_state['inventory_stock'][x]['اسم المنتج']}", key="pin_item_k")
            pin_qty = st.number_input("الكمية المشتراة", min_value=1.0, value=1.0, key="pin_q_k")
            pin_price = st.number_input("سعر التكلفة", value=100.0, key="pin_pr_k")
            
            pin_subtotal = pin_qty * pin_price
            pin_tax_val = pin_subtotal * 0.15
            pin_total_incl = pin_subtotal + pin_tax_val
            
            if st.form_submit_button("حفظ فاتورة المشتريات وزيادة المخزون 💾"):
                st.session_state['inventory_stock'][pin_item]["الكمية المتاحة"] += pin_qty
                
                st.session_state['general_ledger'].append({
                    "رقم المستند": pin_num,
                    "الالتزام/النوع": "فاتورة ضريبية مشتريات",
                    "التاريخ": str(pin_date),
                    "البيان": f"مشتريات من المورد {pin_supp} برقم {pin_num}",
                    "المدين": pin_total_incl,
                    "الدائن": pin_total_incl,
                    "الحساب الطرف": pin_dest
                })
                
                st.session_state['purchases_invoices_full_db'].append({
                    "رقم الفاتورة": pin_num,
                    "المورد": pin_supp,
                    "التاريخ": str(pin_date),
                    "طريقة السداد": pin_pay,
                    "الإجمالي شامل ض ق م": pin_total_incl
                })
                st.success("تم حفظ فاتورة المشتريات وزيادة المخزون وإنشاء القيد المحاسبي بنجاح!")
        
        if st.session_state['purchases_invoices_full_db']:
            render_arabic_table_with_controls(pd.DataFrame(st.session_state['purchases_invoices_full_db']), "فواتير_المشتريات")

    with pur_tab3:
        st.markdown("#### 📊 تقرير المشتريات الشامل")
        if st.session_state['purchases_invoices_full_db']:
            render_arabic_table_with_controls(pd.DataFrame(st.session_state['purchases_invoices_full_db']), "تقرير_المشتريات")
        else:
            st.info("لا توجد بيانات مشتريات متاحة.")

# --- المخزون ---
elif main_menu == "المخزون":
    st.markdown("<h3 style='color: #714B67;'>📋 موديول المخزون والجرد المستمر</h3>", unsafe_allow_html=True)
    stock_rows = [{"كود المنتج": k, "اسم المنتج": v["اسم المنتج"], "السعر الأساسي": v["السعر"], "الكمية المتاحة": v["الكمية المتاحة"]} for k, v in st.session_state['inventory_stock'].items()]
    render_arabic_table_with_controls(pd.DataFrame(stock_rows), "أرصدة_المخزون")

# --- المحاسبة والشجرة ---
elif main_menu == "المحاسبة والشجرة":
    st.markdown("<h3 style='color: #714B67;'>💰 المحاسبة والقيود التلقائية (دفتر الأستاذ)</h3>", unsafe_allow_html=True)
    if st.session_state['general_ledger']:
        render_arabic_table_with_controls(pd.DataFrame(st.session_state['general_ledger']), "دفتر_الأستاذ")
    else:
        st.info("لا توجد قيود محاسبية مسجلة حتى الآن (تتم إضافتها تلقائياً عند حفظ الفواتير).")

# --- الصلاحيات ---
elif main_menu == "الصلاحيات":
    st.markdown("<h3 style='color: #714B67;'>🔐 إدارة الصلاحيات والمستخدمين</h3>", unsafe_allow_html=True)
    perm_rows = [{"اسم المستخدم": k, "الاسم الكامل": v["اسم الكامل"], "الدور": v["الدور"], "الحالة": v["الحالة"]} for k, v in st.session_state['users_permissions_db'].items()]
    render_arabic_table_with_controls(pd.DataFrame(perm_rows), "المستخدمين")

# --- الإعدادات ---
elif main_menu == "الإعدادات":
    st.markdown("<h3 style='color: #714B67;'>⚙️ الإعدادات العامة</h3>", unsafe_allow_html=True)
    if st.button("🔄 إعادة تصفير البرنامج بالكامل"):
        reset_system_to_default()
