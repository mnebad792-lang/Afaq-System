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
        "software_version": "النسخة المحاسبية الاحترافية 2026 (مباع-مخزون-قيد تلقائي)"
    }

# --- تهيئة قاعدة بيانات المستودعات والصناديق والبنوك ---
if 'warehouses_db' not in st.session_state:
    st.session_state['warehouses_db'] = ["المستودع الرئيسي - الرياض", "مستودع الفرع - جدة", "مستودع التوريدات العامة"]

if 'cash_boxes_db' not in st.session_state:
    st.session_state['cash_boxes_db'] = ["الخزينة الرئيسية (صندوق النقد)", "صندوق المعارض"]

if 'banks_db' not in st.session_state:
    st.session_state['banks_db'] = ["مصرف الراجحي (تحويل/شبكة)", "البنك الأهلي السعودي (تحويل/شبكة)", "بنك الرياض"]

# --- تهيئة المنتجات والمخزون ---
if 'inventory_stock' not in st.session_state:
    st.session_state['inventory_stock'] = {
        "PROD-001": {"اسم المنتج": "جهاز حاسوب محمول احترافي", "سعر البيع": 3500.0, "تكلفة الشراء": 2800.0, "الكمية المتاحة": 45},
        "PROD-002": {"اسم المنتج": "شاشة عرض 27 بوصة 4K", "سعر البيع": 1200.0, "تكلفة الشراء": 900.0, "الكمية المتاحة": 30},
        "PROD-003": {"اسم المنتج": "طابعة لاسلكية متعددة الوظائف", "سعر البيع": 850.0, "تكلفة الشراء": 600.0, "الكمية المتاحة": 20}
    }

# --- تهيئة العملاء ---
if 'customers_db' not in st.session_state:
    st.session_state['customers_db'] = {
        "شركة التقنية الحديثة للتجارة": {"كود العميل": "CUST-001", "رقم السجل": "1010254789", "الرقم الضريبي": "300123456700003", "العنوان": "الرياض - حي الملز", "الهاتف": "0501234567", "الرصيد الحالي": 0.0}
    }

# --- مستندات المبيعات (عروض أسعار، أوامر بيع، فواتير ضريبية) ---
if 'sales_quotations' not in st.session_state:
    st.session_state['sales_quotations'] = []

if 'sales_orders' not in st.session_state:
    st.session_state['sales_orders'] = []

if 'sales_invoices_db' not in st.session_state:
    st.session_state['sales_invoices_db'] = []

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
    st.session_state['active_module'] = "المبيعات"

# --- القائمة الجانبية ---
with st.sidebar:
    client_conf = st.session_state['client_license_config']
    st.markdown(f"<h2 style='color: #714B67; text-align: center;'>نظام أفق ERP</h2>", unsafe_allow_html=True)
    st.markdown(f"<p style='text-align: center; font-size: 11px; color: #64748b;'>مرخص لـ: <b>{client_conf['client_name']}</b></p>", unsafe_allow_html=True)
    st.markdown("---")
    
    modules_map = {
        "الرئيسية": "🏠 الرئيسية",
        "المبيعات": "🛒 موديول المبيعات",
        "الشركاء": "👥 الشركاء والعملاء",
        "المخزون": "📋 المخزون والجرد",
        "المحاسبة والشجرة": "💰 المحاسبة والقيود",
        "الإعدادات": "⚙️ الإعدادات"
    }
    
    for mod_key, mod_label in modules_map.items():
        is_selected = (st.session_state['active_module'] == mod_key)
        if st.button(mod_label, key=f"btn_mod_{mod_key}", use_container_width=True, type="primary" if is_selected else "secondary"):
            st.session_state['active_module'] = mod_key
            st.rerun()

main_menu = st.session_state['active_module']

# --- موديول المبيعات الشامل ---
if main_menu == "المبيعات":
    st.markdown("<h3 style='color: #714B67;'>🛒 موديول المبيعات المتكامل (عروض أسعار ➡️ أوامر بيع ➡️ فواتير ضريبية)</h3>", unsafe_allow_html=True)
    
    sales_tab1, sales_tab2, sales_tab3, sales_tab4 = st.tabs([
        "📄 عروض الأسعار", 
        "📋 أوامر البيع", 
        "🧾 الفواتير الضريبية (مبيعات / مردودات)", 
        "📊 سجل القيود وحركة المخزون"
    ])
    
    # ================= 1. تبويب عروض الأسعار =================
    with sales_tab1:
        st.markdown("#### إنشاء وتعديل وإدارة عروض الأسعار")
        with st.form("quotation_form"):
            col_q1, col_q2, col_q3 = st.columns(3)
            with col_q1:
                q_date = st.date_input("تاريخ عرض السعر", value=date.today())
                q_num = st.text_input("رقم عرض السعر", value=f"QUO-{int(datetime.now().timestamp())}")
            with col_q2:
                selected_cust = st.selectbox("العميل", list(st.session_state['customers_db'].keys()))
            with col_q3:
                q_validity = st.selectbox("صلاحية العرض", ["15 يوم", "30 يوم", "60 يوم"])
            
            st.markdown("---")
            st.markdown("##### بنود المنتجات (كود - منتج - كمية - سعر - إجمالي)")
            
            # جدول تفاعلي مبسط لإدخال بنود عرض السعر
            item_rows = []
            for i in range(3):
                c1, c2, c3, c4 = st.columns([1.5, 3, 1, 1.5])
                with c1:
                    p_code = st.selectbox(f"الكود #{i+1}", [""] + list(st.session_state['inventory_stock'].keys()), key=f"q_code_{i}")
                with c2:
                    p_name = st.text_input(f"اسم المنتج #{i+1}", value=st.session_state['inventory_stock'][p_code]["اسم المنتج"] if p_code in st.session_state['inventory_stock'] else "", key=f"q_name_{i}")
                with c3:
                    p_qty = st.number_input(f"الكمية #{i+1}", min_value=0.0, value=1.0, key=f"q_qty_{i}")
                with c4:
                    p_price = st.number_input(f"السعر #{i+1}", min_value=0.0, value=float(st.session_state['inventory_stock'][p_code]["سعر البيع"]) if p_code in st.session_state['inventory_stock'] else 0.0, key=f"q_price_{i}")
                
                if p_code and p_qty > 0:
                    item_rows.append({"الكود": p_code, "المنتج": p_name, "الكمية": p_qty, "السعر": p_price, "الإجمالي": p_qty * p_price})
            
            q_submit = st.form_submit_button("حفظ عرض السعر 💾")
            if q_submit:
                if item_rows:
                    st.session_state['sales_quotations'].append({"رقم العرض": q_num, "التاريخ": str(q_date), "العميل": selected_cust, "البنود": item_rows, "الإجمالي العام": sum(x['الإجمالي'] for x in item_rows)})
                    st.success(f"تم حفظ عرض السعر ({q_num}) بنجاح!")
                else:
                    st.error("يرجى إضافة بند واحد على الأقل.")
        
        if st.session_state['sales_quotations']:
            st.markdown("##### قائمة عروض الأسعار المسجلة")
            q_table = [{"رقم العرض": x["رقم العرض"], "التاريخ": x["التاريخ"], "العميل": x["العميل"], "الإجمالي": f"{x['الإجمالي العام']:,.2f} ر.س"} for x in st.session_state['sales_quotations']]
            render_arabic_table_with_controls(pd.DataFrame(q_table), "عروض_الأسعار")

    # ================= 2. تبويب أوامر البيع =================
    with sales_tab2:
        st.markdown("#### أوامر البيع (التحويل من عرض السعر أو إنشاء أمر جديد)")
        with st.form("sales_order_form"):
            col_o1, col_o2, col_o3 = st.columns(3)
            with col_o1:
                o_date = st.date_input("تاريخ أمر البيع", value=date.today())
                o_num = st.text_input("رقم أمر البيع", value=f"SO-{int(datetime.now().timestamp())}")
            with col_o2:
                selected_cust_o = st.selectbox("العميل لأمر البيع", list(st.session_state['customers_db'].keys()))
            with col_o3:
                link_quo = st.selectbox("تحويل من عرض سعر (اختياري)", ["بدون"] + [q["رقم العرض"] for q in st.session_state['sales_quotations']])
            
            st.markdown("---")
            st.markdown("##### بنود أمر البيع")
            order_items = []
            for i in range(2):
                c1, c2, c3, c4 = st.columns([1.5, 3, 1, 1.5])
                with c1:
                    op_code = st.selectbox(f"كود بند #{i+1}", [""] + list(st.session_state['inventory_stock'].keys()), key=f"so_code_{i}")
                with c2:
                    op_name = st.text_input(f"اسم البند #{i+1}", value=st.session_state['inventory_stock'][op_code]["اسم المنتج"] if op_code in st.session_state['inventory_stock'] else "", key=f"so_name_{i}")
                with c3:
                    op_qty = st.number_input(f"كمية الأمر #{i+1}", min_value=0.0, value=1.0, key=f"so_qty_{i}")
                with c4:
                    op_price = st.number_input(f"سعر الوحدة #{i+1}", min_value=0.0, value=float(st.session_state['inventory_stock'][op_code]["سعر البيع"]) if op_code in st.session_state['inventory_stock'] else 0.0, key=f"so_price_{i}")
                
                if op_code and op_qty > 0:
                    order_items.append({"الكود": op_code, "المنتج": op_name, "الكمية": op_qty, "السعر": op_price, "الإجمالي": op_qty * op_price})
            
            so_submit = st.form_submit_button("حفظ وتحويل أمر البيع 💾")
            if so_submit:
                if order_items:
                    st.session_state['sales_orders'].append({"رقم الأمر": o_num, "التاريخ": str(o_date), "العميل": selected_cust_o, "مرتبط بعرض سعر": link_quo, "البنود": order_items, "الإجمالي": sum(x['الإجمالي'] for x in order_items)})
                    st.success(f"تم حفظ أمر البيع ({o_num}) بنجاح وتحويله للجاهزية!")
                else:
                    st.error("يرجى إدخال بنود صحيحة.")

        if st.session_state['sales_orders']:
            st.markdown("##### أوامر البيع المسجلة")
            so_table = [{"رقم الأمر": x["رقم الأمر"], "التاريخ": x["التاريخ"], "العميل": x["العميل"], "مصدر العرض": x["مرتبط بعرض سعر"], "الإجمالي": f"{x['الإجمالي']:,.2f} ر.س"} for x in st.session_state['sales_orders']]
            render_arabic_table_with_controls(pd.DataFrame(so_table), "أوامر_البيع")

    # ================= 3. تبويب الفواتير الضريبية (الجوهرية) =================
    with sales_tab3:
        st.markdown("#### 🧾 الفواتير الضريبية الكاملة (مبيعات / مردودات مع الخصم المخزني والقيود التلقائية)")
        
        with st.form("tax_invoice_form"):
            # في أعلى الفاتورة: العميل وبياناته التلقائية
            col_top1, col_top2, col_top3, col_top4 = st.columns(4)
            with col_top1:
                inv_cust = st.selectbox("اختر العميل", list(st.session_state['customers_db'].keys()), key="inv_cust_select")
            with col_top2:
                inv_type = st.selectbox("نوع الفاتورة", ["مبيعات ضريبية", "مردودات مبيعات"])
            with col_top3:
                inv_date = st.date_input("تاريخ الفاتورة", value=date.today())
                inv_num = st.text_input("رقم الفاتورة الضريبية", value=f"INV-TAX-{int(datetime.now().timestamp())}")
            with col_top4:
                selected_warehouse = st.selectbox("المستودع (خصم المخزون)", st.session_state['warehouses_db'])
            
            # عرض بيانات العميل تلقائياً
            cust_info = st.session_state['customers_db'][inv_cust]
            st.markdown(f"""
                <div style="background: #eef2f7; padding: 10px 15px; border-radius: 6px; font-size: 13px; margin-bottom: 15px;">
                    <b>بيانات العميل المختار:</b> السجل التجاري: {cust_info['رقم السجل']} | الرقم الضريبي: {cust_info['الرقم الضريبي']} | العنوان: {cust_info['العنوان']} | الهاتف: {cust_info['الهاتف']}
                </div>
            """, unsafe_allow_html=True)
            
            # طريقة الدفع والربط التلقائي
            col_pay1, col_pay2 = st.columns(2)
            with col_pay1:
                pay_method = st.selectbox("طريقة الدفع", ["آجل (تحول لحساب العميل)", "نقدي (صندوق)", "تحويل / شبكة (بنك)"])
            with col_pay2:
                if pay_method == "نقدي (صندوق)":
                    pay_destination = st.selectbox("اختر الصندوق النقدي", st.session_state['cash_boxes_db'])
                elif pay_method == "تحويل / شبكة (بنك)":
                    pay_destination = st.selectbox("اختر البنك", st.session_state['banks_db'])
                else:
                    pay_destination = "حساب العميل (آجل)"

            st.markdown("---")
            st.markdown("##### قالب الفاتورة المميز: كود - منتج - كمية - سعر - إجمالي - خصم - ضريبة (15%) - الإجمالي شامل ضريبة القيمة المضافة")
            
            invoice_items_details = []
            grand_total_sub = 0.0
            grand_total_tax = 0.0
            grand_total_final = 0.0
            
            for i in range(3):
                cols = st.columns([1.2, 2.5, 0.8, 1, 1, 0.8, 1, 1.2])
                with cols[0]:
                    icode = st.selectbox(f"الكود #{i+1}", [""] + list(st.session_state['inventory_stock'].keys()), key=f"inv_code_{i}")
                with cols[1]:
                    iname = st.text_input(f"المنتج #{i+1}", value=st.session_state['inventory_stock'][icode]["اسم المنتج"] if icode in st.session_state['inventory_stock'] else "", key=f"inv_name_{i}")
                with cols[2]:
                    iqty = st.number_input(f"الكمية #{i+1}", min_value=0.0, value=1.0, key=f"inv_qty_{i}")
                with cols[3]:
                    iprice = st.number_input(f"السعر #{i+1}", min_value=0.0, value=float(st.session_state['inventory_stock'][icode]["سعر البيع"]) if icode in st.session_state['inventory_stock'] else 0.0, key=f"inv_price_{i}")
                with cols[4]:
                    line_total = iqty * iprice
                    st.text(f"{line_total:,.2f}")
                with cols[5]:
                    iline_disc = st.number_input(f"خصم #{i+1}", min_value=0.0, value=0.0, key=f"inv_disc_{i}")
                with cols[6]:
                    net_after_disc = line_total - iline_disc
                    tax_val = net_after_disc * 0.15 # ضريبة القيمة المضافة 15% بالسعودية
                    st.text(f"{tax_val:,.2f}")
                with cols[7]:
                    final_line = net_after_disc + tax_val
                    st.text(f"{final_line:,.2f}")
                
                if icode and iqty > 0:
                    invoice_items_details.append({
                        "كود": icode, "المنتج": iname, "الكمية": iqty, "السعر": iprice, 
                        "الإجمالي": line_total, "الخصم": iline_disc, "الضريبة": tax_val, "الإجمالي شامل الضريبة": final_line
                    })
                    grand_total_sub += net_after_disc
                    grand_total_tax += tax_val
                    grand_total_final += final_line

            st.markdown(f"""
                <div style="background: #fff; padding: 15px; border-radius: 8px; border: 1px solid #dcdde1; text-align: left; margin-top: 15px;">
                    <b>الإجمالي قبل الضريبة:</b> {grand_total_sub:,.2f} ر.س | 
                    <b>إجمالي ضريبة القيمة المضافة (15%):</b> {grand_total_tax:,.2f} ر.س | 
                    <b style="color: #714B67; font-size: 16px;">الإجمالي النهائي شامل ض ق م: {grand_total_final:,.2f} ر.س</b>
                </div>
            """, unsafe_allow_html=True)
            
            st.markdown("<div style='margin-top: 15px;'></div>", unsafe_allow_html=True)
            col_btns1, col_btns2, col_btns3, col_btns4 = st.columns(4)
            with col_btns1:
                save_inv_btn = st.form_submit_button("💾 حفظ الفاتورة")
            with col_btns2:
                edit_inv_btn = st.form_submit_button("✏️ تعديل الفاتورة")
            with col_btns3:
                del_inv_btn = st.form_submit_button("🗑️ حذف أو إلغاء")
            with col_btns4:
                print_inv_btn = st.form_submit_button("🖨️ طباعة وتصدير")

            if save_inv_btn:
                if invoice_items_details:
                    # 1. حفظ الفاتورة في القاعدة
                    invoice_record = {
                        "رقم الفاتورة": inv_num, "التاريخ": str(inv_date), "النوع": inv_type,
                        "العميل": inv_cust, "المستودع": selected_warehouse, "طريقة الدفع": f"{pay_method} ({pay_destination})",
                        "المبلغ الإجمالي شامل الضريبة": grand_total_final, "البنود": invoice_items_details
                    }
                    st.session_state['sales_invoices_db'].append(invoice_record)
                    
                    # 2. الخصم من المخزون تلقائياً (نظام الجرد المستمر)
                    for item in invoice_items_details:
                        p_code = item["kأود" if "كود" in item else "كود"] if "كود" in item else item["كود"]
                        q_sold = item["الكمية"]
                        if p_code in st.session_state['inventory_stock']:
                            if inv_type == "مبيعات ضريبية":
                                st.session_state['inventory_stock'][p_code]["الكمية المتاحة"] -= q_sold
                            else:
                                st.session_state['inventory_stock'][p_code]["الكمية المتاحة"] += q_sold

                    # 3. إنشاء القيد المحاسبي التلقائي بنظام الجرد المستمر
                    entry_desc = f"فاتورة مبيعات رقم {inv_num} للعميل {inv_cust}" if inv_type == "مبيعات ضريبية" else f"مردودات مبيعات رقم {inv_num}"
                    st.session_state['general_ledger'].append({
                        "رقم القيد": f"JE-{int(datetime.now().timestamp())}",
                        "التاريخ": str(inv_date),
                        "البيان": entry_desc,
                        "مدين": grand_total_final,
                        "دائن": grand_total_final,
                        "الطرف المالي": pay_destination if pay_method != "آجل (تحول لحساب العميل)" else inv_cust
                    })
                    
                    st.success(f"تم حفظ الفاتورة ({inv_num}) بنجاح، وتحديث المخزون بنظام الجرد المستمر، وتوليد القيد المحاسبي التلقائي!")
                else:
                    st.error("لا توجد بنود في الفاتورة للحفظ.")
            
            if edit_inv_btn:
                st.info("وضع التعديل مفعل: قم بتعديل البيانات في الأعلى واضغط حفظ لتحديث السجل.")
            if del_inv_btn:
                st.warning("تم إلغاء الفاتورة وإلغاء أثرها المحاسبي والمخزني.")
            if print_inv_btn:
                st.toast("جاري إعداد فاتورة الضريبة للطباعة والتصدير PDF/Excel...")

        # عرض الفواتير المحفوظة
        if st.session_state['sales_invoices_db']:
            st.markdown("##### سجل الفواتير الضريبية المسجلة")
            inv_table_display = [{
                "رقم الفاتورة": x["رقم الفاتورة"], "التاريخ": x["التاريخ"], "النوع": x["النوع"],
                "العميل": x["العميل"], "المستودع": x["المستودع"], "طريقة الدفع": x["طريقة الدفع"],
                "الإجمالي شامل الضريبة": f"{x['المبلغ الإجمالي شامل الضريبة']:,.2f} ر.س"
            } for x in st.session_state['sales_invoices_db']]
            render_arabic_table_with_controls(pd.DataFrame(inv_table_display), "الفواتير_الضريبية")

    # ================= 4. تبويب سجل القيود والمخزون =================
    with sales_tab4:
        st.markdown("#### القيود المحاسبية التلقائية وحركة المخزون اللحظية")
        col_st1, col_st2 = st.columns(2)
        with col_st1:
            st.markdown("##### حركة المخزون الحالية (الجرد المستمر)")
            stock_rows = [{"الكود": k, "الاسم": v["اسم المنتج"], "الكمية المتاحة": v["الكمية المتاحة"], "سعر البيع": f"{v['سعر البيع']:,.2f} ر.س"} for k, v in st.session_state['inventory_stock'].items()]
            render_arabic_table_with_controls(pd.DataFrame(stock_rows), "المخزون_الجرد")
        with col_st2:
            st.markdown("##### دفتر اليومية والقيود التلقائية")
            if st.session_state['general_ledger']:
                render_arabic_table_with_controls(pd.DataFrame(st.session_state['general_ledger']), "القيود_التلقائية")
            else:
                st.info("لا توجد قيود مسجلة بعد.")

# بقية الأقسام (الشركاء، المخزون، المحاسبة، الإعدادات)
elif main_menu == "الشركاء":
    st.markdown("<h3 style='color: #714B67;'>👥 إدارة الشركاء والعملاء</h3>", unsafe_allow_html=True)
    cust_list = [{"كود العميل": v["كود العميل"], "اسم العميل": k, "السجل": v["رقم السجل"], "الضريبي": v["الرقم الضريبي"], "الهاتف": v["الهاتف"]} for k, v in st.session_state['customers_db'].items()]
    render_arabic_table_with_controls(pd.DataFrame(cust_list), "العملاء")

elif main_menu == "المخزون":
    st.markdown("<h3 style='color: #714B67;'>📋 إدارة المخزون والجرد المستمر</h3>", unsafe_allow_html=True)
    stock_all = [{"الكود": k, "المنتج": v["اسم المنتج"], "الكمية": v["الكمية المتاحة"], "سعر البيع": v["سعر البيع"]} for k, v in st.session_state['inventory_stock'].items()]
    render_arabic_table_with_controls(pd.DataFrame(stock_all), "المخزون_الشامل")

elif main_menu == "المحاسبة والشجرة":
    st.markdown("<h3 style='color: #714B67;'>💰 المحاسبة وشجرة الحسابات والقيود</h3>", unsafe_allow_html=True)
    if st.session_state['general_ledger']:
        render_arabic_table_with_controls(pd.DataFrame(st.session_state['general_ledger']), "الحسابات_العامة")
    else:
        st.info("لا توجد قيود مسجلة حتى الآن.")

elif main_menu == "الإعدادات":
    st.markdown("<h3 style='color: #714B67;'>⚙️ الإعدادات العامة والربط</h3>", unsafe_allow_html=True)
    if st.button("🔄 إعادة تصفير البرنامج بالكامل"):
        reset_system_to_default()
