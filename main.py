import argparse
from argparse import ArgumentParser
from git import Repo
import os
import re
import textwrap
import shutil
import importlib
import logging
import sys



def mergefolders(root_src_dir, root_dst_dir):
    for src_dir, dirs, files in os.walk(root_src_dir):
        dst_dir = src_dir.replace(root_src_dir, root_dst_dir, 1)
        if not os.path.exists(dst_dir):
            os.makedirs(dst_dir)
        for file_ in files:
            src_file = os.path.join(src_dir, file_)
            dst_file = os.path.join(dst_dir, file_)
            if os.path.exists(dst_file):
                os.remove(dst_file)
            shutil.copy(src_file, dst_dir)


logger = logging.getLogger()
logger.setLevel(logging.WARN)

handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


def clone(repo, project, basedir):
    logger.info(f"Cloning {project} from {repo} to {basedir} and creating clean copy in {project}_orig")

    repo_dir = os.path.join(basedir, "temp", project)
    cloned = Repo.clone_from(repo, repo_dir)

    repo_copy_dir = os.path.join(basedir, "temp", project + "_orig")
    cloned.clone(repo_copy_dir)


def copy_from_local(project, local, base):
    source = os.path.join(local, project)
    destination = os.path.join(base, "temp", project)

    if os.path.exists(destination):
        logger.info(f"removing {destination} because it will be overwritten")
        shutil.rmtree(destination)

    logger.info(f"copying from local repo {source} to {destination}")
    if not os.path.exists(os.path.join(base, "temp")):
        os.makedirs(os.path.join(base, "temp"))

    logger.info(f"Copying files from {source} to {destination}")
    shutil.copytree(source, destination)


def add_files(project, base, files):
    source = os.path.join(files, project)
    destination = os.path.join(base, "temp", project)

    logger.info(f"Copying tester files from {source} to {destination}")
    mergefolders(source, destination)


def execute_tests(options):
    # at this point we should have the directory created before copying stuff into it

    # Get the correct tester
    module_name = options["project"].upper() + "_Tester"
    module = importlib.import_module(module_name)

    # execute the tests
    module.__getattribute__(module_name)(options)


def main():
    """
    Executes the test framework with the given args
    """
    pwd = os.getcwd()
    current_dir = os.path.basename(pwd)
    exercise = None
    project = None

    if re.fullmatch(r"ex\d{2}", current_dir):
        exercise = current_dir
        current_dir = os.path.dirname(pwd)

    if re.fullmatch(r"[Cc]\d{2}", current_dir):
        project = current_dir

    parser = ArgumentParser("francinette",
                            formatter_class=argparse.RawDescriptionHelpFormatter,
                            description=textwrap.dedent("""
            A micro framework that allows you to test your C code with more ease.
            
            If this command is executed inside a project (c##) or an exercise (ex##),
            then it knows automatically which tests to execute, and does. No need to pass 
            arguments.
            If you pass the arguments, then the arguments take precedence.
    """))

    parser.add_argument(
        "-t", "--exercise", nargs="?",
        help="If present, only executes the passed test"
    )
    parser.add_argument(
        "-b", "--base", nargs="?",
        help="The base directory where the temp files are stored. It defaults to the one where this python file is"
    )
    parser.add_argument(
        "-f", "--files", nargs="?",
        help="The directory from where to get the extra files needed to run the tests (main.c, expected, etc)"
             " If defaults to the 'files' folder inside basedir"
    )
    parser.add_argument(
        "-l", "--local", nargs="?",
        help="The local directory to get your local code from, if no repo is passed as parameter. defaults to basedir"
    )
    parser.add_argument(
        "-v", "--verbose", action="store_true",
        help="activates verbose mode, showing more internal details of the execution"
    )
    parser.add_argument(
        "project",
        nargs="?",
        help="If present, it sets the project to be executed under testing"
    )
    parser.add_argument(
        "git_repo",
        nargs="?",
        help="If present, it uses this repository to clone the exercises from"
    )

    args = parser.parse_args()

    base = args.base or os.path.dirname(os.path.realpath(__file__))
    exercise = args.exercise or exercise
    if exercise:
        exercise = exercise.rjust(2, "0")
        logger.info("Will only execute the tests for ex{exercise}")

    options = {
        "exercise": exercise,
        "project": args.project or project,
        "repo": args.git_repo,
        "base": base,
        "files": args.files or os.path.join(base, "files"),
        "local": args.local or base,
    }

    if not options["project"]:
        parser.print_help()
        exit(0)

    logger.info(f'Options for this run: {options}')

    if options["repo"]:
        clone(options["repo"], options["project"], options["base"])
    else:
        copy_from_local(options["project"], options["local"], options["base"])

    add_files(options["project"], options["base"], options["files"])

    execute_tests(options)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()