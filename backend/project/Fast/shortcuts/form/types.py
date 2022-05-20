FIELDS = {
    'name': str,
    # **html_structure_requirements
}


FORM_DESCRIPTION = {
    'fields': list[FIELDS],
    'html_structure': str,
    'changes': list[tuple[str,str]],
}