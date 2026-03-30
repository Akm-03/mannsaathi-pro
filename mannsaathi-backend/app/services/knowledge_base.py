"""
Mental Health Knowledge Base with RAG (Retrieval-Augmented Generation)
"""

import os
import json
import structlog
from typing import List, Dict, Any
from pathlib import Path

# LangChain imports
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma, FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader, DirectoryLoader
from langchain_core.documents import Document

logger = structlog.get_logger()

class MentalHealthKnowledgeBase:
    """Knowledge base for mental health information"""
    
    def __init__(self, persist_directory: str = "knowledge_base"):
        self.persist_directory = persist_directory
        Path(self.persist_directory).mkdir(parents=True, exist_ok=True)
        self.embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2",
            model_kwargs={'device': 'cpu'},
            encode_kwargs={'normalize_embeddings': True}
        )
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=50,
            separators=["\n\n", "\n", " ", ""]
        )
        self.vectorstore = None
        self.load_or_create_knowledge_base()
    
    def load_or_create_knowledge_base(self):
        """Load existing or create new knowledge base"""
        if os.path.exists(self.persist_directory):
            try:
                self.vectorstore = Chroma(
                    persist_directory=self.persist_directory,
                    embedding_function=self.embeddings
                )
                logger.info("Loaded existing knowledge base")
            except Exception as e:
                logger.warning(f"Failed to load existing DB: {e}")
                self.create_knowledge_base()
        else:
            self.create_knowledge_base()
    
    def create_knowledge_base(self):
        """Create knowledge base from mental health resources"""
        documents = []
        
        # Load mental health resources
        resources = self.load_mental_health_resources()
        
        # Create documents
        for resource in resources:
            doc = Document(
                page_content=resource['content'],
                metadata={
                    'source': resource['source'],
                    'category': resource['category'],
                    'language': resource.get('language', 'english'),
                    'tags': resource.get('tags', [])
                }
            )
            documents.append(doc)
        
        # Split documents into chunks
        chunks = self.text_splitter.split_documents(documents)
        
        # Create vector store
        self.vectorstore = Chroma.from_documents(
            documents=chunks,
            embedding=self.embeddings,
            persist_directory=self.persist_directory
        )
        if hasattr(self.vectorstore, "persist"):
            self.vectorstore.persist()
        
        logger.info(f"Created knowledge base with {len(chunks)} chunks from {len(documents)} documents")
    
    def load_mental_health_resources(self) -> List[Dict[str, Any]]:
        """Load mental health resources from various sources"""
        resources = []
        
        # 1. Crisis intervention strategies
        resources.extend([
            {
                'source': 'WHO_Guidelines',
                'category': 'crisis_intervention',
                'content': """
                Crisis Intervention Steps:
                1. Listen actively without judgment
                2. Validate their feelings - "It's okay to feel this way"
                3. Ensure safety - ask about suicidal thoughts directly if concerned
                4. Provide support - let them know they're not alone
                5. Encourage professional help - suggest counseling or helplines
                6. Follow up - check on them after the crisis
                
                For immediate crisis: Stay calm, remove access to harmful objects, don't leave them alone,
                contact emergency services or crisis helpline immediately.
                """
            },
            {
                'source': 'CBT_Techniques',
                'category': 'therapy_techniques',
                'content': """
                Cognitive Behavioral Therapy (CBT) Techniques:
                
                1. Cognitive Restructuring: Identify and challenge negative thought patterns
                   - "What evidence do I have that this thought is true?"
                   - "What would I tell a friend in this situation?"
                
                2. Behavioral Activation: Engage in activities to improve mood
                   - Schedule enjoyable activities even when not motivated
                   - Break large tasks into small, manageable steps
                
                3. Mindfulness: Stay present in the moment
                   - 5-4-3-2-1 grounding technique: Name 5 things you see, 4 you feel, 3 you hear, 2 you smell, 1 you taste
                   - Deep breathing: Inhale for 4, hold for 4, exhale for 4
                
                4. Problem-Solving: Address specific issues
                   - Define the problem clearly
                   - Brainstorm solutions (no judgment)
                   - Choose one solution and try it
                   - Evaluate and adjust if needed
                """
            },
            {
                'source': 'Indian_Cultural_Context',
                'category': 'cultural_adaptation',
                'content': """
                Culturally-Sensitive Approaches for Indian Users:
                
                Understanding Cultural Factors:
                - Family involvement: Many Indians value family support in mental health
                - Stigma: Mental health discussions may be taboo; use normalizing language
                - Spiritual practices: Meditation, yoga, and prayer can be integrated
                - Language: Use Hinglish (Hindi+English) to connect better
                - Community: Emphasize community support and belonging
                
                Culturally-Adapted Techniques:
                - "Aap akela nahi hain" (You are not alone) - normalize struggles
                - "Yeh bahut common hai" (This is very common) - reduce stigma
                - Suggest family involvement when appropriate
                - Incorporate traditional practices like pranayama (breathing exercises)
                - Reference Bollywood or cultural metaphors when helpful
                """
            }
        ])
        
        # 2. Common mental health conditions
        resources.extend([
            {
                'source': 'Anxiety_Management',
                'category': 'anxiety',
                'tags': ['anxiety', 'stress', 'worry'],
                'content': """
                Managing Anxiety and Stress:
                
                Physical Symptoms: Racing heart, sweating, tense muscles, difficulty breathing
                
                Immediate Relief Techniques:
                1. Deep Breathing: Inhale 4 seconds, hold 4, exhale 6 (longer exhale activates parasympathetic nervous system)
                2. Progressive Muscle Relaxation: Tense and relax each muscle group
                3. Grounding: 5-4-3-2-1 technique using senses
                4. Cold water on face or holding ice (activates dive reflex)
                
                Long-term Strategies:
                - Regular exercise (30 mins, 5 days/week)
                - Limiting caffeine and alcohol
                - Journaling thoughts and worries
                - Setting aside "worry time" (15 mins/day)
                - Challenging catastrophic thoughts
                - Building a support network
                
                Indian Context: Consider incorporating yoga nidra, pranayama, and walking in nature (park/garden).
                """
            },
            {
                'source': 'Depression_Support',
                'category': 'depression',
                'tags': ['depression', 'sadness', 'hopelessness'],
                'content': """
                Supporting Someone with Depression:
                
                Signs of Depression:
                - Persistent sad, anxious, or "empty" mood
                - Loss of interest in activities once enjoyed
                - Fatigue and decreased energy
                - Difficulty concentrating or making decisions
                - Changes in sleep and appetite
                - Thoughts of death or suicide
                
                How to Help:
                1. Listen without trying to "fix" them
                2. Validate: "It makes sense you're feeling this way"
                3. Encourage small, achievable goals
                4. Help them maintain routines (eating, sleeping)
                5. Gently suggest professional help
                6. Be patient - recovery takes time
                
                What to Say:
                - "I'm here for you"
                - "You're not alone in this"
                - "This is temporary, it will get better"
                - "What can I do to support you right now?"
                
                What NOT to Say:
                - "Just cheer up"
                - "Others have it worse"
                - "It's all in your head"
                - "You should be grateful"
                """
            }
        ])
        
        # 3. Specific scenarios
        resources.extend([
            {
                'source': 'Relationship_Issues',
                'category': 'relationships',
                'content': """
                Navigating Relationship Challenges:
                
                Communication Techniques:
                - Use "I" statements: "I feel hurt when..." instead of "You always..."
                - Active listening: Reflect back what you hear
                - Take breaks when emotions are high (20-minute rule)
                
                Common Issues:
                - Trust issues: Build gradually through consistency
                - Conflict: Focus on problem, not blame
                - Distance: Schedule quality time together
                
                Indian Context: 
                - Family involvement in relationships is common
                - Balance individual needs with family expectations
                - Consider joint family dynamics
                - Respect cultural values while setting boundaries
                """
            },
            {
                'source': 'Work_Stress',
                'category': 'work',
                'content': """
                Managing Work-Related Stress:
                
                Work-Life Balance:
                - Set clear boundaries between work and personal time
                - Take regular breaks (5 mins every hour)
                - Use vacation time fully
                
                Dealing with Burnout:
                - Recognize signs: exhaustion, cynicism, reduced performance
                - Prioritize self-care as non-negotiable
                - Talk to supervisor about workload
                - Consider temporary reduced hours if possible
                
                Office Politics:
                - Stay professional
                - Document important conversations
                - Build support network at work
                - Know when to escalate issues
                """
            }
        ])
        
        # 4. Helplines and resources (add more)
        resources.append({
            'source': 'Helplines_India',
            'category': 'resources',
            'content': """
            Indian Mental Health Helplines:
            
            24/7 Helplines:
            - iCall: 9152987821 (TISS, Mumbai)
            - Vandrevala Foundation: 9999666555
            - AASRA: 9820466726 (Mumbai)
            - Sneha: 044-24640050 (Chennai)
            
            Specialized Support:
            - LGBTQ+ Support: 1800-123-3425 (Sahodaran)
            - Students: 1800-121-2830 (Jeevan)
            - Elderly: 1800-233-5525 (Nightingales)
            
            Online Resources:
            - MannTalks (free counseling): mantalks.in
            - YourDOST (corporate mental health): yourdost.com
            - NIMHANS (info): nimhans.ac.in
            """
        })
        
        return resources
    
    def get_relevant_context(self, query: str, k: int = 3) -> List[str]:
        """Retrieve relevant mental health information for a query"""
        if not self.vectorstore:
            return []
        
        try:
            docs = self.vectorstore.similarity_search(query, k=min(k, 5))
            contexts = [doc.page_content for doc in docs]
            return contexts
        except Exception as e:
            logger.error(f"Error retrieving context: {e}")
            return []
    
    def get_crisis_resources(self, query: str) -> Dict[str, Any]:
        """Get crisis-specific resources"""
        crisis_keywords = [
                'suicide', 'kill myself', 'end my life', 'want to die',
                'hopeless', 'no reason to live', 'give up', 'self harm'
            ]
        
        is_crisis = any(keyword in query.lower() for keyword in crisis_keywords)
        
        if is_crisis:
            return {
                'is_crisis': True,
                'helplines': [
                    {"name": "iCall", "number": "9152987821", "hours": "24/7"},
                    {"name": "Vandrevala Foundation", "number": "9999666555", "hours": "24/7"},
                    {"name": "AASRA", "number": "9820466726", "hours": "24/7"}
                ],
                'safety_message': "Your feelings are valid. Please reach out to these helplines - trained counselors are available to support you."
            }
        
        return {'is_crisis': False}