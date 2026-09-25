import pandas as pd
import streamlit as st
st.set_page_config(page_title="مساعد القرار",page_icon="🧠",layout="wide")
st.markdown("""<style>
@import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;800&display=swap');
html,body,[class*="css"]{font-family:Cairo,sans-serif}.main{background:#f4f7fb}
.hero{background:linear-gradient(135deg,#06253f,#0b5575,#12a99a);padding:28px 34px;border-radius:22px;color:white;margin-bottom:20px}
.hero h1{font-size:36px;margin:0;font-weight:800}.hero p{font-size:17px}
.card{background:white;border:1px solid #e7edf4;border-radius:18px;padding:18px;box-shadow:0 6px 22px #142d4610}
.kpi{font-size:26px;font-weight:800;color:#073b5c}.lbl{color:#68788a;font-size:13px}
.ins{background:#ecfbf8;border-right:5px solid #10a99a;padding:12px;border-radius:12px;margin:8px 0}
</style>""",unsafe_allow_html=True)
with st.sidebar:
 st.markdown("## 🧠 مساعد القرار"); st.caption("Excel AI Assistant"); st.divider()
 st.markdown("**المصمم**"); st.markdown("### سلطان الضبعان")
 st.caption("المشروع النهائي — البرنامج التأسيسي للذكاء الاصطناعي")
 st.divider(); st.markdown("### طريقة الاستخدام")
 st.markdown("1. ارفع Excel\n2. اطرح سؤالًا\n3. راجع المؤشرات\n4. استخدم الاستنتاجات")
st.markdown('<div class="hero"><h1>مساعد القرار</h1><p>من بيانات Excel إلى رؤى واضحة وقرارات أذكى — باستخدام الذكاء الاصطناعي.</p></div>',unsafe_allow_html=True)
up=st.file_uploader("📁 ارفع ملف Excel",type=["xlsx","xls"])
df=pd.read_excel(up) if up else pd.read_excel("sample_sales_data.xlsx")
if not up: st.info("تم تحميل البيانات التجريبية. يمكنك رفع ملفك بدلًا منها.")
rename={}
for c in df.columns:
 x=str(c).lower().strip()
 if x in ["المبيعات","sales","revenue","amount"]: rename[c]="Sales"
 if x in ["المنتج","product"]: rename[c]="Product"
 if x in ["المنطقة","region","area"]: rename[c]="Region"
df=df.rename(columns=rename); nums=df.select_dtypes("number").columns.tolist()
sc="Sales" if "Sales" in df.columns else (nums[0] if nums else None)
total=df[sc].sum() if sc else 0; avg=df[sc].mean() if sc else 0
a,b,c,d=st.columns(4)
for col,val,label in [(a,f"{total:,.0f}","إجمالي القيمة"),(b,f"{len(df):,}","عدد السجلات"),(c,f"{avg:,.0f}","متوسط القيمة"),(d,str(len(df.columns)),"عدد الحقول")]:
 with col: st.markdown(f'<div class="card"><div class="kpi">{val}</div><div class="lbl">{label}</div></div>',unsafe_allow_html=True)
l,m,r=st.columns([1,1.2,1])
with l:
 st.markdown("### ✨ أهم الاستنتاجات")
 if sc and "Product" in df:
  x=df.groupby("Product")[sc].sum().sort_values(ascending=False); st.markdown(f'<div class="ins">🏆 الأعلى: <b>{x.index[0]}</b><br>{x.iloc[0]:,.0f}</div>',unsafe_allow_html=True)
 if sc and "Region" in df:
  x=df.groupby("Region")[sc].sum().sort_values(ascending=False); st.markdown(f'<div class="ins">📍 المنطقة الأعلى: <b>{x.index[0]}</b><br>{x.iloc[0]:,.0f}</div>',unsafe_allow_html=True)
with m:
 st.markdown("### 💬 اسأل مساعد القرار")
 q=st.text_input("اكتب سؤالك",placeholder="ما أكثر منتج مبيعًا؟")
 if st.button("🔎 تحليل السؤال",type="primary") and q:
  if sc and "Product" in df and ("منتج" in q or "الأكثر" in q):
   x=df.groupby("Product")[sc].sum().sort_values(ascending=False); st.success(f"المنتج الأعلى مبيعًا هو {x.index[0]} بإجمالي {x.iloc[0]:,.0f}.")
  elif sc and ("اجمالي" in q or "الإجمالي" in q): st.success(f"الإجمالي {total:,.0f}.")
  elif sc and "متوسط" in q: st.success(f"المتوسط {avg:,.0f}.")
  else: st.warning("يمكن ربط هذا الحقل بـ LLM لتمكين الأسئلة الحرة.")
 st.markdown("#### 📋 معاينة البيانات"); st.dataframe(df.head(8),use_container_width=True,height=230)
with r:
 st.markdown("### 📈 توزيع القيمة")
 if sc and "Product" in df: st.bar_chart(df.groupby("Product")[sc].sum())
 elif sc: st.bar_chart(df[sc])
st.divider(); st.caption("مساعد القرار | تصميم وتطوير: سلطان الضبعان")
