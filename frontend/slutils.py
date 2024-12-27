import streamlit as st

def display_faq_qna(response):
    st.markdown("""
        <style>
        .small-font {
            font-size: 14px;
            white-space: pre-wrap;
            word-wrap: break-word;
        }
        </style>
        """, unsafe_allow_html=True)
    
    st.markdown(f"**Question:** {response['query']}")
    
    for item in response['reply']:
        faq = item['faq']
        answer = item['answer']
        st.markdown(f"<div class='small-font'><b>{faq.strip()}</b></div>", unsafe_allow_html=True)
        st.markdown(f"<div class='small-font'>{answer.strip()}</div><br>", unsafe_allow_html=True)

def display_faq_qna(response):
    st.markdown("""
        <style>
        .small-font {
            font-size: 14px;
            white-space: pre-wrap;
            word-wrap: break-word;
        }
        </style>
        """, unsafe_allow_html=True)
    
    st.markdown(f"**Question:** {response['query']}")
    
    for idx, item in enumerate(response['reply']):
        faq = item['faq']
        answer = item['answer']
        
        st.markdown(f"<div class='small-font'><b>{faq.strip()}</b></div>", unsafe_allow_html=True)
        st.markdown(f"<div class='small-font'>{answer.strip()}</div>", unsafe_allow_html=True)
        
        # Add line break except for the last item
        if idx < len(response['reply']) - 1:
            st.markdown("<br>", unsafe_allow_html=True)
            
# def display_multi_answer(response):
#     st.markdown("""
#         <style>
#         .small-font {
#             font-size: 14px;
#             white-space: pre-wrap;
#             word-wrap: break-word;
#         }
#         </style>
#         """, unsafe_allow_html=True)
    
#     st.markdown(f"**Question:** {response['query']}")
    
#     for answer in response['reply']:
#         st.markdown(f"<div class='small-font'>{answer.strip()}</div><br>", unsafe_allow_html=True)

# def display_multi_answer(response):
#     st.markdown("""
#         <style>
#         .small-font {
#             font-size: 14px;
#             white-space: pre-wrap;
#             word-wrap: break-word;
#         }
#         </style>
#         """, unsafe_allow_html=True)
    
#     st.markdown(f"**Question:** {response['query']}")
    
#     for idx, answer in enumerate(response['reply']):
#         st.markdown(f"<div class='small-font'>{answer.strip()}</div>", unsafe_allow_html=True)
        
#         # Add line break except for the last item
#         if idx < len(response['reply']) - 1:
#             st.markdown("<br>", unsafe_allow_html=True)

# def display_multi_answer(response):
#     st.markdown("""
#         <style>
#         .small-font {
#             font-size: 14px;
#             white-space: pre-wrap;
#             word-wrap: break-word;
#         }
#         </style>
#         """, unsafe_allow_html=True)
    
#     st.markdown(f"**Question:** {response['query']}")
    
#     answer_text = "<br>".join(
#         [f"<div class='small-font'>{answer.strip()}</div>" for answer in response['reply']]
#     )
    
#     st.markdown(answer_text, unsafe_allow_html=True)

def display_multi_answer(response):
    st.markdown("""
        <style>
        .small-font {
            font-size: 14px;
            white-space: pre-wrap;
            word-wrap: break-word;
        }
        ol {
            margin: 0;
            padding-left: 20px;
        }
        li {
            margin-bottom: 10px;
        }
        </style>
        """, unsafe_allow_html=True)
    
    st.markdown(f"**Question:** {response['query']}")
    
    answer_text = "<ol>" + "".join(
        [f"<li>{answer.strip()}</li>" for answer in response['reply']]
    ) + "</ol>"
    
    st.markdown(answer_text, unsafe_allow_html=True)
        
def display_response(response):
    if not response:
        st.markdown("No answer")
        return 0
        
    if len(response.keys()) == 0:
        st.markdown("No answer")
        return 0

    if isinstance(response['reply'][0], dict):
        display_faq_qna(response)  # Call FAQ parser if list contains dict
    else:
        display_multi_answer(response)  # Call multi-answer parser if list contains text
