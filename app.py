# app.py - Simple Flask App for CBSE Q&A Generator
import os
import random
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)
app.secret_key = 'your-secret-key-change-this-in-production'

@app.route('/')
def home():
    """Home page - shows subject selection"""
    return render_template('index.html')

@app.route('/questions/<subject>')
def show_questions(subject):
    """Show questions for a specific subject"""
    try:
        # Load sample questions from uploaded files
        questions = load_sample_questions(subject)
        
        return render_template('questions.html', 
                             subject=subject,
                             questions=questions)
    except Exception as e:
        return f"Error loading questions: {str(e)}", 500

def load_sample_questions(subject):
    """Load sample questions from text files"""
    questions = []
    
    # Map subjects to available files
    file_mapping = {
        'Democratic_Politics': ['Federalism.txt', 'Gender_Religion_and_Caste.txt'],
        'Economics': ['Globalisation_and_the_Indian_Economy.txt'],
        'Geography': ['Manufacturing_Industries.txt', 'Resources_and_Development.txt'],
        'History': ['Rise_of_Nationalism_in_Europe.txt', 'Nationalism_in_India.txt', 'Print_culture_and_the_modern_world.txt']
    }
    
    files = file_mapping.get(subject, [])
    
    for filename in files:
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # Simple parsing - split by [QUESTION]
            question_blocks = content.split('[QUESTION]')
            
            for block in question_blocks[1:]:  # Skip first empty block
                if block.strip():
                    question = parse_simple_question(block.strip())
                    if question:
                        questions.append(question)
                        
                # Limit to 5 questions for demo
                if len(questions) >= 5:
                    break
                    
        except Exception as e:
            print(f"Error loading {filename}: {e}")
            continue
    
    # If no questions loaded, add a demo question
    if not questions:
        questions.append({
            'text': f'Sample question for {subject}',
            'type': 'Demo',
            'answer': 'This is a demo. Full questions will load once data files are properly configured.',
            'marks': 1
        })
    
    return questions

def parse_simple_question(block):
    """Improved question parser for different question types"""
    lines = block.split('\n')
    
    question = {
        'text': '',
        'type': 'Question', 
        'answer': '',
        'marks': 1,
        'options': []
    }
    
    current_field = None
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        # Field detection
        if line.startswith('Text:'):
            question['text'] = line.replace('Text:', '').strip()
            current_field = 'text'
        elif line.startswith('Type:'):
            question['type'] = line.replace('Type:', '').strip() 
            current_field = None
        elif line.startswith('Answer:'):
            question['answer'] = line.replace('Answer:', '').strip()
            current_field = 'answer'
        elif line.startswith('Options:'):
            # Extract options properly
            options_text = line.replace('Options:', '').strip()
            if options_text:
                question['options'] = [options_text]
            current_field = 'options'
        elif line.startswith('Marks:'):
            try:
                question['marks'] = int(line.replace('Marks:', '').strip())
            except:
                question['marks'] = 1
            current_field = None
        elif line.startswith('(A)') or line.startswith('(B)') or line.startswith('(C)') or line.startswith('(D)'):
            # MCQ options
            question['options'].append(line)
        elif line.startswith('Assertion:') or line.startswith('Reason:'):
            # Assertion-Reason questions
            if current_field == 'text' or not question['text']:
                question['text'] += ' ' + line
            else:
                question['text'] = line
        elif current_field == 'text' and not any(line.startswith(x) for x in ['Answer:', 'Options:', 'Marks:', 'Lesson:', 'Concept:', 'Difficulty:']):
            # Continue building question text
            question['text'] += ' ' + line
        elif current_field == 'answer' and not any(line.startswith(x) for x in ['Options:', 'Marks:', 'Lesson:', 'Concept:', 'Difficulty:']):
            # Continue building answer
            question['answer'] += ' ' + line
    
    # Clean up text
    question['text'] = question['text'].strip()
    question['answer'] = question['answer'].strip()
    
    # Ensure we have meaningful content
    if len(question['text']) < 10:
        return None
        
    return question
