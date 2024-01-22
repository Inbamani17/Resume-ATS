import streamlit as st
import google.generativeai as genai
import os
import PyPDF2 as pdf
from dotenv import load_dotenv

load_dotenv()

#API key from Google Maker Suite
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

HOME = "Home"
CHECKER = "Checker"
CRESULT = "CResult"
MATCHER = "Upload"
MRESULT = "MResult"

#Initialization of State
def init_session_state():
    # Initialize session state variables here
    if 'page' not in st.session_state:
        st.session_state.page = HOME

    st.session_state.input_text = ""
    st.session_state.uploaded_file = None
    st.session_state.content = None

#Generative Model for Job Matcher
def get_gemini_response(input_text, pdf_content, prompt):
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content([input_text, pdf_content, prompt])
    return response.text

#Generative Model for Resume Checker
def cget_gemini_response(pdf_content, prompt):
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content([pdf_content, prompt])
    return response.text

#Text Extraction
def input_pdf_text(uploaded_file):
    reader = pdf.PdfReader(uploaded_file)
    text = ""
    for page in range(len(reader.pages)):
        page = reader.pages[page]
        text += str(page.extract_text())
    return text

#Home Page
def render_home():
    st.markdown("<h1 style='text-align: center;'>RESUME SCORE</h1>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)

    st.write()
    st.write()

    card_container1 = st.container(border = True)
    card_container2 = st.container(border = True)

    with col1:
        with card_container1:
            st.header("Job Matcher")
            st.markdown("✧ Help the job seekers identify how well their resumes align with the requirements of a particular job.")
            st.markdown("✧ Make targeted adjustments to their resumes, ensuring that they are more likely to be noticed by hiring managers and recruiters.")
            st.markdown("✧ Guide the job seekers in tailoring their resume content based on the specific requirements of the job.")
            submit2 = st.button("Job Matcher")

    with col2:
        with card_container2:
            st.header("Score Checker")
            st.markdown("✧ In a competitive job market, getting past the initial ATS screening is crucial.")
            st.markdown("✧ Streamline the process of making adjustments by providing insights into how well a resume matches the criteria set by the ATS.")
            st.markdown("✧ By understanding the ATS score, applicants can optimize their resumes to increase the chances of passing through the initial automated screening process.")
            submit1 = st.button("Check your score")
        
    if submit1:
        st.session_state.page = CHECKER
    elif submit2:
        st.session_state.page = MATCHER

#Resume Uploader for Checker
def render_uchecker():
    submit2 = st.button("Back")
    st.header("Resume Checker")
    st.write()
    st.session_state.uploaded_file = st.file_uploader("Resume(PDF)", type=["pdf"])
    
    submit1 = st.button("Load")

    if submit1:
        if st.session_state.uploaded_file is not None:
            st.session_state.content = input_pdf_text(st.session_state.uploaded_file)
            st.write("PDF Uploaded Successfully")
            st.session_state.page = CRESULT
        else:
            st.write("Please upload the resume")
    elif submit2:
        st.session_state.page = HOME

#Resume Analysis for Checker
def render_cresult():
    submit2 = st.button("Home")
    st.markdown("<h1 style='text-align center;'>Resume Analysis</h1>", unsafe_allow_html=True)
    
    job_desc = st.session_state.input_text
    pdf_content = st.session_state.content

    Atsscore = """
    Consider you are an skilled ATS (Applicant Tracking System) scanner with a deep understanding of ATS functionality, your task is to evaluate the resume
    You must consider the job market is very competitive and you should provide best assistance for improving the resumes.
    Rate the resume out of 100
    Keyword - Scan for keywords relevant to the industry, job title, and skills. Minimum 10 keywords are highly rated, lesser keywords lesser rating.
    Quantifiable Achievements - Scan for quantifiable achievements. Minimum 3 quantifiable elements must be present for high rating, lesser keywords lesser rating.
    Grammar - Check for grammatical error, high error less rating.
    Length - The total word count must be in between 300 to 500 for good rating, lower the count lower rating provided.
    Concise - the resume must be concise without fillers, high fillers less rating.
    The output must be in the following format
    1.Rating(in bold font) - Display the rating out of 100
    2.Keyword(in bold font) - Mention Great or Good or Average or Bad. 
    3.Highlight your view on the use of keywords. Do not list down the keywords mentioned
    4.Quantifiable Achievements(in bold font) - Mention Great or Good or Average or Bad. 
    5.Highlight your view on the use of Quantifiable Achievements .
    6.Grammar(in bold font) - Mention Great or Good or Average or Bad. 
    7.Highlight your view on the use of Grammar.
    8.Length(in bold font) - Mention Great or Good or Average or Bad. 
    9.Highlight your view on the use of Length.
    10.Concise(in bold font) - Mention Great or Good or Average or Bad. 
    11.Highlight your view on the use of Concise.
    """

    Final = """
    Consider you are an skilled ATS (Applicant Tracking System) scanner with a deep understanding of job roles in software field and ATS functionality, your task is to evaluate the resume against the provided job description.
    You must consider the job market is very competitive and you should provide best assistance for improving the resumes.
    Give your final thougths on the resume
    Give the answer in formal tone
    limit the output to 3-5 bullet points
    """

    Atsscore = cget_gemini_response(pdf_content, Atsscore)
    Final = cget_gemini_response(pdf_content, Final)

    st.write()
    st.write()

    card_container = st.container(border = True)
    card_container = st.container(border = True)

    card_container.subheader("ATS Score")
    card_container.write(Atsscore)
    card_container.write()
    st.subheader("Final")
    st.write(Final)
    if submit2:
        st.session_state.page = HOME

#Resume Uploader for Matcher
def render_umatcher():
    submit2 = st.button("Home")
    st.header("Job Matcher")
    col1, col2 = st.columns(2)
    card_container1 = st.container(border = True)
    card_container2 = st.container(border = True)
    with col1:
        with card_container1:
            st.session_state.uploaded_file = st.file_uploader("RESUME (PDF)", type=["pdf"])
    with col2:
        with card_container2:
            st.session_state.input_text = st.text_area("JOB DESCRIPTION", key=input)
    
    submit1 = st.button("Load")

    if submit1:
        if st.session_state.uploaded_file is not None:
            st.session_state.content = input_pdf_text(st.session_state.uploaded_file)
            st.write("PDF Uploaded Successfully")
            st.session_state.page = MRESULT
        else:
            st.write("Please upload the resume")
    elif submit2:
        st.session_state.page = HOME

#Resume Analysis for Job Matcher
def render_mresult():
    st.markdown("<h1 style='text-align:center;'>Resume Analysis</h1>", unsafe_allow_html=True)
    
    job_desc = st.session_state.input_text
    pdf_content = st.session_state.content

    Atsscore = """
    Consider you are an skilled ATS (Applicant Tracking System) scanner with a deep understanding of job roles in software field and ATS functionality, your task is to evaluate the resume against the provided job description.
    You must consider the job market is very competitive and you should provide best assistance for improving the resumes.
    Give the output as score out of 100 on how the resume aligns with the job description
    Give the answer in formal tone
    limit the output to 3-5 bullet points
    """
    
    Overview = """
    Consider you are an skilled ATS (Applicant Tracking System) scanner with a deep understanding of job roles in software field and ATS functionality, your task is to evaluate the resume against the provided job description.
    You must consider the job market is very competitive and you should provide best assistance for improving the resumes.
    Highlight your professional evaluation on whether the candidate's profile and suitable role based on experience. 
    Give the answer in formal tone
    limit the output to 3-5 bullet points
    """

    Strength = """
    Consider you are an skilled ATS (Applicant Tracking System) scanner with a deep understanding of job roles in software field and ATS functionality, your task is to evaluate the resume against the provided job description.
    You must consider the job market is very competitive and you should provide best assistance for improving the resumes.
    Highlight your view in the strengths of the applicant in relation to the specified job requirements.
    Give the answer in formal tone
    limit the output to 3-5 bullet points
    """
    
    Improvement = """
    Consider you are an skilled ATS (Applicant Tracking System) scanner with a deep understanding of job roles in software field and ATS functionality, your task is to evaluate the resume against the provided job description.
    You must consider the job market is very competitive and you should provide best assistance for improving the resumes.
    Highlight your view in the areas of improvemnet the applicant in relation to the specified job requirements.
    Give the answer in formal tone
    limit the output to 3-5 bullet points
    """

    Skills = """
    Consider you are an skilled ATS (Applicant Tracking System) scanner with a deep understanding of job roles in software field and ATS functionality, your task is to evaluate the resume against the provided job description.
    You must consider the job market is very competitive and you should provide best assistance for improving the resumes.
    Make a table with two coloumns and mention the skills the applicant acquired and the skills the applicant must develop
    """

    Keywords = """
    Consider you are an skilled ATS (Applicant Tracking System) scanner with a deep understanding of job roles in software field and ATS functionality, your task is to evaluate the resume against the provided job description.
    You must consider the job market is very competitive and you should provide best assistance for improving the resumes.
    Provide the output with only high priority keywords that are missing in the resume minimum 5 keywords to maximum 10 keywords 
    """

    Final = """
    Consider you are an skilled ATS (Applicant Tracking System) scanner with a deep understanding of job roles in software field and ATS functionality, your task is to evaluate the resume against the provided job description.
    You must consider the job market is very competitive and you should provide best assistance for improving the resumes.
    Give your final thougths on the resume
    Give the answer in formal tone
    limit the output to 3-5 bullet points
    """

    Atsscore = get_gemini_response(job_desc, pdf_content, Atsscore)
    Overview = get_gemini_response(job_desc, pdf_content, Overview)
    Strength = get_gemini_response(job_desc, pdf_content, Strength)
    Improvement = get_gemini_response(job_desc, pdf_content, Improvement)
    Skills = get_gemini_response(job_desc, pdf_content, Skills)
    Keywords = get_gemini_response(job_desc, pdf_content, Keywords)
    Final = get_gemini_response(job_desc, pdf_content, Final)

    st.subheader("ATS Score")
    st.write(Atsscore)
    st.write()
    st.subheader("Overview")
    st.write(Overview)
    st.write()
    st.subheader("Strength")
    st.write(Strength)
    st.write()
    st.subheader("Areas of Improvement")
    st.write(Improvement)
    st.write()
    st.subheader("Skills")
    st.write(Skills)
    st.write()
    st.subheader("Keywords")
    st.write(Keywords)
    st.write()
    st.subheader("Final")
    st.write(Final)

#Main Function
def main():
    #Initialize session state
    if 'page' not in st.session_state:
        init_session_state()

    #Render different pages based on the current page
    if st.session_state.page == HOME:
        render_home()
    elif st.session_state.page == CHECKER:
        render_uchecker()
    elif st.session_state.page == CRESULT:
        render_cresult()
    elif st.session_state.page == MATCHER:
        render_umatcher()
    elif st.session_state.page == MRESULT:
        render_mresult()

#Run the app
if __name__ == "__main__":
    main()
