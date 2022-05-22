class ValidatorSerializer:

    def use_individual_validation(self, data):
        # use in self.validate => return self.use_individual_validation()
        # require self.get_individual_validators => dict[str, FunctionType(data)]
        individual_validators = self.get_individual_validators()
        for validator in individual_validators.keys():
            if validator not in data.keys(): continue
            validation_function = individual_validators[validator]
            validation_function(data) # raises any error if data is not valid
        return super().validate(data)
