# python-project Documentation

This directory contains the documentation for python-project, built with [VitePress](https://vitepress.dev/).

## 🚀 Quick Start

### Prerequisites

- Node.js 16 or higher
- npm or yarn

### Installation

```bash
# Navigate to the docs directory
cd docs

# Install dependencies
npm install
# or if you use yarn
yarn install
```

### Development

To start the development server:

```bash
# Start the development server
npm run docs:dev
# or
yarn docs:dev
```

This will start a local server at `http://localhost:5173`. The documentation will automatically reload when you make changes to the source files.

### Building

To build the documentation for production:

```bash
# Build the documentation
npm run docs:build
# or
yarn docs:build
```

The built files will be in the `.vitepress/dist` directory.

### Preview Production Build

To preview the production build locally:

```bash
# Preview the built documentation
npm run docs:preview
# or
yarn docs:preview
```

## 📁 Directory Structure

```
docs/
├── .vitepress/          # VitePress configuration
│   └── config.mts       # Site configuration
├── public/              # Static assets
│   └── logo.png        # Site logo
├── guide/              # Guide pages
│   ├── index.md        # Getting Started
│   └── installation.md # Installation Guide
├── api/                # API documentation
├── index.md           # Home page
└── package.json       # Project dependencies
```

## 🛠️ Customization

### Configuration

The main configuration file is located at `.vitepress/config.mts`. You can customize:

- Site metadata
- Navigation
- Sidebar
- Theme
- And more...

See the [VitePress Configuration Guide](https://vitepress.dev/reference/site-config) for more details.

### Theme Customization

You can customize the theme by modifying the following files:

- `.vitepress/theme/custom.css` - Custom CSS
- `.vitepress/theme/index.ts` - Theme customization

### Content Organization

- Put your documentation pages in the appropriate directories
- Use Markdown for content
- You can use Vue components in Markdown files
- Images and other assets should go in the `public` directory

## 📝 Writing Documentation

### Markdown Features

VitePress supports all standard Markdown features plus:

- GitHub-style tables
- Code syntax highlighting
- Custom containers
- Front matter
- Vue-powered features

Example:

```md
::: tip
This is a tip
:::

::: warning
This is a warning
:::

::: danger
This is a dangerous warning
:::
```

### Adding New Pages

1. Create a new `.md` file in the appropriate directory
2. Add the page to the sidebar in `.vitepress/config.mts`
3. Link to it from other pages using relative paths

## 🤝 Contributing

If you want to contribute to the documentation:

1. Make your changes
2. Preview them locally
3. Submit a pull request

## 📚 Resources

- [VitePress Documentation](https://vitepress.dev/)
- [Vue.js Documentation](https://vuejs.org/)
- [Markdown Guide](https://www.markdownguide.org/)
