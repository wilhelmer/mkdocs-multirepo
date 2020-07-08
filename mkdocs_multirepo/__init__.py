import yaml
import os
from bs4 import BeautifulSoup
from shutil import copy2

def main():

    # Build MkDocs projects
    with open(r'config.yml') as file:
        config = yaml.safe_load(file)
        # Set defaults
        if not "target_dir" in config:
            config["target_dir"] = "site"
        if not "element_id" in config:
            config["element_id"] = "multirepo"

        for repo in config["repos"]:
            # Copy repo image to target dir
            os.makedirs(os.path.dirname(config["target_dir"] + "/" + repo["image"]), exist_ok=True)
            copy2(repo["image"], config["target_dir"] + "/" + repo["image"])
            # Add repo as git submodule
            os.system("git submodule add " + repo["url"] + " " + repo["name"])
            # Build MkDocs project in submodule dir
            os.chdir(os.getcwd() + os.path.sep + repo["name"])
            os.system("mkdocs build --site-dir ../" + config["target_dir"] + "/" + repo["name"])
            os.chdir("../")

    # Generate index.html based on template
    with open("index.tpl", "r") as f:
        contents = f.read()
        soup = BeautifulSoup(contents, 'html.parser')        
        with open(r'config.yml') as file:
            config = yaml.safe_load(file)
            # Add unordered list as child of element_id
            element = soup.find(id=config["element_id"])
            element.insert(1, soup.new_tag("ul"))
            for repo in config["repos"]:
                # Add a list item for each repo
                list_tag = soup.new_tag("li")
                anchor_tag = soup.new_tag("a", href=repo["name"] + "/index.html")
                image_tag = soup.new_tag("img", src=repo["image"])
                heading_tag = soup.new_tag("h3")
                heading_tag.string = repo["title"]

                anchor_tag.insert(1, image_tag)
                anchor_tag.insert(1, heading_tag)

                list_tag.insert(1, anchor_tag)

                element.ul.insert(1, list_tag)
    
    # Write index.html
    with open(config["target_dir"] + "/index.html", "w", encoding="utf8") as f:
        f.write(str(soup))
