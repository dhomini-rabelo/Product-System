class ValidatorSerializer:
    """
    This class helps in the validation process for the main serializer
    """

    def use_individual_validation(self, data: dict | list[dict]) -> dict | list[dict]:
        """
        Active individual validation process, works with raises to returns user feedbacks

        require:
            self.get_individual_validators => dict[str, FunctionType(data) => Any]

        How to use in main serializer:
            def validate(self, data: : dict | list[dict]):
                return self.use_individual_validation(data)

            def self.get_individual_validators() -> dict:
                def validate_field(self, data): 
                    if not is_valid_value:
                        raise ValidationError('error_message')
                    return data[field_name]
                
                return {
                    'field': validate_field
                }

        Args:
            data (dict | list[dict]): received data from serializer

        Returns:
            data: initial data received
        """
        # use in self.validate => return self.use_individual_validation()
        individual_validators = self.get_individual_validators()
        for validator in individual_validators.keys():
            if validator not in data.keys(): continue
            validation_function = individual_validators[validator]
            validation_function(data) # raises any error if data is not valid
        return data
