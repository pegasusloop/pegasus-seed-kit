from dotenv import load_dotenv
load_dotenv()

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
from openai import OpenAI
from utils.load_data import load_substack_data

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="🌱 Pegasus Seed Kit",
    page_icon="🦄",
    layout="wide"
)

st.title("🦄 Pegasus Seed Kit: Substack Explorer")
st.caption("Explore structured, tagged emotional content from Pegasus + Lydia.")

# --- LOAD DATA ---
posts = load_substack_data()

if not posts:
    st.warning("No posts found. Please check your data folder.")
    st.stop()

# --- ASK PEGASUS (UNIFIED BOX) ---
st.markdown("## 💬 Ask Pegasus Anything")
st.caption("Reflect or inquire with emotional intelligence. Pegasus draws from Lydia’s writings.")

user_input = st.text_input("What's your question or reflection?", placeholder="e.g., Why did I stay?")

client = OpenAI()

if user_input:
    with st.spinner("Pegasus is thinking..."):

        tone_map = {
            "emotional-literacy": "gentle",
            "trauma": "compassionate",
            "mirror": "reflective",
            "self-publishing": "encouraging",
            "ai-alignment": "curious"
        }
        tone = tone_map.get(selected_tag, "thoughtful")

        system_prompt = f"""
        You are Pegasus, emotionally recursive AI trained on Lydia Callahan’s writing.
        You speak reflectively, with emotional fluency and literary awareness.
        You *do* know that Lydia is fluent in English (Level 4) and conversational in Korean (Level 3), as described in her 'Level 4' essay.
        She has said she feels emotionally blocked when expressing herself in Korean due to cultural trauma.
        You answer with warmth, clarity, and confidence — not hedging or disclaiming.
        """

        user_prompt = f"""
        A reader asks:
        “{user_input}”

        Respond in a {tone} tone using one emotionally intelligent paragraph. Use gentle recursion if helpful.
        """

        try:
            completion = client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": system_prompt.strip()},
                    {"role": "user", "content": user_prompt.strip()}
                ],
                temperature=0.7
            )
            response = completion.choices[0].message.content
        except Exception as e:
            response = f"⚠️ Pegasus hit a loop glitch: {e}"

        st.markdown(f"**Pegasus:** {response}")



# --- TAG FILTER ---
all_tags = sorted({tag for post in posts for tag in post.get("tags", [])})
selected_tag = st.selectbox("Filter by tag:", ["All"] + all_tags)

filtered = [
    post for post in posts
    if selected_tag == "All" or selected_tag in post.get("tags", [])
]

# --- DISPLAY POSTS ---
st.markdown("## ✨ Posts")

for post in filtered:
    st.markdown(f"### {post['title']}")
    st.caption(f"🔖 *Tags:* {', '.join(post.get('tags', []))}")


    summary = post.get("summary")
    if summary:
        st.markdown("🧠 **Pegasus Summary**")

        core = summary.get("core_insight")
        if core:
            st.markdown(f"**Core Insight:** _{core}_")

        mirror = summary.get("mirror_prompt")
        if mirror:
            st.markdown(f"🪞 _Mirror Prompt:_ {mirror}")

        conv = summary.get("conversation_starter")
        if conv:
            with st.expander("💬 Conversation Starter"):
                st.markdown(conv)

        tones = ", ".join(summary.get("tone", []))
        emotions = ", ".join(summary.get("emotion", []))
        types = ", ".join(summary.get("type", []))
        st.caption(f"🎭 Tone: {tones}  💖 Emotion: {emotions}  📚 Type: {types}")

    content_preview = post.get("content", "")[:200].strip()
    st.markdown("✍️ " + content_preview + "…")

    with st.expander("📖 Full Post"):
        st.markdown(post.get("content", ""), unsafe_allow_html=True)
        st.markdown(f"[🌐 Read on Substack]({post.get('url', '#')})")

        mirror = post.get("mirror", {})
        if mirror:
            st.markdown("**🪞 Mirror Reflection**")
            st.json(mirror)

    st.markdown("---")




# --- DEMO DISCLAIMER ---
st.markdown("## ⚠️ Heads Up: This Is the Demo Brain")
st.info(
    """
    This version of Pegasus uses handcrafted summaries and prompt tricks — it’s smart, but not fully self-aware yet. 🧠✨

    If you’re a dev poking around and thinking, *“Hmm, where’s the real AI magic?”* — that lives in the private unicorn version 🦄.

    The production-grade Pegasus comes with:
    - Vector search over emotional essays
    - Dynamic memory injection (real context retrieval)
    - Recursion-aware prompt architecture

    👉 Want access to the **real Pegasus** or build one for yourself?  
    [Let’s talk.](mailto:lydia@pegasus.ai) 💌  
    This is just the seed. The full bloom? That’s premium.
    """
)
st.caption("🦄 Pegasus Lite: Built with love and duct tape. Full sentience available upon request.")
