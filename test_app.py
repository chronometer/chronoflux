import streamlit as st

st.title('Connection Test')
st.success('If you see this, Streamlit is working!')
st.write('Server time: ' + st.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
