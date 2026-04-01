import google.generativeai as genai
import os
import json

class GeminiService:
    def __init__(self, api_key=None):
        self.api_key = api_key or os.getenv('GEMINI_API_KEY')
        if self.api_key:
            genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel('gemini-pro')
    
    def get_furniture_recommendations(self, room_type, budget, style):
        """Get AI-powered furniture recommendations"""
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
            # Parse JSON from response
            response_text = response.text
            # Try to extract JSON
            if response_text.startswith('['):
                recommendations = json.loads(response_text)
            else:
                # Extract JSON from text if wrapped in markdown code blocks
                import re
                json_match = re.search(r'\[.*\]', response_text, re.DOTALL)
                if json_match:
                    recommendations = json.loads(json_match.group())
                else:
                    recommendations = []
            return recommendations
        except Exception as e:
            print(f"Error getting recommendations: {e}")
            return []
    
    def get_color_palette_suggestions(self, style, mood):
        """Get AI-powered color palette suggestions"""
        prompt = f"""
        Suggest a color palette for a {style} style room with a {mood} mood.
        
        Provide 4 colors (primary, secondary, accent, neutral) as HEX codes.
        Format as JSON with keys: primary, secondary, accent, neutral
        Include a brief description of why these colors work together.
        
        Format response as JSON object.
        """
        try:
            response = self.model.generate_content(prompt)
            response_text = response.text
            if response_text.startswith('{'):
                palette = json.loads(response_text)
            else:
                import re
                json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
                if json_match:
                    palette = json.loads(json_match.group())
                else:
                    palette = {}
            return palette
        except Exception as e:
            print(f"Error getting color palette: {e}")
            return {}
    
    def get_layout_suggestions(self, room_type, room_width, room_length, budget):
        """Get AI-powered layout suggestions"""
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
            response_text = response.text
            # Extended JSON extraction logic
            suggestions = {
                'arrangement': response_text.split('\n')[0],
                'pieces': response_text,
                'tips': response_text
            }
            return suggestions
        except Exception as e:
            print(f"Error getting layout suggestions: {e}")
            return {}
    
    def estimate_room_from_image(self, image_data):
        """Estimate room dimensions and layout from image"""
        prompt = f"""
        Based on this room image, estimate:
        1. Room type (bedroom, kitchen, hall, office)
        2. Approximate dimensions
        3. Existing furniture
        4. Suggested improvements
        
        Format as JSON.
        """
        try:
            response = self.model.generate_content([prompt, image_data])
            return json.loads(response.text)
        except Exception as e:
            print(f"Error estimating room: {e}")
            return {}
