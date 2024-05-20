from langchain_google_genai import GoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain.text_splitter import CharacterTextSplitter
from langchain.chains import LLMChain
from PyPDF2 import PdfReader
from dotenv import load_dotenv
import db_connection as dbc
import os
import re

load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
llm = GoogleGenerativeAI(model="models/text-bison-001", google_api_key=api_key, temperature=0.5, verbose=True)



# def pdf_to_qa_text(pdf='CBot2/a.pdf'):
#     # extracting pdf text
#     pdf_reader = PdfReader(pdf)
#     text = ''
#     for page in pdf_reader.pages:
#         text += page.extract_text()

#     # split into chunks
#     text_splitter = CharacterTextSplitter(
#         separator="\n",
#         chunk_size=2000,
#         chunk_overlap=100,
#         length_function=len
#     )

#     chunks = text_splitter.split_text(text)
#     print(len(chunks))
#     qa_tuples = []
#     count = 0
#     for text_chunk in chunks:
#         print(count)
#         count += 1
#         template = '''You'll be provided with a text.

# Your task is to craft five unique medium-sized questions based on the given text. Answers can range from one line to descriptive.

# Your response string should be structured as follows:

# Q1: Question 1
# A1: Answer 1
# Q2: Question 2
# A2: Answer 2
# Q3: Question 3
# A3: Answer 3
# Q4: Question 4
# A4: Answer 4
# Q5: Question 5
# A5: Answer 5

# Do not include any special characters including brackets such as ! @ # $ % ^ & * () [] in your response.

# Do not add extra spaces in your response. Make it compact.

# Reformat your response neatly.

# % USER INPUT:

# {text}

# YOUR RESPONSE:
# '''

#         prompt = PromptTemplate(
#             input_variables=["text"],
#             template=template
#         )

#         chain = LLMChain(llm=llm, prompt=prompt)
#         dic = chain.invoke({"text": text_chunk})
#         response_text = dic.get('text')
#         print(response_text)
#         print(); print()

#         # Parse the structured string format
#         qa_pairs = re.findall(r'Q\d+: (.*?)\nA\d+: (.*?)(?:\n|$)', response_text)
#         print(qa_pairs)
#         print(type(qa_pairs))
#         qa_tuples.extend(qa_pairs)

#     return qa_tuples

import re
from PyPDF2 import PdfReader
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.text_splitter import CharacterTextSplitter

def pdf_to_qa_text(pdf='CBot2/a.pdf'):
    # extracting pdf text
    pdf_reader = PdfReader(pdf)
    text = ''
    for page in pdf_reader.pages:
        text += page.extract_text()

    # split into chunks
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=2000,
        chunk_overlap=100,
        length_function=len
    )

    chunks = text_splitter.split_text(text)
    print(len(chunks))
    qa_tuples = []
    count = 0
    for text_chunk in chunks:
        try:
            print(count)
            count += 1
            template = '''You'll be provided with a text.

Your task is to craft five unique medium-sized questions based on the given text. Answers can range from one line to descriptive.

Your response string should be structured as follows:

Q1: Question 1
A1: Answer 1
Q2: Question 2
A2: Answer 2
Q3: Question 3
A3: Answer 3
Q4: Question 4
A4: Answer 4
Q5: Question 5
A5: Answer 5

Do not include any special characters including brackets such as ! @ # $ % ^ & * () [] in your response.

Do not add extra spaces in your response. Make it compact.

Reformat your response neatly.

% USER INPUT:

{text}

YOUR RESPONSE:
'''

            prompt = PromptTemplate(
                input_variables=["text"],
                template=template
            )

            chain = LLMChain(llm=llm, prompt=prompt)
            dic = chain.invoke({"text": text_chunk})
            response_text = dic.get('text')
            # print(response_text)
            print(); print()

            # Parse the structured string format
            qa_pairs = re.findall(r'Q\d+: (.*?)\nA\d+: (.*?)(?:\n|$)', response_text)
            # print(qa_pairs)
            # print(type(qa_pairs))
            qa_tuples.extend(qa_pairs)
        except Exception as e:
            print(f"Error processing chunk {count}: {e}")
            continue

    return qa_tuples


def append_text_to_database(li):
    print("Before\n")
    print( dbc.show_qadb())
    for qa_tuple in li:
        dbc.add_qa_tuple_in_table( qa_tuple)
    print("After")
    print(dbc.show_qadb())
    print('Added to Database')
    return 'Database Createdd successfully!!'

def list_pdf_files(folder_path=os.getcwd()):
    # Initialize an empty list to store PDF files
    pdf_files = []

    # Loop through all files in the folder
    for file in os.listdir(folder_path):
        # Check if the file has a .pdf extension
        if file.lower().endswith('.pdf'):
            # If yes, append the file name to the list
            pdf_files.append(file)

    # Return the list of PDF files
    return pdf_files






