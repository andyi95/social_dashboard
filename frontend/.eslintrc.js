const rules = {
        'vue/multi-word-component-names': 0,
        quotes: 'off',
        'vue/html-ident': 'off',
            'vue/no-template-shadow': 'off',
    'vue/no-v-html': 'off',
    'vue/require-default-prop': 'off',
    }

module.exports = {
    root: true,
    extends: [
        'eslint:recommended',
        'plugin:vue/vue3-recommended'
    ],
    rules: rules,
    overrides: [
        {
            files: ['**/*.ts', '**/*.tsx', '**/*.vue'],
            parserOptions: {
                'parser': '@typescript-eslint/parser',
                'sourceType': 'module'
            },
            rules: rules
        }
    ],
    // parser: "babel-eslint",
    // parserOptions: {
    //     ecmaVersion: "latest"
    // },
    env: {
        es6: true,
        node: true
    },
}
