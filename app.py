import streamlit as st
import json
import os
from datetime import datetime, timedelta
from agent.gmail_client import fetch_newsletters
from agent.synthesizer import synthesize_newsletters, generate_personalized_prompt

st.set_page_config(
    page_title="Newsletter Digest Agent",
    page_icon="📰",
    layout="wide"
)

st.title("📰 Newsletter Digest Agent")
st.markdown("*Your personalized research companion for newsletter insights*")

# Sidebar for configuration
with st.sidebar:
    st.header("⚙️ Settings")
    
    days_back = st.slider("Days to look back", 1, 30, 7)
    max_results = st.slider("Max newsletters", 10, 100, 50)
    
    st.markdown("---")
    
    st.subheader("📧 Gmail Search Query")
    st.markdown("Optional: Customize your newsletter search")
    custom_query = st.text_input(
        "Gmail query",
        placeholder="from:newsletter@example.com",
        help="Use Gmail search syntax. Leave empty for auto-detection."
    )
    
    st.markdown("---")
    
    if st.button("🔄 Fetch & Analyze", type="primary", use_container_width=True):
        with st.spinner("Fetching newsletters from Gmail..."):
            newsletters = fetch_newsletters(
                days_back=days_back,
                max_results=max_results,
                query=custom_query if custom_query else None
            )
            
            if newsletters:
                st.session_state['newsletters'] = newsletters
                st.session_state['last_fetch'] = datetime.now().isoformat()
                
                with st.spinner("Synthesizing insights with AI..."):
                    synthesis = synthesize_newsletters(newsletters)
                    st.session_state['synthesis'] = synthesis
                
                st.success(f"✅ Found {len(newsletters)} newsletters!")
            else:
                st.warning("No newsletters found. Try adjusting your search criteria.")

# Main content area
if 'synthesis' in st.session_state:
    synthesis = st.session_state['synthesis']
    newsletters = st.session_state.get('newsletters', [])
    
    # Summary section
    st.header("📊 Weekly Digest")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Newsletters Analyzed", synthesis.get('newsletter_count', 0))
    with col2:
        st.metric("Key Insights", len(synthesis.get('key_insights', [])))
    with col3:
        st.metric("Trends Identified", len(synthesis.get('trends', [])))
    
    st.markdown("---")
    
    # Summary
    st.subheader("📝 Summary")
    st.write(synthesis.get('summary', 'No summary available'))
    
    # Key Insights
    st.subheader("💡 Key Insights")
    insights = synthesis.get('key_insights', [])
    if insights:
        for i, insight in enumerate(insights, 1):
            with st.expander(f"Insight {i}", expanded=True):
                st.write(insight)
                if st.button(f"Generate Learning Challenge", key=f"insight_{i}"):
                    with st.spinner("Generating personalized prompt..."):
                        prompt = generate_personalized_prompt(insight)
                        st.info(f"🎯 **Learning Challenge:** {prompt}")
    else:
        st.info("No key insights generated")
    
    # Trends
    st.subheader("📈 Emerging Trends")
    trends = synthesis.get('trends', [])
    if trends:
        for trend in trends:
            st.markdown(f"- {trend}")
    else:
        st.info("No trends identified")
    
    # Action Items
    st.subheader("✅ Action Items & Learning Prompts")
    action_items = synthesis.get('action_items', [])
    if action_items:
        for item in action_items:
            st.markdown(f"- {item}")
    else:
        st.info("No action items generated")
    
    st.markdown("---")
    
    # Newsletter list
    with st.expander("📧 View All Newsletters", expanded=False):
        for nl in newsletters:
            st.markdown(f"**{nl['subject']}**")
            st.caption(f"From: {nl['from']} | Date: {nl['date'][:10]}")
            with st.container():
                st.text(nl['body'][:500] + "..." if len(nl['body']) > 500 else nl['body'])
            st.markdown("---")
    
    # Feedback section
    st.subheader("💬 Provide Feedback")
    feedback = st.text_area("How useful was this digest? What would you like to see improved?")
    if st.button("Submit Feedback"):
        # Store feedback (for now, just in session state - could be saved to file/db)
        if 'feedback' not in st.session_state:
            st.session_state['feedback'] = []
        st.session_state['feedback'].append({
            'timestamp': datetime.now().isoformat(),
            'feedback': feedback,
            'synthesis_id': synthesis.get('generated_at')
        })
        st.success("Thank you for your feedback! 🙏")

else:
    # Welcome screen
    st.info("👈 Click 'Fetch & Analyze' in the sidebar to get started!")
    
    st.markdown("""
    ### How it works:
    
    1. **Fetch** - Retrieves newsletters from your Gmail inbox
    2. **Analyze** - AI synthesizes key insights and trends
    3. **Learn** - Get personalized learning prompts and challenges
    4. **Engage** - Track what resonates with you through feedback
    
    ### Features:
    
    - 📧 Automatic newsletter detection from Gmail
    - 🤖 AI-powered insight synthesis
    - 📊 Trend identification across newsletters
    - 🎯 Personalized learning challenges
    - 💾 Memory of your engagement patterns (coming soon)
    """)

# Footer
st.markdown("---")
st.caption(f"Last updated: {st.session_state.get('last_fetch', 'Never')}")
