from typing import Dict, List, Any
import json
import os

class Rule:
    def __init__(self, name: str, condition: str, impact: float, description: str = None):
        self.name = name
        self.condition = condition
        self.impact = impact
        self.description = description

    def evaluate(self, data: Dict[str, Any]) -> bool:
        try:
            return eval(self.condition, {"__builtins__": {}}, data)
        except Exception as e:
            print(f"Error evaluating rule {self.name}: {str(e)}")
            return False

class RulesEngine:
    def __init__(self):
        self.rules = self._load_rules()
        self.base_score = 100.0

    def _load_rules(self) -> List[Rule]:
        """Load rules from configuration file"""
        rules_path = os.path.join(os.path.dirname(__file__), 'rules.json')
        try:
            with open(rules_path, 'r') as f:
                rules_data = json.load(f)
                return [
                    Rule(
                        name=rule['name'],
                        condition=rule['condition'],
                        impact=rule['impact'],
                        description=rule.get('description')
                    )
                    for rule in rules_data['rules']
                ]
        except Exception as e:
            print(f"Error loading rules: {str(e)}")
            # Default rules if file not found
            return [
                Rule(
                    "critical_vulnerabilities",
                    "critical_vulns > 0",
                    -20.0,
                    "Critical vulnerabilities found"
                ),
                Rule(
                    "high_vulnerabilities",
                    "high_vulns > 2",
                    -10.0,
                    "Multiple high vulnerabilities found"
                ),
                Rule(
                    "outdated_dependencies",
                    "outdated_deps_percentage > 20",
                    -5.0,
                    "High percentage of outdated dependencies"
                ),
                Rule(
                    "compliance_violations",
                    "compliance_violations > 0",
                    -15.0,
                    "Compliance violations found"
                )
            ]

    def compute_score(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Compute security score based on rules"""
        score = self.base_score
        triggered_rules = []

        for rule in self.rules:
            if rule.evaluate(data):
                score += rule.impact
                triggered_rules.append({
                    'name': rule.name,
                    'impact': rule.impact,
                    'description': rule.description
                })

        return {
            'score': max(0, min(100, score)),
            'triggered_rules': triggered_rules,
            'base_score': self.base_score
        }
