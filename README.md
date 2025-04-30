# Animal Police hugo website

Made to replace the [old website](https://www.allatrendorseg.com/post/hollandi%C3%A1ban-is).

## Development

### Quick start

Requirements:

- Go
- Git

To use the ananke theme, you need to clone the repo with its submodules.

```bash
# Clone with submodules
git clone --recurse-submodules {repo-url}

# Clone first then initialize submodules
git clone {repo-url}
git submodule init
git submodule update
```

To start the server:

```bash
hugo server -D
```

For further set up, read Hugo's [quick start guide](https://gohugo.io/getting-started/quick-start/).

## Theme

Currently using [ananke](https://github.com/theNewDynamic/gohugo-theme-ananke).

Maybe try [rjordaney](https://rjordaney.is/).

Update the theme:

```bash
cd themes/ananke
git pull origin main

cd ../..
git add themes/your-theme
git commit -m "Update theme to the latest version"
```

## Refs

- Ananke [example site](https://github.com/theNewDynamic/gohugo-theme-ananke/tree/master/exampleSite/content/fr)
- Cover photo by [Pixabay](https://www.pexels.com/photo/adorable-animal-blurred-background-cat-207901/)
