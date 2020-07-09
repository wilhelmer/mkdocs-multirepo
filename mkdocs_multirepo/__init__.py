import yaml
import os
import click
from bs4 import BeautifulSoup
from shutil import copy2

class DefaultHelp(click.Command):
    def __init__(self, *args, **kwargs):
        context_settings = kwargs.setdefault('context_settings', {})
        if 'help_option_names' not in context_settings:
            context_settings['help_option_names'] = ['-h', '--help']
        self.help_flag = context_settings['help_option_names'][0]
        super(DefaultHelp, self).__init__(*args, **kwargs)

    def parse_args(self, ctx, args):
        if not args:
            args = [self.help_flag]
        return super(DefaultHelp, self).parse_args(ctx, args)

@click.command(cls=DefaultHelp)
@click.option("--init", help="Initialize the repos as Git submodules.", is_flag=True, show_default=True)
@click.option("--update", help="Update the repos, i.e., the Git submodules.", is_flag=True, show_default=True)
@click.option("--build", help="Build all MkDocs projects and generate the landing page.", is_flag=True, show_default=True)

def cli(init, update, build):

    config = loadConfig()

    if init:
        # Initialize the repos as Git submodules
        click.echo("Adding submodules ...")
        for repo in config["repos"]:
            # Add repo as git submodule
            os.system("git submodule add " + repo["url"] + " " + repo["name"])
        click.echo("Done.")

    if update:
        # Update the repos, i.e., the Git submodules
        click.echo("Updating submodules ...")
        os.system("git submodule update")
        click.echo("Done.")

    if build:
        # Build MkDocs projects
        # Set defaults
        if not "target_dir" in config:
            config["target_dir"] = "site"
        if not "element_id" in config:
            config["element_id"] = "multirepo"

        # Copy image files and build projects
        click.echo("Building projects ...")
        for repo in config["repos"]:
            os.makedirs(os.path.dirname(config["target_dir"] + "/" + repo["image"]), exist_ok=True)
            copy2(repo["image"], config["target_dir"] + "/" + repo["image"])
            os.chdir(os.getcwd() + os.path.sep + repo["name"])
            os.system("mkdocs build --site-dir ../" + config["target_dir"] + "/" + repo["name"])
            os.chdir("../")

        # Copy extra files
        if "extra_files" in config:
            click.echo("Copying extra files ...")
            for extrafile in config["extra_files"]:
                os.makedirs(os.path.dirname(config["target_dir"] + "/" + extrafile), exist_ok=True)
                copy2(extrafile, config["target_dir"] + "/" + extrafile)

        # Generate index.html based on template
        click.echo("Generating landing page ...")
        soup = loadTemplate()
        # Add unordered list as child of element_id
        element = soup.find(id=config["element_id"])
        element.insert(1, soup.new_tag("ul"))
        for repo in config["repos"]:
            # Add a list item for each repo
            list_tag = soup.new_tag("li")
            anchor_tag = soup.new_tag("a", href=repo["name"] + "/index.html")
            image_tag = soup.new_tag("img", src=repo["image"])
            heading_tag = soup.new_tag("span")
            heading_tag.string = repo["title"]

            anchor_tag.insert(1, image_tag)
            anchor_tag.insert(1, heading_tag)

            list_tag.insert(1, anchor_tag)

            element.ul.insert(1, list_tag)

        # Write index.html
        with open(config["target_dir"] + "/index.html", "w", encoding="utf8") as htmlfile:
            htmlfile.write(str(soup))
            htmlfile.close()
        click.echo("Done.")

def loadConfig():
    configfile = open(r'config.yml')
    try:
        config = yaml.safe_load(configfile)
    finally:
        configfile.close()
    return config

def loadTemplate():
    templatefile = open(r'index.tpl')
    try:
        contents = yaml.safe_load(templatefile)
        soup = BeautifulSoup(contents, 'html.parser')
    finally:
        templatefile.close()
    return soup
