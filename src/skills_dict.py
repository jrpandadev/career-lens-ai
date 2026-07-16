import re

MASTER_SKILLS = {
    "java", "python", "c++", "c#", "go", "rust", "typescript", "javascript",
    "sql", "nosql", "mysql", "postgresql", "mongodb", "redis", "cassandra",
    "aws", "gcp", "google cloud", "azure", "cloud platforms",
    "docker", "kubernetes", "containerization",
    "git", "github", "gitlab", "bitbucket", "version control systems",
    "react", "node.js", 
    "machine learning", "data structures", "data structure implementation",
    "algorithms", "basic algorithm development",
    "object-oriented design", "object-oriented design principles",
    "ci/cd", "github actions", "jenkins", "gitlab ci", "azure devops",
    "ai tools for development productivity",
    "contributing to open-source projects",
    "debugging and troubleshooting complex systems"
}

def extract_skills_from_text(text: str, extra_skills: set[str] = None) -> list[str]:
    """
    Scans a raw string and returns matching skills from the MASTER_SKILLS list and extra_skills.
    """
    if not text:
        return []
        
    text_lower = text.lower()
    extracted = []
    
    search_space = MASTER_SKILLS.union({s.lower() for s in (extra_skills or set())})
    
    for skill in search_space:
        # Use regex to find whole words only, avoiding partial matches 
        # (e.g. matching "go" inside "algorithm")
        # We need to escape the skill for regex in case it contains + or . 
        escaped_skill = re.escape(skill)
        pattern = r'\b' + escaped_skill + r'\b'
        
        if re.search(pattern, text_lower):
            extracted.append(skill)
            
    return extracted
