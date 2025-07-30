# manifest_loader.py - ENHANCED VERSION with Cross-Manifest Support
import json
import os
import re
from typing import Dict, List, Optional, Any

class ManifestLoader:
    """Enhanced manifest loader with cross-manifest name standardization"""
    
    def __init__(self):
        self.master_manifest = {}
        self.individual_manifests = {}
        self.base_data_path = "data/Processed_QA"
        self.manifests_path = "manifests"
        
        # Load all manifests on initialization
        self.load_master_manifest()
        self.load_all_individual_manifests()
    
    def load_master_manifest(self):
        """Load the master manifest file"""
        master_path = os.path.join(self.manifests_path, "master_manifest.json")
        
        try:
            if os.path.exists(master_path):
                with open(master_path, 'r', encoding='utf-8') as f:
                    self.master_manifest = json.load(f)
                print(f"✅ Loaded master manifest ({len(self.master_manifest.get('question_types', {}))} question types)")
            else:
                print(f"❌ Master manifest not found at: {master_path}")
                self.master_manifest = {}
        except Exception as e:
            print(f"❌ Error loading master manifest: {e}")
            self.master_manifest = {}
    
    def load_all_individual_manifests(self):
        """Load all individual question type manifests"""
        if not self.master_manifest:
            print("❌ Cannot load individual manifests - master manifest not available")
            return
        
        question_types = self.master_manifest.get('question_types', {})
        
        for q_type, config in question_types.items():
            if not config.get('enabled', True):
                continue
                
            manifest_file = config.get('manifest_file')
            if manifest_file:
                self.load_individual_manifest(q_type, manifest_file)
    
    def load_individual_manifest(self, q_type: str, manifest_file: str):
        """Load an individual question type manifest"""
        manifest_path = os.path.join(self.manifests_path, manifest_file)
        
        try:
            if os.path.exists(manifest_path):
                with open(manifest_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.individual_manifests[q_type] = data
                    print(f"✅ Loaded {q_type} manifest ({len(data)} entries)")
            else:
                print(f"⚠️ {q_type} manifest not found: {manifest_path}")
                self.individual_manifests[q_type] = {}
        except Exception as e:
            print(f"❌ Error loading {q_type} manifest: {e}")
            self.individual_manifests[q_type] = {}

    # NAME NORMALIZATION SYSTEM
    # =========================
    
    def normalize_name(self, name: str) -> str:
        """Normalize subject/lesson names for consistent matching"""
        if not name:
            return ""
        
        # Convert to lowercase and replace variations
        normalized = name.lower()
        
        # Handle common variations
        normalized = normalized.replace(' ', '_')
        normalized = normalized.replace('-', '_')
        normalized = normalized.replace('__', '_')
        
        # Handle common word variations
        replacements = {
            '_and_': '_',
            '_of_': '_',
            '_the_': '_',
            '_in_': '_',
            'democratic_politics': 'democratic_politics',
            'nationalism_in_india': 'nationalism_in_india',
            'rise_of_nationalism_in_europe': 'rise_of_nationalism_in_europe',
            'print_culture_and_the_modern_world': 'print_culture_and_the_modern_world',
            'the_making_of_a_global_world': 'the_making_of_a_global_world',
            'globalisation_and_the_indian_economy': 'globalisation_and_the_indian_economy',
            'sectors_of_the_indian_economy': 'sectors_of_the_indian_economy',
            'forest_and_wildlife_resources': 'forest_and_wildlife_resources',
            'land_water_soil_and_natural_vegetation_resources': 'land_water_soil_and_natural_vegetation_resources',
            'mineral_and_energy_resources': 'mineral_and_energy_resources'
        }
        
        for old, new in replacements.items():
            normalized = normalized.replace(old, new)
        
        return normalized.strip('_')
    
    def names_match(self, name1: str, name2: str) -> bool:
        """Check if two names match after normalization"""
        return self.normalize_name(name1) == self.normalize_name(name2)
    
    def find_matching_entry(self, manifest_data: Dict, target_subject: str, target_lesson: str) -> Optional[Dict]:
        """Find matching entry in manifest data using fuzzy name matching"""
        target_subject_norm = self.normalize_name(target_subject)
        target_lesson_norm = self.normalize_name(target_lesson)
        
        for entry_key, entry in manifest_data.items():
            manifest_subject = entry.get('subject', '')
            manifest_lesson = entry.get('lesson', '')
            
            if (self.names_match(manifest_subject, target_subject) and 
                self.names_match(manifest_lesson, target_lesson)):
                return entry
        
        return None

    # ENHANCED CORE FUNCTIONS
    # =======================
    
    def get_enabled_question_types(self) -> List[str]:
        """Get list of enabled question types"""
        question_types = self.master_manifest.get('question_types', {})
        return [q_type for q_type, config in question_types.items() 
                if config.get('enabled', True)]
    
    def get_question_type_config(self, q_type: str) -> Dict:
        """Get configuration for a specific question type"""
        return self.master_manifest.get('question_types', {}).get(q_type, {})
    
    def get_available_subjects(self, q_type: str = None) -> List[str]:
        """Get available subjects for a question type or all subjects"""
        if q_type and q_type in self.individual_manifests:
            subjects = set()
            for entry in self.individual_manifests[q_type].values():
                if entry.get('subject'):
                    subjects.add(entry['subject'])
            return sorted(list(subjects))
        else:
            return self.master_manifest.get('subjects', [])
    
    def get_available_lessons(self, q_type: str, subject: str) -> List[str]:
        """Get available lessons for a question type and subject with name matching"""
        if q_type not in self.individual_manifests:
            return []
        
        lessons = set()
        for entry in self.individual_manifests[q_type].values():
            if self.names_match(entry.get('subject', ''), subject) and entry.get('lesson'):
                lessons.add(entry['lesson'])
        
        return sorted(list(lessons))
    
    def get_subjects_lessons_dict(self, q_type: str) -> Dict[str, List[str]]:
        """Get dictionary of subjects with their lessons for a question type"""
        if q_type not in self.individual_manifests:
            return {}
        
        subjects_lessons = {}
        
        for entry in self.individual_manifests[q_type].values():
            subject = entry.get('subject')
            lesson = entry.get('lesson')
            
            if subject and lesson:
                if subject not in subjects_lessons:
                    subjects_lessons[subject] = []
                if lesson not in subjects_lessons[subject]:
                    subjects_lessons[subject].append(lesson)
        
        # Sort lessons for each subject
        for subject in subjects_lessons:
            subjects_lessons[subject].sort()
        
        return subjects_lessons
    
    def get_file_path(self, q_type: str, subject: str, lesson: str) -> Optional[str]:
        """Get file path with enhanced name matching"""
        if q_type not in self.individual_manifests:
            print(f"❌ No {q_type} manifest loaded")
            return None
        
        # Find matching entry using fuzzy matching
        matching_entry = self.find_matching_entry(
            self.individual_manifests[q_type], 
            subject, 
            lesson
        )
        
        if matching_entry:
            file_path = matching_entry.get('file_path')
            
            # Fix path if needed
            if file_path and file_path.startswith('data_qp/'):
                file_path = file_path.replace('data_qp/', 'data/')
            
            return file_path
        
        print(f"❌ No manifest entry found for {q_type}: {subject} - {lesson}")
        return None
    
    def load_questions_from_manifest(self, q_type: str, subject: str, lesson: str) -> List[Dict]:
        """Load questions from manifest for specific type, subject, and lesson"""
        file_path = self.get_file_path(q_type, subject, lesson)
        
        if not file_path:
            return []
        
        if not os.path.exists(file_path):
            print(f"❌ File not found: {file_path}")
            return []
        
        try:
            if q_type in ['visual', 'map']:
                return self.parse_visual_map_questions(file_path, q_type)
            else:
                return self.parse_standard_questions(file_path, q_type)
        except Exception as e:
            print(f"❌ Error loading questions from {file_path}: {e}")
            return []

    # QUESTION PARSING FUNCTIONS
    # ==========================
    
    def parse_standard_questions(self, file_path: str, q_type: str) -> List[Dict]:
        """Parse standard question files (MCQ, Assertion, Matching, etc.)"""
        questions = []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
            
            # Split by [QUESTION] markers
            question_blocks = content.split('[QUESTION]')
            
            for block in question_blocks[1:]:  # Skip first empty block
                if not block.strip():
                    continue
                
                question = self.parse_question_block(block.strip(), q_type)
                if question:
                    questions.append(question)
                    
        except Exception as e:
            print(f"Error parsing file {file_path}: {e}")
        
        return questions
    
    def parse_question_block(self, block: str, q_type: str) -> Optional[Dict]:
        """Parse individual question block"""
        lines = block.split('\n')
        
        question = {
            'Type': q_type,
            'Text': '',
            'Answer': '',
            'Options': [],
            'Marks': 1,
            'Difficulty': 'Medium',
            'Concept': '',
            'SourceText': '',
            'Events': [],
            'ColumnA': [],
            'ColumnB': []
        }
        
        current_field = None
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Field detection
            if line.startswith('Type:'):
                question['Type'] = line.replace('Type:', '').strip()
            elif line.startswith('Text:'):
                current_field = 'Text'
                question['Text'] = line.replace('Text:', '').strip()
            elif line.startswith('Answer:'):
                current_field = 'Answer'
                question['Answer'] = line.replace('Answer:', '').strip()
            elif line.startswith('Options:'):
                current_field = 'Options'
                options_text = line.replace('Options:', '').strip()
                if options_text:
                    question['Options'] = self.parse_options(options_text)
            elif line.startswith('Marks:'):
                question['Marks'] = int(line.replace('Marks:', '').strip() or '1')
            elif line.startswith('Concept:'):
                question['Concept'] = line.replace('Concept:', '').strip()
            elif line.startswith('Difficulty:'):
                question['Difficulty'] = line.replace('Difficulty:', '').strip()
            elif line.startswith('SourceText:'):
                current_field = 'SourceText'
                question['SourceText'] = line.replace('SourceText:', '').strip()
            elif line.startswith('Events:'):
                current_field = 'Events'
                events_text = line.replace('Events:', '').strip()
                if events_text:
                    question['Events'] = events_text.split('\n')
            elif current_field and line:
                # Continue current field
                if current_field == 'Options':
                    if line.startswith('('):
                        question['Options'].append(line)
                else:
                    question[current_field] += ' ' + line
        
        return question if question.get('Text') else None
    
    def parse_options(self, options_text: str) -> List[str]:
        """Parse options into a list"""
        if not options_text:
            return []
        
        # Split by (A), (B), etc.
        options = []
        parts = re.split(r'(?=\([A-D]\))', options_text)
        
        for part in parts:
            part = part.strip()
            if part and part.startswith('('):
                options.append(part)
        
        return options
    
    def parse_visual_map_questions(self, file_path: str, q_type: str) -> List[Dict]:
        """Parse visual/map questions with image references"""
        questions = self.parse_standard_questions(file_path, q_type)
        
        # Add image folder path for visual questions
        if q_type == 'visual':
            image_folder = os.path.dirname(file_path)
            for question in questions:
                question['ImageFolder'] = image_folder
        
        return questions

    # MULTI-MANIFEST FUNCTIONS FOR CROSS-TAB FEATURES
    # ===============================================
    
    def get_unified_subjects(self) -> List[str]:
        """Get unified list of subjects across all manifests"""
        all_subjects = set()
        
        for q_type in self.get_enabled_question_types():
            subjects = self.get_available_subjects(q_type)
            all_subjects.update(subjects)
        
        return sorted(list(all_subjects))
    
    def get_unified_lessons(self, subject: str) -> List[str]:
        """Get unified list of lessons for a subject across all manifests"""
        all_lessons = set()
        
        for q_type in self.get_enabled_question_types():
            lessons = self.get_available_lessons(q_type, subject)
            all_lessons.update(lessons)
        
        return sorted(list(all_lessons))
    
    def get_available_question_types_for_lesson(self, subject: str, lesson: str) -> List[str]:
        """Get available question types for a specific subject and lesson"""
        available_types = []
        
        for q_type in self.get_enabled_question_types():
            if self.get_file_path(q_type, subject, lesson):
                available_types.append(q_type)
        
        return available_types

    # WORKSHEET BUILDER FUNCTIONS
    # ===========================
    
    def get_worksheet_templates(self) -> Dict:
        """Get available worksheet templates"""
        return self.master_manifest.get('worksheet_templates', {})
    
    def get_worksheet_template(self, template_name: str) -> Dict:
        """Get specific worksheet template"""
        templates = self.get_worksheet_templates()
        return templates.get(template_name, {})


# Global instance for easy import
manifest_loader = ManifestLoader()

# Convenience functions for backward compatibility
def get_subjects_lessons_dict(q_type: str) -> Dict[str, List[str]]:
    """Get subjects and lessons for a question type"""
    return manifest_loader.get_subjects_lessons_dict(q_type)

def get_available_lessons(q_type: str, subject: str) -> List[str]:
    """Get available lessons for a question type and subject"""
    return manifest_loader.get_available_lessons(q_type, subject)

def load_questions_from_manifest(q_type: str, subject: str, lesson: str) -> List[Dict]:
    """Load questions from manifest"""
    return manifest_loader.load_questions_from_manifest(q_type, subject, lesson)

def get_enabled_question_types() -> List[str]:
    """Get enabled question types"""
    return manifest_loader.get_enabled_question_types()

def get_question_type_config(q_type: str) -> Dict:
    """Get question type configuration"""
    return manifest_loader.get_question_type_config(q_type)