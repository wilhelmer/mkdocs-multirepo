# mkdocs-multirepo

A bit like [monorepo](https://github.com/spotify/mkdocs-monorepo-plugin), but keeps MkDocs projects separate.

## Use Case

This plugin allows you to combine multiple MkDocs documentation projects.

Unlike the [monorepo](https://github.com/spotify/mkdocs-monorepo-plugin) plugin, the multirepo plugin doesn't merge projects into one. 

Instead, multirepo automatically adds each MkDocs project as a Git Submodule, builds them individually, and generates a landing page based on a template file.

This has the following advantages:

- Keeps the individual mkdocs.yml settings of each subproject. This means that, e.g., each subproject can have its own color set or theme.
- Avoids problems with relative paths in the subprojects.
- Keeps search indexes small instead of creating a giant merged index.

## Installation 

`pip install mkdocs-multirepo`

## Usage

1. Create two files named `config.yml` and `index.tpl` and put them in the same directory.
2. Configure the files as described below.
3. Change to the directory created in step 1 and run `mkdocs-multirepo`.

## Configuration

### Sample

See `mkdocs_multirepo/demo` for a sample project.

### config.yml

Use the `config.yml` file to configure the build process. Example:

```yml
repos:
  - name: repo-1
    title: My Repository 1
    image: images/icon-repo-1.png
    url: https://github.com/giansalex/mkdocs-sample.git
  - name: repo-2
    title: My Repository 2
    image: images/icon-repo-2.png
    url: https://github.com/hristo-mavrodiev/mkdocs-sample.git
element_id: multirepo
target_dir: site
```

Each entry under `repos` configures an MkDocs project:

- `name`: Used to create the Git Submodule directory and also the output directory within `target_dir`.
- `title`: Text for the landing page list item.
- `image`: Image for the landing page list item.
- `url`: URL of the repository.

`element_id`: ID of the DOM element on the landing page where the links to the projects should be created. Default: `multirepo`.
`target_dir`: Output directory. Default: `site`.

### index.tpl

Use the `index.tpl` file to configure the landing page. Example:

```yml
<html>
    <head><title>Multirepo Demo Page</title></head>
    <body>
        <section id="multirepo"></section>
    </body>
</html>
```

The template must be written in HTML and must contain a node with an ID called "multirepo" or as defined using the `element_id` setting.

From this template, a landing page named `index.html` will be generated and placed into `target_dir`.

Sample output:

```html
<html>
<head><title>Multirepo Demo Page</title></head>
<body>
    <section id="multirepo">
        <ul>
            <li><a href="site/repo-1/index.html"><img src="images/icon-repo-1.png"/><h3>My Repository 1</h3></a></li>
            <li><a href="site/repo-2/index.html"><img src="images/icon-repo-2.png"/><h3>My Repository 2</h3></a></li>
        </ul>
    </section>
</body>
</html>
```