module.exports = {
    content: ['./components/**/*.{vue,js,ts}', './layouts/**/*.vue', './pages/**/*.vue', './plugins/**/*.{js,ts}'],
    corePlugins: {
        preflight: false
    },
    important: true,
    theme: {
        extend: {
            colors: {
                theme: {
                    main: 'var(--n-color)'
                }
            }
        }
    },
    plugins: []
};
