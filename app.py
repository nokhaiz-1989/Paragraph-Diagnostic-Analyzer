import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Paragraph Diagnostic Analyzer",layout="wide")
st.title("Paragraph Diagnostic Analyzer")

uploaded=st.file_uploader("Upload Excel",type=["xlsx"])

levels=[(0,20,"Minimal"),(21,40,"Needs Improvement"),(41,60,"Developing"),(61,80,"Proficient"),(81,100,"Exemplary")]
colors={"Minimal":"red","Needs Improvement":"orange","Developing":"#FFD84F","Proficient":"blue","Exemplary":"green"}

def seg(x):
    for a,b,l in levels:
        if a<=x<=b:return l
    return "Unknown"

activities={
"Topic Sentence":["Topic sentence sorting","Rewrite weak topic sentences"],
"Supporting Details":["Expand the sentence","Add examples","Hamburger paragraph"],
"Organization":["Paragraph sequencing","Transition word activity"],
"Unity":["Remove irrelevant sentence","Stay-on-topic exercise"],
"Coherence":["Transition connectors","Sentence linking"],
"Concluding Sentence":["Write better conclusions","Complete the ending"],
"Grammar":["Error correction","Grammar relay"],
"Vocabulary":["Synonym challenge","Academic word bank"],
"Mechanics":["Punctuation hunt","Capitalization practice"]
}

if uploaded:
    df=pd.read_excel(uploaded)
    comps=df.columns[2:]
    st.metric("Students",len(df))
    overall=df[comps].stack()
    st.metric("Overall Average",f"{overall.mean():.1f}%")
    segs=overall.apply(seg).value_counts().reindex(["Minimal","Needs Improvement","Developing","Proficient","Exemplary"],fill_value=0)
    fig=px.pie(values=segs.values,names=segs.index,title="Overall Performance Distribution",color=segs.index,color_discrete_map=colors)
    st.plotly_chart(fig,use_container_width=True)
    avg=df[comps].mean().sort_values()
    st.subheader("Component Performance")
    st.bar_chart(avg)
    matrix=[]
    for c in comps:
        vc=df[c].apply(seg).value_counts()
        matrix.append([c]+[vc.get(k,0) for k in ["Minimal","Needs Improvement","Developing","Proficient","Exemplary"]])
    mdf=pd.DataFrame(matrix,columns=["Component","Minimal","Needs Improvement","Developing","Proficient","Exemplary"])
    st.subheader("Performance Matrix")
    st.dataframe(mdf,use_container_width=True)
    weak=avg.idxmin(); strong=avg.idxmax()
    c1,c2=st.columns(2)
    c1.success(f"Strongest Component: {strong} ({avg.max():.1f}%)")
    c2.error(f"Weakest Component: {weak} ({avg.min():.1f}%)")
    st.subheader("Suggested Activities")
    for a in activities.get(weak,[]): st.write("•",a)
