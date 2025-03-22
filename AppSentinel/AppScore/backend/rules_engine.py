from dataclasses import dataclass
from typing import List, Dict, Any, Optional
import json

@dataclass
class Rule:
    id: str
    name: str
    description: str
    condition: Dict[str, Any]  # Criteria for rule to apply
    impact: float  # Score impact (-100 to +100)
    category: str
    enabled: bool = True

class RulesEngine:
    def __init__(self):
        self.rules: List[Rule] = []
        self._load_default_rules()

    def _load_default_rules(self):
        """Load default security scoring rules."""
        default_rules = [
            Rule(
                id="AUTH001",
                name="Missing MFA",
                description="Application lacks Multi-Factor Authentication",
                condition={"authentication": {"mfa_enabled": False}},
                impact=-20,
                category="Authentication"
            ),
            Rule(
                id="SEC001",
                name="Critical Vulnerabilities",
                description="Application has critical security vulnerabilities",
                condition={"vulnerabilities": {"critical_count": {"gt": 0}}},
                impact=-30,
                category="Security"
            ),
            Rule(
                id="COMP001",
                name="Compliance Requirements Met",
                description="Application meets all compliance requirements",
                condition={"compliance": {"requirements_met": True}},
                impact=20,
                category="Compliance"
            )
        ]
        self.rules.extend(default_rules)

    def add_rule(self, rule: Rule):
        """Add a new rule to the engine."""
        # Check for duplicate rule ID
        if any(r.id == rule.id for r in self.rules):
            raise ValueError(f"Rule with ID {rule.id} already exists")
        self.rules.append(rule)

    def remove_rule(self, rule_id: str):
        """Remove a rule from the engine."""
        self.rules = [r for r in self.rules if r.id != rule_id]

    def _check_condition(self, condition: Dict[str, Any], data: Dict[str, Any]) -> bool:
        """Recursively check if a condition is met."""
        for key, value in condition.items():
            if key not in data:
                return False
            
            if isinstance(value, dict):
                # Handle comparison operators
                if "gt" in value:
                    if not isinstance(data[key], (int, float)) or not data[key] > value["gt"]:
                        return False
                elif "lt" in value:
                    if not isinstance(data[key], (int, float)) or not data[key] < value["lt"]:
                        return False
                elif "eq" in value:
                    if data[key] != value["eq"]:
                        return False
                else:
                    # Nested condition
                    if not self._check_condition(value, data[key]):
                        return False
            else:
                # Direct value comparison
                if data[key] != value:
                    return False
        
        return True

    def calculate_score(self, application_data: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate security score based on rules and application data."""
        base_score = 100
        applied_rules = []
        
        for rule in self.rules:
            if not rule.enabled:
                continue
                
            if self._check_condition(rule.condition, application_data):
                base_score += rule.impact
                applied_rules.append({
                    "id": rule.id,
                    "name": rule.name,
                    "description": rule.description,
                    "impact": rule.impact,
                    "category": rule.category
                })
        
        # Ensure score stays within 0-100 range
        final_score = max(0, min(100, base_score))
        
        return {
            "score": final_score,
            "applied_rules": applied_rules,
            "base_score": base_score,
            "capped_score": final_score != base_score
        }

    def get_rules(self) -> List[Dict[str, Any]]:
        """Get all current rules."""
        return [
            {
                "id": rule.id,
                "name": rule.name,
                "description": rule.description,
                "impact": rule.impact,
                "category": rule.category,
                "enabled": rule.enabled,
                "condition": rule.condition
            }
            for rule in self.rules
        ]

    def update_rule(self, rule_id: str, updates: Dict[str, Any]) -> Optional[Rule]:
        """Update an existing rule."""
        for rule in self.rules:
            if rule.id == rule_id:
                for key, value in updates.items():
                    if hasattr(rule, key):
                        setattr(rule, key, value)
                return rule
        return None

    def load_rules_from_file(self, filepath: str):
        """Load rules from a JSON file."""
        try:
            with open(filepath, 'r') as f:
                rules_data = json.load(f)
                self.rules = [Rule(**rule_data) for rule_data in rules_data]
        except Exception as e:
            raise Exception(f"Error loading rules from file: {str(e)}")

    def save_rules_to_file(self, filepath: str):
        """Save current rules to a JSON file."""
        try:
            rules_data = [
                {
                    "id": rule.id,
                    "name": rule.name,
                    "description": rule.description,
                    "condition": rule.condition,
                    "impact": rule.impact,
                    "category": rule.category,
                    "enabled": rule.enabled
                }
                for rule in self.rules
            ]
            with open(filepath, 'w') as f:
                json.dump(rules_data, f, indent=2)
        except Exception as e:
            raise Exception(f"Error saving rules to file: {str(e)}")
