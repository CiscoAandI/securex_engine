from base import Base
from core.conditional import evaluate_conditional
from variable_parser import Parser

class TargetGroup(Base):
    """
    Example: 
      "unique_name": "target_group_01Q0KDYS80KPZ0pEoFjcKjbyITPb8cCIMOG",
      "name": "SNOW-Pilot-Group",
      "title": "SNOW-Pilot-Group",
      "type": "generic.target_group",
      "base_type": "target_group",
      "version": "1.0.0",
      "targets": [
        {
          "data_target_type": "web-service.endpoint",
          "view_target_type": "web-service.endpoint",
          "include_all_targets": false,
          "selected_target_ids": [
            "definition_target_01Q0G5PJ2ENKQ1Ti8K2TRNAyVqIYiW8mOy2",
            "definition_target_01Q0G683WLDJK5U5myuVByT1llxOByruqpU",
            "definition_target_01Q0G6MXU2JDM4V8ZQGbfoherhsTEN7Jnd9",
            "definition_target_01Q6IMU04QXR54nYseTDh9VK4pweAVtpyt3",
            "definition_target_01Q6INHHIA1SC1LI2qyOGZvaC80jMhkpb2i"
          ]
        }
      ],
      "object_type": "target_group"
    """
    @property
    def unique_name(self):
        return self._spec['unique_name']
    
    @property
    def type(self):
        return self._spec.get('type', '')
    
    @property
    def targets(self):
        targets = []
        for target_type in self._spec.get('targets', []):
            for target in target_type.get('selected_target_ids'):
                targets.append(self._engine.targets[target])
        return targets
    
    def resolve_targets(self, workflow, spec):
        """
        example: {
              "target_group_id": "foo",
              "run_on_all_targets": false,
              "selected_target_types": [
                "web-service.endpoint"
              ],
              "use_criteria": {
                "choose_target_using_algorithm": "choose_first_with_matching_criteria",
                "conditions": [
                  {
                    "operator": "mregex",
                    "left_operand": "$targetgroup.web-service endpoint.input.display_name$",
                    "right_operand": "^foo$workflow.foonIZs0wb6WjVXt$"
                  }
                ]
              }
            }
        """
        # Get the subset of targets that are resolved against the spec
        if spec.get('run_on_all_targets'):
            return self.targets
        
        # Filter out incorrect target types
        if spec.get('selected_target_types'):
            candidates = [i for i in self.targets if i.type in spec.get('selected_target_types', [])]
        else:
            candidates = self.targets
            
        # Resolve criteria
        final_candidates = []
        use_criteria = spec.get('use_criteria', {})
        if use_criteria:
            for candidate in candidates:
                # try condition
                for conditional in spec.get('use_criteria', {}).get('conditions', []):
                    conditional = Parser(workflow, conditional, target=candidate).parse()
                    result = evaluate_conditional(conditional).get('result', False)
                    if not result:
                        # Criteria does not match, go to next candidate
                        break
                else:
                    # Criteria all match
                    if use_criteria.get('choose_target_using_algorithm') == 'choose_first_with_matching_criteria':
                        final_candidates = [candidate]
                        break
                    else:
                        final_candidates.append(candidate)
        else:
            final_candidates = candidates
            
        return final_candidates
    
    @property
    def object_type(self):
        return self._spec.get('object_type', '')
    
    @property
    def name(self):
        return self._spec.get('name', '')
    
    @property
    def title(self):
        return self._spec.get('title', '')
    
    @property
    def base_type(self):
        return self._spec.get('base_type', '')
    
    @property
    def version(self):
        return self._spec.get('version', '')
    
    