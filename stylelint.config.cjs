module.exports = {
  extends: ['stylelint-config-standard'],
  rules: {
    // Existing selectors intentionally scope controls within cards and dialogs.
    'no-descending-specificity': null,
    'selector-id-pattern': '^[a-z][a-z0-9-]*$',
  },
};
