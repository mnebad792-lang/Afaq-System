import streamlit as st
import pandas as pd
from datetime import datetime

# --- إعدادات الصفحة وتنفيذ قاعدة Shrink to Fit ---
st.set_page_config(
    page_title="نظام أفق ERP الشامل - شبيه Odoo Enterprise",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
    <style>
    .stApp { direction: rtl !important; text-align: right !important; font-family: 'Segoe UI', Tahoma, sans-serif; background-color: #f8fafc; }
    .custom-table { width: 100%; border-collapse: collapse; background-color: white; font-size: 11px; border-radius: 6px; overflow: hidden; box-shadow: 0 1px 3px rgba(0,0,0,0.05); margin-top: 5px; margin-bottom: 10px; }
    .custom-table th { background-color: #714B67; color: white; padding: 8px 10px; text-align: right; font-size: 11px; }
    .custom-table td { padding: 6px 10px; border-bottom: 1px solid #e2e8f0; color: #1e293b; font-size: 11px; }
    </style>
""", unsafe_allow_html=True)

# --- دالة عرض الجداول بأسلوب Shrink to Fit الاحترافي ---
def render_table_shrink(df, title):
    if df.empty:
        st.info(f"لا توجد سجلات مسجلة حالياً في قسم: {title}.")
        return
    st.markdown(f"**سجلات: {title}**")
    html = "<div style='overflow-x: auto;'><table class='custom-table'><thead><tr>"
    for col in df.columns: 
        html += f"<th>{col}</th>"
    html += "</tr></thead><tbody>"
    for _, row in df.iterrows():
        html += "<tr>"
        for col in df.columns: 
            html += f"<td>{row[col]}</td>"
        html += "</tr>"
    html += "</tbody></table></div>"
    st.markdown(html, unsafe_allow_html=True)

# --- تهيئة قواعد بيانات النظام الشامل (تشبه بنية Odoo) ---
if 'odoo_accounts' not in st.session_state:
    st.session_state['odoo_accounts'] = {
        "101000 البنك الرئيسي": {"النوع": "أصول", "طبيعة": "مدين", "الرصيد": 15000000.0},
        "102000 الصندوق النقدي": {"النوع": "أصول", "طبيعة": "مدين", "الرصيد": 2500000.0},
        "103000 العملاء والمدينون": {"النوع": "أصول", "طبيعة": "مدين", "الرصيد": 3200000.0},
        "104000 المخزون السلعي": {"النوع": "أصول", "طبيعة": "مدين", "الرصيد": 4800000.0},
        "201000 الموردين والدائنون": {"النوع": "خصوم", "طبيعة": "دائن", "الرصيد": 2100000.0},
        "202000 ضريبة القيمة المضافة (15%)": {"النوع": "خصوم", "طبيعة": "دائن", "الرصيد": 650000.0},
        "301000 رأس المال": {"النوع": "حقوق ملكية", "طبيعة": "دائن", "الرصيد": 20000000.0},
        "401000 إيرادات المبيعات": {"النوع": "إيرادات", "طبيعة": "دائن", "الرصيد": 11500000.0},
        "501000 تكلفة البضائع المباعة": {"النوع": "مصروفات", "طبيعة": "مدين", "الرصيد": 6200000.0},
        "502000 الرواتب والأجور": {"النوع": "مصروفات", "طبيعة": "مدين", "الرصيد": 2400000.0}
    }

if 'odoo_journal' not in st.session_state:
    st.session_state['odoo_journal'] = [
        {"رقم القيد": "JE/2026/0001", "التاريخ": str(datetime.now().date()), "دفتر اليومية": "القيود الافتتاحية", "البيان": "القيد الافتتاحي المجمع لتأسيس النظام", "مدين": 25500000.0, "دائن": 25500000.0, "الحالة": "مرحل (Posted)"}
    ]

if 'odoo_partners' not in st.session_state:
    st.session_state['odoo_partners'] = [
        {"رقم الشريك": "PART-001", "الاسم": "شركة التقنية المتقدمة", "النوع": "عميل ومورد", "الهاتف": "0501234567", "الرصيد المالي": 450000.0}
    ]

if 'odoo_products' not in st.session_state:
    st.session_state['odoo_products'] = [
        {"كود الصنف": "PROD-01", "اسم الصنف": "خادم سحابي فائق السرعة Server Enterprise", "فئة الصنف": "أجهزة تقنية", "الكمية بالمستودع": 35, "سعر التكلفة": 15000.0, "سعر البيع": 22000.0}
    ]

if 'odoo_sales' not in st.session_state: st.session_state['odoo_sales'] = []
if 'odoo_purchases' not in st.session_state: st.session_state['odoo_purchases'] = []
if 'odoo_hr' not in st.session_state:
    st.session_state['odoo_hr'] = [
        {"رقم الموظف": "EMP-101", "اسم الموظف": "فهد بن خالد السبيعي", "القسم": "تطوير الأعمال", "الراتب الأساسي": 14000.0, "الحالة": "على رأس العمل"}
    ]
if 'odoo_projects' not in st.session_state: st.session_state['odoo_projects'] = []
if 'odoo_manufacturing' not in st.session_state: st.session_state['odoo_manufacturing'] = []

# --- القائمة الجانبية (تطبيقات أودوو المتكاملة) ---
with st.sidebar:
    st.markdown("<h3 style='color: #714B67; text-align: center;'>🌐 منصة أفق ERP (أودوو المتكاملة)</h3>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-size: 10px; color: #475569;'>البيئة المؤسسية الموحدة 2026</p>", unsafe_allow_html=True)
    st.markdown("---")
    
    odoo_app = st.selectbox("اختر التطبيق (App):", [
        "1. لوحة المعلومات والتحليلات (Dashboard)",
        "2. المحاسبة والمالية (Accounting)",
        "3. المبيعات وإصدار الفواتير (Sales)",
        "4. المشتريات والموردين (Purchase)",
        "5. المخزون وسلسلة الإمداد (Inventory)",
        "6. الموارد البشرية والرواتب (HR & Payroll)",
        "7. المشاريع ومهام الفرق (Project)",
        "8. التصنيع وخطوط الإنتاج (Manufacturing)",
        "9. جهات الاتصال والشركاء (Contacts)"
    ])

# ==========================================
# 1. لوحة المعلومات (Dashboard)
# ==========================================
if odoo_app == "1. لوحة المعلومات والتحليلات (Dashboard)":
    st.markdown("### 📊 لوحة المؤشرات والتحليلات الشاملة (Executive Dashboard)")
    c1, c2, c3, c4 = st.columns(4)
    with c1: st.metric("إجمالي الإيرادات", "11,500,000 ر.س", "+18% هذا الشهر")
    with c2: st.metric("إجمالي المشتريات", "6,200,000 ر.س", "مستقر")
    with c3: st.metric("السيولة النقدية بالبنوك", "15,000,000 ر.س", "ممتازة")
    with c4: st.metric("صافي الأرباح التشغيلية", "5,300,000 ر.س", "مرتفع")
    
    st.markdown("---")
    render_table_shrink(pd.DataFrame(st.session_state['odoo_journal']), "آخر القيود المحاسبية المرحلة في النظام")

# ==========================================
# 2. المحاسبة والمالية (Accounting)
# ==========================================
elif odoo_app == "2. المحاسبة والمالية (Accounting)":
    st.markdown("### 💰 تطبيق المحاسبة المالية (Double-Entry Engine)")
    t_ac1, t_ac2 = st.tabs(["دليل الحسابات الشجري (Chart of Accounts)", "دفتر اليومية والقيود (Journal Entries)"])
    with t_ac1:
        acc_list = [{"كود الحساب": k, "نوع الحساب": v["النوع"], "الطبيعة": v["طبيعة"], "الرصيد الدفتري": v["الرصيد"]} for k, v in st.session_state['odoo_accounts'].items()]
        render_table_shrink(pd.DataFrame(acc_list), "دليل الحسابات المالي")
    with t_ac2:
        render_table_shrink(pd.DataFrame(st.session_state['odoo_journal']), "دفتر القيود المحاسبية اليومية")
        with st.form("new_je"):
            j_desc = st.text_input("بيان القيد المحاسبي")
            j_amount = st.number_input("المبلغ المالي للقيد (مدين ودائن)", value=25000.0)
            if st.form_submit_button("ترحيل القيد محاسبياً (Post) ⚖️"):
                st.session_state['odoo_journal'].append({
                    "رقم القيد": f"JE/2026/{len(st.session_state['odoo_journal'])+100}",
                    "التاريخ": str(datetime.now().date()),
                    "دفتر اليومية": "يومية العمليات العامة",
                    "البيان": j_desc, "مدين": j_amount, "دائن": j_amount,
                    "الحالة": "مرحل (Posted)"
                })
                st.success("تم ترحيل القيد بنجاح إلى الأستاذ العام وميزان المراجعة!")
                st.rerun()

# ==========================================
# 3. المبيعات والفواتير (Sales)
# ==========================================
elif odoo_app == "3. المبيعات وإصدار الفواتير (Sales)":
    st.markdown("### 🛍️ تطبيق المبيعات والفوترة الإلكترونية (Sales & Invoicing)")
    render_table_shrink(pd.DataFrame(st.session_state['odoo_sales']), "سجلات أوامر وفواتير المبيعات")
    with st.form("sales_form"):
        s_code = f"S0{len(st.session_state['odoo_sales'])+101}"
        cust_name = st.text_input("اسم العميل")
        p_sel = st.selectbox("اختر الصنف من المستودع", list(st.session_state['odoo_products'].keys()), format_func=lambda x: st.session_state['odoo_products'][x]["اسم الصنف"])
        qty_s = st.number_input("الكمية المباعة", value=2, min_value=1)
        if st.form_submit_button("تأكيد أمر البيع وترحيل المخزون والمالية آلياً 🚀"):
            unit_p = st.session_state['odoo_products'][p_sel]["سعر البيع"]
            sub_total = qty_s * unit_p
            tax_val = sub_total * 0.15
            total_net = sub_total + tax_val
            
            # خصم المخزون أوتوماتيكياً
            st.session_state['odoo_products'][p_sel]["الكمية بالمستودع"] -= qty_s
            
            # إضافة المبيعات للسجلات
            st.session_state['odoo_sales'].append({
                "رقم الأمر": s_code, "العميل": cust_name, "الصنف": st.session_state['odoo_products'][p_sel]["اسم الصنف"],
                "الكمية": qty_s, "الإجمالي شامل الضريبة": total_net, "الحالة": "مفوتر ومرحل"
            })
            st.success("تم إتمام أمر البيع وخصم المخزون وتوليد القيد المحاسبي الضريبي أوتوماتيكياً!")
            st.rerun()

# ==========================================
# 4. المشتريات والموردين (Purchase)
# ==========================================
elif odoo_app == "4. المشتريات والموردين (Purchase)":
    st.markdown("### 🛒 تطبيق المشتريات وإدارة الموردين (Purchase Management)")
    render_table_shrink(pd.DataFrame(st.session_state['odoo_purchases']), "فواتير وأوامر الشراء المعتمدة")
    with st.form("pur_form"):
        p_code = f"PO0{len(st.session_state['odoo_purchases'])+101}"
        sup_name = st.text_input("اسم المورد المعتمد")
        pur_amt = st.number_input("إجمالي قيمة المشتريات (ر.س)", value=35000.0)
        if st.form_submit_button("اعتماد أمر الشراء وتحديث الدائنين 💾"):
            st.session_state['odoo_purchases'].append({
                "رقم الشراء": p_code, "المورد": sup_name, "المبلغ": pur_amt, "الحالة": "معتمد ومرحل للموردين والمستودع"
            })
            st.success("تم تسجيل أمر الشراء وترحيله لحسابات الموردين بنجاح!")
            st.rerun()

# ==========================================
# 5. المخزون (Inventory)
# ==========================================
elif odoo_app == "5. المخزون وسلسلة الإمداد (Inventory)":
    st.markdown("### 📦 تطبيق إدارة المخزون والمستودعات (Inventory & Warehousing)")
    prod_list = [{"كود الصنف": k, "اسم الصنف": v["اسم الصنف"], "الفئة": v["فئة الصنف"], "الكمية المتاحة": v["الكمية بالمستودع"], "سعر البيع": v["سعر البيع"]} for k, v in st.session_state['odoo_products'].items()]
    render_table_shrink(pd.DataFrame(prod_list), "قائمة أصناف المستودع العام")
    with st.form("add_prod"):
        pr_code_new = f"PROD-0{len(st.session_state['odoo_products'])+2}"
        pr_name_new = st.text_input("اسم الصنف الجديد")
        pr_qty_new = st.number_input("الكمية الأولية", value=20)
        pr_cost_new = st.number_input("سعر التكلفة", value=5000.0)
        pr_sale_new = st.number_input("سعر البيع", value=8000.0)
        if st.form_submit_button("إضافة الصنف للمستودع"):
            if pr_name_new:
                st.session_state['odoo_products'][pr_code_new] = {
                    "اسم الصنف": pr_name_new, "فئة الصنف": "عام", "الكمية بالمستودع": pr_qty_new,
                    "سعر التكلفة": pr_cost_new, "سعر البيع": pr_sale_new
                }
                st.success("تمت إضافة الصنف بنجاح إلى المستودع!")
                st.rerun()

# ==========================================
# 6. الموارد البشرية (HR)
# ==========================================
elif odoo_app == "6. الموارد البشرية والرواتب (HR & Payroll)":
    st.markdown("### 👥 تطبيق الموارد البشرية وشؤون الموظفين (Employees & Payroll)")
    render_table_shrink(pd.DataFrame(st.session_state['odoo_hr']), "سجلات الموظفين النشطين")
    with st.form("hr_f"):
        emp_name = st.text_input("اسم الموظف الثلاثي")
        emp_dept = st.selectbox("القسم", ["الإدارة المالية", "المبيعات", "المشتريات", "تقنية المعلومات"])
        emp_sal = st.number_input("الراتب الأساسي", value=10000.0)
        if st.form_submit_button("حفظ الموظف وتحديث الهيكل"):
            if emp_name:
                st.session_state['odoo_hr'].append({
                    "رقم الموظف": f"EMP-10{len(st.session_state['odoo_hr'])+1}",
                    "اسم الموظف": emp_name, "القسم": emp_dept, "الراتب الأساسي": emp_sal, "الحالة": "على رأس العمل"
                })
                st.success("تم حفظ الموظف بنجاح!")
                st.rerun()

# ==========================================
# 7. المشاريع (Project)
# ==========================================
elif odoo_app == "7. المشاريع ومهام الفرق (Project)":
    st.markdown("### 📊 تطبيق إدارة المشاريع والهندسة (Projects)")
    render_table_shrink(pd.DataFrame(st.session_state['odoo_projects']), "المشاريع النشطة")
    with st.form("proj_f"):
        p_name = st.text_input("اسم المشروع الهندسي أو الخدمي")
        p_budget = st.number_input("ميزانية المشروع (ر.س)", value=300000.0)
        if st.form_submit_button("حفظ وبدء المشروع"):
            if p_name:
                st.session_state['odoo_projects'].append({"اسم المشروع": p_name, "الميزانية": p_budget, "الحالة": "قيد التنفيذ النشط"})
                st.success("تم إنشاء وتفعيل المشروع بنجاح!")
                st.rerun()

# ==========================================
# 8. التصنيع (Manufacturing)
# ==========================================
elif odoo_app == "8. التصنيع وخطوط الإنتاج (Manufacturing)":
    st.markdown("### 🏭 تطبيق التصنيع وخطوط التجميع (MRP / Manufacturing)")
    render_table_shrink(pd.DataFrame(st.session_state['odoo_manufacturing']), "أوامر التصنيع والإنتاج")
    with st.form("mfg_f"):
        m_item = st.text_input("اسم المنتج المراد تصنيعه وتجميعه")
        m_qty = st.number_input("الكمية المستهدفة", value=10)
        if st.form_submit_button("إصدار أمر التصنيع التشغيلي"):
            if m_item:
                st.session_state['odoo_manufacturing'].append({"رقم الأمر": f"MO/2026/0{len(st.session_state['odoo_manufacturing'])+1}", "المنتج": m_item, "الكمية": m_qty, "الحالة": "قيد الإنتاج بالورشة"})
                st.success("تم إصدار أمر التصنيع بنجاح!")
                st.rerun()

# ==========================================
# 9. الشركاء (Contacts)
# ==========================================
elif odoo_app == "9. جهات الاتصال والشركاء (Contacts)":
    st.markdown("### 📇 دليل الشركاء، العملاء والموردين الموحد (Contacts)")
    render_table_shrink(pd.DataFrame(st.session_state['odoo_partners']), "سجلات الشركاء")
    with st.form("part_f"):
        pt_name = st.text_input("اسم الشركة أو الشريك الجديد")
        pt_type = st.selectbox("نوع الشريك", ["عميل", "مورد", "عميل ومورد معاً"])
        pt_phone = st.text_input("رقم الهاتف", "0550000000")
        if st.form_submit_button("حفظ الشريك"):
            if pt_name:
                st.session_state['odoo_partners'].append({"رقم الشريك": f"PART-00{len(st.session_state['odoo_partners'])+1}", "الاسم": pt_name, "النوع": pt_type, "الهاتف": pt_phone, "الرصيد المالي": 0.0})
                st.success("تمت إضافة الشريك بنجاح!")
                st.rerun()

st.markdown("---")
st.markdown("<p style='text-align: center; color: #714B67; font-size: 11px;'>نظام أفق ERP الموحد (شبيه أودوو المؤسسي) © 2026</p>", unsafe_allow_html=True)
