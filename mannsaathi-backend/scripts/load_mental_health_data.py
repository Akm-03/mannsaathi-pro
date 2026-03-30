"""
Load Mental Health Data - Simplified Version
This script creates mental health resources without importing the main app
"""

import os
import sys
import json
import csv
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any

class SimpleMentalHealthDataLoader:
    """Simplified data loader that doesn't require app imports"""
    
    def __init__(self):
        self.data_dir = Path(__file__).parent / "data"
        self.data_dir.mkdir(exist_ok=True)
        self.resources_file = self.data_dir / "mental_health_resources.json"
        print("✅ Data loader initialized")
    
    def load_all_sources(self):
        """Load all mental health resources"""
        print("\n" + "="*60)
        print("📚 LOADING MENTAL HEALTH DATA")
        print("="*60)
        
        all_resources = []
        
        # Load from different categories
        all_resources.extend(self.get_indian_resources())
        all_resources.extend(self.get_international_resources())
        all_resources.extend(self.get_crisis_resources())
        all_resources.extend(self.get_cultural_resources())
        all_resources.extend(self.get_age_specific_resources())
        all_resources.extend(self.get_therapy_techniques())
        
        # Save all resources to JSON file
        self.save_resources(all_resources)
        
        print("\n" + "="*60)
        print(f"✅ Loaded {len(all_resources)} mental health resources")
        print(f"📁 Saved to: {self.resources_file}")
        print("="*60)
        
        return all_resources
    
    def get_indian_resources(self) -> List[Dict]:
        """India-specific mental health resources"""
        return [
            {
                'source': 'NIMHANS_Guidelines',
                'category': 'indian_context',
                'language': 'english',
                'tags': ['india', 'clinical', 'guidelines'],
                'content': """
                NIMHANS Guidelines for Mental Health in India:
                
                Common Mental Health Issues in India:
                1. Depression - affects 45 million Indians
                2. Anxiety disorders - affects 40 million Indians
                3. Stress-related disorders - increasing in urban areas
                4. Substance abuse - particularly alcohol in rural areas
                
                Culturally Appropriate Interventions:
                - Use family-based therapy approaches
                - Incorporate traditional healing practices
                - Address stigma through community education
                - Utilize peer support groups
                - Leverage community health workers (ASHA workers)
                """
            },
            {
                'source': 'Indian_Family_Dynamics',
                'category': 'cultural',
                'language': 'hinglish',
                'tags': ['family', 'india', 'relationships'],
                'content': """
                Indian Family Dynamics and Mental Health:
                
                Common Family-Related Stressors:
                1. Marriage pressure (age, arranged marriages, inter-caste)
                2. Career expectations (doctor/engineer syndrome)
                3. Financial responsibilities toward family
                4. Caring for elderly parents
                5. Parenting pressures (academic performance)
                
                Supportive Approaches:
                - "Family counseling can help everyone understand each other better"
                - "Setting boundaries while maintaining respect is possible"
                - "It's okay to seek help - mental health is family health"
                - "Open communication can reduce misunderstandings"
                """
            },
            {
                'source': 'Urban_Stress_India',
                'category': 'stress',
                'language': 'hinglish',
                'tags': ['urban', 'work', 'stress'],
                'content': """
                Urban Stress in Indian Cities:
                
                Common Urban Stressors:
                1. Traffic and commute stress (2-3 hours daily in metros)
                2. Work pressure and job insecurity
                3. High cost of living and housing stress
                4. Social isolation despite crowded cities
                5. Technology overload and screen time
                
                Coping Strategies for Urban Indians:
                - Micro-breaks: 5 minutes every hour away from screens
                - Morning walk or yoga before traffic rush
                - Connect with community groups (apartment associations, clubs)
                - Digital detox on weekends
                - Find green spaces even in cities (parks, terrace gardens)
                """
            }
        ]
    
    def get_international_resources(self) -> List[Dict]:
        """International mental health resources"""
        return [
            {
                'source': 'WHO_Mental_Health',
                'category': 'global_guidelines',
                'language': 'english',
                'tags': ['who', 'global', 'guidelines'],
                'content': """
                WHO Mental Health Guidelines:
                
                Key Principles:
                1. Mental health is a universal human right
                2. No health without mental health
                3. Community-based care is more effective than institutionalization
                4. Early intervention prevents chronic conditions
                
                Evidence-Based Interventions:
                - Psychological interventions: CBT, IPT, problem-solving therapy
                - Pharmacological interventions when appropriate
                - Psychosocial support: peer support, family interventions
                - mHealth: using technology to deliver mental health services
                """
            },
            {
                'source': 'Positive_Psychology',
                'category': 'wellbeing',
                'language': 'english',
                'tags': ['happiness', 'wellbeing', 'strengths'],
                'content': """
                Positive Psychology Interventions:
                
                Evidence-Based Practices:
                1. Gratitude Journaling: Write 3 things you're grateful for daily
                2. Signature Strengths: Identify and use your top 5 strengths
                3. Acts of Kindness: Do 5 kind things weekly
                4. Savoring: Mindfully enjoy positive experiences
                5. Best Possible Self: Visualize your ideal future
                
                Simple Practice:
                "Before sleeping, think of one good thing that happened today"
                "Write a gratitude letter to someone who helped you"
                """
            }
        ]
    
    def get_crisis_resources(self) -> List[Dict]:
        """Crisis intervention resources"""
        return [
            {
                'source': 'Crisis_Protocol',
                'category': 'crisis',
                'language': 'english',
                'tags': ['crisis', 'suicide', 'emergency'],
                'content': """
                Crisis Intervention Protocol:
                
                Step 1: Assess Risk
                - Ask directly: "Are you thinking about suicide?"
                - Determine if they have a plan, means, timeline
                - Ask about previous attempts
                
                Step 2: Ensure Safety
                - Remove means (medications, weapons)
                - Don't leave person alone
                - Contact emergency services if imminent risk
                
                Step 3: Provide Support
                - Listen without judgment
                - Validate their pain: "I can hear how much pain you're in"
                - Express hope: "This feeling won't last forever"
                - Connect to professional help
                
                Indian Crisis Helplines:
                - iCall: 9152987821 (24/7)
                - Vandrevala Foundation: 9999666555 (24/7)
                - AASRA: 9820466726 (24/7)
                - Sneha: 044-24640050 (Chennai)
                
                What to Say:
                "You are not alone"
                "Your feelings are valid"
                "There is help available"
                """
            }
        ]
    
    def get_cultural_resources(self) -> List[Dict]:
        """Culturally-adapted approaches"""
        return [
            {
                'source': 'Hinglish_Communication',
                'category': 'communication',
                'language': 'hinglish',
                'tags': ['hinglish', 'communication', 'india'],
                'content': """
                Effective Hinglish Communication for Mental Health:
                
                Key Phrases:
                - "Aap akela nahi hain" (You're not alone)
                - "Main samajh sakta/sakti hoon" (I understand)
                - "Yeh bahut common hai" (This is very common)
                - "Aap strong hain" (You are strong)
                - "Step by step, sab theek ho jayega" (Step by step, everything will be okay)
                
                Normalizing Language:
                "Mental health issues kisi ko bhi ho sakte hain"
                "Stress hona normal hai, lekin agar bahut zyada ho toh help lena important hai"
                """
            },
            {
                'source': 'Yoga_Mindfulness',
                'category': 'traditional_practices',
                'language': 'english',
                'tags': ['yoga', 'mindfulness', 'meditation'],
                'content': """
                Yoga and Mindfulness for Mental Health:
                
                Simple Practices:
                
                1. Pranayama (Breathing):
                   - Anulom Vilom: Alternate nostril breathing (5 minutes)
                   - Bhramari: Humming bee breath for anxiety
                   - Deep breathing: Inhale 4, hold 4, exhale 6
                
                2. Mindfulness Meditation:
                   - Body scan: 5-10 minutes
                   - Mindful eating: Eat one meal without distractions
                   - Walking meditation: Focus on each step
                
                3. Yoga Asanas:
                   - Child's pose (Balasana): For anxiety
                   - Legs up wall (Viparita Karani): For stress
                   - Cat-cow stretch: For releasing tension
                """
            }
        ]
    
    def get_age_specific_resources(self) -> List[Dict]:
        """Age-specific mental health resources"""
        return [
            {
                'source': 'Student_Resources',
                'category': 'students',
                'language': 'hinglish',
                'tags': ['students', 'exams', 'education'],
                'content': """
                Student Mental Health Support:
                
                Common Issues:
                - Exam anxiety and performance pressure
                - Career choice stress
                - Peer pressure and social media
                - Relationship issues
                - Family expectations
                
                Coping Strategies:
                1. Study Smart: 45-minute study blocks with 15-min breaks
                2. Sleep: Minimum 7-8 hours (critical for memory)
                3. Exercise: 30 minutes daily (reduces anxiety)
                4. Connect: Talk to friends and family
                
                When to Seek Help:
                - Constant worry affecting studies
                - Loss of interest in activities
                - Sleep or appetite changes
                - Thoughts of self-harm
                """
            },
            {
                'source': 'Elderly_Care',
                'category': 'elderly',
                'language': 'hinglish',
                'tags': ['elderly', 'aging', 'seniors'],
                'content': """
                Mental Health Support for Elderly:
                
                Common Challenges:
                - Loneliness and isolation
                - Health issues and mobility limitations
                - Loss of spouse or friends
                - Feeling of being a burden
                - Financial dependence
                
                Support Strategies:
                1. Regular Social Connection:
                   - Daily phone calls with family
                   - Senior citizen groups
                   - Community center activities
                
                2. Maintain Purpose:
                   - Share wisdom with younger generation
                   - Hobbies and interests
                   - Volunteer if possible
                
                Warning Signs:
                - Withdrawal from activities
                - Neglecting personal care
                - Memory concerns
                - Expressing hopelessness
                """
            }
        ]
    
    def get_therapy_techniques(self) -> List[Dict]:
        """Evidence-based therapy techniques"""
        return [
            {
                'source': 'CBT_Techniques',
                'category': 'therapy',
                'language': 'english',
                'tags': ['cbt', 'thoughts', 'patterns'],
                'content': """
                Cognitive Behavioral Therapy (CBT) Techniques:
                
                Technique 1: Thought Challenging
                - Identify negative thought
                - Evidence for the thought?
                - Evidence against the thought?
                - Balanced alternative thought
                
                Example:
                Thought: "I always fail at everything"
                Evidence for: "Failed one exam"
                Evidence against: "Passed other subjects, good at sports"
                Balanced: "Sometimes I face challenges, but I also have successes"
                
                Technique 2: Behavioral Activation
                - Schedule enjoyable activities
                - Start with small, achievable tasks
                - Notice mood before and after
                - Gradually increase activities
                """
            },
            {
                'source': 'DBT_Skills',
                'category': 'skills',
                'language': 'english',
                'tags': ['dbt', 'emotions', 'regulation'],
                'content': """
                Dialectical Behavior Therapy (DBT) Skills:
                
                Mindfulness Skills:
                - Observe: Notice thoughts without judgment
                - Describe: Put words to experiences
                - Participate: Fully engage in present moment
                
                Distress Tolerance - TIP:
                - Temperature: Cold water on face
                - Intense exercise
                - Paced breathing
                
                Emotional Regulation - PLEASE:
                - Physical health
                - Lack of substances
                - Eat balanced
                - Avoid mood-altering drugs
                - Sleep well
                - Exercise
                """
            }
        ]
    
    def save_resources(self, resources: List[Dict]):
        """Save resources to JSON file"""
        output = {
            'created_at': datetime.now().isoformat(),
            'total_resources': len(resources),
            'resources': resources
        }
        
        with open(self.resources_file, 'w', encoding='utf-8') as f:
            json.dump(output, f, indent=2, ensure_ascii=False)
    
    def create_sample_csv(self):
        """Create a sample CSV template for custom data"""
        csv_file = self.data_dir / "custom_resources_template.csv"
        
        if not csv_file.exists():
            with open(csv_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(['source', 'category', 'language', 'tags', 'content'])
                writer.writerow([
                    'Your_Resource_Name',
                    'general',
                    'english',
                    'tag1,tag2,tag3',
                    'Your mental health content goes here...'
                ])
            print(f"✅ Created CSV template: {csv_file}")
    
    def print_summary(self):
        """Print summary of loaded resources"""
        with open(self.resources_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        print("\n📊 RESOURCE SUMMARY:")
        print(f"Total Resources: {data['total_resources']}")
        
        categories = {}
        for resource in data['resources']:
            cat = resource['category']
            categories[cat] = categories.get(cat, 0) + 1
        
        print("\nBy Category:")
        for cat, count in categories.items():
            print(f"  - {cat}: {count} resources")
        
        print(f"\n📁 JSON file: {self.resources_file}")

def main():
    """Main function"""
    print("\n🌟 MENTAL HEALTH DATA LOADER 🌟")
    print("This will create a JSON file with mental health resources")
    
    loader = SimpleMentalHealthDataLoader()
    
    # Create CSV template for custom data
    loader.create_sample_csv()
    
    # Load all resources
    resources = loader.load_all_sources()
    
    # Print summary
    loader.print_summary()
    
    print("\n✅ Done! You can now:")
    print("1. Edit the JSON file to add more resources")
    print("2. Use the CSV template to add custom data")
    print("3. Import this JSON into your knowledge base")
    
    print(f"\n📁 Files created in: {loader.data_dir}")

if __name__ == "__main__":
    main()