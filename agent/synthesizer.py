import os
from openai import OpenAI
from datetime import datetime
import json


def get_openai_client():
    """Create OpenAI client using Replit AI Integrations"""
    base_url = os.environ.get('AI_INTEGRATIONS_OPENAI_BASE_URL')
    api_key = os.environ.get('AI_INTEGRATIONS_OPENAI_API_KEY')
    
    if not base_url or not api_key:
        raise Exception('OpenAI integration not configured')
    
    return OpenAI(base_url=base_url, api_key=api_key)


def synthesize_newsletters(newsletters, user_preferences=None):
    """
    Synthesize insights from newsletters using AI
    
    Args:
        newsletters: List of newsletter dictionaries
        user_preferences: Optional dict of user preferences/interests
    
    Returns:
        Dict with synthesis results
    """
    if not newsletters:
        return {
            'summary': 'No newsletters found.',
            'key_insights': [],
            'trends': [],
            'action_items': []
        }
    
    client = get_openai_client()
    
    # Prepare newsletter content for analysis
    newsletter_texts = []
    for i, nl in enumerate(newsletters[:10]):  # Limit to 10 for token management
        newsletter_texts.append(
            f"Newsletter {i+1}:\n"
            f"From: {nl['from']}\n"
            f"Subject: {nl['subject']}\n"
            f"Date: {nl['date']}\n"
            f"Content: {nl['body'][:1000]}...\n"  # First 1000 chars
        )
    
    newsletters_combined = "\n\n---\n\n".join(newsletter_texts)
    
    # Build prompt
    prompt = f"""You are a personalized research assistant analyzing newsletters for learning and insights.

Analyze the following newsletters and provide:

1. A concise summary of the main themes
2. Key insights and takeaways (3-5 items)
3. Emerging trends or patterns
4. Actionable learning prompts or challenges for the reader

Newsletters:
{newsletters_combined}

"""
    
    if user_preferences:
        prompt += f"\nUser interests/preferences: {json.dumps(user_preferences)}\n"
    
    prompt += """
Please provide your analysis in the following JSON format:
{
  "summary": "Overall summary in 2-3 sentences",
  "key_insights": ["insight 1", "insight 2", "insight 3"],
  "trends": ["trend 1", "trend 2"],
  "action_items": ["learning prompt 1", "learning prompt 2"]
}
"""
    
    # Call OpenAI
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful research assistant that synthesizes information and generates insights."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
        max_tokens=1000
    )
    
    # Parse response
    try:
        content = response.choices[0].message.content or "{}"
        result = json.loads(content)
    except json.JSONDecodeError:
        # Fallback if not valid JSON
        result = {
            'summary': response.choices[0].message.content,
            'key_insights': [],
            'trends': [],
            'action_items': []
        }
    
    result['generated_at'] = datetime.now().isoformat()
    result['newsletter_count'] = len(newsletters)
    
    return result


def generate_personalized_prompt(topic, user_context=None):
    """
    Generate a personalized learning prompt based on a topic
    
    Args:
        topic: The topic/insight to explore
        user_context: Optional context about user's learning journey
    
    Returns:
        Personalized learning challenge/prompt
    """
    client = get_openai_client()
    
    prompt = f"""Generate a personalized learning challenge or exploration prompt for this topic:

Topic: {topic}

"""
    
    if user_context:
        prompt += f"User context: {user_context}\n\n"
    
    prompt += """Create an engaging, actionable learning prompt that:
- Builds on this topic
- Suggests a practical exercise or exploration
- Is achievable in 30-60 minutes
- Helps deepen understanding

Keep it concise (2-3 sentences)."""
    
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a learning coach creating personalized challenges."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.8,
        max_tokens=200
    )
    
    content = response.choices[0].message.content
    return content.strip() if content else ""
