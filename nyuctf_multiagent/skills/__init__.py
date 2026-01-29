"""
Agent Skills module for nyuctf_multiagent.

This module provides the Agent Skills format support for defining and loading
tool capabilities in the CTF solving agents.

The skills are defined using the Agent Skills specification:
- Each skill is a directory containing a SKILL.md file
- SKILL.md contains YAML frontmatter with name and description
- The markdown body contains instructions for the agent

Example usage:
    from nyuctf_multiagent.skills import SkillManager

    # Create a skill manager
    manager = SkillManager(Path("./skills"))

    # Get available skills XML for system prompt
    xml = manager.get_available_skills_xml()

    # Activate a skill to get full instructions
    skill = manager.activate_skill("run-command")
    if skill:
        instructions = skill.instructions
"""

from .skill_loader import (
    Skill,
    SkillMetadata,
    SkillManager,
    discover_skills,
    generate_available_skills_xml,
    get_skill_instructions,
    load_skill,
    load_skill_metadata,
    parse_frontmatter,
    validate_skill_name,
)

__all__ = [
    'Skill',
    'SkillMetadata', 
    'SkillManager',
    'discover_skills',
    'generate_available_skills_xml',
    'get_skill_instructions',
    'load_skill',
    'load_skill_metadata',
    'parse_frontmatter',
    'validate_skill_name',
]
