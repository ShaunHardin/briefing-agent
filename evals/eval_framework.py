import json
from datetime import datetime
from typing import List, Dict


class EvalMetrics:
    """Basic evaluation framework for digest quality"""
    
    @staticmethod
    def relevance_score(synthesis: Dict, newsletters: List[Dict]) -> float:
        """
        Evaluate relevance of synthesis to source newsletters
        Simple heuristic: check if key terms from newsletters appear in insights
        """
        if not synthesis.get('key_insights'):
            return 0.0
        
        # Extract key terms from newsletters
        newsletter_terms = set()
        for nl in newsletters:
            words = nl['body'].lower().split()
            newsletter_terms.update([w for w in words if len(w) > 5][:20])
        
        # Check insights for newsletter terms
        insights_text = ' '.join(synthesis.get('key_insights', [])).lower()
        
        matched_terms = sum(1 for term in newsletter_terms if term in insights_text)
        relevance = matched_terms / max(len(newsletter_terms), 1)
        
        return min(relevance, 1.0)
    
    @staticmethod
    def completeness_score(synthesis: Dict) -> float:
        """
        Evaluate completeness of synthesis output
        """
        required_fields = ['summary', 'key_insights', 'trends', 'action_items']
        present_fields = sum(1 for field in required_fields if synthesis.get(field))
        
        # Also check if fields have content
        non_empty_fields = sum(1 for field in required_fields if synthesis.get(field))
        
        return non_empty_fields / len(required_fields)
    
    @staticmethod
    def actionability_score(synthesis: Dict) -> float:
        """
        Evaluate if synthesis provides actionable insights
        """
        action_items = synthesis.get('action_items', [])
        key_insights = synthesis.get('key_insights', [])
        
        # Check for action-oriented language
        action_words = ['try', 'explore', 'consider', 'build', 'create', 'learn', 'practice', 'implement']
        
        action_count = 0
        all_text = ' '.join(action_items + key_insights).lower()
        
        for word in action_words:
            if word in all_text:
                action_count += 1
        
        return min(action_count / len(action_words), 1.0)
    
    @staticmethod
    def evaluate_synthesis(synthesis: Dict, newsletters: List[Dict], feedback: Dict = None) -> Dict:
        """
        Run full evaluation on synthesis
        """
        metrics = {
            'relevance': EvalMetrics.relevance_score(synthesis, newsletters),
            'completeness': EvalMetrics.completeness_score(synthesis),
            'actionability': EvalMetrics.actionability_score(synthesis),
            'timestamp': datetime.now().isoformat()
        }
        
        # Calculate overall score
        metrics['overall_score'] = (
            metrics['relevance'] * 0.4 +
            metrics['completeness'] * 0.3 +
            metrics['actionability'] * 0.3
        )
        
        # Add user feedback if available
        if feedback:
            metrics['user_feedback'] = feedback
        
        return metrics
    
    @staticmethod
    def save_eval_results(eval_results: Dict, filepath: str = 'evals/results.json'):
        """Save evaluation results"""
        import os
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        # Load existing results
        if os.path.exists(filepath):
            with open(filepath, 'r') as f:
                results = json.load(f)
        else:
            results = []
        
        results.append(eval_results)
        
        with open(filepath, 'w') as f:
            json.dump(results, f, indent=2)
        
        return filepath
