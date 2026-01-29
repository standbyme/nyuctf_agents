"""
Skill loader for Agent Skills format.
This module provides utilities for discovering, parsing, and using skills
following the Agent Skills specification.
"""

import re
import yaml
from pathlib import Path
from dataclasses import dataclass
from typing import Optional, Dict, List

@dataclass
class SkillMetadata:
    """Holds the metadata from a skill's SKILL.md frontmatter"""
    name: str
    description: str
    path: Path
    license: Optional[str] = None
    compatibility: Optional[str] = None
    metadata: Optional[Dict[str, str]] = None
    allowed_tools: Optional[str] = None


@dataclass 
class Skill:
    """Represents a complete skill with metadata and instructions"""
    metadata: SkillMetadata
    instructions: str  # The markdown body content


def parse_frontmatter(content: str) -> tuple[dict, str]:
    """
    Parse YAML frontmatter from markdown content.
    
    Returns a tuple of (frontmatter_dict, body_content)
    """
    # Match YAML frontmatter at the start of the file
    pattern = r'^---\s*\n(.*?)\n---\s*\n(.*)$'
    match = re.match(pattern, content, re.DOTALL)
    
    if not match:
        raise ValueError("No valid YAML frontmatter found in SKILL.md")
    
    frontmatter_yaml = match.group(1)
    body = match.group(2)
    
    frontmatter = yaml.safe_load(frontmatter_yaml)
    if frontmatter is None:
        frontmatter = {}
    
    return frontmatter, body


def validate_skill_name(name: str) -> bool:
    """
    Validate skill name according to the Agent Skills specification.
    
    - Must be 1-64 characters
    - May only contain lowercase alphanumeric characters and hyphens
    - Must not start or end with hyphen
    - Must not contain consecutive hyphens
    """
    if not name or len(name) > 64:
        return False
    if not re.match(r'^[a-z0-9][a-z0-9-]*[a-z0-9]$|^[a-z0-9]$', name):
        return False
    if '--' in name:
        return False
    return True


def load_skill_metadata(skill_path: Path) -> SkillMetadata:
    """
    Load only the metadata from a skill's SKILL.md file.
    This is used for discovery and matching without loading full instructions.
    """
    skill_md = skill_path / "SKILL.md"
    if not skill_md.exists():
        raise FileNotFoundError(f"SKILL.md not found in {skill_path}")
    
    content = skill_md.read_text()
    frontmatter, _ = parse_frontmatter(content)
    
    # Validate required fields
    if 'name' not in frontmatter:
        raise ValueError(f"Missing required 'name' field in {skill_md}")
    if 'description' not in frontmatter:
        raise ValueError(f"Missing required 'description' field in {skill_md}")
    
    name = frontmatter['name']
    if not validate_skill_name(name):
        raise ValueError(f"Invalid skill name '{name}' in {skill_md}")
    
    # Check that name matches directory name
    if skill_path.name != name:
        raise ValueError(f"Skill name '{name}' does not match directory name '{skill_path.name}'")
    
    return SkillMetadata(
        name=name,
        description=frontmatter['description'],
        path=skill_path,
        license=frontmatter.get('license'),
        compatibility=frontmatter.get('compatibility'),
        metadata=frontmatter.get('metadata'),
        allowed_tools=frontmatter.get('allowed-tools')
    )


def load_skill(skill_path: Path) -> Skill:
    """
    Load a complete skill including metadata and instructions.
    """
    skill_md = skill_path / "SKILL.md"
    if not skill_md.exists():
        raise FileNotFoundError(f"SKILL.md not found in {skill_path}")
    
    content = skill_md.read_text()
    frontmatter, body = parse_frontmatter(content)
    
    metadata = load_skill_metadata(skill_path)
    
    return Skill(
        metadata=metadata,
        instructions=body.strip()
    )


def discover_skills(skills_dir: Path) -> List[SkillMetadata]:
    """
    Discover all skills in a directory by scanning for SKILL.md files.
    Returns a list of skill metadata.
    """
    skills = []
    
    if not skills_dir.exists():
        return skills
    
    for item in skills_dir.iterdir():
        if item.is_dir():
            skill_md = item / "SKILL.md"
            if skill_md.exists():
                try:
                    metadata = load_skill_metadata(item)
                    skills.append(metadata)
                except (ValueError, FileNotFoundError) as e:
                    # Log warning but continue discovering other skills
                    print(f"Warning: Failed to load skill from {item}: {e}")
    
    return skills


def generate_available_skills_xml(skills: List[SkillMetadata], include_location: bool = True) -> str:
    """
    Generate the <available_skills> XML block for injection into system prompts.
    
    Args:
        skills: List of skill metadata to include
        include_location: Whether to include the location (path) field
    
    Returns:
        XML string for the available skills
    """
    lines = ['<available_skills>']
    
    for skill in skills:
        lines.append('  <skill>')
        lines.append(f'    <name>{skill.name}</name>')
        lines.append(f'    <description>{skill.description}</description>')
        if include_location:
            lines.append(f'    <location>{skill.path.absolute()}/SKILL.md</location>')
        lines.append('  </skill>')
    
    lines.append('</available_skills>')
    
    return '\n'.join(lines)


def get_skill_instructions(skill: Skill) -> str:
    """
    Get the full instructions for a skill, formatted for injection into context.
    """
    return f"""# Skill: {skill.metadata.name}

{skill.instructions}
"""


class SkillManager:
    """
    Manages skill discovery, loading, and activation for an agent.
    """
    
    def __init__(self, skills_dir: Path):
        self.skills_dir = skills_dir
        self._metadata_cache: Dict[str, SkillMetadata] = {}
        self._skill_cache: Dict[str, Skill] = {}
        self._discover_skills()
    
    def _discover_skills(self):
        """Discover and cache skill metadata"""
        skills = discover_skills(self.skills_dir)
        for metadata in skills:
            self._metadata_cache[metadata.name] = metadata
    
    @property
    def available_skills(self) -> List[SkillMetadata]:
        """Get list of all available skill metadata"""
        return list(self._metadata_cache.values())
    
    def get_skill_metadata(self, name: str) -> Optional[SkillMetadata]:
        """Get metadata for a specific skill by name"""
        return self._metadata_cache.get(name)
    
    def activate_skill(self, name: str) -> Optional[Skill]:
        """
        Activate a skill by loading its full instructions.
        Returns None if skill not found.
        """
        if name not in self._metadata_cache:
            return None
        
        if name not in self._skill_cache:
            metadata = self._metadata_cache[name]
            self._skill_cache[name] = load_skill(metadata.path)
        
        return self._skill_cache[name]
    
    def get_available_skills_xml(self, include_location: bool = True) -> str:
        """Generate XML for available skills"""
        return generate_available_skills_xml(self.available_skills, include_location)
    
    def match_skill(self, task_description: str) -> Optional[SkillMetadata]:
        """
        Simple keyword-based skill matching.
        Returns the best matching skill or None.
        
        Note: In a production system, this would use more sophisticated
        matching (embeddings, LLM-based selection, etc.)
        """
        task_lower = task_description.lower()
        
        best_match = None
        best_score = 0
        
        for metadata in self.available_skills:
            # Simple keyword matching based on name and description
            score = 0
            name_words = metadata.name.replace('-', ' ').split()
            desc_words = metadata.description.lower().split()
            
            for word in name_words:
                if word.lower() in task_lower:
                    score += 2
            
            for word in desc_words:
                if len(word) > 3 and word in task_lower:
                    score += 1
            
            if score > best_score:
                best_score = score
                best_match = metadata
        
        return best_match if best_score > 0 else None
