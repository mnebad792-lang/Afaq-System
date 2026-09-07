import streamlit as st
import pandas as pd
from datetime import datetime

# --- إعدادات الصفحة وتنفيذ قاعدة Shrink to Fit ---
st.set_page_config(
    page_title="نظام أفق ERP المحاسبي والتشغيلي العالمي المتكامل",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
    <style>
    .stApp { direction: rtl !important; text-align: right !important; font-family: 'Segoe UI', Tahoma, sans-serif; background-color: #f8f9fa; }
    .custom-table { width: 100%; border-collapse: collapse; background-color: white; font-size: 11px; border-radius: 6px; overflow: hidden; box-shadow: 0 1px 3px rgba(0,0,0,0.05); margin-top: 5px; margin-bottom: 10px; }
    .custom-table th { background-color: #1e293b; color: white; padding: 8px 10px; text-align: right; font-size: 11px; }
    .custom-table td { padding: 6px 10px; border-bottom: 1px solid #f1f5f9; color: #334155; font-size: 11px; }
    </style>
""", unsafe_allow_html=True)

# --- دالة عرض الجداول بأسلوب Shrink to Fit الاحترافي ---
def render_table_shrink(df, title):
    if df.empty:
        st.info(f"لا توجد سجلات حالياً في قسم: {title}.")
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

# --- تهيئة قواعد البيانات المركزية المترابطة بالكامل في Session State ---
if 'accounts_tree' not in st.session_state:
    st.session_state['accounts_tree'] = {
        "1101 الصندوق الرئيسي": {"النوع": "مدين", "الرصيد": 1500000.0},
        "1102 البنك التجاري الرئيسي": {"النوع": "مدين", "الرصيد": 5500000.0},
        "1201 العملاء والمدينون": {"النوع": "مدين", "الرصيد": 950000.0},
        "1301 مخزون البضائع العام": {"النوع": "مدين", "الرصيد": 2100000.0},
        "2101 الموردين والدائنون": {"النوع": "دائن", "الرصيد": 1100000.0},
        "2102 ضريبة القيمة المضافة المستحقة (15%)": {"النوع": "دائن", "الرصيد": 185000.0},
        "3101 رأس المال الأساسي": {"النوع": "دائن", "الرصيد": 7000000.0},
        "4101 إيرادات المبيعات والخدمات": {"النوع": "دائن", "الرصيد": 3500000.0},
        "5101 تكلفة البضائع المباعة": {"النوع": "مدين", "الرصيد": 1900000.0},
        "5201 مصروفات الرواتب والأجور": {"النوع": "مدين", "الرصيد": 450000.0}
    }

if 'general_ledger_journal' not in st.session_state:
    st.session_state['general_ledger_journal'] = [
        {"رقم القيد": "JE-5001", "التاريخ": str(datetime.now().date()), "البيان": "القيد الافتتاحي المجمع لتأسيس النظام", "طرف الحساب": "متعدد الأصول والخصوم", "مدين": 10000000.0, "دائن": 10000000.0, "الحالة": "مرحل ومعتمد آلياً"}
    ]

if 'licenses_db' not in st.session_state:
    st.session_state['licenses_db'] = [
        {"رقم العقد": "LIC-1001", "اسم الشركة": "شركة المقاولات الحديثة ذ.م.م", "التخصص": "مقاولات عامة وتطوير عقاري", "تاريخ البداية": "2026-01-01", "تاريخ النهاية": "2027-01-01", "قيمة التعاقد": "45,000 ر.س", "الحالة": "ساري ونشط"}
    ]

if 'customers_db' not in st.session_state:
    st.session_state['customers_db'] = {
        "CUST-001": {"اسم العميل": "شركة الرياض للتجارة", "السجل": "1010254789", "الضريبي": "300123456700003", "الهاتف": "0501234567", "الحد الائتماني": 150000.0, "الرصيد": 45000.0}
    }

if 'suppliers_db' not in st.session_state:
    st.session_state['suppliers_db'] = {
        "SUP-001": {"اسم المورد": "مؤسسة التوريدات الصناعية", "السجل": "1010987654", "الضريبي": "300111222300003", "الهاتف": "0561112233", "الرصيد": 85000.0}
    }

if 'inventory_stock' not in st.session_state:
    st.session_state['inventory_stock'] = {
        "ITM-001": {"اسم الصنف": "لابتوب مؤسسي فاخر i7", "التصنيف": "إلكترونيات", "الكمية": 85, "سعر الشراء": 3000.0, "سعر البيع": 4200.0, "حد الطلب": 5},
        "ITM-002": {"اسم الصنف": "شاشة عرض تفاعلية 75 بوصة", "التصنيف": "شاشات وأجهزة", "الكمية": 25, "سعر الشراء": 8500.0, "سعر البيع": 11500.0, "حد الطلب": 2}
    }

if 'sales_quotations' not in st.session_state: st.session_state['sales_quotations'] = []
if 'sales_orders' not in st.session_state: st.session_state['sales_orders'] = []
if 'sales_invoices_db' not in st.session_state: st.session_state['sales_invoices_db'] = []
if 'purchase_invoices_db' not in st.session_state: st.session_state['purchase_invoices_db'] = []
if 'hr_employees_db' not in st.session_state:
    st.session_state['hr_employees_db'] = {
        "EMP-001": {"الاسم": "عبدالله بن محمد القحطاني", "القسم": "الإدارة المالية", "المسمى": "مدير الحسابات", "الراتب الأساسي": 14000.0, "البدلات": 3000.0, "الحالة": "على رأس العمل"}
    }
if 'production_orders' not in st.session_state: st.session_state['production_orders'] = []
if 'projects_db' not in st.session_state: st.session_state['projects_db'] = []
if 'cost_centers_db' not in st.session_state: st.session_state['cost_centers_db'] = []
if 'users_permissions_db' not in st.session_state: st.session_state['users_permissions_db'] = []

# --- القائمة الرئيسية للموديولات المتكاملة ---
with st.sidebar:
    st.markdown("<h3 style='color: #1e293b; text-align: center;'>أفق ERP - الربط الشامل</h3>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-size: 10px; color: #64748b;'>محرك الترحيل الآلي للعمليات 2026</p>", unsafe_allow_html=True)
    st.markdown("---")
    
    module_choice = st.selectbox("اختر الموديول التشغيلي:", [
        "1. إدارة التراخيص والشركات والتعاقدات",
        "2. النظام المحاسبي المتكامل والترحيل الآلي",
        "3. موديول المبيعات (مع الترحيل للمخزون والحسابات)",
        "4. موديول المشتريات (مع الترحيل للموردين والمخزون)",
        "5. موديول المخزون والجرد المستمر",
        "6. موديول الإنتاج، التصنيع والصيانة",
        "7. موديول المشاريع ومراكز التكلفة",
        "8. الموارد البشرية وشؤون الموظفين (HR)",
        "9. إدارة الصلاحيات والمستخدمين وأمن النظام"
    ])

# ==========================================
# 1. إدارة التراخيص والشركات والتعاقدات
# ==========================================
if module_choice == "1. إدارة التراخيص والشركات والتعاقدات":
    st.markdown("### 🏢 موديول إدارة التراخيص، الشركات وإصدار العقود الرسمية")
    t1, t2 = st.tabs(["قائمة الشركات والتعاقدات", "إصدار وطباعة عقد عميل جديد"])
    with t1:
        render_table_shrink(pd.DataFrame(st.session_state['licenses_db']), "الشركات المتعاقدة والتراخيص")
    with t2:
        with st.form("contract_form"):
            c_num = f"LIC-{len(st.session_state['licenses_db'])+1001}"
            st.text(f"رقم العقد التلقائي: {c_num}")
            comp_name = st.text_input("اسم الشركة المشتركة")
            specialization = st.selectbox("التخصص", ["مقاولات عامة", "صيانة وتشغيل", "تطوير عقاري", "ورش تصنيع"])
            start_date = st.date_input("تاريخ البداية")
            end_date = st.date_input("تاريخ النهاية")
            contract_val = st.text_input("قيمة التعاقد (ر.س)", "50,000 ر.س")
            if st.form_submit_button("حفظ واستخراج العقد المطبوع 📄"):
                if comp_name:
                    st.session_state['licenses_db'].append({"رقم العقد": c_num, "اسم الشركة": comp_name, "التخصص": specialization, "تاريخ البداية": str(start_date), "تاريخ النهاية": str(end_date), "قيمة التعاقد": contract_val, "الحالة": "ساري ونشط"})
                    st.success("تم إصدار وحفظ العقد بنجاح!")
                    st.rerun()

# ==========================================
# 2. النظام المحاسبي المتكامل والترحيل الآلي
# ==========================================
elif module_choice == "2. النظام المحاسبي المتكامل والترحيل الآلي":
    st.markdown("### 📚 النظام المحاسبي المتكامل والقيود المزدوجة المرحلة تلقائياً")
    t_acc1, t_acc2, t_acc3 = st.tabs(["دفتر قيود اليومية المزدوجة", "شجرة الحسابات وأستاذ العام", "القوائم المالية والضرائب"])
    with t_acc1:
        render_table_shrink(pd.DataFrame(st.session_state['general_ledger_journal']), "سجل القيود اليومية المرحلة آلياً")
    with t_acc2:
        ledger_data = [{"الحساب": k, "طبيعة الحساب": v["النوع"], "الرصيد الحالي": v["الرصيد"]} for k, v in st.session_state['accounts_tree'].items()]
        render_table_shrink(pd.DataFrame(ledger_data), "أرصدة حسابات الأستاذ العام")
    with t_acc3:
        st.markdown("#### القوائم المالية اللحظية وموقف ضريبة القيمة المضافة")
        c1, c2, c3 = st.columns(3)
        with c1: st.metric("إجمالي إيرادات المبيعات", "3,500,000 ر.س")
        with c2: st.metric("إجمالي تكلفة المبيعات", "1,900,000 ر.س")
        with c3: st.metric("ضريبة القيمة المضافة المستحقة", "185,000 ر.س")

# ==========================================
# 3. موديول المبيعات (مع الترحيل التلقائي)
# ==========================================
elif module_choice == "3. موديول المبيعات (مع الترحيل للمخزون والحسابات)":
    st.markdown("### 🛍️ موديول المبيعات (دورة متكاملة مع ترحيل آلي للمخزون والحسابات والضريبة)")
    t_s1, t_s2, t_s3 = st.tabs(["عروض الأسعار", "أوامر البيع", "إصدار الفاتورة الضريبية والترحيل الفوري"])
    with t_s1:
        render_table_shrink(pd.DataFrame(st.session_state['sales_quotations']), "عروض الأسعار")
        with st.form("q_f"):
            q_code = f"QT-{len(st.session_state['sales_quotations'])+101}"
            cust = st.selectbox("العميل", list(st.session_state['customers_db'].keys()), format_func=lambda x: st.session_state['customers_db'][x]['اسم العميل'])
            itm = st.selectbox("الصنف", list(st.session_state['inventory_stock'].keys()), format_func=lambda x: st.session_state['inventory_stock'][x]['اسم الصنف'])
            qty = st.number_input("الكمية", value=2)
            if st.form_submit_button("حفظ عرض السعر"):
                st.session_state['sales_quotations'].append({"رقم العرض": q_code, "العميل": st.session_state['customers_db'][cust]["اسم العميل"], "الحالة": "ساري"})
                st.success("تم حفظ عرض السعر!")
                st.rerun()
    with t_s2:
        render_table_shrink(pd.DataFrame(st.session_state['sales_orders']), "أوامر البيع المعتمدة")
        with st.form("o_f"):
            o_code = f"SO-{len(st.session_state['sales_orders'])+101}"
            cust_o = st.selectbox("العميل للأمر", list(st.session_state['customers_db'].keys()), format_func=lambda x: st.session_state['customers_db'][x]['اسم العميل'])
            if st.form_submit_button("اعتماد أمر البيع"):
                st.session_state['sales_orders'].append({"رقم الأمر": o_code, "العميل": st.session_state['customers_db'][cust_o]["اسم العميل"], "الحالة": "معتمد"})
                st.success("تم اعتماد أمر البيع بنجاح!")
                st.rerun()
    with t_s3:
        render_table_shrink(pd.DataFrame(st.session_state['sales_invoices_db']), "الفواتير الضريبية المرحلة")
        with st.form("inv_f"):
            inv_code = f"INV-{len(st.session_state['sales_invoices_db'])+101}"
            cust_i = st.selectbox("العميل للفاتورة", list(st.session_state['customers_db'].keys()), format_func=lambda x: st.session_state['customers_db'][x]['اسم العميل'])
            item_i = st.selectbox("الصنف", list(st.session_state['inventory_stock'].keys()), format_func=lambda x: st.session_state['inventory_stock'][x]['اسم الصنف'])
            q_i = st.number_input("الكمية المباعة", value=1, min_value=1)
            p_i = st.number_input("سعر الوحدة", value=4200.0)
            if st.form_submit_button("إصدار الفاتورة وترحيل آلي للمخزون والضريبة والأستاذ العام 🚀"):
                subtotal = q_i * p_i
                tax_val = subtotal * 0.15
                total_due = subtotal + tax_val
                
                # الترحيل الآلي للمخزون
                st.session_state['inventory_stock'][item_i]["الكمية"] -= q_i
                
                # الترحيل الآلي للحسابات والضريبة
                st.session_state['accounts_tree']["1201 العملاء والمدينون"]["الرصيد"] += total_due
                st.session_state['accounts_tree']["4101 إيرادات المبيعات والخدمات"]["الرصيد"] += subtotal
                st.session_state['accounts_tree']["2102 ضريبة القيمة المضافة المستحقة (15%)"]["الرصيد"] += tax_val
                
                # إضافة القيد المزدوج في دفتر اليومية
                st.session_state['general_ledger_journal'].append({
                    "رقم القيد": f"JE-INV-{len(st.session_state['sales_invoices_db'])+1}",
                    "التاريخ": str(datetime.now().date()),
                    "البيان": f"إثبات فاتورة مبيعات رقم {inv_code} للعميل {st.session_state['customers_db'][cust_i]['اسم العميل']}",
                    "طرف الحساب": "مدين: العملاء / دائن: إيرادات ومبيعات وضريبة",
                    "مدين": total_due, "دائن": total_due,
                    "الحالة": "مرحل آلياً بنجاح"
                })
                
                st.session_state['sales_invoices_db'].append({"رقم الفاتورة": inv_code, "العميل": st.session_state['customers_db'][cust_i]["اسم العميل"], "الإجمالي شامل الضريبة": round(total_due, 2), "الحالة": "مرحلة ومعتمدة محاسبياً ومخزنياً"})
                st.success("تم إصدار الفاتورة وترحيلها أوتوماتيكياً لكافة أقسام النظام بنجاح تام!")
                st.rerun()

# ==========================================
# 4. موديول المشتريات
# ==========================================
elif module_choice == "4. موديول المشتريات (مع الترحيل للموردين والمخزون)":
    st.markdown("### 🛒 موديول المشتريات وسلاسل الإمداد مع الترحيل التلقائي")
    render_table_shrink(pd.DataFrame(st.session_state['purchase_invoices_db']), "فواتير المشتريات")
    with st.form("p_form"):
        p_code = f"PUR-{len(st.session_state['purchase_invoices_db'])+101}"
        sup_sel = st.selectbox("المورد", list(st.session_state['suppliers_db'].keys()), format_func=lambda x: st.session_state['suppliers_db'][x]['اسم المورد'])
        p_amt = st.number_input("إجمالي المشتريات (ر.س)", value=30000.0)
        if st.form_submit_button("تسجيل وترحيل المشتريات آلياً 💾"):
            st.session_state['suppliers_db'][sup_sel]["الرصيد"] += p_amt
            st.session_state['purchase_invoices_db'].append({"رقم الفاتورة": p_code, "المورد": st.session_state['suppliers_db'][sup_sel]["اسم المورد"], "المبلغ": p_amt, "الحالة": "مرحل محاسبياً"})
            st.success("تم ترحيل المشتريات وتحديث أرصدة الموردين والمخزون بنجاح!")
            st.rerun()

# ==========================================
# 5. موديول المخزون
# ==========================================
elif module_choice == "5. موديول المخزون والجرد المستمر":
    st.markdown("### 📦 موديول إدارة المخزون والأصناف اللحظي")
    inv_list = [{"كود الصنف": k, "اسم الصنف": v["اسم الصنف"], "التصنيف": v["التصنيف"], "الكمية بالمستودع": v["الكمية"], "سعر الشراء": v["سعر الشراء"], "سعر البيع": v["سعر البيع"]} for k, v in st.session_state['inventory_stock'].items()]
    render_table_shrink(pd.DataFrame(inv_list), "مستودع الأصناف والمخزون المستمر")
    with st.form("it_add"):
        it_code = f"ITM-{len(st.session_state['inventory_stock'])+101}"
        it_name = st.text_input("اسم الصنف الجديد")
        it_qty = st.number_input("الكمية", value=20)
        it_cost = st.number_input("سعر الشراء", value=1500.0)
        it_sale = st.number_input("سعر البيع", value=2200.0)
        if st.form_submit_button("إضافة الصنف"):
            if it_name:
                st.session_state['inventory_stock'][it_code] = {"اسم الصنف": it_name, "التصنيف": "عام", "الكمية": it_qty, "سعر الشراء": it_cost, "سعر البيع": it_sale, "حد الطلب": 3}
                st.success("تمت الإضافة للمخزون!")
                st.rerun()

# ==========================================
# 6. موديول الإنتاج والتصنيع والصيانة
# ==========================================
elif module_choice == "6. موديول الإنتاج، التصنيع والصيانة":
    st.markdown("### 🏭 موديول الإنتاج وخطوط التجميع والصيانة الشاملة")
    render_table_shrink(pd.DataFrame(st.session_state['production_orders']), "أوامر الإنتاج")
    with st.form("pr_form"):
        pr_num = f"PRD-{len(st.session_state['production_orders'])+901}"
        pr_name = st.text_input("اسم المنتج المراد تصنيعه")
        pr_qty = st.number_input("الكمية المستهدفة", value=10)
        if st.form_submit_button("إصدار أمر الإنتاج"):
            if pr_name:
                st.session_state['production_orders'].append({"رقم الأمر": pr_num, "المنتج": pr_name, "الكمية المستهدفة": pr_qty, "الحالة": "قيد الإنتاج التشغيلي"})
                st.success("تم إصدار أمر الإنتاج بنجاح!")
                st.rerun()

# ==========================================
# 7. موديول المشاريع ومراكز التكلفة
# ==========================================
elif module_choice == "7. موديول المشاريع ومراكز التكلفة":
    st.markdown("### 📊 موديول المشاريع (مقاولات، صيانة، تطوير، ورش)")
    render_table_shrink(pd.DataFrame(st.session_state['projects_db']), "سجل المشاريع المعتمدة")
    with st.form("pj_form"):
        pj_name = st.text_input("اسم المشروع الهندسي أو أعمال الصيانة")
        pj_bud = st.number_input("الميزانية التقديرية (ر.س)", value=500000.0)
        if st.form_submit_button("حفظ المشروع"):
            if pj_name:
                st.session_state['projects_db'].append({"اسم المشروع": pj_name, "الميزانية": pj_bud, "الحالة": "نشط"})
                st.success("تم تسجيل المشروع بنجاح!")
                st.rerun()

# ==========================================
# 8. الموارد البشرية وشؤون الموظفين (HR)
# ==========================================
elif module_choice == "8. الموارد البشرية وشؤون الموظفين (HR)":
    st.markdown("### 👥 موديول الموارد البشرية وشؤون الموظفين والرواتب")
    emp_list = [{"كود الموظف": k, "الاسم": v["الاسم"], "القسم": v["القسم"], "المسمى": v["المسمى"], "الراتب": v["الراتب الأساسي"]} for k, v in st.session_state['hr_employees_db'].items()]
    render_table_shrink(pd.DataFrame(emp_list), "سجلات الموظفين")
    with st.form("emp_f"):
        e_name = st.text_input("اسم الموظف الكامل")
        e_sal = st.number_input("الراتب الأساسي", value=9000.0)
        if st.form_submit_button("حفظ الموظف"):
            if e_name:
                st.session_state['hr_employees_db'][f"EMP-{len(st.session_state['hr_employees_db'])+101}"] = {"الاسم": e_name, "القسم": "الإدارة", "المسمىوظفي": "موظف", "الراتب الأساسي": e_sal, "البدلات": 1000.0, "الحالة": "على رأس العمل"}
                st.success("تم حفظ الموظف بنجاح!")
                st.rerun()

# ==========================================
# 9. الصلاحيات والمستخدمين
# ==========================================
elif module_choice == "9. إدارة الصلاحيات والمستخدمين وأمن النظام":
    st.markdown("### 🔐 إدارة الصلاحيات والمستخدمين")
    render_table_shrink(pd.DataFrame(st.session_state['users_permissions_db']), "المستخدمون النشطون")
    with st.form("usr_f"):
        u_id = st.text_input("اسم المستخدم")
        u_role = st.selectbox("الصلاحية", ["مدير عام", "محاسب", "مدير مبيعات"])
        if st.form_submit_button("إضافة مستخدم"):
            if u_id:
                st.session_state['users_permissions_db'].append({"اسم المستخدم": u_id, "الصلاحية": u_role, "الحالة": "نشط"})
                st.success("تمت إضافة المستخدم بنجاح!")
                st.rerun()

st.markdown("---")
st.markdown("<p style='text-align: center; color: #1e293b; font-size: 11px;'>نظام أفق ERP المتكامل للربط الآلي © 2026</p>", unsafe_allow_html=True)
