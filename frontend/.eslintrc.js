module.exports = {
    extends: [
        "plugin:vue/vue3-essential",
      "eslint:recommended"
    ],
    rules: {
        'vue/multi-word-component-names': 0,
    },
    // parser: "babel-eslint",
    // parserOptions: {
    //     ecmaVersion: "latest"
    // },
    env: {
        es6: true
    }
}
