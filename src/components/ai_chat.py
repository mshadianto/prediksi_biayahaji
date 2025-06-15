"""AI Chat component"""
import streamlit as st

def render_ai_chat(agentic_ai, rag_system):
    """Render AI chat interface"""
    
    st.header("Analisis RAG Agentic AI")
    
    # Pre-defined questions
    st.subheader("Pertanyaan Populer")
    
    example_questions = [
        "Bagaimana pengaruh kenaikan harga emas terhadap biaya haji?",
        "Prediksi biaya haji untuk 2 tahun ke depan?",
        "Faktor apa saja yang mempengaruhi biaya haji?",
        "Strategi menabung untuk biaya haji yang efektif?",
        "Kapan waktu terbaik untuk mendaftar haji?"
    ]
    
    for i, question in enumerate(example_questions):
        if st.button(f"Q: {question[:50]}...", key=f"q_{i}"):
            st.session_state['user_question'] = question
    
    # User input
    st.subheader("Ajukan Pertanyaan Anda")
    
    user_query = st.text_area(
        "Pertanyaan:",
        value=st.session_state.get('user_question', ''),
        placeholder="Contoh: Bagaimana pengaruh inflasi terhadap biaya haji tahun depan?",
        height=100
    )
    
    col1, col2 = st.columns([1, 4])
    
    with col1:
        analyze_button = st.button("Analisis", type="primary")
    
    with col2:
        if st.button("Clear"):
            st.session_state['user_question'] = ''
            st.rerun()
    
    if analyze_button and user_query:
        with st.spinner("AI sedang menganalisis..."):
            # Retrieve context
            context = rag_system.retrieve_context(user_query)
            
            # Add current data context (simplified for demo)
            current_data_context = """
            Data Real-time Saat Ini:
            - Harga Emas: ~$2000/oz
            - Nilai Tukar USD/IDR: ~Rp 15,000
            - Prediksi Biaya Realistis: ~Rp 75-80 juta
            """
            
            full_context = context + current_data_context
            
            # Generate AI response
            ai_response = agentic_ai.generate_response(user_query, full_context)
            
            # Display response
            st.markdown("### Analisis AI:")
            st.markdown(ai_response)
            
            # Feedback
            st.markdown("---")
            st.markdown("**Apakah analisis ini membantu?**")
            feedback_cols = st.columns(3)
            
            with feedback_cols[0]:
                if st.button("Ya"):
                    st.success("Terima kasih atas feedback Anda!")
            
            with feedback_cols[1]:
                if st.button("Tidak"):
                    st.info("Kami akan terus meningkatkan kualitas analisis")
            
            with feedback_cols[2]:
                if st.button("Saran"):
                    suggestion = st.text_input("Saran perbaikan:")
                    if suggestion:
                        st.success("Saran Anda telah dicatat!")
    
    elif analyze_button and not user_query:
        st.warning("Silakan masukkan pertanyaan terlebih dahulu.")
