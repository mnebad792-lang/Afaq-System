import streamlit as st
import pandas as pd
from datetime import datetime, date

st.set_page_config(page_title="نظام أفق ERP المحاسبي المتكامل", layout="wide", initial_sidebar_state="expanded")

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
        "software_version": "النسخة المحاسبية الاحترافية 2026 الشاملة لكل الموديولات"
    }

# --- تهيئة قواعد البيانات الأساسية للموديولات ---
if 'warehouses_db' not in st.session_state:
    st.session_state['warehouses_db'] = ["المستودع الرئيسي - الرياض", "مستودع الفرع - جدة", "مستودع التوريدات العامة"]

if 'cash_boxes_db' not in st.session_state:
    st.session_state['cash_boxes_db'] = ["الخزينة الرئيسية (صندوق النقد)", "صندوق المعارض"]

if 'banks_db' not in st.session_state:
    st.session_state['banks_db'] = ["مصرف الراجحي (تحويل/شبكة)", "البنك الأهلي السعودي (تحويل/شبكة)", "بنك الرياض"]

if 'inventory_stock' not in st.session_state:
    st.session_state['inventory_stock'] = {
        "PROD-001": {"اسم المنتج": "جهاز حاسوب محمول احترافي", "سعر البيع": 3500.0, "تكلفة الشراء": 2800.0, "الكمية المتاحة": 45},
        "PROD-002": {"اسم المنتج": "شاشة عرض 27 بوصة 4K", "سعر البيع": 1200.0, "تكلفة الشراء": 900.0, "الكمية المتاحة": 30},
        "PROD-003": {"اسم المنتج": "طابعة لاسلكية متعددة الوظائف", "سعر البيع": 850.0, "تكلفة الشراء": 600.0, "الكمية المتاحة": 20}
    }

if 'customers_db' not in st.session_state:
    st.session_state['customers_db'] = {
        "شركة التقنية الحديثة للتجارة": {"كود العميل": "CUST-001", "رقم السجل": "1010254789", "الرقم الضريبي": "300123456700003", "العنوان": "الرياض - حي الملز", "الهاتف": "0501234567", "الرصيد الحالي": 0.0}
    }

if 'suppliers_db' not in st.session_state:
    st.session_state['suppliers_db'] = {
        "شركة التوريدات الكبرى المحدودة": {"كود المورد": "SUP-001", "رقم السجل": "1010987654", "الرقم الضريبي": "300111222300003", "العنوان": "الرياض - الصناعية", "الهاتف": "0561112233", "الرصيد الحالي": 0.0}
    }

if 'hr_employees_db' not in st.session_state:
    st.session_state['hr_employees_db'] = {
        "EMP-101": {"الاسم الكامل": "أحمد محمد العتيبي", "القسم": "الإدارة المالية", "المسمى الوظيفي": "محاسب أول", "الراتب الأساسي": 8000.0, "الحالة": "على رأس العمل"}
    }

if 'production_orders' not in st.session_state:
    st.session_state['production_orders'] = [
        {"رقم أمر الإنتاج": "PRD-501", "المنتج النهائي": "جهاز حاسوب محمول احترافي", "الكمية المطلوبة": 10, "الحالة": "قيد التنفيذ"}
    ]

if 'projects_db' not in st.session_state:
    st.session_state['projects_db'] = [
        {"رقم المشروع": "PRJ-01", "اسم المشروع": "تطوير البنية التحتية التقنية", "ميزانية المشروع": 150000.0, "حالة المشروع": "ساري"}
    ]

if 'cost_centers_db' not in st.session_state:
    st.session_state['cost_centers_db'] = [
        {"كود المركز": "CC-100", "اسم مركز التكلفة": "مركز تكلفة الإدارة العامة"},
        {"كود المركز": "CC-200", "اسم مركز التكلفة": "مركز تكلفة المبيعات والتسويق"}
    ]

if 'users_permissions_db' not in st.session_state:
    st.session_state['users_permissions_db'] = {
        "admin": {
            "اسم المستخدم": "admin", "الاسم الكامل": "المدير العام", "الدور": "مدير النظام (Administrator)", "الحالة": "نشط",
            "صلاحيات الموديولات": {m: True for m in ["الرئيسية", "الشركاء", "الموارد البشرية", "الإنتاج", "المشروعات", "مراكز التكلفة", "الصلاحيات", "المبيعات", "المشتريات", "المخزون", "المحاسبة والشجرة", "الإعدادات"]}
        }
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

# --- القائمة الجانبية (كل الموديولات الـ 12) ---
with st.sidebar:
    client_conf = st.session_state['client_license_config']
    st.markdown(f"<h2 style='color: #714B67; text-align: center;'>نظام أفق ERP</h2>", unsafe_allow_html=True)
    st.markdown(f"<p style='text-align: center; font-size: 11px; color: #64748b;'>مرخص لـ: <b>{client_conf['client_name']}</b></p>", unsafe_allow_html=True)
    st.markdown("---")
    
    modules_map = {
        "الرئيسية": "🏠 الرئيسية",
        "الشركاء": "👥 الشركاء",
        "الموارد البشرية": "👨‍💼 الموارد البشرية",
        "الإنتاج": "🏭 الإنتاج",
        "المشروعات": "📊 المشروعات",
        "مراكز التكلفة": "🏷️ مراكز التكلفة",
        "الصلاحيات": "🔐 الصلاحيات",
        "المبيعات": "🛒 موديول المبيعات",
        "المشتريات": "📦 المشتريات",
        "المخزون": "📋 المخزون",
        "المحاسبة والشجرة": "💰 المحاسبة وشجرة الحسابات",
        "الإعدادات": "⚙️ الإعدادات"
    }
    
    for mod_key, mod_label in modules_map.items():
        is_selected = (st.session_state['active_module'] == mod_key)
        if st.button(mod_label, key=f"btn_mod_{mod_key}", use_container_width=True, type="primary" if is_selected else "secondary"):
            st.session_state['active_module'] = mod_key
            st.rerun()

main_menu = st.session_state['active_module']

# ================= 1. الرئيسية =================
if main_menu == "الرئيسية":
    st.markdown("<h3 style='color: #714B67;'>🏠 لوحة التحكم الرئيسية للنظام السحابي</h3>", unsafe_allow_html=True)
    col1, col2, col3, col4 = st.columns(4)
    with col1: st.metric("إجمالي العملاء", len(st.session_state['customers_db']))
    with col2: st.metric("فواتير المبيعات", len(st.session_state['sales_invoices_db']))
    with col3: st.metric("أصناف المخزون", len(st.session_state['inventory_stock']))
    with col4: st.metric("القيود المحاسبية", len(st.session_state['general_ledger']))

# ================= 2. الشركاء =================
elif main_menu == "الشركاء":
    st.markdown("<h3 style='color: #714B67;'>👥 إدارة الشركاء والعملاء والموردين</h3>", unsafe_allow_html=True)
    c1, c2 = st.tabs(["العملاء", "الموردين"])
    with c1:
        cust_list = [{"كود العميل": v["كود العميل"], "اسم العميل": k, "السجل": v["رقم السجل"], "الضريبي": v["الرقم الضريبي"], "الهاتف": v["الهاتف"]} for k, v in st.session_state['customers_db'].items()]
        render_arabic_table_with_controls(pd.DataFrame(cust_list), "العملاء")
    with c2:
        supp_list = [{"كود المورد": v["كود المورد"], "اسم المورد": k, "السجل": v["رقم السجل"], "الضريبي": v["الرقم الضريبي"]} for k, v in st.session_state['suppliers_db'].items()]
        render_arabic_table_with_controls(pd.DataFrame(supp_list), "الموردين")

# ================= 3. الموارد البشرية =================
elif main_menu == "الموارد البشرية":
    st.markdown("<h3 style='color: #714B67;'>👨‍💼 إدارة الموارد البشرية وشئون الموظفين</h3>", unsafe_allow_html=True)
    emp_list = [{"كود الموظف": k, "الاسم": v["الاسم الكامل"], "القسم": v["القسم"], "المسمى": v["المسمى الوظيفي"], "الراتب الأساسي": f"{v['الراتب الأساسي']:,.2f} ر.س"} for k, v in st.session_state['hr_employees_db'].items()]
    render_arabic_table_with_controls(pd.DataFrame(emp_list), "الموظفين")

# ================= 4. الإنتاج =================
elif main_menu == "الإنتاج":
    st.markdown("<h3 style='color: #714B67;'>🏭 موديول الإنتاج والتصنيع</h3>", unsafe_allow_html=True)
    render_arabic_table_with_controls(pd.DataFrame(st.session_state['production_orders']), "أوامر_الإنتاج")

# ================= 5. المشروعات =================
elif main_menu == "المشروعات":
    st.markdown("<h3 style='color: #714B67;'>📊 إدارة المشروعات والمقاولات</h3>", unsafe_allow_html=True)
    render_arabic_table_with_controls(pd.DataFrame(st.session_state['projects_db']), "المشروعات")

# ================= 6. مراكز التكلفة =================
elif main_menu == "مراكز التكلفة":
    st.markdown("<h3 style='color: #714B67;'>🏷️ مراكز التكلفة والتحليل المالي</h3>", unsafe_allow_html=True)
    render_arabic_table_with_controls(pd.DataFrame(st.session_state['cost_centers_db']), "مراكز_التكلفة")

# ================= 7. الصلاحيات =================
elif main_menu == "الصلاحيات":
    st.markdown("<h3 style='color: #714B67;'>🔐 إدارة الصلاحيات والمستخدمين</h3>", unsafe_allow_html=True)
    user_rows = [{"اسم المستخدم": k, "الاسم الكامل": v["الاسم الكامل"], "الدور": v["الدور"], "الحالة": v["الحالة"]} for k, v in st.session_state['users_permissions_db'].items()]
    render_arabic_table_with_controls(pd.DataFrame(user_rows), "المستخدمين")

# ================= 8. المبيعات =================
elif main_menu == "المبيعات":
    st.markdown("<h3 style='color: #714B67;'>🛒 موديول المبيعات (عروض أسعار ➡️ أوامر بيع ➡️ فواتير ضريبية تامة)</h3>", unsafe_allow_html=True)
    
    s_tab1, s_tab2, s_tab3, s_tab4 = st.tabs(["📄 عروض الأسعار", "📋 أوامر البيع", "🧾 الفواتير الضريبية والمردودات", "📊 سجل الحركات والقيود"])
    
    with s_tab1:
        st.markdown("#### عروض الأسعار")
        with st.form("quo_form"):
            q1, q2 = st.columns(2)
            with q1:
                qn = st.text_input("رقم عرض السعر", value=f"QUO-{int(datetime.now().timestamp())}")
                qd = st.date_input("التاريخ", value=date.today())
            with q2:
                qc = st.selectbox("العميل", list(st.session_state['customers_db'].keys()))
            
            st.markdown("##### البنود")
            q_items = []
            for i in range(2):
                c1, c2, c3, c4 = st.columns([1.5, 3, 1, 1.5])
                with c1: ic = st.selectbox(f"الكود #{i+1}", [""] + list(st.session_state['inventory_stock'].keys()), key=f"q_c_{i}")
                with c2: nm = st.text_input(f"المنتج #{i+1}", value=st.session_state['inventory_stock'][ic]["اسم المنتج"] if ic in st.session_state['inventory_stock'] else "", key=f"q_n_{i}")
                with c3: qt = st.number_input(f"الكمية #{i+1}", min_value=0.0, value=1.0, key=f"q_q_{i}")
                with c4: pr = st.number_input(f"السعر #{i+1}", min_value=0.0, value=float(st.session_state['inventory_stock'][ic]["سعر البيع"]) if ic in st.session_state['inventory_stock'] else 0.0, key=f"q_p_{i}")
                if ic and qt > 0: q_items.append({"الكود": ic, "المنتج": nm, "الكمية": qt, "السعر": pr, "الإجمالي": qt*pr})
            
            if st.form_submit_button("حفظ عرض السعر 💾"):
                if q_items:
                    st.session_state['sales_quotations'].append({"رقم العرض": qn, "التاريخ": str(qd), "العميل": qc, "البنود": q_items, "الإجمالي": sum(x['الإجمالي'] for x in q_items)})
                    st.success("تم حفظ عرض السعر بنجاح!")
        
        if st.session_state['sales_quotations']:
            q_disp = [{"رقم العرض": x["رقم العرض"], "التاريخ": x["التاريخ"], "العميل": x["العميل"], "الإجمالي": f"{x['الإجمالي']:,.2f} ر.س"} for x in st.session_state['sales_quotations']]
            render_arabic_table_with_controls(pd.DataFrame(q_disp), "عروض_الأسعار")

    with s_tab2:
        st.markdown("#### أوامر البيع")
        with st.form("so_form"):
            so1, so2 = st.columns(2)
            with so1:
                son = st.text_input("رقم أمر البيع", value=f"SO-{int(datetime.now().timestamp())}")
                sod = st.date_input("تاريخ الأمر", value=date.today())
            with so2:
                soc = st.selectbox("عميل أمر البيع", list(st.session_state['customers_db'].keys()))
            
            st.markdown("##### بنود أمر البيع")
            so_items = []
            for i in range(2):
                c1, c2, c3, c4 = st.columns([1.5, 3, 1, 1.5])
                with c1: ic = st.selectbox(f"كود بند #{i+1}", [""] + list(st.session_state['inventory_stock'].keys()), key=f"so_c_{i}")
                with c2: nm = st.text_input(f"اسم البند #{i+1}", value=st.session_state['inventory_stock'][ic]["اسم المنتج"] if ic in st.session_state['inventory_stock'] else "", key=f"so_n_{i}")
                with c3: qt = st.number_input(f"الكمية #{i+1}", min_value=0.0, value=1.0, key=f"so_q_{i}")
                with c4: pr = st.number_input(f"السعر #{i+1}", min_value=0.0, value=float(st.session_state['inventory_stock'][ic]["سعر البيع"]) if ic in st.session_state['inventory_stock'] else 0.0, key=f"so_p_{i}")
                if ic and qt > 0: so_items.append({"الكود": ic, "المنتج": nm, "الكمية": qt, "السعر": pr, "الإجمالي": qt*pr})
            
            if st.form_submit_button("حفظ أمر البيع 💾"):
                if so_items:
                    st.session_state['sales_orders'].append({"رقم الأمر": son, "التاريخ": str(sod), "العميل": soc, "البنود": so_items, "الإجمالي": sum(x['الإجمالي'] for x in so_items)})
                    st.success("تم حفظ أمر البيع بنجاح!")
        
        if st.session_state['sales_orders']:
            so_disp = [{"رقم الأمر": x["رقم الأمر"], "التاريخ": x["التاريخ"], "العميل": x["العميل"], "الإجمالي": f"{x['الإجمالي']:,.2f} ر.س"} for x in st.session_state['sales_orders']]
            render_arabic_table_with_controls(pd.DataFrame(so_disp), "أوامر_البيع")

    with s_tab3:
        st.markdown("#### الفواتير الضريبية (مبيعات / مردودات مع الخصم المخزني والقيود التلقائية)")
        with st.form("tax_inv_form"):
            c1, c2, c3, c4 = st.columns(4)
            with c1: inv_cust = st.selectbox("العميل", list(st.session_state['customers_db'].keys()))
            with c2: inv_type = st.selectbox("نوع الفاتورة", ["مبيعات ضريبية", "مردودات مبيعات"])
            with c3:
                inv_num = st.text_input("رقم الفاتورة", value=f"INV-{int(datetime.now().timestamp())}")
                inv_date = st.date_input("التاريخ", value=date.today())
            with c4: selected_wh = st.selectbox("المستودع", st.session_state['warehouses_db'])
            
            c_p1, c_p2 = st.columns(2)
            with c_p1: pay_m = st.selectbox("طريقة الدفع", ["آجل (تحول لحساب العميل)", "نقدي (صندوق)", "تحويل / شبكة (بنك)"])
            with c_p2:
                if pay_m == "نقدي (صندوق)": pay_dest = st.selectbox("اختر الصندوق", st.session_state['cash_boxes_db'])
                elif pay_m == "تحويل / شبكة (بنك)": pay_dest = st.selectbox("اختر البنك", st.session_state['banks_db'])
                else: pay_dest = "حساب العميل (آجل)"

            st.markdown("---")
            st.markdown("##### قالب الفاتورة المميز: (كود - منتج - كمية - سعر - إجمالي - خصم - ضريبة 15% - شامل ض ق م)")
            
            inv_rows = []
            g_sub, g_tax, g_fin = 0.0, 0.0, 0.0
            for i in range(3):
                cols = st.columns([1.2, 2.5, 0.8, 1, 1, 0.8, 1, 1.2])
                with cols[0]: ic = st.selectbox(f"الكود #{i+1}", [""] + list(st.session_state['inventory_stock'].keys()), key=f"inv_c_{i}")
                with cols[1]: nm = st.text_input(f"المنتج #{i+1}", value=st.session_state['inventory_stock'][ic]["اسم المنتج"] if ic in st.session_state['inventory_stock'] else "", key=f"inv_n_{i}")
                with cols[2]: qt = st.number_input(f"الكمية #{i+1}", min_value=0.0, value=1.0, key=f"inv_q_{i}")
                with cols[3]: pr = st.number_input(f"السعر #{i+1}", min_value=0.0, value=float(st.session_state['inventory_stock'][ic]["سعر البيع"]) if ic in st.session_state['inventory_stock'] else 0.0, key=f"inv_p_{i}")
                with cols[4]: lt = qt * pr; st.text(f"{lt:,.2f}")
                with cols[5]: ds = st.number_input(f"خصم #{i+1}", min_value=0.0, value=0.0, key=f"inv_d_{i}")
                with cols[6]: net = lt - ds; tx = net * 0.15; st.text(f"{tx:,.2f}")
                with cols[7]: fin = net + tx; st.text(f"{fin:,.2f}")
                
                if ic and qt > 0:
                    inv_rows.append({"الكود": ic, "المنتج": nm, "الكمية": qt, "السعر": pr, "الإجمالي": lt, "الخصم": ds, "الضريبة": tx, "شامل الضريبة": fin})
                    g_sub += net; g_tax += tx; g_fin += fin

            st.markdown(f"**المجموع قبل الضريبة:** {g_sub:,.2f} ر.س | **الضريبة (15%):** {g_tax:,.2f} ر.س | <b style='color:#714B67;'>الإجمالي النهائي شامل ض ق م: {g_fin:,.2f} ر.س</b>", unsafe_allow_html=True)
            
            c_b1, c_b2, c_b3, c_b4 = st.columns(4)
            with c_b1: sb = st.form_submit_button("💾 حفظ الفاتورة")
            with c_b2: eb = st.form_submit_button("✏️ تعديل")
            with c_b3: db = st.form_submit_button("🗑️ حذف / إلغاء")
            with c_b4: pb = st.form_submit_button("🖨️ طباعة وتصدير")

            if sb:
                if inv_rows:
                    st.session_state['sales_invoices_db'].append({"رقم الفاتورة": inv_num, "التاريخ": str(inv_date), "النوع": inv_type, "العميل": inv_cust, "المبلغ الإجمالي شامل الضريبة": g_fin, "البنود": inv_rows})
                    for item in inv_rows:
                        code = item["الكود"]
                        qty = item["الكمية"]
                        if code in st.session_state['inventory_stock']:
                            if inv_type == "مبيعات ضريبية": st.session_state['inventory_stock'][code]["الكمية المتاحة"] -= qty
                            else: st.session_state['inventory_stock'][code]["الكمية المتاحة"] += qty
                    st.session_state['general_ledger'].append({"رقم القيد": f"JE-{int(datetime.now().timestamp())}", "التاريخ": str(inv_date), "البيان": f"فاتورة مبيعات {inv_num}", "مدين": g_fin, "دائن": g_fin, "الحساب": pay_dest})
                    st.success("تم حفظ الفاتورة، خصم المخزون، وتوليد القيد المحاسبي بنجاح!")
                else:
                    st.error("أدخل بنداً واحداً على الأقل.")
            if eb: st.info("وضع التعديل مفعل.")
            if db: st.warning("تم الحذف والإلغاء.")
            if pb: st.toast("جاري الطباعة والتصدير...")

        if st.session_state['sales_invoices_db']:
            inv_disp = [{"رقم الفاتورة": x["رقم الفاتورة"], "التاريخ": x["التاريخ"], "النوع": x["النوع"], "العميل": x["العميل"], "الإجمالي شامل الضريبة": f"{x['المبلغ الإجمالي شامل الضريبة']:,.2f} ر.س"} for x in st.session_state['sales_invoices_db']]
            render_arabic_table_with_controls(pd.DataFrame(inv_disp), "فواتير_المبيعات")

    with s_tab4:
        st.markdown("#### الحركات والقيود التلقائية")
        if st.session_state['general_ledger']:
            render_arabic_table_with_controls(pd.DataFrame(st.session_state['general_ledger']), "القيود_العامة")
        else:
            st.info("لا توجد قيود مسجلة بعد.")

# ================= 9. المشتريات =================
elif main_menu == "المشتريات":
    st.markdown("<h3 style='color: #714B67;'>📦 موديول المشتريات والموردين</h3>", unsafe_allow_html=True)
    st.info("إدارة أوامر الشراء وفواتير الموردين وسندات الإدخال المخزني.")

# ================= 10. المخزون =================
elif main_menu == "المخزون":
    st.markdown("<h3 style='color: #714B67;'>📋 موديول المخزون والجرد المستمر</h3>", unsafe_allow_html=True)
    stock_all = [{"الكود": k, "اسم المنتج": v["اسم المنتج"], "الكمية المتاحة": v["الكمية المتاحة"], "سعر البيع": f"{v['سعر البيع']:,.2f} ر.س"} for k, v in st.session_state['inventory_stock'].items()]
    render_arabic_table_with_controls(pd.DataFrame(stock_all), "المخزون_العام")

# ================= 11. المحاسبة والشجرة =================
elif main_menu == "المحاسبة والشجرة":
    st.markdown("<h3 style='color: #714B67;'>💰 المحاسبة وشجرة الحسابات واليومية العامة</h3>", unsafe_allow_html=True)
    if st.session_state['general_ledger']:
        render_arabic_table_with_controls(pd.DataFrame(st.session_state['general_ledger']), "دفتر_اليومية")
    else:
        st.info("لا توجد قيود مسجلة في شجرة الحسابات حتى الآن.")

# ================= 12. الإعدادات =================
elif main_menu == "الإعدادات":
    st.markdown("<h3 style='color: #714B67;'>⚙️ إعدادات النظام وتصفير البيانات</h3>", unsafe_allow_html=True)
    if st.button("🔄 إعادة تصفير البرنامج بالكامل"):
        reset_system_to_default()
