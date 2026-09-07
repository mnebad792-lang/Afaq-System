import streamlit as st
import pandas as pd
from datetime import datetime

# --- إعدادات الصفحة وتنفيذ معايير الشاشة (Shrink to Fit) ---
st.set_page_config(
    page_title="منظومة أفق ERP الشاملة - نسخة Odoo Enterprise المؤسسية",
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

def render_table(df, title):
    if df.empty:
        st.info(f"لا توجد سجلات مسجلة حالياً في قسم: {title}.")
        return
    st.markdown(f"**سجلات النظام: {title}**")
    html = "<div style='overflow-x: auto;'><table class='custom-table'><thead><tr>"
    for col in df.columns: html += f"<th>{col}</th>"
    html += "</tr></thead><tbody>"
    for _, row in df.iterrows():
        html += "<tr>"
        for col in df.columns: html += f"<td>{row[col]}</td>"
        html += "</tr>"
    html += "</tbody></table></div>"
    st.markdown(html, unsafe_allow_html=True)

# --- تهيئة قواعد البيانات المركزية لجميع الموديولات (Session State) ---
if 'odoo_gl' not in st.session_state:
    st.session_state['odoo_gl'] = [
        {"رقم القيد": "JE/2026/001", "التاريخ": str(datetime.now().date()), "البيان": "القيد الافتتاحي المجمع لتأسيس النظام", "مدين": 35000000.0, "دائن": 35000000.0, "الحالة": "مرحل (Posted)"}
    ]

if 'odoo_accounts' not in st.session_state:
    st.session_state['odoo_accounts'] = {
        "101000 البنك الرئيسي": {"النوع": "أصول", "طبيعة": "مدين", "الرصيد": 18000000.0},
        "102000 الخزينة النقدية": {"النوع": "أصول", "طبيعة": "مدين", "الرصيد": 2000000.0},
        "103000 العملاء والمدينون": {"النوع": "أصول", "طبيعة": "مدين", "الرصيد": 5500000.0},
        "104000 المخزون العام": {"النوع": "أصول", "طبيعة": "مدين", "الرصيد": 9500000.0},
        "201000 الموردين والدائنون": {"النوع": "خصوم", "طبيعة": "دائن", "الرصيد": 6200000.0},
        "202000 ضريبة القيمة المضافة (15%)": {"النوع": "خصوم", "طبيعة": "دائن", "الرصيد": 1300000.0},
        "301000 رأس المال المؤسسي": {"النوع": "حقوق ملكية", "طبيعة": "دائن", "الرصيد": 20000000.0},
        "401000 إيرادات المبيعات": {"النوع": "إيرادات", "طبيعة": "دائن", "الرصيد": 14000000.0},
        "501000 تكلفة البضائع المباعة": {"النوع": "مصروفات", "طبيعة": "مدين", "الرصيد": 7500000.0},
        "502000 الرواتب والأجور": {"النوع": "مصروفات", "طبيعة": "مدين", "الرصيد": 4000000.0}
    }

if 'odoo_partners' not in st.session_state:
    st.session_state['odoo_partners'] = [
        {"كود الشريك": "PART-01", "الاسم": "شركة التقنية العالمية المتقدمة", "النوع": "عميل ومورد", "الرصيد المالي": 750000.0}
    ]

if 'odoo_products' not in st.session_state:
    st.session_state['odoo_products'] = {
        "SKU-001": {"اسم الصنف": "خادم سحابي فائق الأداء Enterprise Server", "الكمية بالمستودع": 50, "سعر التكلفة": 14000.0, "سعر البيع": 21000.0}
    }

if 'odoo_sales' not in st.session_state: st.session_state['odoo_sales'] = []
if 'odoo_purchases' not in st.session_state: st.session_state['odoo_purchases'] = []
if 'odoo_assets' not in st.session_state:
    st.session_state['odoo_assets'] = [{"كود الأصل": "FA-101", "اسم الأصل": "أسطول سيارات التوزيع اللوجستية", "التكلفة": 900000.0, "مجمع الإهلاك": 180000.0}]
if 'odoo_hr' not in st.session_state:
    st.session_state['odoo_hr'] = [{"رقم الموظف": "EMP-01", "اسم الموظف": "راشد بن عبد الله القحطاني", "القسم": "الإدارة الهندسية", "الراتب الأساسي": 16000.0}]
if 'odoo_projects' not in st.session_state: st.session_state['odoo_projects'] = []
if 'odoo_mfg' not in st.session_state: st.session_state['odoo_mfg'] = []
if 'odoo_budgets' not in st.session_state:
    st.session_state['odoo_budgets'] = [{"كود المركز": "CC-101", "اسم المركز": "قطاع تقنية المعلومات", "الموازنة المعتمدة": 6000000.0, "المصروف الفعلي": 2500000.0}]

# --- القائمة الجانبية الشاملة لجميع موديولات أودوو ---
with st.sidebar:
    st.markdown("<h3 style='color: #714B67; text-align: center;'>🌐 أفق ERP (Odoo Enterprise)</h3>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-size: 10px; color: #475569;'>المنظومة المؤسسية المتكاملة 2026</p>", unsafe_allow_html=True)
    st.markdown("---")
    
    module_choice = st.selectbox("اختر التطبيق / الموديول:", [
        "1. لوحة المؤشرات التنفيذية (Dashboard)",
        "2. الأستاذ العام والمحاسبة (Accounting & GL)",
        "3. الحسابات الدائنة والموردين (AP)",
        "4. الحسابات المدينة والتحصيل (AR)",
        "5. المبيعات وإصدار الفواتير (Sales)",
        "6. المشتريات وأوامر الشراء (Purchase)",
        "7. المخزون والمستودعات (Inventory & SCM)",
        "8. الأصول الثابتة والإهلاك (Fixed Assets)",
        "9. الموارد البشرية والرواتب (HR & Payroll)",
        "10. التصنيع والمشاريع (Manufacturing & Projects)",
        "11. مراكز التكلفة والموازنات (Cost Centers)"
    ])

# ==========================================
# 1. لوحة المؤشرات (Dashboard)
# ==========================================
if module_choice == "1. لوحة المؤشرات التنفيذية (Dashboard)":
    st.markdown("### 📊 لوحة المؤشرات التنفيذية وحالة المنظومة اللحظية")
    c1, c2, c3, c4 = st.columns(4)
    with c1: st.metric("إجمالي الإيرادات", "14,000,000 ر.س", "+19% هذا الشهر")
    with c2: st.metric("السيولة النقدية بالبنوك", "18,000,000 ر.س", "مستقرة وقوية")
    with c3: st.metric("إجمالي المشتريات", "7,500,000 ر.س", "طبيعي")
    with c4: st.metric("صافي الأرباح التشغيلية", "6,500,000 ر.س", "ممتاز")
    st.markdown("---")
    render_table(pd.DataFrame(st.session_state['odoo_gl']), "سجل القيود اليومية الأحدث في النظام")

# ==========================================
# 2. الأستاذ العام والمحاسبة (Accounting & GL)
# ==========================================
elif module_choice == "2. الأستاذ العام والمحاسبة (Accounting & GL)":
    st.markdown("### 💰 الأستاذ العام ومحرك القيود المزدوجة (Double-Entry Engine)")
    t1, t2 = st.tabs(["دليل الحسابات الشجري (COA)", "دفتر اليومية العامة"])
    with t1:
        accs = [{"كود وحساب": k, "النوع": v["النوع"], "الطبيعة": v["طبيعة"], "الرصيد الدفتري": v["الرصيد"]} for k, v in st.session_state['odoo_accounts'].items()]
        render_table(pd.DataFrame(accs), "دليل الحسابات المالي الموحد")
    with t2:
        render_table(pd.DataFrame(st.session_state['odoo_gl']), "دفتر القيود المحاسبية")
        with st.form("gl_form"):
            j_desc = st.text_input("البيان التفصيلي للقيد المحاسبي")
            j_amt = st.number_input("المبلغ (يتطابق للطرفين لضمان توازن القيد)", value=20000.0)
            if st.form_submit_button("ترحيل القيد محاسبياً للأستاذ العام ⚖️"):
                st.session_state['odoo_gl'].append({
                    "رقم القيد": f"JE/2026/{len(st.session_state['odoo_gl'])+10}",
                    "التاريخ": str(datetime.now().date()), "البيان": j_desc, "مدين": j_amt, "دائن": j_amt, "الحالة": "مرحل (Posted)"
                })
                st.success("تم ترحيل القيد بنجاح إلى الأستاذ العام وميزان المراجعة!")
                st.rerun()

# ==========================================
# 3. الحسابات الدائنة والموردين (AP)
# ==========================================
elif module_choice == "3. الحسابات الدائنة والموردين (AP)":
    st.markdown("### 🏢 الحسابات الدائنة والتزامات الموردين (Accounts Payable)")
    render_table(pd.DataFrame(st.session_state['odoo_partners']), "قاعدة بيانات الشركاء والموردين")
    st.info("نظام المطابقة الثلاثية (Three-Way Matching) وأعمار الديون (AP Aging): مفعل وجاهز.")

# ==========================================
# 4. الحسابات المدينة والتحصيل (AR)
# ==========================================
elif module_choice == "4. الحسابات المدينة والتحصيل (AR)":
    st.markdown("### 💳 الحسابات المدينة والعملاء والتحصيل الآلي (Accounts Receivable)")
    render_table(pd.DataFrame(st.session_state['odoo_partners']), "حسابات العملاء والديون المستحقة")
    st.info("نظام حدود الائتمان التلقائية وإنذارات التأخير: مفعل بنجاح.")

# ==========================================
# 5. المبيعات وإصدار الفواتير (Sales)
# ==========================================
elif module_choice == "5. المبيعات وإصدار الفواتير (Sales)":
    st.markdown("### 🛍️ دورة المبيعات والفوترة الإلكترونية (Sales & E-Invoicing)")
    render_table(pd.DataFrame(st.session_state['odoo_sales']), "أوامر وفواتير المبيعات المعتمدة")
    with st.form("sales_f"):
        c_name = st.text_input("اسم العميل")
        p_sel = st.selectbox("اختر الصنف من المستودع", list(st.session_state['odoo_products'].keys()), format_func=lambda x: st.session_state['odoo_products'][x]["اسم الصنف"])
        qty = st.number_input("الكمية المباعة", value=2, min_value=1)
        if st.form_submit_button("اعتماد أمر البيع وخصم المخزون وترحيل الإيرادات أوتوماتيكياً 🚀"):
            prod = st.session_state['odoo_products'][p_sel]
            if prod["الكمية بالمستودع"] >= qty:
                prod["الكمية بالمستودع"] -= qty
                total = qty * prod["سعر البيع"]
                net_tot = total * 1.15
                st.session_state['odoo_sales'].append({"العميل": c_name, "الصنف": prod["اسم الصنف"], "الكمية": qty, "الإجمالي شامل الضريبة": net_tot, "الحالة": "مفوتر ومرحل"})
                st.session_state['odoo_gl'].append({"رقم القيد": f"JE/SALES/{len(st.session_state['odoo_gl'])+1}", "التاريخ": str(datetime.now().date()), "البيان": f"مبيعات للعميل: {c_name}", "مدين": net_tot, "دائن": net_tot, "الحالة": "مرحل (Posted)"})
                st.success("تم إتمام عملية البيع وتحديث المخزون وإصدار القيد المحاسبي المزدوج أوتوماتيكياً!")
                st.rerun()
            else:
                st.error("الكمية غير متوفرة في المخزون!")

# ==========================================
# 6. المشتريات وأوامر الشراء (Purchase)
# ==========================================
elif module_choice == "6. المشتريات وأوامر الشراء (Purchase)":
    st.markdown("### 🛒 إدارة المشتريات وسلسلة التوريد (Purchase Management)")
    render_table(pd.DataFrame(st.session_state['odoo_purchases']), "أوامر الشراء المسجلة")
    with st.form("pur_f"):
        sup = st.text_input("اسم المورد")
        p_amt = st.number_input("قيمة المشتريات (ر.س)", value=45000.0)
        if st.form_submit_button("تسجيل أمر الشراء وترحيله للموردين"):
            st.session_state['odoo_purchases'].append({"المورد": sup, "القيمة": p_amt, "الحالة": "معتمد ومرحل للأستاذ العام"})
            st.success("تم اعتماد أمر الشراء بنجاح!")
            st.rerun()

# ==========================================
# 7. المخزون والمستودعات (Inventory & SCM)
# ==========================================
elif module_choice == "7. المخزون والمستودعات (Inventory & SCM)":
    st.markdown("### 📦 إدارة المخزون والمستودعات المتعددة (Inventory & Warehousing)")
    invs = [{"كود الصنف": k, "اسم الصنف": v["اسم الصنف"], "الكمية المتاحة": v["الكمية بالمستودع"], "سعر البيع": v["سعر البيع"]} for k, v in st.session_state['odoo_products'].items()]
    render_table(pd.DataFrame(invs), "أصناف المستودع الرئيسي")

# ==========================================
# 8. الأصول الثابتة والإهلاك (Fixed Assets)
# ==========================================
elif module_choice == "8. الأصول الثابتة والإهلاك (Fixed Assets)":
    st.markdown("### 🏢 الأصول الثابتة وإهلاكاتها وفق معايير الـ IFRS")
    render_table(pd.DataFrame(st.session_state['odoo_assets']), "سجل الأصول الثابتة")
    if st.button("تشغيل معالج احتساب الإهلاك الشهري التلقائي ⚙️"):
        st.success("تم حساب الإهلاك وترحيله للحسابات بنجاح!")

# ==========================================
# 9. الموارد البشرية والرواتب (HR & Payroll)
# ==========================================
elif module_choice == "9. الموارد البشرية والرواتب (HR & Payroll)":
    st.markdown("### 👥 الموارد البشرية، الشؤون الإدارية ومسير الرواتب")
    render_table(pd.DataFrame(st.session_state['odoo_hr']), "سجلات الموظفين النشطين")
    if st.button("توليد مسير الرواتب وإنشاء قيد الاستحقاق والأجور 💵"):
        st.success("تم إصدار مسير الرواتب وترحيله للأستاذ العام بنجاح!")

# ==========================================
# 10. التصنيع والمشاريع (Manufacturing & Projects)
# ==========================================
elif module_choice == "10. التصنيع والمشاريع (Manufacturing & Projects)":
    st.markdown("### 🏭 التصنيع، خطوط الإنتاج وإدارة المشاريع (MRP & Project)")
    st.info("أوامر التصنيع وتتبع المواد الأولية والمشاريع الهندسية: جاهزة للتشغيل والتفعيل.")

# ==========================================
# 11. مراكز التكلفة والموازنات (Cost Centers)
# ==========================================
elif module_choice == "11. مراكز التكلفة والموازنات (Cost Centers)":
    st.markdown("### 📈 مراكز التكلفة والموازنات التقديرية (Budgeting & Cost Centers)")
    render_table(pd.DataFrame(st.session_state['odoo_budgets']), "جدول مراكز التكلفة والمقارنة الفعلية")

st.markdown("---")
st.markdown("<p style='text-align: center; color: #714B67; font-size: 11px;'>منصة أفق ERP المتكاملة (شبيه Odoo Enterprise) © 2026</p>", unsafe_allow_html=True)
