import streamlit as st
import pandas as pd
from datetime import datetime

# --- إعدادات الصفحة وتنفيذ قاعدة Shrink to Fit ---
st.set_page_config(
    page_title="نظام أفق ERP المحاسبي والتشغيلي العالمي المتكامل - النسخة التفصيلية الكاملة",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
    <style>
    .stApp { direction: rtl !important; text-align: right !important; font-family: 'Segoe UI', Tahoma, sans-serif; background-color: #f1f5f9; }
    .custom-table { width: 100%; border-collapse: collapse; background-color: white; font-size: 11px; border-radius: 6px; overflow: hidden; box-shadow: 0 1px 3px rgba(0,0,0,0.05); margin-top: 5px; margin-bottom: 10px; }
    .custom-table th { background-color: #0f172a; color: white; padding: 8px 10px; text-align: right; font-size: 11px; }
    .custom-table td { padding: 6px 10px; border-bottom: 1px solid #e2e8f0; color: #1e293b; font-size: 11px; }
    </style>
""", unsafe_allow_html=True)

# --- دالة عرض الجداول بأسلوب Shrink to Fit الاحترافي ---
def render_table_shrink(df, title):
    if df.empty:
        st.info(f"لا توجد سجلات مسجلة حالياً في قسم: {title}.")
        return
    st.markdown(f"**سجلات وقيود: {title}**")
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

# --- تهيئة القواعد والبيانات المركزية الشاملة في Session State ---
if 'accounts_tree' not in st.session_state:
    st.session_state['accounts_tree'] = {
        "1101 الصندوق الرئيسي": {"النوع": "مدين", "الرصيد": 2500000.0},
        "1102 البنك التجاري السعودي": {"النوع": "مدين", "الرصيد": 8500000.0},
        "1201 العملاء والمدينون": {"النوع": "مدين", "الرصيد": 1450000.0},
        "1301 مخزون المستودع العام": {"النوع": "مدين", "الرصيد": 3200000.0},
        "1401 الأصول الثابتة والمعدات": {"النوع": "مدين", "الرصيد": 4500000.0},
        "2101 الموردين والدائنون": {"النوع": "دائن", "الرصيد": 1800000.0},
        "2102 ضريبة القيمة المضافة المستحقة (15%)": {"النوع": "دائن", "الرصيد": 310000.0},
        "3101 رأس المال الأساسي": {"النوع": "دائن", "الرصيد": 15000000.0},
        "4101 إيرادات المبيعات والخدمات": {"النوع": "دائن", "الرصيد": 6200000.0},
        "5101 تكلفة البضائع المباعة": {"النوع": "مدين", "الرصيد": 3100000.0},
        "5201 مصروفات الرواتب والأجور": {"النوع": "مدين", "الرصيد": 950000.0},
        "5301 المصروفات التشغيلية والخدمية": {"النوع": "مدين", "الرصيد": 420000.0}
    }

if 'general_ledger_journal' not in st.session_state:
    st.session_state['general_ledger_journal'] = [
        {"رقم القيد": "JE-1001", "التاريخ": str(datetime.now().date()), "البيان": "القيد الافتتاحي المجمع لتأسيس النظام المالي", "طرف الحساب": "تأسيس الأصول والخصوم ورأس المال", "مدين": 20100000.0, "دائن": 20100000.0, "الحالة": "مرحل ومعتمد نظامياً"}
    ]

if 'treasury_vouchers' not in st.session_state: st.session_state['treasury_vouchers'] = []
if 'licenses_db' not in st.session_state:
    st.session_state['licenses_db'] = [
        {"رقم العقد": "LIC-501", "اسم الشركة": "شركة الإنشاءات الهندسية الحديثة", "التخصص": "مقاولات عامة وبناء", "تاريخ البداية": "2026-01-01", "تاريخ النهاية": "2027-01-01", "قيمة التعاقد": "120,000 ر.س", "الحالة": "ساري"}
    ]
if 'customers_db' not in st.session_state:
    st.session_state['customers_db'] = {
        "CUST-01": {"اسم العميل": "مؤسسة الرواد للتجارة", "السجل": "1010458796", "الضريبي": "30045879600003", "الهاتف": "0501122334", "الرصيد": 125000.0}
    }
if 'suppliers_db' not in st.session_state:
    st.session_state['suppliers_db'] = {
        "SUP-01": {"اسم المورد": "شركة التوريدات الوطنية المحدودة", "السجل": "1010998877", "الضريبي": "30099887700003", "الهاتف": "0554433221", "الرصيد": 95000.0}
    }
if 'inventory_stock' not in st.session_state:
    st.session_state['inventory_stock'] = {
        "ITM-101": {"اسم الصنف": "سيرفر مؤسسي فائق السرعة", "التصنيف": "أجهزة تقنية", "الكمية": 45, "سعر الشراء": 12000.0, "سعر البيع": 16500.0},
        "ITM-102": {"اسم الصنف": "وحدة تخزين طاقة شمسية 10 كيلو", "التصنيف": "طاقة متجددة", "الكمية": 30, "سعر الشراء": 18000.0, "سعر البيع": 24000.0}
    }
if 'sales_invoices_db' not in st.session_state: st.session_state['sales_invoices_db'] = []
if 'purchase_invoices_db' not in st.session_state: st.session_state['purchase_invoices_db'] = []
if 'fixed_assets_db' not in st.session_state:
    st.session_state['fixed_assets_db'] = [
        {"كود الأصل": "AST-01", "اسم الأصل": "أسطول سيارات النقل والتوزيع", "تاريخ الاقتناء": "2024-05-10", "التكلفة": 600000.0, "مجمع الإهلاك": 120000.0, "القيمة الدفترية": 480000.0}
    ]
if 'hr_employees_db' not in st.session_state:
    st.session_state['hr_employees_db'] = {
        "EMP-01": {"الاسم": "صالح بن فهد العتيبي", "القسم": "الإدارة المالية", "المسمى": "مدير الحسابات العامة", "الراتب الأساسي": 15000.0}
    }
if 'production_orders' not in st.session_state: st.session_state['production_orders'] = []
if 'projects_db' not in st.session_state: st.session_state['projects_db'] = []
if 'users_permissions_db' not in st.session_state:
    st.session_state['users_permissions_db'] = [
        {"اسم المستخدم": "system_admin", "الصلاحية الممنوحة": "مدير النظام الكامل (Super Admin)", "الحالة": "نشط ومعتمد"}
    ]

# --- القائمة الجانبية المتقدمة والكاملة ---
with st.sidebar:
    st.markdown("<h3 style='color: #0f172a; text-align: center;'>أفق ERP - النظام التفصيلي</h3>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-size: 10px; color: #475569;'>محرك العمليات والربط المحاسبي التلقائي 2026</p>", unsafe_allow_html=True)
    st.markdown("---")
    
    module_choice = st.selectbox("اختر الموديول التشغيلي للتفاصيل:", [
        "1. إدارة التراخيص، الشركات والعقود الرسمية",
        "2. النظام المحاسبي العام والقيود المزدوجة",
        "3. الخزينة، البنوك وسندات القبض والصرف النقدية",
        "4. موديول المبيعات والفواتير الضريبية والترحيل",
        "5. موديول المشتريات وإدارة الموردين",
        "6. إدارة المخزون والجرد المستمر والأصناف",
        "7. موديول الأصول الثابتة وإهلاكاتها",
        "8. الموارد البشرية والرواتب والأجور (HR)",
        "9. الإنتاج، التصنيع ومراكز التكلفة والمشاريع",
        "10. إدارة الصلاحيات المتقدمة والمستخدمين"
    ])

# ==========================================
# 1. التراخيص والشركات والعقود
# ==========================================
if module_choice == "1. إدارة التراخيص، الشركات والعقود الرسمية":
    st.markdown("### 🏢 موديول إدارة التراخيص والشركات وإصدار العقود الرسمية المعتمدة")
    t1, t2 = st.tabs(["قائمة الشركات والعقود السارية", "إصدار عقد جديد وطباعته"])
    with t1:
        render_table_shrink(pd.DataFrame(st.session_state['licenses_db']), "الشركات المتعاقدة والتراخيص")
    with t2:
        with st.form("contract_full_form"):
            c_num = f"LIC-{len(st.session_state['licenses_db'])+502}"
            st.text(f"رقم العقد التلقائي المولد: {c_num}")
            comp_name = st.text_input("اسم الشركة أو الجهة المتعاقدة")
            specialization = st.selectbox("المجال والتخصص", ["مقاولات عامة", "صيانة وتشغيل", "توريدات تقنية", "استشارات هندسية"])
            start_date = st.date_input("تاريخ بدء العقد")
            end_date = st.date_input("تاريخ انتهاء العقد")
            contract_val = st.text_input("قيمة العقد المالیة", "85,000 ر.س")
            if st.form_submit_button("حفظ وحفظ العقد بالوثائق الرسمية 📄"):
                if comp_name:
                    st.session_state['licenses_db'].append({"رقم العقد": c_num, "اسم الشركة": comp_name, "التخصص": specialization, "تاريخ البداية": str(start_date), "تاريخ النهاية": str(end_date), "قيمة التعاقد": contract_val, "الحالة": "ساري ونشط"})
                    st.success("تم إصدار وحفظ العقد بنجاح تام!")
                    st.rerun()

# ==========================================
# 2. النظام المحاسبي العام
# ==========================================
elif module_choice == "2. النظام المحاسبي العام والقيود المزدوجة":
    st.markdown("### 📚 النظام المحاسبي العام (محرك القيد المزدوج والترحيل اللحظي)")
    t_acc1, t_acc2, t_acc3 = st.tabs(["دفتر قيود اليومية العامة", "شجرة الحسابات وأستاذ العام", "ميزان المراجعة والقوائم المالية"])
    with t_acc1:
        render_table_shrink(pd.DataFrame(st.session_state['general_ledger_journal']), "دفتر اليومية العامة للقيود المحاسبية")
    with t_acc2:
        ledger_data = [{"الحساب": k, "طبيعة الحساب": v["النوع"], "الرصيد الدفتري الحالي": v["الرصيد"]} for k, v in st.session_state['accounts_tree'].items()]
        render_table_shrink(pd.DataFrame(ledger_data), "شجرة الحسابات والأستاذ العام")
    with t_acc3:
        st.markdown("#### ميزان المراجعة العام والموقف المالي")
        c1, c2, c3 = st.columns(3)
        with c1: st.metric("إجمالي الأصول والسيولة", "18,700,000 ر.س")
        with c2: st.metric("إجمالي الخزينة والدائنين", "2,110,000 ر.س")
        with c3: st.metric("صافي رأس المال والأرباح", "16,590,000 ر.س")

# ==========================================
# 3. الخزينة والبنوك وسندات القبض والصرف
# ==========================================
elif module_choice == "3. الخزينة، البنوك وسندات القبض والصرف النقدية":
    st.markdown("### 💰 موديول الخزينة والبنوك وإدارة الحركات النقدية وسندات القبض والصرف")
    t_tr1, t_tr2 = st.tabs(["سجل سندات القبض والصرف", "إصدار سند جديد (قبض / صرف)"])
    with t_tr1:
        render_table_shrink(pd.DataFrame(st.session_state['treasury_vouchers']), "سندات النقدية والبنوك")
    with t_tr2:
        with st.form("voucher_form"):
            v_type = st.selectbox("نوع السند", ["سند قبض نقدي/بنوك", "سند صرف نقدي/بنوك"])
            v_party = st.text_input("اسم الجهة / الشخص (المستفيد أو الدافع)")
            v_amt = st.number_input("المبلغ المالي (ر.س)", value=5000.0)
            v_desc = st.text_area("بيان الحركة التفصيلي")
            if st.form_submit_button("اعتماد وترحيل السند محاسبياً 🔄"):
                v_code = f"VCH-{len(st.session_state['treasury_vouchers'])+1001}"
                st.session_state['treasury_vouchers'].append({"رقم السند": v_code, "النوع": v_type, "الطرف": v_party, "المبلغ": v_amt, "البيان": v_desc, "الحالة": "مرحل للخزينة والأستاذ العام"})
                
                # الترحيل الآلي للحسابات
                if "قبض" in v_type:
                    st.session_state['accounts_tree']["1101 الصندوق الرئيسي"]["الرصيد"] += v_amt
                else:
                    st.session_state['accounts_tree']["1101 الصندوق الرئيسي"]["الرصيد"] -= v_amt
                
                st.success("تم إصدار السند وترحيله إلى الخزينة ودفتر الأستاذ العام بنجاح!")
                st.rerun()

# ==========================================
# 4. المبيعات والفواتير الضريبية
# ==========================================
elif module_choice == "4. موديول المبيعات والفواتير الضريبية والترحيل":
    st.markdown("### 🛍️ موديول المبيعات والفوترة الإلكترونية (الربط الآلي بالمخزون والضريبة)")
    render_table_shrink(pd.DataFrame(st.session_state['sales_invoices_db']), "الفواتير الضريبية المسجلة")
    with st.form("inv_full_f"):
        inv_code = f"INV-{len(st.session_state['sales_invoices_db'])+501}"
        cust_sel = st.selectbox("العميل", list(st.session_state['customers_db'].keys()), format_func=lambda x: st.session_state['customers_db'][x]['اسم العميل'])
        item_sel = st.selectbox("الصنف المباع", list(st.session_state['inventory_stock'].keys()), format_func=lambda x: st.session_state['inventory_stock'][x]['اسم الصنف'])
        qty_sold = st.number_input("الكمية المباعة", value=2, min_value=1)
        unit_price = st.number_input("سعر البيع للوحدة", value=16500.0)
        if st.form_submit_button("إصدار الفاتورة وترحيلها آلياً لجميع الأقسام 🚀"):
            subtotal = qty_sold * unit_price
            tax_val = subtotal * 0.15
            total_due = subtotal + tax_val
            
            # خصم المخزون
            st.session_state['inventory_stock'][item_sel]["الكمية"] -= qty_sold
            # تحديث الحسابات
            st.session_state['accounts_tree']["1201 العملاء والمدينون"]["الرصيد"] += total_due
            st.session_state['accounts_tree']["4101 إيرادات المبيعات والخدمات"]["الرصيد"] += subtotal
            st.session_state['accounts_tree']["2102 ضريبة القيمة المضافة المستحقة (15%)"]["الرصيد"] += tax_val
            
            # قيد اليومية المزدوج
            st.session_state['general_ledger_journal'].append({
                "رقم القيد": f"JE-INV-{len(st.session_state['sales_invoices_db'])+10}",
                "التاريخ": str(datetime.now().date()),
                "البيان": f"إثبات فاتورة مبيعات ضريبية {inv_code} للعميل {st.session_state['customers_db'][cust_sel]['اسم العميل']}",
                "طرف الحساب": "مدين: العملاء / دائن: الإيرادات والضريبة المستحقة",
                "مدين": total_due, "دائن": total_due,
                "الحالة": "مرحل آلياً بنجاح"
            })
            
            st.session_state['sales_invoices_db'].append({"رقم الفاتورة": inv_code, "العميل": st.session_state['customers_db'][cust_sel]["اسم العميل"], "الإجمالي شامل الضريبة": round(total_due, 2), "الحالة": "مرحلة ومعتمدة محاسبياً ومخزنياً"})
            st.success("تم إصدار الفاتورة الضريبية وتطبيق الترحيل الآلي الشامل بنجاح تام!")
            st.rerun()

# ==========================================
# 5. المشتريات والموردين
# ==========================================
elif module_choice == "5. موديول المشتريات وإدارة الموردين":
    st.markdown("### 🛒 موديول المشتريات وسلاسل الإمداد وإدارة أرصدة الموردين")
    render_table_shrink(pd.DataFrame(st.session_state['purchase_invoices_db']), "فواتير وسجلات المشتريات")
    with st.form("pur_full_f"):
        p_code = f"PUR-{len(st.session_state['purchase_invoices_db'])+301}"
        sup_sel = st.selectbox("المورد المعتمد", list(st.session_state['suppliers_db'].keys()), format_func=lambda x: st.session_state['suppliers_db'][x]['اسم المورد'])
        p_amt = st.number_input("إجمالي قيمة المشتريات (ر.س)", value=45000.0)
        if st.form_submit_button("تسجيل وترحيل المشتريات آلياً 💾"):
            st.session_state['suppliers_db'][sup_sel]["الرصيد"] += p_amt
            st.session_state['purchase_invoices_db'].append({"رقم الفاتورة": p_code, "المورد": st.session_state['suppliers_db'][sup_sel]["اسم المورد"], "المبلغ": p_amt, "الحالة": "مرحل للموردين والمخزون"})
            st.success("تم ترحيل المشتريات وتحديث أرصدة الموردين بنجاح!")
            st.rerun()

# ==========================================
# 6. المخزون والأصناف
# ==========================================
elif module_choice == "6. إدارة المخزون والجرد المستمر والأصناف":
    st.markdown("### 📦 موديول إدارة المخزون والأصناف والجرد اللحظي المستمر")
    inv_list = [{"كود الصنف": k, "اسم الصنف": v["اسم الصنف"], "التصنيف": v["التصنيف"], "الكمية بالمستودع": v["الكمية"], "سعر الشراء": v["سعر الشراء"], "سعر البيع": v["سعر البيع"]} for k, v in st.session_state['inventory_stock'].items()]
    render_table_shrink(pd.DataFrame(inv_list), "مستودع الأصناف والمخزون العام")
    with st.form("it_full_add"):
        it_code = f"ITM-{len(st.session_state['inventory_stock'])+105}"
        it_name = st.text_input("اسم الصنف الجديد بالكامل")
        it_qty = st.number_input("الكمية الأولية بالمستودع", value=25)
        it_cost = st.number_input("سعر الشراء", value=5000.0)
        it_sale = st.number_input("سعر البيع المقترح", value=7500.0)
        if st.form_submit_button("إضافة الصنف لقاعدة المستودعات"):
            if it_name:
                st.session_state['inventory_stock'][it_code] = {"اسم الصنف": it_name, "التصنيف": "عام ومستودعات", "الكمية": it_qty, "سعر الشراء": it_cost, "سعر البيع": it_sale}
                st.success("تمت إضافة الصنف بنجاح تام للمستودع!")
                st.rerun()

# ==========================================
# 7. الأصول الثابتة
# ==========================================
elif module_choice == "7. موديول الأصول الثابتة وإهلاكاتها":
    st.markdown("### 🏛️ موديول إدارة الأصول الثابتة، المعدات وحسابات الإهلاك السنوي")
    render_table_shrink(pd.DataFrame(st.session_state['fixed_assets_db']), "سجل الأصول الثابتة")
    with st.form("ast_f"):
        ast_name = st.text_input("اسم الأصل الثابت الجديد (معدات، مبانٍ، سيارات)")
        ast_cost = st.number_input("تكلفة الاقتناء الأصلية (ر.س)", value=150000.0)
        if st.form_submit_button("حفظ الأصل الثابت"):
            if ast_name:
                st.session_state['fixed_assets_db'].append({"كود الأصل": f"AST-0{len(st.session_state['fixed_assets_db'])+1}", "اسم الأصل": ast_name, "تاريخ الاقتناء": str(datetime.now().date()), "التكلفة": ast_cost, "مجمع الإهلاك": 0.0, "القيمة الدفترية": ast_cost})
                st.success("تم تسجيل الأصل الثابت وتكوين سجله المحاسبي بنجاح!")
                st.rerun()

# ==========================================
# 8. الموارد البشرية (HR)
# ==========================================
elif module_choice == "8. الموارد البشرية والرواتب والأجور (HR)":
    st.markdown("### 👥 موديول الموارد البشرية وشؤون الموظفين ومسير الرواتب")
    emp_list = [{"كود الموظف": k, "الاسم": v["الاسم"], "القسم": v["القسم"], "المسمى الوظيفي": v["المسمى"], "الراتب الأساسي": v["الراتب الأساسي"]} for k, v in st.session_state['hr_employees_db'].items()]
    render_table_shrink(pd.DataFrame(emp_list), "سجلات الموظفين وأقسامهم")
    with st.form("emp_full_f"):
        e_name = st.text_input("اسم الموظف الرباعي")
        e_dept = st.selectbox("القسم الإداري", ["الإدارة المالية", "الإدارة الهندسية", "المبيعات والتسويق", "المستودعات والخدمات"])
        e_sal = st.number_input("الراتب الأساسي الشهري", value=11000.0)
        if st.form_submit_button("حفظ ملف الموظف"):
            if e_name:
                st.session_state['hr_employees_db'][f"EMP-0{len(st.session_state['hr_employees_db'])+2}"] = {"الاسم": e_name, "القسم": e_dept, "المسمى": "موظف ميداني/إداري", "الراتب الأساسي": e_sal}
                st.success("تم حفظ الموظف وتحديث بيانات الهيكل الإداري بنجاح!")
                st.rerun()

# ==========================================
# 9. الإنتاج والمشاريع
# ==========================================
elif module_choice == "9. الإنتاج، التصنيع ومراكز التكلفة والمشاريع":
    st.markdown("### 🏭 موديول الإنتاج، أوامر التصنيع، المشاريع الهندسية ومراكز التكلفة")
    render_table_shrink(pd.DataFrame(st.session_state['production_orders']), "أوامر الإنتاج والتصنيع")
    with st.form("prd_full_f"):
        pr_num = f"PRD-90{len(st.session_state['production_orders'])+1}"
        pr_name = st.text_input("اسم المنتج أو المشروع الصناعي")
        pr_qty = st.number_input("الكمية المستهدفة للإنتاج", value=15)
        if st.form_submit_button("إصدار أمر الإنتاج التشغيلي"):
            if pr_name:
                st.session_state['production_orders'].append({"رقم الأمر": pr_num, "المنتج": pr_name, "الكمية المستهدفة": pr_qty, "الحالة": "قيد الإنتاج والتشغيل في الورشة"})
                st.success("تم إصدار أمر الإنتاج بنجاح تام!")
                st.rerun()

# ==========================================
# 10. الصلاحيات والمستخدمين
# ==========================================
elif module_choice == "10. إدارة الصلاحيات المتقدمة والمستخدمين":
    st.markdown("### 🔐 إدارة الصلاحيات المتقدمة، أدوار المستخدمين وأمن النظام")
    render_table_shrink(pd.DataFrame(st.session_state['users_permissions_db']), "صلاحيات وأدوار المستخدمين")
    with st.form("usr_full_f"):
        u_id = st.text_input("اسم المستخدم الجديد للنظام")
        u_role = st.selectbox("الدور والصلاحية", ["مدير النظام (Admin)", "محاسب أول", "مسؤول مبيعات", "أمين مستودع"])
        if st.form_submit_button("منح الصلاحية وحفظ المستخدم"):
            if u_id:
                st.session_state['users_permissions_db'].append({"اسم المستخدم": u_id, "الصلاحية الممنوحة": u_role, "الحالة": "نشط ومرخص"})
                st.success("تمت إضافة وتفعيل مستخدم النظام الجديد بنجاح!")
                st.rerun()

st.markdown("---")
st.markdown("<p style='text-align: center; color: #0f172a; font-size: 11px;'>نظام أفق ERP المحاسبي والتشغيلي المتكامل (النسخة التفصيلية الكاملة) © 2026</p>", unsafe_allow_html=True)
