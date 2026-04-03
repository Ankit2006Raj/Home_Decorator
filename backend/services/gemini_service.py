import google.generativeai as genai
import os
import json
import logging
import re

logger = logging.getLogger(__name__)

class GeminiService:
    """Service for AI-powered recommendations using Google Gemini API"""
    
    def __init__(self, api_key=None):
        self.api_key = api_key or os.getenv('GEMINI_API_KEY')
        self.model = None
        
        if not self.api_key:
            logger.warning("GEMINI_API_KEY not found in environment variables")
            return
        
        try:
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel('gemini-pro')
            logger.info("Gemini service initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize Gemini service: {str(e)}")
    
    def _extract_json(self, text, json_type='array'):
        """Extract JSON from text response"""
        try:
            # Try direct JSON parse
            if text.strip().startswith('[' if json_type == 'array' else '{'):
                return json.loads(text)
            
            # Try to extract from code blocks
            pattern = r'```(?:json)?\n(.*?)\n```' if json_type == 'array' else r'```(?:json)?\n(.*?)\n```'
            match = re.search(pattern, text, re.DOTALL)
            if match:
                return json.loads(match.group(1))
            
            # Try to find JSON in text
            pattern = r'\[.*\]' if json_type == 'array' else r'\{.*\}'
            match = re.search(pattern, text, re.DOTALL)
            if match:
                return json.loads(match.group())
            
            logger.warning(f"Could not extract {json_type} from response")
            return [] if json_type == 'array' else {}
        except json.JSONDecodeError as e:
            logger.error(f"JSON decode error: {str(e)}")
            return [] if json_type == 'array' else {}
    
    def get_furniture_recommendations(self, room_type, budget, style):
        """Get AI-powered furniture recommendations"""
        if not self.model:
            logger.error("Gemini model not initialized")
            return []
        
        prompt = f"""
        Based on the following criteria, suggest 5 furniture items for a {room_type}:
        - Budget: ${budget}
        - Style: {style}
        
        For each item, provide:
        1. Furniture name
        2. Category (bed, sofa, chair, table, etc.)
        3. Estimated price
        4. Material
        5. Why it's suitable
        
        Format response as JSON array with objects containing these fields.
        """
        try:
            response = self.model.generate_content(prompt)
            recommendations = self._extract_json(response.text, 'array')
            logger.info(f"Generated {len(recommendations)} furniture recommendations")
            return recommendations
        except Exception as e:
            logger.error(f"Error getting recommendations: {str(e)}", exc_info=True)
            return []
    
    def get_color_palette_suggestions(self, style, mood):
        """Get AI-powered color palette suggestions"""
        if not self.model:
            logger.error("Gemini model not initialized")
            return {}
        
        prompt = f"""
        Suggest a color palette for a {style} style room with a {mood} mood.
        
        Provide 4 colors (primary, secondary, accent, neutral) as HEX codes.
        Format as JSON with keys: primary, secondary, accent, neutral
        Include a brief description of why these colors work together.
        
        Format response as JSON object.
        """
        try:
            response = self.model.generate_content(prompt)
            palette = self._extract_json(response.text, 'object')
            logger.info("Generated color palette suggestions")
            return palette
        except Exception as e:
            logger.error(f"Error getting color palette: {str(e)}", exc_info=True)
            return {}
    
    def get_layout_suggestions(self, room_type, room_width, room_length, budget):
        """Get AI-powered layout suggestions"""
        if not self.model:
            logger.error("Gemini model not initialized")
            return {}
        
        prompt = f"""
        Suggest an optimal furniture layout for a {room_type} with dimensions {room_width}ft x {room_length}ft and budget ${budget}.
        
        Provide:
        1. Optimal furniture arrangement
        2. Key furniture pieces to include
        3. Space-saving tips
        4. Cost breakdown
        
        Format as JSON with structured suggestions.
        """
        try:
            response = self.model.generate_content(prompt)
            suggestions = self._extract_json(response.text, 'object')
            logger.info("Generated layout suggestions")
            return suggestions
        except Exception as e:
            logger.error(f"Error getting layout suggestions: {str(e)}", exc_info=True)
            return {}

